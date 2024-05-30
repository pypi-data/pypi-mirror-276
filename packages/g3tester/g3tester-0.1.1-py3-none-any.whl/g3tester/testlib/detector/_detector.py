import shv

from g3shvnodes.detector import SHVDetectorControlNode, SHVDetectorTestNode

from ..element import ControlNodeStatusValueSingleTest
from ...tags import command


class DetectorSetFreeTest(
    ControlNodeStatusValueSingleTest[SHVDetectorControlNode]
):
    def __init__(
        self,
        control_node: SHVDetectorControlNode,
        test_node: SHVDetectorTestNode,
        name: str | None = None,
        execution_sleep: float = 1,
        min_duration: float | None = None,
        max_duration: float | None = None,
        max_evaluation_retries: int | None = None
    ) -> None:
        super().__init__(
            node=control_node,
            success_value=control_node.status.BitAlias.FREE,
            fail_value=control_node.status.BitAlias.ERROR_INPUT,
            mask=control_node.status.BitMask.STATE,
            name=name,
            execution_sleep=execution_sleep,
            min_duration=min_duration,
            max_duration=max_duration,
            max_evaluation_retries=max_evaluation_retries
            )
        self.test_node = test_node

    @command
    async def set_false(self) -> shv.SHVType:
        return await self.test_node.set_false()


class DetectorSetOccupiedTest(
    ControlNodeStatusValueSingleTest[SHVDetectorControlNode]
):
    def __init__(
        self,
        control_node: SHVDetectorControlNode,
        test_node: SHVDetectorTestNode,
        name: str | None = None,
        execution_sleep: float = 1,
        min_duration: float | None = None,
        max_duration: float | None = None,
        max_evaluation_retries: int | None = None
    ) -> None:
        super().__init__(
            node=control_node,
            success_value=control_node.status.BitAlias.OCCUPIED,
            fail_value=control_node.status.BitAlias.ERROR_INPUT,
            mask=control_node.status.BitMask.STATE,
            name=name,
            execution_sleep=execution_sleep,
            min_duration=min_duration,
            max_duration=max_duration,
            max_evaluation_retries=max_evaluation_retries
            )
        self.test_node = test_node

    @command
    async def set_true(self) -> shv.SHVType:
        return await self.test_node.set_true()


class DetectorResetTest(
    ControlNodeStatusValueSingleTest[SHVDetectorControlNode]
):
    def __init__(
        self,
        control_node: SHVDetectorControlNode,
        test_node: SHVDetectorTestNode,
        name: str | None = None,
        execution_sleep: float = 1,
        min_duration: float | None = None,
        max_duration: float | None = None,
        max_evaluation_retries: int | None = None
    ) -> None:
        super().__init__(
            node=control_node,
            success_value=control_node.status.BitAlias.FREE,
            fail_value=control_node.status.BitAlias.ERROR_INPUT,
            mask=control_node.status.BitMask.STATE,
            name=name,
            execution_sleep=execution_sleep,
            min_duration=min_duration,
            max_duration=max_duration,
            max_evaluation_retries=max_evaluation_retries
            )
        self.test_node = test_node

    @command
    async def reset(self) -> shv.SHVType:
        return await self.test_node.reset()
