import typing

import shv

from g3shvnodes.node import SHVNode
from g3shvnodes.pointmachine import (
    SHVPMEControlNode,
    SHVPMMControlNode,
    SHVPMETestNode,
    SHVPMMTestNode
)

from ...exceptions import TestFailFatal
from ...tags import command, after_command
from ..element import ControlNodeStatusValueSingleTest


class _PMPositionTest(
    ControlNodeStatusValueSingleTest[SHVPMEControlNode | SHVPMMControlNode]
):
    def __init__(
        self,
        success_value: int,
        control_node: SHVPMEControlNode | SHVPMMControlNode,
        test_node: SHVPMETestNode | SHVPMMTestNode | None = None,
        pm_type: typing.Literal['pme', 'pmm', 'auto'] = 'auto',
        name: str | None = None,
        execution_sleep: float = 1,
        min_duration: float | None = None,
        max_duration: float | None = None,
        max_evaluation_retries: int | None = None
    ) -> None:
        super().__init__(
            node=control_node,
            success_value=success_value,
            fail_value=control_node.status.BitAlias.ERROR_POSITION,
            mask=control_node.status.BitMask.POSITION,
            name=name,
            execution_sleep=execution_sleep,
            min_duration=min_duration,
            max_duration=max_duration,
            max_evaluation_retries=max_evaluation_retries
            )
        self.test_node = test_node
        if pm_type.lower() == 'auto':
            self.pm_type = self.get_pm_type_from_node_type(control_node)
        else:
            self.pm_type = pm_type.lower()

    @staticmethod
    def get_pm_type_from_node_type(node: SHVNode) -> str:
        if isinstance(node, SHVPMEControlNode):
            return 'pme'
        if isinstance(node, SHVPMMControlNode):
            return 'pmm'
        raise ValueError(f'Unknown node type: "{type(node).__name__}"')

    @after_command
    async def await_motor_not_moving(self) -> bool:
        if self.pm_type == 'pmm':
            return True
        if not hasattr(self.control_node.status.BitAlias, 'MOTOR_MOVING'):
            self._logger.warning(
                '"MOTOR_MOVING" bit was not found in status BitAlias enum. '
                'Skipping check.'
                )
            return True
        await self.control_node.status.status_change_wait(
            any_false=[self.control_node.status.BitAlias.MOTOR_MOVING],
            timeout=self.max_duration,
            get_period=self._exec_sleep
            )
        return True


class PMSetPositionTest(_PMPositionTest):
    def __init__(
        self,
        control_node: SHVPMEControlNode | SHVPMMControlNode,
        test_node: SHVPMETestNode | SHVPMMTestNode | None = None,
        set_to: typing.Literal['left', 'right', 'middle'] = 'left',
        set_from: typing.Literal['test', 'control'] = 'test',
        pm_type: typing.Literal['pme', 'pmm', 'auto'] = 'auto',
        name: str | None = None,
        execution_sleep: float = 1,
        min_duration: float | None = None,
        max_duration: float | None = None,
        max_evaluation_retries: int | None = None
    ) -> None:
        super().__init__(
            success_value=self.pos_to_bit(control_node, set_to),
            control_node=control_node,
            test_node=test_node,
            pm_type=pm_type,
            name=name,
            execution_sleep=execution_sleep,
            min_duration=min_duration,
            max_duration=max_duration,
            max_evaluation_retries=max_evaluation_retries
            )
        self.set_to = set_to.lower()
        self.set_from = set_from.lower()

    @staticmethod
    def pos_to_bit(
        node: SHVPMEControlNode | SHVPMMControlNode, set_to_pos: str
    ) -> int:
        set_to_pos = set_to_pos.lower()
        if set_to_pos == 'left':
            return node.status.BitAlias.LEFT
        if set_to_pos == 'right':
            return node.status.BitAlias.RIGHT
        if set_to_pos == 'middle':
            return node.status.BitAlias.MIDDLE
        raise ValueError(f'Invalid position: "{set_to_pos}"')

    @command
    async def set_position(self) -> shv.SHVType:
        match self.set_from, self.pm_type, self.set_to:
            case 'test', _, 'left':
                assert self.test_node is not None, 'Test node not set'
                return await self.test_node.set_position_left()
            case 'test', _, 'right':
                assert self.test_node is not None, 'Test node not set'
                return await self.test_node.set_position_right()
            case 'test', _, 'middle':
                assert self.test_node is not None, 'Test node not set'
                return await self.test_node.set_position_middle()
            case 'control', 'pme', 'left':
                if not hasattr(self.control_node, 'switch_left'):
                    node_cls_name = type(self.control_node).__name__
                    raise TestFailFatal(
                        f'PME control node "{node_cls_name}" doe not '
                        f'implement "switch_left" method'
                        )
                return await self.control_node.switch_left()
            case 'control', 'pme', 'right':
                if not hasattr(self.control_node, 'switch_right'):
                    node_cls_name = type(self.control_node).__name__
                    raise TestFailFatal(
                        f'PME control node "{node_cls_name}" doe not '
                        f'implement "switch_right" method'
                        )
                return await self.control_node.switch_right()
            case _:
                raise TestFailFatal(
                    f'Invalid combination of test parameters: '
                    f'set_from="{self.set_from}", pm_type="{self.pm_type}", '
                    f'set_to="{self.set_to}"'
                    )


class PMResetTest(_PMPositionTest):
    def __init__(
        self,
        control_node: SHVPMEControlNode | SHVPMMControlNode,
        test_node: SHVPMETestNode | SHVPMMTestNode,
        pm_type: typing.Literal['pme', 'pmm', 'auto'] = 'auto',
        name: str | None = None,
        execution_sleep: float = 1,
        min_duration: float | None = None,
        max_duration: float | None = None,
        max_evaluation_retries: int | None = None
    ) -> None:
        super().__init__(
            success_value=control_node.status.BitAlias.LEFT,
            control_node=control_node,
            test_node=test_node,
            pm_type=pm_type,
            name=name,
            execution_sleep=execution_sleep,
            min_duration=min_duration,
            max_duration=max_duration,
            max_evaluation_retries=max_evaluation_retries
            )

    @command
    async def reset(self) -> shv.SHVType:
        assert self.test_node is not None, 'Test node not set'
        return await self.test_node.reset()
