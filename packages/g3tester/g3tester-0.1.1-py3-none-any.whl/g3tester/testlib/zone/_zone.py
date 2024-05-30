import typing

import shv

from g3shvnodes.zone import SHVZoneControlNode
from g3shvnodes.detector import SHVDetectorControlNode, SHVDetectorTestNode
from g3shvnodes.pointmachine import (
    SHVPMEControlNode, SHVPMETestNode, SHVPMMControlNode, SHVPMMTestNode
)

from ...tags import command
from ..._test import SequentialMultiTest, ParallelMultiTest
from ..element import ControlNodeStatusValueSingleTest
from ..detector import DetectorResetTest
from ..pointmachine import PMResetTest


class SetZoneABTest(ControlNodeStatusValueSingleTest[SHVZoneControlNode]):
    def __init__(
        self,
        node: SHVZoneControlNode,
        name: str | None = None,
        execution_sleep: float = 1,
        min_duration: float | None = None,
        max_duration: float | None = None,
        max_evaluation_retries: int | None = None
    ) -> None:
        super().__init__(
            node=node,
            success_value=node.status.BitAlias.AB,
            fail_value=None,
            mask=node.status.BitMask.STATE,
            name=name,
            execution_sleep=execution_sleep,
            min_duration=min_duration,
            max_duration=max_duration,
            max_evaluation_retries=max_evaluation_retries
            )

    @command
    async def set_ab(self) -> shv.SHVType:
        return await self.control_node.set_all_blocked()


class SetZoneNormTest(ControlNodeStatusValueSingleTest[SHVZoneControlNode]):
    def __init__(
        self,
        node: SHVZoneControlNode,
        name: str | None = None,
        execution_sleep: float = 1,
        min_duration: float | None = None,
        max_duration: float | None = None,
        max_evaluation_retries: int | None = None
    ) -> None:
        super().__init__(
            node=node,
            success_value=node.status.BitAlias.NORM,
            fail_value=None,
            mask=node.status.BitMask.STATE,
            name=name,
            execution_sleep=execution_sleep,
            min_duration=min_duration,
            max_duration=max_duration,
            max_evaluation_retries=max_evaluation_retries
            )

    @command
    async def set_norm(self) -> shv.SHVType:
        return await self.control_node.set_normal()


SHVPMControlNode: typing.TypeAlias = typing.Union[
    SHVPMEControlNode, SHVPMMControlNode
    ]

SHVPMTestNode: typing.TypeAlias = typing.Union[
    SHVPMETestNode, SHVPMMTestNode
    ]


class ResetZoneTest(SequentialMultiTest):
    def __init__(
        self,
        zone_control_node: SHVZoneControlNode,
        detector_control_nodes: typing.Collection[SHVDetectorControlNode],
        detector_test_nodes: typing.Collection[SHVDetectorTestNode],
        pm_control_nodes: typing.Collection[SHVPMControlNode],
        pm_test_nodes: typing.Collection[SHVPMTestNode],
        name: str | None = None,
        min_duration: float | None = None,
        max_duration: float | None = None,
    ) -> None:
        super().__init__(
            ParallelMultiTest(
                *self._init_reset_detector_tests(
                    detector_control_nodes, detector_test_nodes, max_duration
                    ),
                *self._init_reset_pm_tests(
                    pm_control_nodes, pm_test_nodes, max_duration
                    ),
                name='Reset all detectors and point machines',
                allow_fail=True,
                max_duration=max_duration
                ),
            self._init_set_ab_test(zone_control_node),
            self._init_set_norm_test(zone_control_node),
            allow_fail=False,
            name=name,
            min_duration=min_duration,
            max_duration=max_duration,
            )

    @staticmethod
    def _get_name_from_shv_path(path: str) -> str:
        return path.split('/')[-1]

    def _init_reset_detector_tests(
        self,
        control_nodes: typing.Collection[SHVDetectorControlNode],
        test_nodes: typing.Collection[SHVDetectorTestNode],
        max_duration: float | None = None
    ) -> list[DetectorResetTest]:
        if len(control_nodes) != len(test_nodes):
            raise ValueError(
                'Control and test nodes must have the same length.'
                )
        tests: list[DetectorResetTest] = []
        for control_node, test_node in zip(control_nodes, test_nodes):
            detector_name = self._get_name_from_shv_path(control_node.path)
            tests.append(
                DetectorResetTest(
                    control_node=control_node,
                    test_node=test_node,
                    name=f'Reset detector {detector_name}',
                    max_duration=5
                    )
                )
        return tests

    def _init_reset_pm_tests(
        self,
        control_nodes: typing.Collection[SHVPMControlNode],
        test_nodes: typing.Collection[SHVPMTestNode],
        max_duration: float | None = None
    ) -> list[PMResetTest]:
        if len(control_nodes) != len(test_nodes):
            raise ValueError(
                'Control and test nodes must have the same length.'
                )
        tests: list[PMResetTest] = []
        for control_node, test_node in zip(control_nodes, test_nodes):
            pm_name = self._get_name_from_shv_path(control_node.path)
            tests.append(
                PMResetTest(
                    control_node=control_node,
                    test_node=test_node,
                    name=f'Reset PM {pm_name}',
                    max_duration=5
                    )
                )
        return tests

    def _init_set_ab_test(
        self, node: SHVZoneControlNode
    ) -> ControlNodeStatusValueSingleTest[SHVZoneControlNode]:
        zone_name = self._get_name_from_shv_path(node.path)
        return SetZoneABTest(
            node=node,
            name=f'Set Zone {zone_name} AB',
            )

    def _init_set_norm_test(
        self, node: SHVZoneControlNode
    ) -> ControlNodeStatusValueSingleTest[SHVZoneControlNode]:
        zone_name = self._get_name_from_shv_path(node.path)
        return SetZoneNormTest(
            node=node,
            name=f'Set Zone {zone_name} NORM',
            )
