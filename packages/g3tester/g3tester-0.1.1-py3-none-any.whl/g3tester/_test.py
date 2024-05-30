from __future__ import annotations

import asyncio
import logging

from abc import ABC, abstractmethod
from collections.abc import MutableSequence
from datetime import datetime
from functools import wraps
from inspect import isawaitable
from typing import (
    Any,
    Awaitable,
    Callable,
    Collection,
    Generic,
    Iterable,
    Literal,
    NamedTuple,
    Sequence,
    TypeGuard,
    TypeVar,
    overload
)

from . import exceptions
from .enums import TestStatus, TestType
from .tags._tags import ObjectTagCollector, TagType, on_status_change
from ._memory import TestMemory


logger = logging.getLogger('g3tester')
"""The logger object for the `g3tester` module."""


###############################################################################
# TEST ABC
###############################################################################


class RoutineExecInfo(NamedTuple):
    """A named tuple to store information about a tagged routine execution."""
    name: str
    """The name of the routine method."""
    retval: Any | None
    """The return value of the routine method."""
    is_executed: bool
    """A flag indicating if the routine method was executed."""


TNumber = TypeVar('TNumber', int, float)


class TestABC(ABC):
    """
    An abstract base class for the test objects. The class provides the basic
    functionality for the test objects, such as the test status management,
    tagged routine execution, common test attributes, etc.
    """
    def __init__(
        self,
        name: str | None = None,
        type_: TestType = TestType.OTHER,
        min_duration: float | None = None,
        max_duration: float | None = None
    ) -> None:
        """Initialize the test object.

        Args:
            name (str | None, optional): The name of the test. If None, the\
                name is set to the class name with the object ID. Defaults to\
                None.
            type_ (TestType, optional): The type of the test. Defaults to\
                TestType.OTHER.
            min_duration (float | None, optional): The minimum duration of the\
                test in seconds. The test will not finish before this time has\
                passed. Defaults to None.
            max_duration (float | None, optional): The maximum duration of the\
                test in seconds. The test will be stopped if it runs longer\
                than this time. Defaults to None.
        """
        self._name: str = self._validate_name(name)
        self._type: TestType = type_
        min_dur, max_dur = self._validate_duration(min_duration, max_duration)
        self._min_duration: float = min_dur
        self._max_duration: float = max_dur
        self._raise_exc_on_fail: bool = False
        self._memory: TestMemory = TestMemory()
        self._status: TestStatus = TestStatus.PENDING
        self._failed: bool = False
        self.status_reason: str | None = None
        self.warnings: list[str] = []
        self._timestamp_start: float | None = None
        self._timestamp_finish: float | None = None
        self._parent: TestABC | None = None
        self._tag_collector = ObjectTagCollector(self)
        self._tagged_passed: dict[TagType, list[str]] = {}
        self._logger = logging.getLogger(self._name)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        def init_decorator(previous_init):
            """
            A decorator to add a side effect of triggering the `__post_init__`
            method to the base class after the class instantiation.
            """
            @wraps(previous_init)
            def new_init(self, *args, **kwargs):
                previous_init(self, *args, **kwargs)
                if type(self) is cls:     # ensure __post_init__
                    self.__post_init__()  # is only called for the base class

            return new_init  # return the new __init__ method

        cls.__init__ = init_decorator(cls.__init__)

    def __post_init__(self):
        """Execute the post-initialization logic."""
        self._post_init()

    def __str__(self) -> str:
        return self._name

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(name={self._name})'

    def _post_init(self) -> None:
        """
        Owerwrite this method in the subclass to add custom post-initialization
        logic. This method is called after the class instantiation.
        """
        pass

    def _validate_name(self, name: str | None) -> str:
        """Validate the test name. If the name is None, it is set to the class
        name with the object ID. If the name is a string, an object ID
        is appended to it.

        Args:
            name (str | None): The test name. If None, defaults to the class\
                name with the object ID.

        Raises:
            exceptions.TestFailFatal: If the name is not a string.

        Returns:
            str: The formatted test name.
        """
        if name is None:
            name = self.__class__.__name__
        elif not isinstance(name, str):
            raise exceptions.TestFailFatal(
                f'Invalid test name type "{type(name).__name__}", '
                f'expected type "str".'
                )
        return f'{name} (ID {id(self)})'

    def _validate_positive_number(self, value: TNumber) -> TNumber:
        """Validate if the value is a positive number.

        Args:
            value (TNumber): The value to validate.

        Raises:
            TypeError: If the value is not an integer or a float.
            ValueError: If the value is not a positive number.

        Returns:
            TNumber: The validated positive number.
        """
        if not isinstance(value, (int, float)):
            raise TypeError(
                f'Invalid value type "{type(value).__name__}", '
                f'expected type "int" or "float".'
                )
        if value <= 0:
            raise ValueError(
                f'Invalid value "{value}", expected a positive number.'
                )
        return value

    def _validate_duration(
        self, min_duration: float | None, max_duration: float | None
    ) -> tuple[float, float]:
        """Validate the minimum and maximum duration values. If the minimum
        duration is None, it is set to 0. If the maximum duration is None,
        it is set to infinity. The minimum duration must be less than the
        maximum duration.

        Args:
            min_duration (float | None): The minimum duration value.
            max_duration (float | None): The maximum duration value.

        Raises:
            ValueError: If the minimum duration is greater than or equal to\
                the maximum duration.

        Returns:
            tuple[float, float]: The validated minimum and maximum duration\
                values.
        """
        if min_duration is None:
            min_duration = 0
        else:
            min_duration = self._validate_positive_number(min_duration)
        if max_duration is None:
            max_duration = float('inf')
        else:
            max_duration = self._validate_positive_number(max_duration)
        if min_duration >= max_duration:
            raise ValueError(
                f'Invalid minimum duration "{min_duration}", expected a value '
                f'less than the maximum duration "{max_duration}".'
                )
        return min_duration, max_duration

    def _validate_retval(self, retval: Any, tag: TagType) -> Any:
        """Validate the return value of a tagged routine. The return value must
        be a boolean or `None` if the tag is "fail", "warning", or "success".

        Args:
            retval (Any): The return value of the tagged routine.
            tag (TagType): The tag type of the routine.

        Raises:
            exceptions.TestFailFatal: If the return value is not a boolean or\
                `None` when the tag is "fail", "warning", or "success".

        Returns:
            Any: The validated return value.
        """
        if tag in [TagType.FAIL, TagType.WARNING, TagType.SUCCESS]:
            if retval is not None and not isinstance(retval, bool):
                raise exceptions.TestFailFatal(
                    f'A "{tag}" routine returned type '
                    f'"{type(retval).__name__}",  expected type "bool".'
                    )
        return retval

    async def _exec_tagged_routine(
        self,
        name: str,
        tag: TagType,
        target: Any | None = "N/A",
    ) -> RoutineExecInfo:
        """Execute a tagged routine and handle the exceptions that may occur
        during the execution.

        Args:
            name (str): The name of the routine method to execute.
            tag (TagType): The tag type of the routine.
            target (Any | None, optional): The target of the routine.\
                For example, for @before_command and @after_command routines,\
                the target is the command name. Defaults to "N/A".

        Raises:
            asyncio.TimeoutError: If the routine execution times out.
            exceptions.TestFail: If the routine execution fails on\
                an expected condition.
            exceptions.TestFailFatal: If the routine execution fails\
                unexpectedly.
            Exception: If an unexpected error occurs during the routine\
                execution.

        Returns:
            RoutineExecInfo: The information about the routine execution.
        """
        tag_target = f'{tag}:{target}' if target is not None else tag
        self._logger.debug(
            'Executing a "%s" routine "%s"', tag_target, name
            )
        try:
            # get the routine method by its name and execute it
            routine = getattr(self, name)
            result = routine()
            if isawaitable(result):
                result = await result
            # validate the return value
            result = self._validate_retval(result, tag)
            self._logger.debug(
                'Executed the "%s" routine "%s". Return value: %s',
                tag_target, name, result
                )
            return RoutineExecInfo(name=name, retval=result, is_executed=True)
        except asyncio.TimeoutError as exc:
            note = (
                f'Timeout occured while executing the "{tag}:{target}" '
                f'routine "{name}"'
                )
            self._logger.debug(note)
            exc.add_note(note)
            raise exc
        except exceptions.TestFail as exc:
            note = (
                f'Test failed while executing the "{tag_target}" routine '
                f'"{name}" (reason: "{exc}")'
                )
            self._logger.debug(note)
            exc.add_note(note)
            raise exc
        except exceptions.TestFailFatal as exc:
            note = (
                f'Fatal test failure occured while executing '
                f'the "{tag_target}" routine "{name}" (reason: "{exc}")'
                )
            self._logger.error(note)
            raise exc
        except Exception as exc:
            note = (
                f'Unexpected error occured while executing '
                f'the "{tag_target}" routine "{name}" (reason: "{exc}")'
                )
            self._logger.error(note)
            raise exceptions.TestFailFatal(note) from exc

    def _evaluate_terminate_exec_early(self, tag: TagType, retval) -> bool:
        """Evaluate if the execution of the tagged routines should be
        terminated early based on the return value of the last executed
        routine. Continuing the evaluation in such cases would be redundant.

        Args:
            tag (TagType): The tag type of the routine.
            retval (Any): The return value of the last executed routine.

        Returns:
            bool: True if the execution should be terminated early, False\
                otherwise.
        """
        if retval is False and tag in [
            TagType.BEFORE_COMMAND, TagType.AFTER_COMMAND, TagType.SUCCESS
        ]:
            return True
        if retval is True and tag == TagType.FAIL:
            return True
        return False

    async def _exec_tagged_routines(
        self,
        names: Sequence[str],
        tag: TagType,
        target: Any | None = "N/A",
        skip_names: Collection[str] | None = None
    ) -> dict[str, RoutineExecInfo]:
        """Execute a sequence of tagged routines of a specific type.

        Args:
            names (Sequence[str]): The names of the routine methods to execute.
            tag (TagType): The tag type of the routines.
            target (Any | None, optional): The target of the routines.\
                For example, for @before_command and @after_command routines,\
                the target is the command name. Defaults to "N/A".
            skip_names (Collection[str] | None, optional): The names of the\
                routines to skip. Defaults to None.

        Returns:
            dict[str, RoutineExecInfo]: A dictionary with the information\
                about the routine executions.
        """
        tag_target = f'{tag}:{target}' if target is not None else tag
        if names:
            self._logger.debug(
                'Executing %d "%s" routine(s)', len(names), tag_target
                )
        else:
            self._logger.debug(
                'No "%s" routines to execute', tag_target
                )
        # create a dict to store the evaluation results for each routine
        results: dict[str, RoutineExecInfo] = {
            name: RoutineExecInfo(name=name, retval=None, is_executed=False)
            for name in names
            }
        # execute the routines one by one
        terminate_after_priority: int | None = None
        for name in names:
            # skip the routine if it is in the skip list
            # (may be valid for routines that have already been executed
            # and returned a "positive" result or None)
            if skip_names and name in skip_names:
                self._logger.debug(
                    'Skipping the "%s" routine "%s"', tag_target, name
                    )
                continue
            # check if the execution should be terminated early
            # (may be triggered if a returned value of a previous routine
            # was evaluated as a "negative" result)
            if terminate_after_priority is not None:
                # if the execution is to be terminated early, and the current
                # routine has a higher priority than the one that triggered
                # the termination, terminate the execution
                priority = self._tag_collector.get_method_priority(name, tag)
                if terminate_after_priority < priority:
                    self._logger.debug(
                        'The "%s" routine(s) execution terminated early',
                        tag_target
                        )
                    break
            # execute the routine and store the result
            result = await self._exec_tagged_routine(name, tag, target)
            results[name] = result
            # check if the execution should be terminated early based on the
            # return value of the last executed routine
            if terminate_after_priority is None and name != names[-1]:
                if self._evaluate_terminate_exec_early(tag, result.retval):
                    # if the routine returned a value that leads to
                    # the early termination of the execution, store
                    # the priority of this routine. The execution will
                    # be terminated after the routines with the same
                    # priority are executed
                    pr = self._tag_collector.get_method_priority(name, tag)
                    terminate_after_priority = pr
                    self._logger.debug(
                        'The "%s" routine(s) execution will be terminated '
                        'early due to the return value of the routine "%s". '
                        'Executing the rest of the routines with priority %d',
                        tag_target, name, terminate_after_priority
                        )
        return results

    @property
    def name(self) -> str:
        """The name of the test."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Set the name of the test."""
        self._name = self._validate_name(value)

    @property
    def type(self) -> TestType:
        """The type of the test."""
        return self._type

    @property
    def min_duration(self) -> float:
        """
        The minimum duration of the test in seconds.
        The test will not finish before this time has passed.
        """
        return self._min_duration

    @property
    def max_duration(self) -> float:
        """
        The maximum duration of the test in seconds.
        The test will be stopped if it runs longer than this time.
        """
        return self._max_duration

    def set_duration(
        self,
        min_duration: float | Literal[-1] | None = None,
        max_duration: float | Literal[-1] | None = None
    ) -> None:
        """Set the minimum and maximum duration of the test.

        Args:
            min_duration (float | Literal[-1, optional): minimum duration of\
                the test in seconds. If set to -1, the current value is kept.\
                If set to None, the duration is set to 0. Defaults to None.
            max_duration (float | Literal[-1, optional): maximum duration of\
                the test in seconds. If set to -1, the current value is kept.\
                If set to None, the duration is indefinite. Defaults to None.
        """
        if min_duration == -1:
            min_duration = self._min_duration
        if max_duration == -1:
            max_duration = self._max_duration
        min_dur, max_dur = self._validate_duration(min_duration, max_duration)
        self._min_duration, self._max_duration = min_dur, max_dur

    @property
    def logger(self) -> logging.Logger:
        """The logger object for the test."""
        return self._logger

    @property
    def memory(self) -> TestMemory:
        """The memory object of the test."""
        return self._memory

    @property
    def started_at(self) -> datetime | None:
        """
        The time when the test was started. If the test has not been
        started yet, the value is None.
        """
        if self._timestamp_start is None:
            return None
        return datetime.fromtimestamp(round(self._timestamp_start, 3))

    @property
    def finished_at(self) -> datetime | None:
        """
        The time when the test was finished. If the test has not been
        finished yet, the value is None.
        """
        if self._timestamp_finish is None:
            return None
        return datetime.fromtimestamp(round(self._timestamp_finish, 3))

    @property
    def duration_sec(self) -> float:
        """
        The duration of the test in seconds. If the test has not been
        started yet, the value is 0. If the test has not been finished
        yet, the value is the time passed since the test was started.
        """
        if self._timestamp_start is None:
            return 0
        if self._timestamp_finish is None:
            timestamp_now = datetime.now().timestamp()
            return round(timestamp_now - self._timestamp_start, 3)
        return round(self._timestamp_finish - self._timestamp_start, 3)

    @property
    def parent(self) -> TestABC | None:
        """
        The parent test of the test. May be None if the test has no parent.
        """
        return self._parent

    @property
    def parents(self) -> list[TestABC]:
        """
        The list of parent tests of the test. The list is ordered from the
        direct parent to the root parent.
        """
        parents: list[TestABC] = []
        parent = self.parent
        while parent:
            parents.append(parent)
            parent = parent.parent
        return parents

    @property
    def depth(self) -> int:
        """
        The depth of the test in the test tree. The depth is 0 for the root
        test, 1 for the direct child of the root test, and so on.
        """
        return len(self.parents)

    @property
    def status(self) -> TestStatus:
        """The status of the test."""
        return self._status

    @property
    def passed(self) -> bool | None:
        """
        `True` if the test has finished with the status "PASSED" or
        "PASSED_WITH_WARNING", `False` if the test has finished with the
        status "FAILED" or "TIMEOUT", `None` otherwise.
        """
        if self.is_status(TestStatus.PASSED, TestStatus.PASSED_WITH_WARNING):
            return True
        if self.is_status(TestStatus.FAILED, TestStatus.TIMEOUT):
            return False
        return None

    def is_status(self, *statuses: TestStatus) -> bool:
        """Check if the test has one of the specified statuses.

        Returns:
            bool: True if the test has one of the specified statuses,\
                False otherwise.
        """
        return self._status in statuses

    async def set_status(
        self,
        status: TestStatus,
        reason: str | None = None,
        execute_routines: bool = True
    ) -> None:
        """Set the status of the test and execute the tagged routines that
        are triggered by the status change.

        Args:
            status (TestStatus): The new status of the test.
            reason (str | None, optional): The reason for the status change.\
                Defaults to None.
            execute_routines (bool, optional): If True, the tagged routines\
                that are triggered by the status change are executed.\
                Defaults to True.
        """
        # if the status is already set, skip the status change
        if self._status == status:
            self._logger.debug(
                'Status is already "%s", skipping the status change', status
                )
            return
        # check for side effects of the status change
        if status == TestStatus.RUNNING:
            self._start_time = datetime.now().timestamp()
        elif status == TestStatus.PASSED and (self._failed or self.warnings):
            status = TestStatus.PASSED_WITH_WARNING
        elif status in (
            TestStatus.ABORTED, TestStatus.FAILED, TestStatus.TIMEOUT
        ):
            self._failed = True
        # set the new status
        self._logger.info('Status change to %s', status.name)
        if reason:
            self._logger.debug('Status change reason: %s', reason)
        self._status = status
        # execute the tagged routines that are triggered by the status change
        if execute_routines:
            actions = self._tag_collector.status_change_actions
            await self._exec_tagged_routines(
                names=actions.get(status, []),
                tag=TagType.ON_STATUS_CHANGE,
                target=self._status.name,
                )

    @abstractmethod
    async def _run(self):
        """Overwrite this method in the subclass to implement the test logic.
        This method is called during the test execution. Do not catch any
        errors explicitly in your implementation. The error catching
        algorithm is implemented within the test run loop.
        """
        ...

    @abstractmethod
    def _set_memory(self, memory: TestMemory) -> None:
        """Implement this method in the subclass to set the test memory.

        Args:
            memory (TestMemory): The memory object of the test.
        """
        ...

    async def _background_wait(self):
        """Wait in the background for the minimum duration of the test."""
        await asyncio.sleep(self._min_duration)

    async def _handle_exc_timeout(self, exc: ExceptionGroup):
        """
        Handle the timeout exception that occurs during the test execution.
        """
        await self.set_status(TestStatus.TIMEOUT)
        if self._raise_exc_on_fail:
            raise exc

    async def _handle_exc_testfail(self, exc: ExceptionGroup):
        """
        Handle the test fail exception that occurs during the test execution.
        """
        err = '; '.join((f'"{e}"' for e in exc.exceptions))
        await self.set_status(TestStatus.FAILED, reason=err)
        if self._raise_exc_on_fail:
            raise exc

    async def _handle_exc_unexpected(self, exc: ExceptionGroup):
        """
        Handle the unexpected exception that occurs during the test execution.
        """
        err = '; '.join((f'"{e}"' for e in exc.exceptions))
        await self.set_status(TestStatus.FAILED, reason=err)
        if self._raise_exc_on_fail:
            raise exc

    async def _safe_handle_exc(
        self, handler: Callable[..., Awaitable[None]], *args
    ) -> None:
        """
        Safely handle an exception that occurs during the test execution by
        calling the specified handler method with the provided arguments and
        catching any exceptions that may occur during the handler execution if
        the `_raise_exc_on_fail` attribute is set to `False`.

        Args:
            handler (Callable[..., Awaitable[None]]): The handler method to\
                call.

        Raises:
            Exception: If the `_raise_exc_on_fail` attribute is set to `True`\
                and an exception occurs during the handler execution, this
                exception is re-raised.
        """
        try:
            await handler(*args)
        except Exception as exc:
            if self._raise_exc_on_fail:
                raise exc

    async def run(self):
        """
        Run the test.

        Raises:
            exceptions.TestFailFatal: If the test cannot be started due to\
                its current status.
        """
        if not self.is_status(TestStatus.PENDING, TestStatus.QUEUED):
            raise exceptions.TestFailFatal(
                f'Cannot start the test "{self._name}" with the status '
                f'"{self._status.name}". Only tests with the status '
                f'"PENDING" or "QUEUED" can be started.'
                )
        try:
            self._timestamp_start = datetime.now().timestamp()
            self._logger.debug('Test started')
            await self.set_status(TestStatus.RUNNING)
            async with asyncio.TaskGroup() as tg:
                timeout = self._max_duration + 0.5
                tg.create_task(asyncio.wait_for(self._run(), timeout))
                tg.create_task(self._background_wait())
            await self.set_status(TestStatus.PASSED)
        except* exceptions.TestFail as exc:
            await self._safe_handle_exc(self._handle_exc_testfail, exc)
        except* asyncio.TimeoutError as exc:
            await self._safe_handle_exc(self._handle_exc_timeout, exc)
        except* Exception as exc:
            await self._safe_handle_exc(self._handle_exc_unexpected, exc)
        finally:
            self._timestamp_finish = datetime.now().timestamp()
            self._logger.debug('Test finished')


###############################################################################
# SINGLETEST
###############################################################################

TTestValue = TypeVar('TTestValue')


class SingleTest(TestABC, Generic[TTestValue]):
    """
    A generic single test. Implement a simple loop of executing the tagged
    routines (applying the commands and corresponding command conditions,
    fetching the value, evaluating the results, etc). This class is thus
    a generic test runner that can be subclassed to implement specific testing
    scenarios.
    """
    def __init__(
        self,
        name: str | None = None,
        execution_sleep: float = 1,
        min_duration: float | None = None,
        max_duration: float | None = None,
        max_evaluation_retries: int | None = None,
    ) -> None:
        """Initialize the single test object.

        Args:
            name (str | None, optional): The name of the test. If None, the\
                name is set to the class name with the object ID. Defaults to\
                None.
            execution_sleep (float, optional): The sleep time in seconds\
                between the test loop iterations. Defaults to 1 second.
            min_duration (float | None, optional): The minimum duration of the\
                test in seconds. The test will not finish before this time has\
                passed. Defaults to None.
            max_duration (float | None, optional): The maximum duration of the\
                test in seconds. The test will be stopped if it runs longer\
                than this time. Defaults to None.
            max_evaluation_retries (int | None, optional): Maximum number of\
                value asquisition and evaluation retries within the test loop.\
                If set to `None`, the test will fetch and evaluate the value\
                until the test finishes or a timeout occurs. Defaults to None.
        """
        # init the parent class first!
        super().__init__(name, TestType.SINGLETEST, min_duration, max_duration)
        exec_sleep = self._validate_positive_number(execution_sleep)
        self._exec_sleep: float = exec_sleep
        if max_evaluation_retries is None:
            retries = None
        else:
            retries = self._validate_positive_number(max_evaluation_retries)
        self._max_evaluation_retries: int | None = retries
        """
        Maximum number of value asquisition and evaluation retries. within
        the test loop. If set to `None`, the test will fetch and evaluate
        the value until the test succeeds or a timeout occurs.
        """
        self._value: TTestValue | None = None
        """
        The actual value that is acquired by the value getter method.
        """

    @property
    def value(self) -> TTestValue | None:
        """
        The value returned by the @value_getter method. If such a method is not
        defined or the value is not yet acquired, the value is `None`.
        """
        return self._value

    def _set_memory(self, memory: TestMemory) -> None:
        """Set the test memory object. Implementation of the abstract method
        of the base parent class for a single test.

        Args:
            memory (TestMemory): memory object to set.
        """
        self._memory = memory

    # COMMAND EXECUTION #

    def _is_routine_passed(
        self, exec_info: RoutineExecInfo, retval_passed: Any | None = None
    ) -> bool:
        """Check if the routine is passed, i.e., if it has been executed and
        has returned either a `None` value or the specified value.

        Args:
            exec_info (RoutineExecInfo): The information about the routine\
                execution.
            retval_passed (Any | None, optional): The expected return value\
                of the routine to be considered as passed. Note that if the\
                return value of the routine is `None`, the routine is always\
                considered as passed. Defaults to None.

        Returns:
            bool: True if the routine is passed, False otherwise.
        """
        if exec_info.is_executed is False:
            return False
        if retval_passed is None:
            return True
        return exec_info.retval is None or exec_info.retval == retval_passed

    async def _exec_tagged_routines_until_all_passed(
        self,
        names: Sequence[str],
        tag: TagType,
        target: Any | None = "N/A",
        skip_passed: bool = False,
        passed_if_all_return: Any | None = None,
        timer: float = float('inf'),
    ) -> None:
        """Execute a sequence of tagged routines until all of them pass, i.e.,
        until all of them return either a `None` value or the specified value.

        This method wraps the `_exec_tagged_routines` method and executes the
        routines in a loop until all of them pass. The method
        `_is_routine_passed` is used to determine if the routine is passed.

        Args:
            names (Sequence[str]): The names of the routine methods to execute.
            tag (TagType): The tag type of the routines.
            target (Any | None, optional): The target of the routines.\
                For example, for @before_command and @after_command routines,\
                the target is the command name. Defaults to "N/A".
            skip_names (Collection[str] | None, optional): The names of the\
                routines to skip. Defaults to None.
            passed_if_all_return (Any | None, optional): The expected return\
                value of the routine to be considered as passed. Note that if\
                the return value of the routine is `None`, the routine is\
                always considered as passed. Defaults to None.
            timer (float, optional): Global timer for the execution of the\
                test. Defaults to float('inf').

        Raises:
            asyncio.TimeoutError: If the execution of the routines times out.
        """
        tag_target = f'{tag}:{target}' if target is not None else tag
        if not names:            # check before starting the loop to prevent
            self._logger.debug(  # unnecessary logging messages
                'No "%s" routines to execute', tag_target
                )
            return
        counter = 1
        skip_names: set[str] = set()
        while True:
            self._logger.debug(
                'Awaiting until "%s" routine(s) pass (attempt: %d)',
                tag_target, counter
                )
            if timer - datetime.now().timestamp() <= 0:
                raise asyncio.TimeoutError
            all_passed = True
            result = await self._exec_tagged_routines(
                names, tag, target, skip_names
                )
            for routine, exec_info in result.items():
                if self._is_routine_passed(exec_info, passed_if_all_return):
                    if skip_passed:
                        skip_names.add(routine)
                elif all_passed is True:
                    all_passed = False
            if all_passed:
                self._logger.debug(
                    'Awaited the "%s" routine(s) to pass', tag_target
                    )
                break
            self._logger.debug(
                '"%s" routine(s) did not pass. Retrying in %s second(s)',
                tag_target, self._exec_sleep
                )
            counter += 1
            await asyncio.sleep(self._exec_sleep)

    async def _exec_commands(self, timer: float = float('inf')) -> None:
        """Execute the `@command` routines and corresponding
        `@before_command` and `@after_command` routines.

        Args:
            timer (float, optional): Global timer for the execution of the\
                test. Defaults to float('inf').
        """
        commands_with_conditions = self._tag_collector.commands_with_conditions
        # execute precondition routines that are not bound to any command
        await self._exec_tagged_routines_until_all_passed(
            names=commands_with_conditions[None][TagType.BEFORE_COMMAND],
            tag=TagType.BEFORE_COMMAND,
            target='all',
            passed_if_all_return=True,
            skip_passed=True,
            timer=timer,
            )
        for command, conditions in commands_with_conditions.items():
            if command is None:
                continue
            # execute precondition routines
            await self._exec_tagged_routines_until_all_passed(
                names=conditions[TagType.BEFORE_COMMAND],
                tag=TagType.BEFORE_COMMAND,
                target=command,
                passed_if_all_return=True,
                skip_passed=True,
                timer=timer,
                )
            # execute the command
            await self._exec_tagged_routine(command, TagType.COMMAND, None)
            # execute postcondition routines
            await self._exec_tagged_routines_until_all_passed(
                names=conditions[TagType.AFTER_COMMAND],
                tag=TagType.AFTER_COMMAND,
                target=command,
                passed_if_all_return=True,
                skip_passed=True,
                timer=timer,
                )
        # execute postcondition routines that are not bound to any command
        await self._exec_tagged_routines_until_all_passed(
            names=commands_with_conditions[None][TagType.AFTER_COMMAND],
            tag=TagType.AFTER_COMMAND,
            target='all',
            passed_if_all_return=True,
            skip_passed=True,
            timer=timer,
            )

    # COMMAND EXECUTION END #

    # VALUE ACQUSITION AND EVALUATION #

    async def _get_value(self) -> TTestValue | None:
        """Fetch the current value required for the evaluation using the
        `@value_getter` method. If the method is not defined, the value is
        set to `None`.

        Returns:
            TTestValue | None: The actual value fetched by the value getter.
        """
        getter = self._tag_collector.value_getter
        if getter is not None:
            tag = TagType.VALUE_GETTER
            exec_info = await self._exec_tagged_routine(getter, tag, None)
            self._value = exec_info.retval
        return self._value

    async def _exec_fail_routines(self) -> None:
        """Execute the routines tagged with the `@fail` tag and check if
        any of the fail conditions are met.

        Raises:
            exceptions.TestFail: If any of the fail conditions are met.
        """
        result = await self._exec_tagged_routines(
            names=self._tag_collector.get_tagged_methods(TagType.FAIL),
            tag=TagType.FAIL,
            target=None,
            )
        for routine, exec_info in result.items():
            if exec_info.retval is True:
                self._logger.debug(
                    'Awaited the test evaluation to complete. Test failed'
                    )
                raise exceptions.TestFail(
                    f'A fail condition "{routine}" was met'
                    )

    async def _exec_warning_routines(self) -> None:
        """Execute the routines tagged with the `@warning` tag and check if
        any of the warning conditions are met.
        """
        result = await self._exec_tagged_routines(
            names=self._tag_collector.get_tagged_methods(TagType.WARNING),
            tag=TagType.WARNING,
            target=None,
            )
        for routine, exec_info in result.items():
            if exec_info.retval is True:
                self.warnings.append(routine)

    async def _exec_success_routines(self) -> bool:
        """Execute the routines tagged with the `@success` tag and check if
        all of the success conditions are met.

        Returns:
            bool: True if all of the success conditions are met, False\
                otherwise.
        """
        result = await self._exec_tagged_routines(
            names=self._tag_collector.get_tagged_methods(TagType.SUCCESS),
            tag=TagType.SUCCESS,
            target=None,
            )
        return all(
            exec_info.retval is None or exec_info.retval is True
            for exec_info in result.values()
            )

    async def _wait_for_test_eval(self, timer: float = float('inf')) -> None:
        """Evaluate the test until it succeeds or fails or a timeout occurs.

        This method performs the following in a loop:
        1. Fetches the current value required for the evaluation.
        2. Evaluates if the failure conditions are met. If any of the\
            conditions are met, the test fails immediately.
        3. Evaluates if the warning conditions are met.
        4. Evaluates if the success conditions are met. If all of the\
            conditions are met, the test passes.
        5. If none of the conditions are met, the loop continues until\
            the test succeeds or fails or a timeout occurs.

        Args:
            timer (Optional[float], optional): Global timer for the execution\
                of the test. Defaults to float('inf').

        Raises:
            asyncio.TimeoutError: If the timer expires before
            the test evaluation completes.
            exceptions.TestFail: If any of the `@fail` conditions are met or
            not all of the `@success` conditions are met within the maximum
            number of retries.
        """
        # start the evaluation (run in loop until complete or timeout)
        retries_counter = 1
        while True:
            if timer - datetime.now().timestamp() <= 0:
                raise asyncio.TimeoutError
            if self._max_evaluation_retries is None:
                self._logger.debug(
                    'Awaiting the test evaluation to complete (attempt: '
                    '%d)', retries_counter
                    )
            elif retries_counter <= self._max_evaluation_retries:
                self._logger.debug(
                    'Awaiting the test evaluation to complete (attempt: '
                    '%d/%d)', retries_counter, self._max_evaluation_retries
                    )
            else:
                self._logger.debug(
                    'Awaited the test evaluation to complete. Test failed'
                    )
                raise exceptions.TestFail(
                    'A success condition was not met within '
                    'the maximum number of retries'
                    )
            # fetch the currect actual value
            await self._get_value()
            # evaluate if the @error conditions are met
            await self._exec_fail_routines()
            # evaluate if the @warning conditions are met
            await self._exec_warning_routines()
            # evaluate if the @success conditions are met
            passed = await self._exec_success_routines()
            if passed:
                self._logger.debug(
                    'Awaited the test evaluation to complete. Test passed'
                    )
                break
            self._logger.debug(
                'Test evaluation did not complete, neither passing nor '
                'failing. Retrying in %s seconds', self._exec_sleep
                )
            retries_counter += 1
            await asyncio.sleep(self._exec_sleep)

    async def _run(self):
        """Test run logic implementation of a single test."""
        timer = self._start_time + self._max_duration + 0.5
        await self._exec_commands(timer)
        await self._wait_for_test_eval(timer)

    # VALUE ACQUSITION AND EVALUATION END #

    @on_status_change(change_to=TestStatus.TIMEOUT, priority=0)
    async def log_value_on_timeout(self):
        """Log the value after a timeout occurs."""
        if self._tag_collector.value_getter is None:
            return
        self._logger.debug('Fetching the value after a timeout')
        try:
            self._logger.debug(
                'Value after the timeout: %s', await self._get_value()
                )
        except Exception as exc:
            self._logger.debug(
                'Failed to fetch the value after the timeout (reason: "%s")',
                exc
                )


###############################################################################
# MULTITESTS
###############################################################################

TTestType = TypeVar('TTestType', bound=TestABC)


class MultiTestABC(TestABC, MutableSequence[TTestType]):
    """
    A generic multi-test class that can be used to group multiple tests
    together. The class is a subclass of the `TestABC` class and implements
    the `MutableSequence` abstract base class to store the child tests in a
    list-like manner. It should be further subclassed to implement specific
    run logic.
    """
    def __init__(
        self,
        *tests: TTestType,
        type_: TestType = TestType.MULTITEST,
        allow_fail: bool = False,
        name: str | None = None,
        min_duration: float | None = None,
        max_duration: float | None = None
    ) -> None:
        """Initialize the multi-test object.

        Args:
            type_ (TestType, optional): The type of the test. Defaults to\
                TestType.MULTITEST.
            allow_fail (bool, optional): If `True`, the multi-test will\
                continue execution if one of the child tests fails.\
                If `False`, it will terminate the execution and abort\
                the remaining tests. Defaults to False.
            name (str | None, optional): The name of the test. If None, the\
                name is set to the class name with the object ID. Defaults to\
                None.
            min_duration (float | None, optional): The minimum duration of the\
                test in seconds. The test will not finish before this time has\
                passed. Defaults to None.
            max_duration (float | None, optional): The maximum duration of the\
                test in seconds. The test will be stopped if it runs longer\
                than this time. Defaults to None.
        """
        super().__init__(name, type_, min_duration, max_duration)
        self._allow_fail = allow_fail  # must be above of the test appending!
        self._tests: list[TTestType] = []
        for test in tests:
            self.append(test)

    @overload
    def __getitem__(self, index: int) -> TTestType: ...

    @overload
    def __getitem__(self, index: slice) -> list[TTestType]: ...

    def __getitem__(self, index: int | slice) -> TTestType | list[TTestType]:
        return self._tests[index]

    def __setitem__(self, index: int | slice, test) -> None:
        self._assert_is_pending(self)
        if not isinstance(test, Iterable) or isinstance(test, str):
            test = [test]
        for t in test:
            if self._assert_is_test(t):
                self._assert_is_pending(t)
                self._bind_test(t)
        self._tests[index] = test

    def __delitem__(self, index: int | slice) -> None:
        self._assert_is_pending(self)
        test = self._tests[index]
        if not isinstance(test, list):
            test = [test]
        for t in test:
            self._assert_is_pending(t)
            self._unbind_test(t)
        del self._tests[index]

    def __len__(self) -> int:
        return len(self._tests)

    def insert(self, index: int, test: TTestType) -> None:
        self._assert_is_pending(self)
        self._assert_is_test(test)
        self._assert_is_pending(test)
        self._bind_test(test)
        self._tests.insert(index, test)

    @staticmethod
    def _assert_is_test(test: Any) -> TypeGuard[TTestType]:
        """Assure that the given object is a subclass of the `TestABC` class.
        This method is implemented as a type guard.

        Args:
            test (Any): The object to check.

        Raises:
            TypeError: If the object is not a subclass of the `TestABC` class.

        Returns:
            TypeGuard[TTestType]: Always True if the object is a subclass of\
                the `TestABC` class.
        """
        if not isinstance(test, TestABC):
            raise TypeError(
                f'Invalid test "{test}" of type "{type(test)}" '
                f'(expected a subclass of "TestABC").'
                )
        return True

    @staticmethod
    def _assert_is_pending(test: TestABC) -> bool:
        """Assure that the given test is in the "PENDING" status.

        Args:
            test (TestABC): The test to check.

        Raises:
            exceptions.TestFailFatal: If the test is not in the "PENDING"\
                status.

        Returns:
            bool: Always True if the test is in the "PENDING" status.
        """
        if not test.is_status(TestStatus.PENDING):
            raise exceptions.TestFailFatal(
                f'Invalid test "{test}" with the status "{test.status.name}".'
                f'Only tests with the status "PENDING" can be modified.'
                )
        return True

    def _set_memory(self, memory: TestMemory) -> None:
        """Set the test memory object. Implementation of the abstract method
        of the base parent class for a multi-test.

        Args:
            memory (TestMemory): memory object to set.
        """
        self._memory = memory
        for test in self._tests:
            test._set_memory(memory)

    def _bind_test(self, test: TTestType) -> None:
        """Bind the given test to the multi-test. The test is set as a child
        of the multi-test and the memory object is set to the memory of the
        multi-test.

        Args:
            test (TTestType): The test to bind.
        """
        test._parent = self
        test._raise_exc_on_fail = not self.allow_fail
        test._set_memory(memory=self._memory)

    def _unbind_test(self, test: TTestType) -> None:
        """Unbind the given test from the multi-test. The test is removed as a
        child of the multi-test and the memory object is set to the default
        empty memory object.

        Args:
            test (TTestType): The test to unbind.
        """
        test._parent = None
        test._raise_exc_on_fail = True
        test._set_memory(memory=TestMemory())

    @property
    def allow_fail(self) -> bool:
        """
        If `True`, the multi-test will not raise an exception if one of the
        child tests fails. Instead, the test will continue to run the remaining
        tests. If `False`, the multi-test will raise an exception if one of the
        child tests fails and stop the execution of the remaining tests.
        """
        return self._allow_fail

    @allow_fail.setter
    def allow_fail(self, value: bool) -> None:
        """Set the `allow_fail` attribute of the multi-test."""
        if not isinstance(value, bool):
            raise TypeError(
                f'Invalid value type "{type(value).__name__}", '
                f'expected type "bool".'
                )
        self._allow_fail = value
        for test in self._tests:
            test._raise_exc_on_fail = not value

    def get_loggers(
        self, max_depth: int | None = None
    ) -> list[logging.Logger]:
        """Collect the loggers of the multi-test and its child tests.
        The loggers are collected recursively up to the specified depth.

        Args:
            max_depth (int | None, optional): The maximum depth of the test\
                tree to collect the loggers. If set to None, all loggers are\
                collected. Defaults to None.

        Returns:
            list[logging.Logger]: The list of loggers of the multi-test and\
                its child tests.
        """

        def collect_loggers_recursive(
            test: TestABC, max_depth: int | None, loggers: list[logging.Logger]
        ) -> None:
            if max_depth is not None and test.depth > max_depth:
                return
            loggers.append(test._logger)
            if isinstance(test, MultiTestABC):
                for child in test._tests:
                    collect_loggers_recursive(child, max_depth, loggers)

        loggers: list[logging.Logger] = []
        collect_loggers_recursive(self, max_depth, loggers)
        return loggers

    async def set_status(
        self,
        status: TestStatus,
        reason: str | None = None,
        execute_routines: bool = True
    ) -> None:
        """Set the status of the test and execute the tagged routines that
        are triggered by the status change. Note that this may affect the
        status of the child tests.

        Args:
            status (TestStatus): The new status of the test.
            reason (str | None, optional): The reason for the status change.\
                Defaults to None.
            execute_routines (bool, optional): If True, the tagged routines\
                that are triggered by the status change are executed.\
                Defaults to True.
        """
        if status == TestStatus.PASSED:
            if any(child.status != TestStatus.PASSED for child in self._tests):
                status = TestStatus.PASSED_WITH_WARNING
        await super().set_status(status, reason, execute_routines)
        # set the status of the child tests based on the parent test status
        # notes ↓ ↓ ↓
        """
        Although the following matching logic should work for the most
        common cases, it is not a complete solution. It would be nice to have
        some kind of a state machine for each test in the multitest.
        """
        match status:
            case TestStatus.QUEUED | TestStatus.RUNNING:
                for test in self._tests:
                    match test.status:
                        case (
                            TestStatus.UNKNOWN |
                            TestStatus.PENDING
                        ):
                            await test.set_status(TestStatus.QUEUED)
            case TestStatus.TIMEOUT:
                for test in self._tests:
                    match test.status:
                        case (
                            TestStatus.UNKNOWN |
                            TestStatus.PENDING |
                            TestStatus.QUEUED
                        ):
                            await test.set_status(TestStatus.ABORTED)
                        case TestStatus.RUNNING:
                            await test.set_status(TestStatus.TIMEOUT)
            case TestStatus.FAILED | TestStatus.ABORTED:
                for test in self._tests:
                    match test.status:
                        case (
                            TestStatus.UNKNOWN |
                            TestStatus.PENDING |
                            TestStatus.QUEUED |
                            TestStatus.RUNNING
                        ):
                            await test.set_status(TestStatus.ABORTED)
            case _:
                pass  # add generic child test status setting here?...

    @abstractmethod
    async def _run(self):
        """Overwrite this method in the subclass to implement the test logic.
        This method is called during the test execution. Do not catch any
        errors explicitly in your implementation. The error catching
        algorithm is implemented within the test run loop.
        """
        ...


class SequentialMultiTest(MultiTestABC[TTestType]):
    """
    A sequential multi-test. The child tests are executed sequentially in the
    order they were added to the multi-test. The test is passed if all child
    tests are passed. The test is passed with warning if one of the child tests
    fails, but the `allow_fail` attribute is set to `True`. Otherwise, the test
    is failed.
    """
    def __init__(
        self,
        *tests: TTestType,
        allow_fail: bool = False,
        name: str | None = None,
        min_duration: float | None = None,
        max_duration: float | None = None
    ) -> None:
        """Initialize the sequential multi-test object.

        Args:
            allow_fail (bool, optional): If `True`, the multi-test will\
                continue execution if one of the child tests fails.\
                If `False`, it will terminate the execution and abort\
                the remaining tests. Defaults to False.
            name (str | None, optional): The name of the test. If None, the\
                name is set to the class name with the object ID. Defaults to\
                None.
            min_duration (float | None, optional): The minimum duration of the\
                test in seconds. The test will not finish before this time has\
                passed. Defaults to None.
            max_duration (float | None, optional): The maximum duration of the\
                test in seconds. The test will be stopped if it runs longer\
                than this time. Defaults to None.
        """
        super().__init__(
            *tests,
            type_=TestType.MULTITEST_SEQUENTIAL,
            allow_fail=allow_fail,
            name=name,
            min_duration=min_duration,
            max_duration=max_duration
            )

    async def _run(self) -> None:
        """Test run logic implementation of a sequential multi-test."""
        for test in self._tests:
            await test.run()


class ParallelMultiTest(MultiTestABC[TTestType]):
    """
    A parallel multi-test. The child tests are executed simultaneously in the
    order they were added to the multi-test. The test is passed if all child
    tests are passed. The test is passed with warning if one of the child tests
    fails, but the `allow_fail` attribute is set to `True`. Otherwise, the test
    is failed.
    """
    def __init__(
        self,
        *tests: TTestType,
        allow_fail: bool = False,
        name: str | None = None,
        min_duration: float | None = None,
        max_duration: float | None = None
    ) -> None:
        """Initialize the parallel multi-test object.

        Args:
            allow_fail (bool, optional): If `True`, the multi-test will\
                continue execution if one of the child tests fails.\
                If `False`, it will terminate the execution and abort\
                the remaining tests. Defaults to False.
            name (str | None, optional): The name of the test. If None, the\
                name is set to the class name with the object ID. Defaults to\
                None.
            min_duration (float | None, optional): The minimum duration of the\
                test in seconds. The test will not finish before this time has\
                passed. Defaults to None.
            max_duration (float | None, optional): The maximum duration of the\
                test in seconds. The test will be stopped if it runs longer\
                than this time. Defaults to None.
        """
        super().__init__(
            *tests,
            type_=TestType.MULTITEST_PARALLEL,
            allow_fail=allow_fail,
            name=name,
            min_duration=min_duration,
            max_duration=max_duration
            )

    async def _run(self):
        """Test run logic implementation of a parallel multi-test."""
        async with asyncio.TaskGroup() as tg:
            for test in self._tests:
                tg.create_task(test.run())
