import asyncio

from typing import Generic, TypeVar

from g3shvnodes import SHVNode, SHVStatusNode

from ..._test import SingleTest
from ...enums import TestStatus
from ...exceptions import TestFailFatal
from ...tags import (
    before_command,
    after_command,
    success,
    fail,
    on_status_change,
    value_getter
)


TSHVNode = TypeVar('TSHVNode', bound=SHVNode)


class ControlNodeStatusValueSingleTest(SingleTest[int], Generic[TSHVNode]):
    FAIL_EVAL_DELAY_SEC = 0.5
    """
    Specifies the time delay in seconds added before the test starts
    comparing the actual value with the expected error value. This delay
    is applied in cases where the initial actual value equals the error value.
    The delay accounts for the latency between the application of a command
    by the test and the actual effect of that command on the system.
    """

    def __init__(
        self,
        node: TSHVNode,
        success_value: int,
        fail_value: int | None = None,
        mask: int | None = None,
        name: str | None = None,
        execution_sleep: float = 1,
        min_duration: float | None = None,
        max_duration: float | None = None,
        max_evaluation_retries: int | None = None
    ) -> None:
        super().__init__(
            name,
            execution_sleep,
            min_duration,
            max_duration,
            max_evaluation_retries,
            )
        self.control_node: TSHVNode = node
        self.success_value: int = success_value
        self.fail_value: int | None = fail_value
        self.mask: int | None = mask

    @property
    def control_status_node(self) -> SHVStatusNode:
        status_node = getattr(self.control_node, 'status', None)
        if not isinstance(status_node, SHVStatusNode):
            node_cls_name = self.control_node.__class__.__name__
            raise TestFailFatal(
                f'Control node "{node_cls_name}" does not have a "status" '
                f'attribute storing a status property node'
                )
        return status_node

    @value_getter
    async def get_control_status_value(self) -> int:
        """
        Read the status of the tracked element node (a 32-bit uint).

        Raises:
            exceptions.TestFailFatal: If the node does not have a status
            property node with the `get()` method.

        Returns:
            int: The status value.
        """
        return await self.control_status_node.get()

    @before_command(priority=-1)
    async def subscribe_control_status_node(self) -> bool:
        """
        Subscribe to the status change events of the control status node.
        """
        async with asyncio.Lock():
            if self.control_status_node.is_subscribed:
                return True
            return await self.control_status_node.subscribe()

    @after_command
    async def delay_init_fail_eval(self) -> None:
        value = await self._get_value()
        if value == self.fail_value:
            await asyncio.sleep(self.FAIL_EVAL_DELAY_SEC)

    @success
    def is_equal_to_success_value(self) -> bool:
        if self.mask is None:
            value = self.value
        elif self.value is not None:  # should be always True
            value = self.value & self.mask
        return value == self.success_value

    @fail
    def is_equal_to_fail_value(self) -> bool:
        if self.fail_value is None:
            return False
        if self.mask is None:
            value = self.value
        elif self.value is not None:  # should be always True
            value = self.value & self.mask
        return value == self.fail_value

    @on_status_change(
        change_to=[
            TestStatus.TIMEOUT,
            TestStatus.FAILED,
            TestStatus.ABORTED,
            TestStatus.PASSED,
            TestStatus.PASSED_WITH_WARNING
        ]
    )
    async def unsubscribe_control_status_node(self) -> bool:
        """
        Unsubscribe from the status change events of the control status node.
        """
        async with asyncio.Lock():
            if not self.control_status_node.is_subscribed:
                return True
            return await self.control_status_node.unsubscribe()
