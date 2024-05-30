
import math
import typing
import logging

from shv import ValueClient

from g3elements import (
    ElementABC,
    Detector,
    PointMachineElectrical,
    PointMachineMechanical,
    Route,
    Gate,
    Zone,
    Signal,
    SignalSymbol,
    PointMachine,
    RouteLayoutDetector,
    ConnectorNotSetError,
    PointMachinePosition,
)
from g3elements.route_utils import RouteAnalyzer, DetectorEvent, RouteManager

from g3shvnodes import SHVNode
from g3shvnodes.detector import SHVDetectorControlNode, SHVDetectorTestNode
from g3shvnodes.pointmachine import (
    SHVPMEControlNode, SHVPMETestNode, SHVPMMControlNode, SHVPMMTestNode
)
from g3shvnodes.route import SHVRouteControlNode, SHVRouteStatusNode
from g3shvnodes.gate import SHVGateControlNode
from g3shvnodes.zone import SHVZoneControlNode
from g3shvnodes.signal import (
    SHVSignalControlNode,
    SHVSignalSymbolControlNode,
    SHVSignalSymbolTestNode
)

from ..._test import (
    TestABC,
    MultiTestABC,
    ParallelMultiTest,
    SequentialMultiTest
)
from ..detector import DetectorSetOccupiedTest, DetectorSetFreeTest
from ..element import ControlNodeStatusValueSingleTest
from ..zone import ResetZoneTest
from ..route import RequestRouteTest, WaitUntilRouteIsReadyTest


logger = logging.getLogger('g3tester')


TControlNode = typing.TypeVar('TControlNode', bound=typing.Optional[SHVNode])
TTestNode = typing.TypeVar('TTestNode', bound=typing.Optional[SHVNode])


class ElementSHVNodes(
    typing.NamedTuple, typing.Generic[TControlNode, TTestNode]
):
    control: TControlNode
    test: TTestNode


class SHVNodeFactory:
    def __init__(
        self,
        control_client: ValueClient,
        test_client: ValueClient,
        control_paths: dict[str, str] | None = None,
        test_paths: dict[str, str] | None = None
    ) -> None:
        self.control_client = control_client
        self.test_client = test_client
        self.control_paths = control_paths or {}
        self.test_paths = test_paths or {}

    def get_default_path_control(self, element: ElementABC) -> str:
        return self.control_paths.setdefault(
            element.shv_path_full, f'{element.shv_path_full}'
            )

    def get_default_path_test(self, element: ElementABC) -> str:
        path = self.test_paths.setdefault(
            element.name, f'{element.shv_path_full}/_test'
            )
        return path

    @typing.overload
    def __call__(
        self, element: Detector
    ) -> ElementSHVNodes[SHVDetectorControlNode, SHVDetectorTestNode]: ...

    @typing.overload
    def __call__(
        self, element: PointMachineElectrical
    ) -> ElementSHVNodes[SHVPMEControlNode, SHVPMETestNode]: ...

    @typing.overload
    def __call__(
        self, element: PointMachineMechanical
    ) -> ElementSHVNodes[SHVPMMControlNode, SHVPMMTestNode]: ...

    @typing.overload
    def __call__(
        self, element: Gate
    ) -> ElementSHVNodes[SHVGateControlNode, None]: ...

    @typing.overload
    def __call__(
        self, element: Route
    ) -> ElementSHVNodes[SHVRouteControlNode, None]: ...

    @typing.overload
    def __call__(
        self, element: Signal
    ) -> ElementSHVNodes[SHVSignalControlNode, None]: ...

    @typing.overload
    def __call__(
        self, element: SignalSymbol
    ) -> ElementSHVNodes[SHVSignalControlNode, SHVSignalSymbolTestNode]: ...

    @typing.overload
    def __call__(
        self, element: Zone
    ) -> ElementSHVNodes[SHVZoneControlNode, None]: ...

    def __call__(self, element: ElementABC) -> ElementSHVNodes:
        control_node_cls: typing.Type[SHVNode] | None
        test_node_cls: typing.Type[SHVNode] | None
        if isinstance(element, Detector):
            control_node_cls = SHVDetectorControlNode
            test_node_cls = SHVDetectorTestNode
        elif isinstance(element, PointMachineElectrical):
            control_node_cls = SHVPMEControlNode
            test_node_cls = SHVPMETestNode
        elif isinstance(element, PointMachineMechanical):
            control_node_cls = SHVPMMControlNode
            test_node_cls = SHVPMMTestNode
        elif isinstance(element, Gate):
            control_node_cls = SHVGateControlNode
            test_node_cls = None
        elif isinstance(element, Route):
            control_node_cls = SHVRouteControlNode
            test_node_cls = None
        elif isinstance(element, Signal):
            control_node_cls = SHVSignalControlNode
            test_node_cls = None
        elif isinstance(element, SignalSymbol):
            control_node_cls = SHVSignalSymbolControlNode
            test_node_cls = SHVSignalSymbolTestNode
        elif isinstance(element, Zone):
            control_node_cls = SHVZoneControlNode
            test_node_cls = None
        else:
            raise NotImplementedError(
                f'Element type "{type(element).__name__}" is not supported.'
                )
        if control_node_cls is not None:
            control_path = self.get_default_path_control(element)
            control_node = control_node_cls(control_path)
            control_node.set_client_unsafe(self.control_client)
        else:
            control_node = None
        if test_node_cls is not None:
            test_path = self.get_default_path_test(element)
            test_node = test_node_cls(test_path)
            test_node.set_client_unsafe(self.test_client)
        else:
            test_node = None
        return ElementSHVNodes(control_node, test_node)


class PassageGenerator:
    _MIN_TEST_MAX_DURATION: float = 2.0
    _PM_SWITCH_DURATION: float = 3.0
    _DETECTOR_RELEASE_DURATION: float = 2.0
    _MAX_DURATION_MULTIPLIER: float = 1.5

    def __init__(
        self,
        *routes: Route | typing.Iterable[Route | typing.Iterable],
        control_client: ValueClient,
        test_client: ValueClient,
        control_paths: dict[str, str] | None = None,
        test_paths: dict[str, str] | None = None,
    ) -> None:
        self.route_analyzer = RouteAnalyzer(*routes)
        self.shvnode_factory = SHVNodeFactory(
            control_client, test_client, control_paths, test_paths
            )

    @property
    def route_manager(self) -> RouteManager:
        return self.route_analyzer._route_manager

    @staticmethod
    def _check_if_above_boundary(
        value: int | float, boundary: int | float = 0
    ):
        """
        Check if the given value is strictly greater than a specified boundary.

        Args:
            value (int | float): The value to check.
            boundary (int | float): The lower limit that `value` must exceed.

        Raises:
            TypeError: If the value is not a number.
            ValueError: If the value is not strictly greater than the boundary.
        """
        if not isinstance(value, (int, float)):
            raise TypeError(f'"{value}" is not a numeric value.')
        if value <= boundary:
            raise ValueError(f'Value must be greater than {boundary}.')

    @classmethod
    def set_minimum_test_max_duration(cls, max_duration: float = 2.0):
        """
        Sets a minimum base `max_duration` for a test. Any test with a finite
        `max_duration` will have the `max_duration` value at least as large as
        this minimum `max_duration` value, adjusted by the maximum duration
        multiplier factor (set with the `set_max_duration_multiplier` method).
        If a test has an infinite duration, this base value does not affect it.

        Args:
            max_duration (float): The minimum base `max_duration` value
            in seconds. Default is 2.0 seconds.

        Raises:
            ValueError: If max_duration is not strictly greater than 0.
            TypeError: If the max_duration is not a numeric value.
        """
        cls._check_if_above_boundary(max_duration)
        cls._MIN_TEST_MAX_DURATION = max_duration

    @classmethod
    def set_pm_switch_duration(cls, duration: float = 3.0):
        """
        Sets the duration of a point machine switch from one position
        to another.

        Args:
            duration (float): The PM switch duration in seconds.
            Default is 3.0 seconds.

        Raises:
            ValueError: If duration is not strictly greater than 0.
            TypeError: If the duration is not a numeric value.
        """
        cls._check_if_above_boundary(duration)
        cls._PM_SWITCH_DURATION = duration

    @classmethod
    def set_detector_release_duration(cls, duration: float = 2.0):
        """
        Sets the duration of a position detector release lag.

        Args:
            duration (float): The detector release duration in seconds.
            Default is 2.0 seconds.

        Raises:
            ValueError: If duration is not strictly greater than 0.
            TypeError: If the duration is not a numeric value.
        """
        cls._check_if_above_boundary(duration)
        cls._DETECTOR_RELEASE_DURATION = duration

    @classmethod
    def set_max_duration_multiplier(cls, multiplier: float = 1.5):
        """
        Sets the safety multiplier for a test max_duration.

        Args:
            multiplier (float): The max_duration multiplier.
            Must be greater than 1. Default is 2.0.

        Raises:
            ValueError: If multiplier is not strictly greater than 1.
            TypeError: If the multiplier is not a numeric value.
        """
        cls._check_if_above_boundary(multiplier, boundary=1)
        cls._MAX_DURATION_MULTIPLIER = multiplier

    def _ceil_with_multiplier(self, base_max_duration: float) -> float:
        """
        Multiplies the given duration value with maximum duration
        multiplier and rounds it up to the next natural number.

        Args:
            base_max_duration (float): The base max_duration value to be
            multiplied.

        Returns:
            float: The multiplied max_duration value rounded up.

        Raises:
            ValueError: If base_max_duration is not strictly greater than 0.
            TypeError: If base_max_duration is not a numeric value.
        """
        self._check_if_above_boundary(base_max_duration)
        return math.ceil(self._MAX_DURATION_MULTIPLIER * base_max_duration)

    def _calculate_pms_switch_duration(
        self, pms: typing.Sequence[PointMachine]
    ) -> float:
        """
        Calculates the total time required for all point machines to
        switch. The calculation is based on the assumption that only one
        point machine can switch at a time, which is a worst-case scenario.

        Args:
            pms (list[PointMachineType | str]): List of point machines.

        Returns:
            float: The time required for all point machines to switch.
        """
        return self._PM_SWITCH_DURATION * len(pms)

    def _calculate_detectors_release_duration(
        self,
        detectors: typing.Sequence[Detector],
        last_detector: Detector | None = None
    ) -> float:
        """
        Calculates the total time required to release a sequence of detectors,
        under the assumption that only one detector can be released at a time
        (a worst-case scenario). This method allows for truncating
        the sequence at a specified `last_detector`, which can be useful in
        truncated route passage scenarios.

        Args:
            detectors (list[DetectorType | str]): List of detectors.
            last_detector (DetectorType | None): The last detector to be
            released in the sequence. If None, the duration considers
            the release of all detectors in the list.

        Returns:
            float: The total time required to release the specified detectors.
        """
        duration: float = 0
        for det in detectors:
            duration += self._DETECTOR_RELEASE_DURATION
            if det == last_detector:
                break
        return duration

    def _calculate_zone_reset_duration(self, zone: Zone) -> float:
        """
        Calculates the total time required to reset a zone.
        It is determined by the maximum of either the time to switch all
        point machines or the time to release all detectors in the zone.

        Args:
            zone (Zone): The zone to be reset.

        Returns:
            float: The total time required to reset the zone.
        """
        pmes = zone.find_by_type(PointMachineElectrical)
        pmms = zone.find_by_type(PointMachineMechanical)
        dets = zone.find_by_type(Detector)
        return max(
            self._calculate_pms_switch_duration(pmes + pmms),  # type: ignore
            self._calculate_detectors_release_duration(dets)
            )

    def _calculate_route_set_duration(self, route: Route) -> float:
        """
        Calculates the total time required to set a route as the time
        it takes to switch all the point machines in the route layout.

        Args:
            route (Route): The route to be set.

        Returns:
            float: The total time required to set a Route.
        """
        pms = [pm.core for pm in route.layout.pointmachines]
        return self._calculate_pms_switch_duration(pms)

    def _calculate_total_test_max_duration(self, test: TestABC) -> float:
        """
        Recursively calculates the total maximum duration for a given test.
        This method takes into account the hierarchical structure of tests,
        which can include MultiTests that contain child tests.

        For a test with a finite `max_duration`, it will simply return
        this `max_duration`, regardless of whether the test is a `MultiTest`
        or not. This is to avoid  potentially double-counting the child tests'
        maximum durations.

        For a `MultiTest` with an infinite `max_duration`, the method behaves
        differently depending on the type of this `MultiTest`:
        - `SequentialMultiTest`: returns the sum of the maximum durations of
        all child tests.
        - `ParallelMultiTest`: returns the biggest maximum duration among
        all child tests.

        Args:
            test (TestABC): The test for which the total maximum duration
            is calculated.

        Returns:
            float: The calculated total max_duration for the test.
        """
        if test.max_duration != float('inf'):
            return test.max_duration
        if isinstance(test, MultiTestABC):
            child_max_durations = [
                self._calculate_total_test_max_duration(t) for t in test
                ]
            if any(d == float('inf') for d in child_max_durations):
                return float('inf')
            if isinstance(test, SequentialMultiTest):
                return sum(child_max_durations)
            if isinstance(test, ParallelMultiTest):
                return max(child_max_durations, default=float('inf'))
        return float('inf')

    def _calculate_time_between_events(
        self, event: DetectorEvent, i_event: int, events: list[DetectorEvent]
    ) -> float:
        """
        Calculates the time between the given event and the next event in the
        list. This time is the time it takes the passing tram to move between
        the position detector areas. If the given event is the last one in
        the list, it calculates the time until the tram leaves the exit gate.

        Args:
            event (DetectorEvent): The initial event.
            i_event (int): The index of the initial event in the events list.
            events (list[DetectorEvent]): The list of events.

        Returns:
            float: The time between the initial event and the next event or
            exit time.
        """
        try:
            next_event = events[i_event + 1]
            return next_event.time - event.time
        except IndexError:
            next_event_time = self.route_analyzer.estimate_passage_duration(
                route=event.detector.layout.route
                )  # tram leaves the exit gate
            return next_event_time - event.time

    def _assert_zone_set(self, zone: Zone | None) -> typing.TypeGuard[Zone]:
        """
        Asserts that the provided zone object is not None.

        Args:
            zone (Zone | None): The zone object to be checked.

        Raises:
            ConnectorNotSetError: If the zone object is None.
        """
        if zone is None:
            raise ConnectorNotSetError('Zone element has not been found.')
        return True

    def _generate_reset_zone_test(self, zone: Zone) -> ResetZoneTest:
        """
        Generates a `ResetZone` test instance. This test applier the "reset"
        command to every point machine and position detector in the given zone.

        Args:
            zone (Zone | typing.Any): The zone to be reset.

        Raises:
            InvalidZone: If the provided zone object is None or
            not an instance of the `Zone` object.

        Returns:
            ResetZone: A `ResetZone` test instance.
        """
        duration = self._calculate_zone_reset_duration(zone)
        detectors = zone.find_by_type(Detector)
        pmes = zone.find_by_type(PointMachineElectrical)
        pmms = zone.find_by_type(PointMachineMechanical)
        zone_nodes = self.shvnode_factory(zone)
        detectors_nodes = [self.shvnode_factory(det) for det in detectors]
        pmes_nodes = [self.shvnode_factory(pm) for pm in pmes]
        pmms_nodes = [self.shvnode_factory(pm) for pm in pmms]
        return ResetZoneTest(
            zone_control_node=zone_nodes.control,
            detector_control_nodes=[det.control for det in detectors_nodes],
            detector_test_nodes=[det.test for det in detectors_nodes],
            pm_control_nodes=[pm.control for pm in pmes_nodes + pmms_nodes],
            pm_test_nodes=[pm.test for pm in pmes_nodes + pmms_nodes],
            name=f'Reset zone {zone.name}',
            min_duration=None,
            max_duration=self._ceil_with_multiplier(duration)
            )

    def _generate_request_route_test(self, route: Route) -> RequestRouteTest:
        """
        Generates a `RequestRoute` test instance.
        This test is responsible for requesting a route for a passage.

        Args:
            route (Route): The route to be requested.

        Returns:
            RequestRoute: A `RequestRoute` test instance.
        """
        duration = self._MIN_TEST_MAX_DURATION
        gate = route.layout.entry_gate
        return RequestRouteTest(
            route_node=self.shvnode_factory(route).control,
            route_entry_gate_node=self.shvnode_factory(gate).control,
            name=f'Request route {route.name}',
            min_duration=None,
            max_duration=self._ceil_with_multiplier(duration),
            )

    def _generate_check_detector_claimed_test(
        self, detector: Detector
    ) -> ControlNodeStatusValueSingleTest:
        node = self.shvnode_factory(detector).control
        return ControlNodeStatusValueSingleTest(
            node=node,
            success_value=node.status.BitAlias.CLAIMED,
            fail_value=node.status.BitAlias.ERROR_INPUT,
            mask=node.status.BitMask.CLAIMED,
            name=f'Check if detector {detector.name} is CLAIMED',
            max_duration=4,
            max_evaluation_retries=1
            )

    def _generate_check_pm_position_test(
        self, pm: PointMachine, position: PointMachinePosition
    ) -> ControlNodeStatusValueSingleTest:
        node = self.shvnode_factory(pm).control
        match position:
            case PointMachinePosition.LEFT:
                position_value = node.status.BitAlias.LEFT
            case PointMachinePosition.RIGHT:
                position_value = node.status.BitAlias.RIGHT
            case PointMachinePosition.MIDDLE:
                position_value = node.status.BitAlias.MIDDLE
            case _:
                raise ValueError(f'Invalid position value: {position}')
        return ControlNodeStatusValueSingleTest(
            node=node,
            success_value=position_value,
            fail_value=node.status.BitAlias.ERROR_POSITION,
            mask=node.status.BitMask.POSITION,
            name=f'Check if PM {pm.name} is in {position.name}',
            max_duration=4,
            max_evaluation_retries=1
            )

    def _generate_wait_for_route_test(
        self,
        route: Route,
        trigger: RouteLayoutDetector | None,
        check_elements_before_passage: bool,
        min_duration: float | None = None,
        max_duration_offset: float = 0.0
    ) -> WaitUntilRouteIsReadyTest | SequentialMultiTest:
        """
        Generates a `WaitForRoute` test. If `duration` is a non-zero value,
        the test is wrapped in a `SequentialMultiTest` with a wait period.
        This test is responsible for waiting for a route's trigger detector
        to be released.

        Args:
            route (Route): The route to be awaited for.
            trigger (RouteDetector | None): The detector that must be freed
            before this route may be passed.
            check_elements_before_passage (bool): Flag indicating if the state
            of the route's point machines and detectors should be checked
            before the passage.
            duration (float, optional): Optional wait period. Default is 0.0.
            max_duration_offset (float, optional): An offset to add to the minimum  # noqa
            max_duration of the `WaitForRoute` test to reflect the waiting time for 
            the previous routes to pass.

        Returns:
            Union[WaitForRoute, SequentialMultiTest]: The test instance.
        """
        max_duration = self._calculate_route_set_duration(route)
        if trigger is None:
            trigger_detector_node = None
            name = f'Wait until route {route.name} is READY'
        else:
            trigger_detector_node = self.shvnode_factory(trigger.core).control
            name = (
                f'Wait until route {route.name} is READY '
                f'after detector {trigger.core.name} is released'
                )
        wait_for_route_test = WaitUntilRouteIsReadyTest(
            route_control_node=self.shvnode_factory(route).control,
            trigger_detector_control_node=trigger_detector_node,
            name=name,
            min_duration=None,
            max_duration=(max_duration + max_duration_offset),
            prevent_race_condition=True
            )
        if not check_elements_before_passage:
            return wait_for_route_test
        det_tests = [
            self._generate_check_detector_claimed_test(det.core)
            for det in route.layout.detectors
            ]
        pm_tests = [
            self._generate_check_pm_position_test(pm.core, pm.position)
            for pm in route.layout.pointmachines
            ]
        return SequentialMultiTest(
            wait_for_route_test,
            ParallelMultiTest(
                *det_tests,
                *pm_tests,
                name=f'Check elements before route {route.name} passage'
                ),
            name=f'Wait for route {route.name} and check elements'
            )

    def _generate_route_state_check_test(
        self, route: Route, released_detector: RouteLayoutDetector
    ) -> ControlNodeStatusValueSingleTest:
        """
        Generates a 'CheckIfRouteFree' or 'CheckIfRouteOccupied' test instance
        based on the position of the released detector in the route. The test
        is used to check if the route is free or occupied after a detector
        has been released.

        Args:
            route (Route): The route to be checked.
            released_detector (RouteDetector): The detector that has been
            released.

        Returns:
            Union[CheckIfRouteFree, CheckIfRouteOccupied]: The test instance.
        """
        route_node = self.shvnode_factory(route).control
        if route.layout.index(released_detector) == len(route.layout) - 1:
            name = (
                f'Check if route {route.name} is FREE after detector '
                f'{released_detector.name} is released'
                )
            return ControlNodeStatusValueSingleTest(
                node=route_node,
                success_value=SHVRouteStatusNode.BitAlias.FREE,
                fail_value=SHVRouteStatusNode.BitAlias.OCCUPIED,
                mask=SHVRouteStatusNode.BitMask.STATE,
                name=name,
                execution_sleep=1,
                max_duration=4,
                max_evaluation_retries=1
                )
        else:
            name = (
                f'Check if route {route.name} is OCCUPIED after detector '
                f'{released_detector.name} is released'
                )
            return ControlNodeStatusValueSingleTest(
                node=route_node,
                success_value=SHVRouteStatusNode.BitAlias.OCCUPIED,
                fail_value=SHVRouteStatusNode.BitAlias.FREE,
                mask=SHVRouteStatusNode.BitMask.STATE,
                name=f'Check route {route.name} status',
                max_duration=4,
                max_evaluation_retries=1
                )

    def _generate_detector_occupation_test(
        self,
        detector: RouteLayoutDetector,
        min_duration: float | None = None
    ) -> DetectorSetOccupiedTest:
        """
        Generates a `SetDetectorOccupied` test, which simulates the occupation
        of a position detector. If `duration` is a non-zero value, the test is
        wrapped in a `ParallelMultiTest` with a wait period, which represents
        the time it takes a passing tram to move between the detector areas.

        Args:
            detector (RouteDetector): The detector to be set as occupied.
            duration (float, optional): Time for the Wait test to simulate
            the tram's movement time. Defaults to 0.

        Returns:
            Union[SetDetectorOccupied, ParallelMultiTest]: The generated test.
        """
        max_duration = self._ceil_with_multiplier(self._MIN_TEST_MAX_DURATION)
        return DetectorSetOccupiedTest(
            control_node=self.shvnode_factory(detector.core).control,
            test_node=self.shvnode_factory(detector.core).test,
            name=f'Set {detector.core.name} occupied',
            min_duration=None,
            max_duration=max_duration
            )

    def _generate_detector_release_test(
        self,
        detector: RouteLayoutDetector,
        route: Route,
        duration: float | None = None
    ) -> SequentialMultiTest:
        """
        Generates a `SetDetectorFree` test, which simulates the occupation
        of a position detector. If `duration` is a non-zero value, the test is
        wrapped in a `ParallelMultiTest` with a wait period, which represents
        the time it takes a passing tram to move between the detector areas.

        Args:
            detector (RouteDetector): The detector to be set as occupied.
            duration (float, optional): Time for the Wait test to simulate
            the tram's movement time. Defaults to 0.

        Returns:
            Union[SetDetectorOccupied, ParallelMultiTest]: The generated test.
        """
        # create a test to change the detector state
        max_duration = self._ceil_with_multiplier(self._MIN_TEST_MAX_DURATION)
        set_detector_free = DetectorSetFreeTest(
            control_node=self.shvnode_factory(detector.core).control,
            test_node=self.shvnode_factory(detector.core).test,
            name=f'Set {detector.core.name} free',
            min_duration=None,
            max_duration=max_duration
            )
        # create a test to validate the route state after the change
        check_route = self._generate_route_state_check_test(route, detector)
        # combine the tests into a SequentialMultiTest
        return SequentialMultiTest(
            set_detector_free,
            check_route,
            name=f'Release {detector.name} and check route {route.name} state'
            )

    def _generate_detector_state_change_test(
        self,
        detector: RouteLayoutDetector,
        change_state_to: bool,
        route: Route,
        duration: float | None = None
    ) -> typing.Union[DetectorSetOccupiedTest, SequentialMultiTest]:
        """
        Generates a test or test sequence to simulate a state change of
        a detector, either to 'occupied' or 'free'. Depending on the
        `change_state_to` parameter, this function calls either
        `_generate_detector_occupation_test` or
        `_generate_detector_release_test`.

        Args:
            detector (RouteDetector): The detector, the state of which is
            to be changed.
            change_state_to (bool): The desired state of the detector.
            True for 'occupied', False for 'free'.
            route (Route): The route for the route state check test in case of
            detector release.
            duration (float, optional): Time for the Wait test to simulate
            the tram's  movement time. Defaults to 0.

        Returns:
            Union[SetDetectorOccupied, SequentialMultiTest, ParallelMultiTest]:
            The generated test or test sequence.
        """
        if change_state_to is True:  # detector occupation event
            return self._generate_detector_occupation_test(
                detector, duration
                )
        elif change_state_to is False:  # detector release event
            return self._generate_detector_release_test(
                detector, route, duration
                )
        raise TypeError(
            f'Invalid value for the "change_state_to" parameter: '
            f'{change_state_to}'
            )

    def _generate_passage_test_sequence(
        self,
        route: Route,
        fastmode: bool,
        trigger: RouteLayoutDetector | None,
        last_detector_to_release: RouteLayoutDetector | None,
        check_elements_before_passage: bool,
        wait_for_route_max_duration_offset: float = 0.0
    ) -> SequentialMultiTest:
        """
        This function creates a sequence of tests that simulates the passage of
        a tram through the specified route. It constructs this simulation based
        on the trigger detector of the route and the sequence of the occupation
        and release events of the detectors if the route layout
        (up to the specified last detector).

        Args:
            route (Route): The route to be passed.
            fastmode (bool): If True, the time delays between the detector
            occupation and release events in the passage test sequence are
            ignored.
            trigger (RouteDetector | None): A detector that needs to be
            released before the route switches to BUILD / READY state.
            If None, it means that the route can start immediately, which is
            common for the first route in the passage sequence or for a route
            that does not share elements with any passing route.
            last_detector_to_release (RouteDetector): This is the last
            detector in the layout of the route that needs to be released
            as part of the test sequence.
            check_elements_before_passage (bool): A flag indicating whether
            the state of point machines and detectors in the layout of the
            route should be checked before the passage test sequence begins.
            wait_for_route_max_duration_offset (float, optional): An additional
            time delay added to the max_duration for the `WaitForRoute` test.
            It is used when there is a need to account for the passage time of
            previous routes. Defaults to 0.0.

        Returns:
            SequentialMultiTest: The passage test sequence.
        """
        passage_test_max_duration: float = 0
        passage_test_sequence: list[TestABC] = []
        events = self.route_analyzer._determine_detector_events(
            route, last_detector_to_release
            )
        # the time it takes the front of the tram to get to
        # the start of the first detector area is the route layout
        time_to_first_detector: float = 0 if fastmode else events[0].time
        # start the passage test sequence with checking the route state
        wait_for_route_test = self._generate_wait_for_route_test(
            route, trigger, check_elements_before_passage,
            time_to_first_detector, wait_for_route_max_duration_offset
            )
        passage_test_sequence.append(wait_for_route_test)
        passage_test_max_duration += time_to_first_detector
        passage_test_max_duration += self._calculate_total_test_max_duration(
            wait_for_route_test
            )
        # iterate though the events and generate the corresponding tests
        for i, event in enumerate(events):
            if fastmode:
                time_between_events: float = 0
            else:
                time_between_events = self._calculate_time_between_events(
                    event, i, events
                    )
            # create a detector test based on the event type
            detector_test = self._generate_detector_state_change_test(
                event.detector, event.action, route, time_between_events
                )
            detector_test_duration = self._calculate_total_test_max_duration(
                detector_test
                )
            passage_test_max_duration += time_between_events
            passage_test_max_duration += detector_test_duration
            passage_test_sequence.append(detector_test)
        return SequentialMultiTest(
            *passage_test_sequence,
            max_duration=math.ceil(passage_test_max_duration),
            name=f'Route {route.name} passage simulation'
            )  # wrap the generated tests into a SequentialMultiTest

    def _generate_passage_scenario_single_route(
        self,
        route: Route,
        add_zone_reset: bool,
        truncate: bool,
        fastmode: bool,
    ) -> SequentialMultiTest:
        """
        Generate a tram passage scenario for a single route
        with a route request and an optional Zone reset.

        The scenario includes:

        1. `ResetZone` (optional);
        2. `RequestRoute`;
        3. `WaitForRoute` (checks the state of the route and its elements);
        4. A sequence of `SetDetectorOccupied` and `SetDetectorFree` tests
        (the latter are applied in conjuction with the route state ckecker
        tests `CheckIfRouteOccupied` or `CheckIfRouteFree`).

        Args:
            route (Route): The Route object to generate the scenario for.
            add_zone_reset (bool): If True, add a Zone reset test sequence,
            which resets all the detectors the point machines in this Zone.
            truncate (bool): If True, the passage scenario ends with the
            occupation of the route's first detector. Otherwise the scenario
            continues to the release of the route's last detector.
            fastmode (bool): If True, the time delays between the detector
            occupation and release events in the passage test sequence are
            ignored.

        Returns:
            SequentialMultiTest: The passage scenario wrapped into
            a `SequentialMultiTest`.
        """
        max_duration: float = 0
        tests: list[TestABC] = []
        # add the Reset test (optional)
        if add_zone_reset:
            if route.zone is None:
                raise ValueError(f'Route {route.name} has no Zone assigned.')
            reset_zone_test = self._generate_reset_zone_test(route.zone)
            tests.append(reset_zone_test)
            max_duration += self._calculate_total_test_max_duration(
                reset_zone_test
                )
        # add the RouteRequest test
        request_route_test = self._generate_request_route_test(route)
        tests.append(request_route_test)
        max_duration += self._calculate_total_test_max_duration(
            request_route_test
            )
        # create a passage test sequence
        last_detector_to_release = None if truncate else route.layout.detectors[-1]  # noqa
        passage_test = self._generate_passage_test_sequence(
            route=route,
            fastmode=fastmode,
            trigger=None,
            last_detector_to_release=last_detector_to_release,
            check_elements_before_passage=True,
            )
        tests.append(passage_test)
        max_duration += self._calculate_total_test_max_duration(passage_test)
        return SequentialMultiTest(
            *tests,
            max_duration=max_duration,
            name=f'Route {route.name} passage'
            )

    def _generate_passage_scenario_multiple_routes(
        self,
        routes: list[Route],
        add_zone_reset: bool,
        truncate: bool,
        fastmode: bool,
    ) -> SequentialMultiTest:
        """
        Generate a tram passage scenario for multiple routes with
        a route request for each route and an optional Zone reset.

        The scenario includes:

        1. `ResetZone` (optional);
        2. A sequence of `RequestRoute` tests for each route;
        3. A sequence of `WaitForRoute` tests for each (checks the state of
        the route and whether it is set in the right time);
        4. A sequence of `SetDetectorOccupied` and `SetDetectorFree` tests
        for each route (the latter are applied in conjuction with the route
        state ckecker tests `CheckIfRouteOccupied` or `CheckIfRouteFree`).

        Args:
            routes (list[Route]): A list of Route objects
            to generate the scenario for.
            add_zone_reset (bool): If True, adds a Zone reset test sequence
            at the beginning of the scenario.
            truncate (bool): If True, the passage scenario ends with
            the occupation of the route's furthest-from-its-startgate detector,
            which is also a trigger detector for some other route in
            the scenario. Otherwise, the scenario continues to the release of
            the route's last detector.
            fastmode (bool): If True, the time delays between the detector
            occupation and release events in the passage test sequence are
            ignored.

        Returns:
            SequentialMultiTest: The generated passage scenario wrapped into
            a SequentialMultiTest.
        """
        max_duration: float = 0
        tests: list[TestABC] = []
        # add the Reset test (optional)
        if add_zone_reset:
            zone: Zone | None = None
            for route in routes:
                if route.zone is not None:
                    zone = route.zone
                    break
            if zone is None:
                raise ValueError('Routes have no Zone assigned.')
            reset_zone_test = self._generate_reset_zone_test(zone)
            tests.append(reset_zone_test)
            max_duration += self._calculate_total_test_max_duration(
                reset_zone_test
                )
        # add the RouteRequest test for every route in the list
        route_request_tests = [
            self._generate_request_route_test(r) for r in routes
            ]
        tests.append(
            SequentialMultiTest(
                *route_request_tests,
                name=f'Request routes {", ".join(r.name for r in routes)}'
                )
            )
        for test in route_request_tests:
            max_duration += self._calculate_total_test_max_duration(test)
        # add a passage test sequence for each route
        route_passage_tests: list[SequentialMultiTest] = []
        route_passage_order = self.route_analyzer.determine_route_order(
            routes, truncate=truncate
            )
        max_duration_offset: float = 0
        for item in route_passage_order:
            passage_test = self._generate_passage_test_sequence(
                route=item.route,
                fastmode=fastmode,
                trigger=item.trigger_detector,
                last_detector_to_release=item.last_detector_to_release,
                check_elements_before_passage=False,
                wait_for_route_max_duration_offset=max_duration_offset
                )
            max_duration_offset += self._calculate_total_test_max_duration(
                passage_test
                )
            route_passage_tests.append(passage_test)
        tests.append(
            ParallelMultiTest(
                *route_passage_tests,
                name=(
                    f'Routes {", ".join(route.name for route in routes)} '
                    f'simultaneous passage'
                )
            )
        )
        max_duration += max_duration_offset
        # combine all the generated tests into a multipassage test scenario
        return SequentialMultiTest(
            *tests,
            max_duration=max_duration,
            name=(
                f'Routes {", ".join(route.name for route in routes)} '
                f'simultaneous passage simulation'
            )
        )

    def generate_passage_scenario(
        self,
        *routes: str | Route,
        add_zone_reset: bool = True,
        truncate: bool = True,
        fastmode: bool = True,
    ) -> SequentialMultiTest:
        """
        Generate a passage scenario for the provided route or a set of routes.

        The scenario includes:

        1. A `ResetZone` test (optional);
        2. A sequence of `RequestRoute` tests for each route;
        3. A sequence of `WaitForRoute` tests for each route (check the state
        of the route and its elements, and whether the route is set
        in the right time);
        4. A sequence of `SetDetectorOccupied` and `SetDetectorFree` tests
        for each route (the latter are applied in conjuction with the route
        state ckecker tests `CheckIfRouteOccupied` or `CheckIfRouteFree`).

        Args:
            routes (str | Route): A set of routes to generate the scenario for.
            Can be specified as route names (strings) or Route objects.
            add_zone_reset (bool): If True, adds the `ResetZone` test sequence
            at the beginning of the scenario. Defaults to True.
            truncate (bool): If True, the passage scenario ends with the
            occupation of the route's furthest-from-startgate detector,
            which is also a trigger detector for some other route in the
            scenario. (A detector is considered a trigger for a route if
            this detector must be released before this route may be passed.
            Such a detector usually releases the last common layout element
            shared between the this route and some route that has started
            being passed before it.) In case there are no such detectors,
            the fisrt detector in the layout is occupied. Without trucnation,
            the scenario continues to the release of the route's last detector.
            fastmode (bool): If True, the time delays between the detector
            occupation and release events in the passage test sequence are
            ignored. Defaults to True.

        Returns:
            SequentialMultiTest | None: The generated passage scenario wrapped
            into a SequentialMultiTest. If the route list is empty,
            the function returns None.
        """
        route_objs = self.route_manager._get_route_batch(routes)
        if not route_objs:
            raise ValueError('No routes have been found.')
        if len(route_objs) == 1:
            logger.info(
                'Generating a test scenario for the route %s passage',
                route_objs[0].name
                )
            return self._generate_passage_scenario_single_route(
                route_objs[0], add_zone_reset, truncate, fastmode
                )
        else:
            logger.info(
                'Generating a test scenario for the routes %s passage',
                ", ".join(r.name for r in route_objs)
                )
            return self._generate_passage_scenario_multiple_routes(
                route_objs, add_zone_reset, truncate, fastmode
                )
