import asyncio

import shv

from g3shvnodes.route import SHVRouteControlNode
from g3shvnodes.gate import SHVGateControlNode
from g3shvnodes.detector import SHVDetectorControlNode, SHVDetectorStatusNode

from ...enums import TestStatus
from ...exceptions import TestFail, TestFailFatal
from ...tags import (
    command, before_command, value_getter, success, on_status_change
)
from ..._test import SingleTest


class RequestRouteTest(SingleTest[list[str]]):
    def __init__(
        self,
        route_node: SHVRouteControlNode,
        route_entry_gate_node: SHVGateControlNode,
        name: str | None = None,
        execution_sleep: float = 1,
        min_duration: float | None = None,
        max_duration: float | None = None,
        max_evaluation_retries: int | None = None
    ) -> None:
        super().__init__(
            name=name,
            execution_sleep=execution_sleep,
            min_duration=min_duration,
            max_duration=max_duration,
            max_evaluation_retries=max_evaluation_retries
            )
        self.route_node = route_node
        self.route_entry_gate_node = route_entry_gate_node
        self.gate_memory_before_request: list[str] = []

    @property
    def route_name(self) -> str:
        return self.route_node.path.split('/')[-1]

    @command
    async def request(self) -> shv.SHVType:
        return await self.route_node.request()

    @value_getter
    async def get_route_memory(self) -> list[str]:
        
        memory = await self.route_entry_gate_node.request_memory.get()
        if not isinstance(memory, str):
            raise TestFailFatal(f'Expected str, got {type(memory).__name__}')
        return memory.splitlines()

    @before_command(command=request)
    async def get_route_memory_before_request(self) -> None:
        memory = await self.get_route_memory()
        self.gate_memory_before_request = memory

    @success
    def is_route_requested(self) -> bool:
        berofe_request = set(self.gate_memory_before_request)
        assert self.value is not None, 'value is None'
        after_request = set(self.value)
        diff = after_request - berofe_request
        route_name = self.route_name
        return any(route_name in line for line in diff)


class WaitUntilRouteIsReadyTest(SingleTest[int]):
    def __init__(
        self,
        route_control_node: SHVRouteControlNode,
        trigger_detector_control_node: SHVDetectorControlNode | None = None,
        name: str | None = None,
        execution_sleep: float = 1,
        min_duration: float | None = None,
        max_duration: float | None = None,
        prevent_race_condition: bool = True
    ) -> None:
        super().__init__(
            name=name,
            execution_sleep=execution_sleep,
            min_duration=min_duration,
            max_duration=max_duration,
            max_evaluation_retries=1
            )
        self.route_control_node = route_control_node
        self.trigger_detector_control_node = trigger_detector_control_node
        self.trigger_detector_occupied: bool = False
        self.trigger_detector_released: bool = False
        self.trigger_detector_status_update_task: asyncio.Task | None = None
        self.prevent_race_condition = prevent_race_condition

    @property
    def trigger_status_node(self) -> SHVDetectorStatusNode:
        if self.trigger_detector_control_node is None:
            raise AttributeError('trigger_detector_control_node is None')
        return self.trigger_detector_control_node.status

    @property
    def trigger_name(self) -> str:
        return self.trigger_status_node.path.split('/')[-2]

    @property
    def route_name(self) -> str:
        return self.route_control_node.path.split('/')[-1]

    async def _await_trigger_detector_occupied(self) -> int:
        self._logger.debug(
            'Waiting for the trigger detector "%s" to be occupied',
            self.trigger_name
            )
        status = await self.trigger_status_node.status_change_wait(
            any_false=[SHVDetectorStatusNode.BitAlias.FREE],
            any_true=[SHVDetectorStatusNode.BitAlias.OCCUPIED],
            timeout=self.max_duration,
            get_period=self._exec_sleep
            )
        self._logger.debug(
            'The trigger detector "%s" is occupied',
            self.trigger_name
            )
        return status

    async def _await_trigger_detector_released(self) -> int:
        self._logger.debug(
            'Waiting for the trigger detector "%s" to be released',
            self.trigger_name
            )
        status = await self.trigger_status_node.status_change_wait(
            any_false=[SHVDetectorStatusNode.BitAlias.OCCUPIED],
            any_true=[SHVDetectorStatusNode.BitAlias.FREE],
            timeout=self.max_duration,
            get_period=self._exec_sleep
            )
        self._logger.debug(
            'The trigger detector "%s" is released',
            self.trigger_name
            )
        return status

    async def track_trigger_detector(self) -> None:
        if self.trigger_detector_control_node is None:
            self.trigger_detector_occupied = True
            self.trigger_detector_released = True
            return
        await self._await_trigger_detector_occupied()
        self.trigger_detector_occupied = True
        await self._await_trigger_detector_released()
        self.trigger_detector_released = True

    @on_status_change(
        change_to=[TestStatus.RUNNING],
        priority=1
        )
    async def subscribe(self) -> None:
        if self.trigger_detector_control_node is not None:
            await self.trigger_status_node.subscribe()
        await self.route_control_node.status.subscribe()

    @on_status_change(
        change_to=[TestStatus.RUNNING],
        priority=2
        )
    def start_tracking_trigger_detector(self) -> None:
        if (
            self.trigger_detector_status_update_task is None or
            self.trigger_detector_status_update_task.done()
        ):
            self.trigger_detector_status_update_task = asyncio.create_task(
                self.track_trigger_detector()
                )

    @on_status_change(
        change_to=[
            TestStatus.PASSED,
            TestStatus.PASSED_WITH_WARNING,
            TestStatus.FAILED,
            TestStatus.TIMEOUT,
            TestStatus.ABORTED
            ],
        priority=1
        )
    async def stop_tracking_trigger_detector(self) -> None:
        if self.trigger_detector_status_update_task is not None:
            self.trigger_detector_status_update_task.cancel()
            try:
                await self.trigger_detector_status_update_task
            except asyncio.CancelledError:
                pass
            self.trigger_detector_status_update_task = None

    @on_status_change(
        change_to=[
            TestStatus.PASSED,
            TestStatus.PASSED_WITH_WARNING,
            TestStatus.FAILED,
            TestStatus.TIMEOUT,
            TestStatus.ABORTED
            ],
        priority=2
        )
    async def unsubscribe(self) -> None:
        if self.trigger_detector_control_node is not None:
            await self.trigger_status_node.unsubscribe()
        await self.route_control_node.status.unsubscribe()

    @value_getter
    async def get_route_status(self) -> int:
        return await self.route_control_node.status.get()

    @before_command
    async def await_route_status_change(self) -> None:
        route_status = await self.get_route_status()
        if self.route_control_node.status.is_free(route_status) is False:
            if self.trigger_detector_control_node is not None:
                raise TestFail(
                    f'Route "{self.route_name}" is not free in the beginning '
                    f'of the test. Route status: {route_status}. '
                    f'The trigger detector "{self.trigger_name}" state: '
                    f'FREED={self.trigger_detector_released}, '
                    f'OCCUPIED={self.trigger_detector_occupied}'
                    )
        self._logger.debug(
            'Waiting until the route "%s" switches to READY',
            self.route_name
            )
        bit_alias = self.route_control_node.status.BitAlias

        if(route_status != bit_alias.READY):
            await self.route_control_node.status.status_change_wait(
                any_true=[bit_alias.READY, bit_alias.BUILD],
                any_false=[bit_alias.FREE],
                timeout=self.max_duration,
                get_period=self._exec_sleep
                )
        if self.trigger_detector_control_node is not None:
            # prevent race condition, when the trigger detector release after
            # its occupation is registered with a delay. This can happen if
            # the detector datachange event is not registered or
            # is registered with a delay. This is slightly unsafe, because
            # theoretically (although very unlikely) the detector release can
            # physically happen and be registered AFTER the route is ready,
            # which should fail the test, but will not.
            if self.prevent_race_condition:
                if (
                    self.trigger_detector_occupied is False or
                    self.trigger_detector_released is False
                ):
                    await asyncio.sleep(self._exec_sleep + 0.05)

    @success
    async def is_route_status_build_or_ready(self) -> bool:
        status = self.value
        assert status is not None, 'value has not been set by the getter'
        return (
            (
                self.route_control_node.status.is_build(status) or
                self.route_control_node.status.is_ready(status)
            ) and
            (
                self.trigger_detector_occupied is True and
                self.trigger_detector_released is True
            )
        )
