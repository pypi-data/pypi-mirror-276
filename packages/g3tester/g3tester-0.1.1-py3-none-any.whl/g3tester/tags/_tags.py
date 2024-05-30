import enum

from functools import cached_property, wraps
from typing import Any, Callable, Iterable, Iterator, Literal, NamedTuple

from ..enums import TestStatus


class LogFilter(enum.StrEnum):
    """
    Enumeration that defines log filter options for tagged methods
    in test classes.

    Note that the log filter only governs the "outer" logging during test
    execution; internal log messages remain unaffected.

    WARNING: Currently, setting this for a tagged method does not change
    logging behavior.
    """
    NEVER = enum.auto()
    """Do not log method execution."""
    IF_TRUE = enum.auto()
    """Log method execution only if it returns `True`."""
    IF_FALSE = enum.auto()
    """Log method execution only if it returns `False`."""
    ALWAYS = enum.auto()
    """Always log method execution."""


class TagType(enum.StrEnum):
    """
    Enumeration that defines types of tags applicable to methods
    in test classes.
    """
    BEFORE_COMMAND = enum.auto()
    """Method that is executed before a test command."""
    AFTER_COMMAND = enum.auto()
    """Method that is executed after a test command."""
    FAIL = enum.auto()
    """Method that evaluates whether the test has failed."""
    WARNING = enum.auto()
    """Method that evaluates whether the test has produced a warning."""
    SUCCESS = enum.auto()
    """Method that evaluates whether the test has succeeded."""
    ON_STATUS_CHANGE = enum.auto()
    """Method that is executed when the test status changes."""
    COMMAND = enum.auto()
    """Method that represents a test command."""
    VALUE_GETTER = enum.auto()
    """Method that acquires the value of the test."""
    DESCRIPTION = enum.auto()
    """Method that provides a description of the test."""


class TagInfo(NamedTuple):
    """
    A names tuple that holds tag information for a method in a test class,
    including the type of tag, the target command, priority, logging filter,
    and an optional description.
    """
    type_: TagType
    """The type of the tag."""
    target: Any | None
    """The target of the tag (e.g., the command name)."""
    priority: int
    """The priority of the tagged method execution."""
    log: LogFilter
    """The log filter for the tagged method."""
    description: str | None
    """The description of the tagged method."""


class TagDecorator:
    """
    A decorator factory that provides a mechanism for dynamically attaching
    metadata, or "tags," to methods in test classes. These tags categorize
    methods based on their function and importance in the overall test
    execution process.

    New decorators can be created using the class method `new`. The produced
    decorator can be used with parentheses, as in `@decorator(...)`, or
    without them, as in `@decorator`.

    Attributes:
        TAG_ATTR (str): Attribute name used to attach tags to methods.\
            Stores tags in a list of `TagInfo` named tuples.
    """

    TAG_ATTR: str = "_tags"
    """
    Name of the attribute used to store a list of `TagInfo` objects
    attached to a method.
    """

    def __init__(self, tags: TagInfo | Iterable[TagInfo]) -> None:
        """Initialize the `TagDecorator` with a set of tags that can be
        attached to methods.

        Args:
            tags (TagInfo | Iterable[TagInfo]): A single `TagInfo` or \
                an iterable of `TagInfo` instances to be used as tags.
        """
        self.tags: list[TagInfo] = self.format_tags(tags)

    def __call__(self, func: Callable) -> Callable:
        """Makes `TagDecorator` instance callable, allowing it to be used
        directly as a decorator without parameters. This method is invoked when
        the decorator is applied directly to a function, as in `@decorator`.

        When applied, it attached predefined tags to the function.
        Execution of the function is not affected.

        Args:
            func (Callable): The method to decorate with tags.

        Returns:
            Callable: A wrapper that decorates the method with tags,
            adding specified tag metadata to the method.
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return self.attach_tags(wrapper)

    @classmethod
    def new(
        cls, func: Callable | None = None, *, tags: TagInfo | Iterable[TagInfo]
    ) -> Callable:
        """Creates a decorator with specified tags.

        This method acts as a factory for creating a new `TagDecorator`
        instance. The decorator can be used with or without parentheses.

        When called without a function argument (`func`), it returns
        a decorator configured with the specified tags. This returned decorator
        can then be applied to a function using parentheses, as in
        `@decorator(...)`. If `func` is provided, it applies the decorator
        immediately to that function.

        Args:
            func (Callable | None, optional): The method to decorate.
            tags (TagInfo | Iterable[TagInfo]): Tags to attach to the method.

        Returns:
            Callable: Either the decorated method or a decorator\
                configured with specific tags, depending on the usage.
        """
        decorator = cls(tags)
        if func is None:  # the decorator was called with parentheses
            return decorator
        else:
            return decorator(func)

    @classmethod
    def get_func_tags(cls, func: Callable) -> list[TagInfo] | None:
        """Get the tags attached to a method, if any.

        Args:
            func (Callable): The method to get the tags from.

        Returns:
            list[TagInfo] | None: The list of `TagInfo` named tuples\
                assigned to the method or `None` if no tags are assigned.
        """
        return getattr(func, cls.TAG_ATTR, None)

    @staticmethod
    def format_tags(tags: TagInfo | Iterable[TagInfo]) -> list[TagInfo]:
        """Validate and format the tags into a list of `TagInfo` named tuples.

        Args:
            tags (TagInfo | Iterable[TagInfo]): The tags to format.

        Raises:
            ValueError: If the tags are of an invalid type.

        Returns:
            list[TagInfo]: The list of `TagInfo` named tuples.
        """
        if isinstance(tags, TagInfo):
            return [tags]
        elif isinstance(tags, Iterable):
            return [tag for tag in tags]
        raise ValueError(f'Invalid tag type "{type(tags).__name__}".')

    def attach_tags(self, func: Callable) -> Callable:
        """Associate tags with a method, storing them within the method's
        attributes under the `TAG_ATTR` attribute name.

        Args:
            func (Callable): The method to attach the tags to.

        Returns:
            Callable: The method with the tags attached.
        """
        if not hasattr(func, self.TAG_ATTR):
            setattr(func, self.TAG_ATTR, [])
        assert isinstance((tags := getattr(func, self.TAG_ATTR)), list)
        for tag in self.tags:
            tags.append(tag)
        return func


def get_obj_name(obj: Any) -> str:
    """Get the name of the object via the `__name__` attribute. If the object
    does not have this attribute, the object is converted to a string.

    Args:
        obj (Any): The object to get the name of.

    Returns:
        str: The name of the object.
    """
    try:
        return obj.__name__
    except AttributeError:
        return str(obj)


class ObjectTagCollector:
    """
    A utility class for collecting and organizing methods tagged with metadata
    within a given object. This class helps to categorize methods by their tags
    and provides facilities for accessing and sorting these methods based on
    their relevance to specific operations, such as test execution flow.
    """
    def __init__(self, obj: object) -> None:
        """Initialize the `ObjectTagCollector`.

        The methods that have been tagged using the `TagDecorator` are
        collected and organized them based on the tags.

        Args:
            obj (object): The object to collect tagged methods from.
        """
        self._obj = obj
        self.tagged_methods = self.collect_tagged_methods(obj)

    def _get_method_tags(self, method_name: str) -> list[TagInfo]:
        """Get the tags attached to the specified method.

        Args:
            method_name (str): The name of the method to get the tags from.

        Returns:
            list[TagInfo]: The list of `TagInfo` named tuples assigned to the\
                method.
        """
        method = getattr(self._obj, method_name)
        return TagDecorator.get_func_tags(method) or []

    def _get_method_priority(
        self, method_name: str, matches: Callable[[TagInfo], bool]
    ) -> int:
        """Get the priority of the method based on the specified tag matching
        function. This function is used to evaluate which tag to get
        the priority from when multiple tags are attached to the method.

        Args:
            method_name (str): The name of the method to get the priority of.
            matches (Callable[[TagInfo], bool]): The function that matches\
                the tag to the specified criteria to choose which tag to get\
                the priority from. It should accept a `TagInfo` named tuple\
                and return a boolean value.

        Raises:
            TypeError: If no matching tag attached to the method is found.

        Returns:
            int: The priority of the method.
        """
        method_tags = self._get_method_tags(method_name)
        for tag in method_tags:
            if matches(tag):
                return tag.priority
        # should be unreachable
        raise TypeError(f'Method "{method_name}" was not mached.')

    def _sort_methods_by_priority(
        self, method_names: Iterable[str], matches: Callable[[TagInfo], bool]
    ) -> list[str]:
        """Sort the methods by priority and then alphabetically by name for
        ties.

        Args:
            method_names (Iterable[str]): The names of the methods to sort.
            matches (Callable[[TagInfo], bool]): The function that matches\
                the tag to the specified criteria.

        Returns:
            list[str]: The sorted list of method names.
        """
        # get priority value for each method
        method_names_priorities = [
            (name, self._get_method_priority(name, matches))
            for name in method_names
            ]
        # sort by priority first, and then alphabetically by name for ties
        method_names_priorities.sort(key=lambda t: (t[1], t[0]))
        return [name for name, _ in method_names_priorities]

    @staticmethod
    def list_obj_methods(
        obj: object, exclude_dunder_methods: bool = True
    ) -> Iterator[str]:
        """List the method names of the specified object, excluding properties
        and optionally excluding dunder methods.

        Args:
            obj (object): The object to list the methods of.
            exclude_dunder_methods (bool, optional): Whether to exclude\
                dunder methods from the list. Defaults to `True`.

        Yields:
            Iterator[str]: A generator that yields method names of the object.
        """
        for method_name in dir(obj):
            method = getattr(obj, method_name, None)
            if (
                callable(method) and
                not isinstance(method, (property, cached_property)) and
                not (exclude_dunder_methods and method_name.startswith("__"))
            ):
                yield method_name

    def collect_tagged_methods(self, obj: object) -> dict[TagType, list[str]]:
        """Collect tagged methods from the specified object.

        Args:
            obj (object):  The object from which to collect tagged methods.

        Returns:
            dict[TagType, list[str]]: The dictionary categorizing methods by\
                their tag types. Dictionary keys are `TagType` values, and\
                the corresponding values are lists of method names.
        """
        tagged: dict[TagType, set[str]] = {tag: set() for tag in TagType}
        # collect tagged methods
        for method_name in self.list_obj_methods(obj):
            method_tags = self._get_method_tags(method_name)
            for tag in method_tags:
                tagged[tag.type_].add(method_name)
        # sort tagged methods by priority
        tagged_sorted: dict[TagType, list[str]] = {}
        for tag_type, method_names in tagged.items():
            tagged_sorted[tag_type] = self._sort_methods_by_priority(
                method_names, lambda tag: tag.type_ == tag_type
                )
        return tagged_sorted

    def count_tags(self, tag_type: TagType) -> int:
        """Get the number of methods tagged with the specified tag type.

        Args:
            tag_type (TagType): The tag type to count.

        Returns:
            int: The number of methods tagged with the specified tag type.
        """
        return len(self.tagged_methods.get(tag_type, []))

    def get_tagged_methods(self, tag_type: TagType) -> list[str]:
        """Get the methods tagged with the specified tag type.

        Args:
            tag_type (TagType): The type of tag to filter methods by.

        Returns:
            list[str]: The list of method names tagged with\
                the specified tag type.
        """
        return self.tagged_methods.get(tag_type, [])

    def get_method(self, method_name: str) -> Callable:
        """Get the method callable object from the object by its name.

        Args:
            method_name (str): The name of the method to get.

        Returns:
            Callable: The method object with the specified name.
        """
        return getattr(self._obj, method_name)

    def get_method_priority(self, method_name: str, tag_type: TagType) -> int:
        """Get the priority of a method within the context of a specified tag
        type. This method iterates over tags attached to the method and matches
        them against the specified tag type to determine the relevant priority.

        Args:
            method_name (str): The name of the method to get the priority of.
            tag_type (TagType): The tag type to match.

        Returns:
            int: The priority of the method within the specified tag type.
        """
        return self._get_method_priority(
            method_name, lambda tag: tag.type_ == tag_type
            )

    @cached_property
    def status_change_actions(self) -> dict[TestStatus, list[str]]:
        """
        A dictionary of the possible test status values and corresponding
        methods that are triggered when the status changes to this value.
        The list of method names is sorted by priority first, and then
        alphabetically by name for ties.
        """
        actions: dict[TestStatus, set[str]] = {ts: set() for ts in TestStatus}
        # collect tagged methods that are to be executed on status change
        tag_type = TagType.ON_STATUS_CHANGE
        for method_name in self.tagged_methods.get(tag_type, []):
            method_tags = self._get_method_tags(method_name)
            for tag in method_tags:
                if tag.type_ == tag_type:
                    assert isinstance(tag.target, TestStatus)
                    actions[tag.target].add(method_name)
        # sort status change actions by priority
        actions_sorted: dict[TestStatus, list[str]] = {}
        for status, method_names in actions.items():
            actions_sorted[status] = self._sort_methods_by_priority(
                method_names, lambda tag: tag.target == status
                )
        return actions_sorted

    @cached_property
    def commands_with_conditions(self) -> dict[
        str | None,
        dict[Literal[TagType.BEFORE_COMMAND, TagType.AFTER_COMMAND], list[str]]
    ]:
        """
        A dictionary of test command methods and corresponding routines that
        are executed before and after the commands. Both the commands
        (the dictionary keys) and the routines (lists mapped to
        the "TagType.BEFORE_COMMAND" and "TagType.AFTER_COMMAND" keys within
        the inner dictionary) are sorted by priority first, and then
        alphabetically by name for ties.
        """
        commands: dict = {
            command: {TagType.BEFORE_COMMAND: [], TagType.AFTER_COMMAND: []}
            for command in self.tagged_methods.get(TagType.COMMAND, [])
            }
        if None not in commands:
            commands[None] = {
                TagType.BEFORE_COMMAND: [], TagType.AFTER_COMMAND: []
                }
        for tag_type in [TagType.BEFORE_COMMAND, TagType.AFTER_COMMAND]:
            for method_name in self.tagged_methods.get(tag_type, []):
                method_tags = self._get_method_tags(method_name)
                for tag in method_tags:
                    if tag.type_ == tag_type:
                        target = tag.target
                        if target is None or isinstance(target, str):
                            conditions = commands[target][tag_type]
                            conditions.append(method_name)
                        else:
                            target_type = type(target).__name__
                            raise TypeError(
                                f'Invalid target type "{target_type}".'
                                )
        return commands

    @cached_property
    def value_getter(self) -> str | None:
        """
        A method that implements the value acqusition logic. Only one method
        within a class can be tagged as a value getter! If more than one
        method is tagged as a value getter, a ValueError is raised. If no
        method is tagged as a value getter, `None` is returned.
        """
        getter = self.tagged_methods.get(TagType.VALUE_GETTER, [])
        if len(getter) == 0:
            return None
        if len(getter) == 1:
            return getter[0]
        getters = ", ".join(f'"{g}"' for g in getter)
        raise ValueError(
            f'Test cannot have more than 1 value getter '
            f'(found {len(getter)}: {getters}).'
            )


def command_to_list(obj: Any) -> list[str] | list[None]:
    """Convert an object to a list of bounded commands.

    Args:
        obj (Any): The object to convert.

    Raises:
        ValueError: If the object cannot be converted to a list of bounded\
            commands.

    Returns:
        list[str] | list[None]: A list of bounded commands.
    """
    if obj is None:
        return [None]
    if callable(obj):
        obj = get_obj_name(obj)
    if isinstance(obj, str):
        return [obj]
    if isinstance(obj, Iterable):
        objs = []
        for o in obj:
            if callable(o):
                objs.append(get_obj_name(o))
            else:
                objs.append(o)
        return objs
    raise ValueError(
        f'Object of type "{type(obj).__name__}" cannot be converted to '
        f'a list of bounded commands.'
        )


def test_status_to_list(obj: Any) -> list[TestStatus]:
    """Convert an object to a list of bounded test statuses.

    Args:
        obj (Any): The object to convert.

    Raises:
        ValueError: If the object cannot be converted to a list of bounded\
            test statuses.

    Returns:
        list[TestStatus]: A list of bounded test statuses.
    """
    if obj is None:
        return [s for s in TestStatus]
    if isinstance(obj, str) or isinstance(obj, TestStatus):
        return [TestStatus(obj)]
    if isinstance(obj, Iterable):
        objs = []
        for o in obj:
            if isinstance(o, str):
                objs.append(TestStatus(o))
            else:
                objs.append(o)
        return objs
    raise ValueError(
        f'Object of type "{type(obj).__name__}" cannot be converted to '
        f'a list of bounded test statuses.'
        )


def description(method: Callable | None = None) -> Callable:
    """A decorator that marks a method as a dynamic description generator
    within a test class. Although the decorator does not expect any arguments
    except for the method itself, it can be used directly (without parentheses)
    or with parentheses. The latter makes no difference in the decorator's
    behavior.

    The decorated method should expect no arguments and return a string.
    It may be asynchronous. Only one method in any test class should be
    decorated with `@description`.
    Note:
        Method decorated with `@description` do not influence the flow of test
        execution, but are used to dynamically generate descriptions for
        reporting or logging purposes.

    Example:
        ```python
        class MyTest(SingleTest):
            @description
            def my_description(self) -> str:
                return f'Test description for {self.name}'
        ```

    Args:
        method (Callable | None, optional): The method to be decorated.\
            Usually, this argument should not be provided explicitly.\
            If None, the decorator prepares to be applied when the method\
            is passed in a subsequent call.

    Returns:
        Callable: A decorated method with the attached description tag when\
            the decorator is applied directly, or the decorator itself\
            when used with parentheses.
    """
    tag = TagInfo(TagType.DESCRIPTION, None, 0, LogFilter.NEVER, None)
    return TagDecorator.new(method, tags=tag)


def command(
    method: Callable | None = None,
    /,
    *,
    priority: int = 999,
    log: LogFilter = LogFilter.ALWAYS,
    description: str | None = None
) -> Callable:
    """A decorator that marks a method as a test command within a test class.
    A command is a method that represents a specific action or operation that
    is executed before the test evaluation. The decorator may be used directly
    without parentheses or with parentheses to specify additional parameters.

    The command priority can be set using the `priority` parameter. The lower
    the priority value, the command is executed. Commands with the same
    priority are executed in the alphabetical order of the method names.

    The `log` parameter specifies the log filter value for the command. See
    the `LogFilter` enumeration for possible values. WARNING: Currently,
    setting this for a tagged method does not change logging behavior.

    Description of the command action purpose can be specified using
    the `description` parameter.

    The decorated method should expect no arguments. It may return a value of
    any type. The decorated method may be asynchronous. The number of methods
    in a test class that can be decorated with `@command` is not limited.

    Example:
        ```
        # In this example, the `increment_by_one` and `increment_by_two`
        # methods are marked as commands. The `priority` parameter determines
        # the order of execution: `increment_by_one` will be executed before
        # `increment_by_two`.

        class MyTest(SingleTest):
            @command(priority=1, description="Increment the value by one")
            def increment_by_one(self):
                self.value += 1

            @command(priority=2, description="Increment the value by two")
            def increment_by_two(self):
                self.value += 2
        ```

    Args:
        method (Callable | None, optional): The method to be decorated.\
            Usually, this argument should not be provided explicitly.\
            If None, the decorator prepares to be applied when the method\
            is passed in a subsequent call.
        priority (int, optional): Priority of the command. Lower values\
            indicate higher priority. Commands with the same priority\
            are evaluated in alphabetical order of their method names.\
            Defaults to 999.
        log (LogFilter, optional): Specifies the logging behavior for\
            the command. See `LogFilter` enumeration for possible values.
            Defaults to LogFilter.ALWAYS. Note: Current implementation does not
            alter logging behavior.
        description (str | None, optional): Description of the purpose of\
            the command action. Defaults to None.

    Returns:
        Callable: A decorated method with the attached description tag when\
            the decorator is applied directly, or the decorator itself\
            when used with parentheses.
    """
    tag = TagInfo(TagType.COMMAND, None, priority, log, description)
    return TagDecorator.new(method, tags=tag)


def before_command(
    method: Callable | None = None,
    /,
    *,
    command: str | Iterable[str] | Callable | Iterable[Callable] | None = None,
    priority: int = 999,
    log: LogFilter = LogFilter.ALWAYS,
    description: str | None = None
) -> Callable:
    """A decorator that marks a method as a prerequisite condition for one or
    more test commands. This condition must be met before the specified
    command(s) can be executed. The decorator may be used directly without
    parentheses or with parentheses to specify additional parameters.

    The target command can be specified in the `command` parameter as a string,
    a list of strings, a callable, or a list of callables. If more than one
    command is specified, the condition is applied to all of them. If no
    command is specified, the condition must be met before the first command
    is executed. If a test does not implement commands, the condition must be
    met before the test evaluation.

    The prerequisite condition priority can be set using the `priority`
    parameter. The lower the priority value, the earlier the condition is
    checked. Conditions with the same priority are checked in the alphabetical
    order of the method names.

    The `log` parameter specifies the log filter value for the condition. See
    the `LogFilter` enumeration for possible values. WARNING: Currently,
    setting this for a tagged method does not change logging behavior.

    Description of the condition purpose can be specified using
    the `description` parameter.

    The decorated method should expect no arguments and return a boolean value
    or `None`. In the latter case, the condition is aumatically considered met.
    The decorated method may be asynchronous. The number of methods in a test
    class that can be decorated with `@before_command` is not limited.

    Example:
        ```
        # In this example, the "MyTest" class implements a command "increment"
        # that adds 1 to the value. To ensure that the value is 0 before the
        # command is applied, the "is_value_zero" method is marked as a
        # precondition for the "increment" method. Now, the "increment" method
        # will not be executed until the "is_value_zero" method returns True.

        class MyTest(SingleTest):

            @before_command(
                command='increment',
                description="Check if the initial value is 0"
                )
            def is_value_zero(self) -> bool:
                return self.value == 0

            @command(description="Increment the value by 1")
            def increment(self):
                self.value += 1
        ```

    Args:
        method (Callable | None, optional): The method to be decorated.\
            Usually, this argument should not be provided explicitly.\
            If None, the decorator prepares to be applied when the method\
            is passed in a subsequent call.
        command (str | Iterable[str] | Callable | Iterable[Callable] | None,\
        optional): Command(s) the condition applies to. If None, the condition\
            must be met before the first command is executed. Defaults to None.
        priority (int, optional): Priority of the condition. Lower values\
            indicate higher priority. Conditions with the same priority\
            are evaluated in alphabetical order of their method names.\
            Defaults to 999.
        log (LogFilter, optional): Specifies the logging behavior for\
            the condition. See `LogFilter` enumeration for possible values.
            Defaults to LogFilter.ALWAYS. Note: Current implementation does not
            alter logging behavior.
        description (str | None, optional): Description of the purpose of\
            the prerequisite condition. Defaults to None.

    Returns:
        Callable: A decorated method with the attached description tag when\
            the decorator is applied directly, or the decorator itself\
            when used with parentheses.
    """
    tags = [
        TagInfo(TagType.BEFORE_COMMAND, target, priority, log, description)
        for target in command_to_list(command)
        ]
    return TagDecorator.new(method, tags=tags)


def after_command(
    method: Callable | None = None,
    /,
    *,
    command: str | Iterable[str] | Callable | Iterable[Callable] | None = None,
    priority: int = 999,
    log: LogFilter = LogFilter.ALWAYS,
    description: str | None = None
) -> Callable:
    """A decorator that marks a method as a post-condition for one or
    more test commands. This post-condition is executed after the specified
    command(s) have been executed. The decorator may be used directly without
    parentheses or with parentheses to specify additional parameters.

    The target command can be specified in the `command` parameter as a string,
    a list of strings, a callable, or a list of callables. If more than one
    command is specified, the post-condition is applied to all of them. If no
    command is specified, the post-condition is executed after the last command
    is executed. If a test does not implement commands, the post-condition is
    executed before the test evaluation.

    The post-condition's execution priority can be set using the `priority`
    parameter. The lower the priority value, the earlier the post-condition is
    executed after the command(s). Post-conditions with the same priority are
    executed in the alphabetical order of the method names.

    The `log` parameter specifies the log filter value for the post-condition.
    See the `LogFilter` enumeration for possible values. WARNING: Currently,
    setting this for a tagged method does not change logging behavior.

    Description of the post-condition's purpose can be specified using
    the `description` parameter.

    The decorated method should expect no arguments and return a boolean value
    or `None`. In the latter case, the post-condition is automatically
    considered met. The decorated method may be asynchronous. The number of
    methods in a test class that can be decorated with `@after_command` is not
    limited.

    Example:
        ```
        # In this example, the "MyTest" class implements a command "decrement"
        # that subtracts 1 from the value. To check if the value is
        # non-negative after the "decrement" command is applied,
        # the "is_non_negative" method is marked as a post-condition for
        # the "decrement" method. Now, the "is_non_negative" method will be
        # executed immediately after the "decrement" method is called.

        class MyTest(SingleTest):

            @command(description="Decrement the value by 1")
            def decrement(self):
                self.value -= 1

            @after_command(
                command='decrement',
                description="Check if the final value is non-negative"
                )
            def is_non_negative(self) -> bool:
                return self.value >= 0
        ```

    Args:
        method (Callable | None, optional): The method to be decorated.\
            Usually, this argument should not be provided explicitly.\
            If None, the decorator prepares to be applied when the method\
            is passed in a subsequent call.
        command (str | Iterable[str] | Callable | Iterable[Callable] | None,
        optional): Command(s) that the post-condition applies to. If None,\
            the post-condition is executed after the last command is executed.\
            Defaults to None.
        priority (int, optional): Priority of the post-condition. Lower values\
            indicate higher priority. Post-conditions with the same priority\
            are executed in alphabetical order of their method names.\
            Defaults to 999.
        log (LogFilter, optional): Specifies the logging behavior for the\
            post-condition. See `LogFilter` enumeration for possible values.\
            Defaults to LogFilter.ALWAYS. Note: Current implementation\
            does not alter logging behavior.
        description (str | None, optional): Description of the purpose of\
            the post-condition. Defaults to None.

    Returns:
        Callable: A decorated method with the attached description tag when\
            the decorator is applied directly, or the decorator itself\
            when used with parentheses.
    """
    tags = [
        TagInfo(TagType.AFTER_COMMAND, target, priority, log, description)
        for target in command_to_list(command)
    ]
    return TagDecorator.new(method, tags=tags)


def value_getter(
    method: Callable | None = None,
    /,
    *,
    log: LogFilter = LogFilter.ALWAYS,
    description: str | None = None,
) -> Callable:
    """A decorator that marks a method as a value getter within a test class.
    The value getter is a method that acquires the value that is a subject of
    the test evaluation. The decorator may be used directly without parentheses
    or with parentheses to specify additional parameters.

    The `log` parameter specifies the log filter value for the post-condition.
    See the `LogFilter` enumeration for possible values. WARNING: Currently,
    setting this for a tagged method does not change logging behavior.

    Description of the post-condition's purpose can be specified using
    the `description` parameter.

    The decorated method should expect no arguments and return a value of any
    type. It may be asynchronous. Only one method in any test class should be
    decorated with `@value_getter`.

    Example:
        ```
        # In this example, the "MyTest" class defines a method
        # "get_current_value" that simply returns the sum of 1 and 1.
        # This method is executed within the test evaluation loop to acquire
        # the current value. The return value of the "get_current_value" method
        # is stored under the "value" attribute of the test instance.
        # The "is_value_two" method then checks if the value is equal to 2.

        class MyTest(SingleTest):

            @value_getter(description="Get the current value")
            def get_current_value(self) -> int:
                return 1 + 1

            @success(description="Check if the value is 2")
            def is_value_two(self) -> bool:
                return self.value == 2
        ```

    Args:
        method (Callable | None, optional): The method to be decorated.\
            Usually, this argument should not be provided explicitly.\
            If None, the decorator prepares to be applied when the method\
            is passed in a subsequent call.
        log (LogFilter, optional): Specifies the logging behavior for the\
            value getter. See `LogFilter` enumeration for possible values.\
            Defaults to LogFilter.ALWAYS. Note: Current implementation\
            does not alter logging behavior.
        description (str | None, optional): Description of the retrieved\
            value. Defaults to None.

    Returns:
        Callable: A decorated method with the attached description tag when\
            the decorator is applied directly, or the decorator itself\
            when used with parentheses.
    """
    tag = TagInfo(TagType.VALUE_GETTER, None, 0, log, description)
    return TagDecorator.new(method, tags=tag)


def fail(
    method: Callable | None = None,
    /,
    *,
    priority: int = 999,
    log: LogFilter = LogFilter.ALWAYS,
    description: str | None = None
) -> Callable:
    """A decorator that marks a method as a fail condition within a test class.
    If at least one of such conditions is met, the test is considered failed.
    The decorator may be used directly without parentheses or with parentheses
    to specify additional parameters.

    The execution priority of fail conditions can be set using the `priority`
    parameter. The lower the priority value, the earlier the fail condition is
    checked. Fail conditions with the same priority are checked in the
    alphabetical order of the method names.

    The `log` parameter specifies the log filter value for the fail condition.
    See the `LogFilter` enumeration for possible values. WARNING: Currently,
    setting this for a tagged method does not change logging behavior.

    Description of the fail condition can be specified using
    the `description` parameter.

    The decorated method should expect no arguments and return a boolean value
    or `None`. If the method returns `True`, the fail condition is considered
    met. If the method returns `False` or `None`, the condition is considered
    not met. The decorated method may be asynchronous. The number of methods
    in a test class that can be decorated with `@fail` is not limited.

    Example:
        ```
        # In this example, the "MyTest" class defines a method
        # "is_value_negative", which checks if the value is negative.
        # If the method returns True, the test is considered failed.

        class MyTest(SingleTest):
            @fail(description="Check if the value is negative")
            def is_value_negative(self) -> bool:
                return self.value < 0
        ```

    Args:
        method (Callable | None, optional): The method to be decorated.\
            Usually, this argument should not be provided explicitly.\
            If None, the decorator prepares to be applied when the method\
            is passed in a subsequent call.
        priority (int, optional): Priority of the fail condition. Lower values\
            indicate higher priority. Fail conditions with the same priority\
            are executed in alphabetical order of their method names.\
            Defaults to 999.
        log (LogFilter, optional): Specifies the logging behavior for the\
            fail condition. See `LogFilter` enumeration for possible values.\
            Defaults to LogFilter.ALWAYS. Note: Current implementation\
            does not alter logging behavior.
        description (str | None, optional): Description of the fail condition.\
            Defaults to None.

    Returns:
        Callable: A decorated method with the attached description tag when\
            the decorator is applied directly, or the decorator itself\
            when used with parentheses.
    """
    tag = TagInfo(TagType.FAIL, None, priority, log, description)
    return TagDecorator.new(method, tags=tag)


def warning(
    method: Callable | None = None,
    /,
    *,
    priority: int = 999,
    log: LogFilter = LogFilter.ALWAYS,
    description: str | None = None
) -> Callable:
    """A decorator that marks a method as a warning condition within a test
    class. If this condition is met, it triggers a warning but does not
    necessarily fail the test. The decorator may be used directly without
    parentheses or with parentheses to specify additional parameters.

    The execution priority of warning conditions can be set using
    the `priority` parameter. The lower the priority value, the earlier
    the warning condition is checked. Warning conditions with the same priority
    are checked in the alphabetical order of the method names.

    The `log` parameter specifies the log filter value for the warning
    condition. See the `LogFilter` enumeration for possible values.
    WARNING: Currently, setting this for a tagged method does not change
    logging behavior.

    A description of the warning condition can be specified using
    the `description` parameter.

    The decorated method should expect no arguments and return a boolean value
    or `None`. If the method returns `True`, the warning condition is
    considered met. If the method returns `False` or `None`, the condition is
    considered not met. The decorated method may be asynchronous.
    The number of methods in a test class that can be decorated with `@warning`
    is not limited.

    Example:
        ```
        # In this example, the "MyTest" class defines a method "is_value_zero",
        # which checks if the value is zero. If the method returns True,
        # a warning is triggered.

        class MyTest(SingleTest):
            @warning(description="Check if the value is zero")
            def is_value_zero(self) -> bool:
                return self.value == 0
        ```

    Args:
        method (Callable | None, optional): The method to be decorated.\
            Usually, this argument should not be provided explicitly.\
            If None, the decorator prepares to be applied when the method\
            is passed in a subsequent call.
        priority (int, optional): Priority of the warning condition. Lower\
            values indicate higher priority. Warning conditions with the same\
            priority are executed in alphabetical order of their method names.\
            Defaults to 999.
        log (LogFilter, optional): Specifies the logging behavior for\
            the warning condition. See `LogFilter` enumeration for possible\
            values. Defaults to LogFilter.ALWAYS. Note: Current implementation\
            does not alter logging behavior.
        description (str | None, optional): Description of the warning\
            condition. Defaults to None.

    Returns:
        Callable: A decorated method with the attached description tag when
            the decorator is applied directly, or the decorator itself
            when used with parentheses.
    """
    tag = TagInfo(TagType.WARNING, None, priority, log, description)
    return TagDecorator.new(method, tags=tag)


def success(
    method: Callable | None = None,
    /,
    *,
    priority: int = 999,
    log: LogFilter = LogFilter.ALWAYS,
    description: str | None = None
) -> Callable:
    """A decorator that marks a method as a success condition within a test
    class. Every success condition must be met for the test to be considered
    successful. The decorator may be used directly without parentheses or
    with parentheses to specify additional parameters.

    The execution priority of success conditions can be set using
    the `priority` parameter. The lower the priority value, the earlier
    the success condition is checked. Success conditions with the same priority
    are checked in the alphabetical order of the method names.

    The `log` parameter specifies the log filter value for the success
    condition. See the `LogFilter` enumeration for possible values.
    WARNING: Currently, setting this for a tagged method does not change
    logging behavior.

    Description of the success condition can be specified using
    the `description` parameter.

    The decorated method should expect no arguments and return a boolean value
    or `None`. If the method returns `True` or `None`, the success condition is
    considered met. If the method returns `False`, the condition is considered
    not met. The decorated method may be asynchronous. The number of methods
    in a test class that can be decorated with `@success` is not limited.

    Example:
        ```
        # In this example, the "MyTest" class defines a method
        # "is_value_nonnegative", which checks if the value is non-negative.
        # If the method returns True, the test is considered successful.

        class MyTest(SingleTest):
            @success(description="Check if the value is non-negative")
            def is_value_nonnegative(self) -> bool:
                return self.value >= 0
        ```

    Args:
        method (Callable | None, optional): The method to be decorated.
            Usually, this argument should not be provided explicitly.
            If None, the decorator prepares to be applied when the method
            is passed in a subsequent call.
        priority (int, optional): Priority of the success condition. Lower\
            values indicate higher priority. Success conditions with the same\
            priority are executed in alphabetical order of their method names.\
            Defaults to 999.
        log (LogFilter, optional): Specifies the logging behavior for\
            the success condition. See `LogFilter` enumeration for possible\
            values. Defaults to LogFilter.ALWAYS. Note: Current implementation\
            does not alter logging behavior.
        description (str | None, optional): Description of the success\
            condition. Defaults to None.

    Returns:
        Callable: A decorated method with the attached description tag when
            the decorator is applied directly, or the decorator itself
            when used with parentheses.
    """
    tag = TagInfo(TagType.SUCCESS, None, priority, log, description)
    return TagDecorator.new(method, tags=tag)


def on_status_change(
    method: Callable | None = None,
    /,
    *,
    change_to: (
        str | Iterable[str] | TestStatus | Iterable[TestStatus] | None
        ) = None,
    priority: int = 999,
    log: LogFilter = LogFilter.ALWAYS,
    description: str | None = None
) -> Callable:
    """Decorator for marking a method as an action to be performed when a test
    status changes to a specific status value(s). The method decorated with
    this decorator will be executed when the test's status changes to the
    specified status value(s). The decorator may be used directly without
    parentheses or with parentheses to specify additional parameters.

    The triggering status value(s) can be specified in the `change_to`
    parameter as a string, a list of strings, a member of the `TestStatus`
    enumeration, or a list of `TestStatus` members. If more than one status
    value is specified, the action is executed for all of them. If no status
    value is specified, the action is executed when the test status changes
    to any value.

    Priority of the action execution can be set using the `priority` parameter.
    The lower the priority value, the earlier the action is triggered after
    the status change. Actions with the same priority are executed in
    the alphabetical order of the method names.

    The `log` parameter specifies the log filter value for the action.
    See the `LogFilter` enumeration for possible values. WARNING: Currently,
    setting this for a tagged method does not change logging behavior.

    Description of the action's purpose can be specified using
    the `description` parameter.

    The decorated method should expect no arguments. It may return value of
    any type. The decorated method may be asynchronous. The number of actions
    in a test class that can be triggered by a status change is not limited.
    Overall number of methods in a test class that can be decorated with
    `@on_status_change` is not limited, too.

    Example:
        ```
        # In this example, the "MyTest" class implements methods that react to
        # status changes. The "log_status_change" method logs every status
        # change at the INFO level. The "log_timeout" method logs a warning
        # when the status changes to `TestStatus.TIMEOUT`.

        class MyTest(SingleTest):

            @on_status_change(
                description="log status change"
                )
            def log_status_change(self) -> None:
                self.logger.info("status changed to %s", self.status)

            @on_status_change(
                change_to=TestStatus.TIMEOUT, description="log timeout"
                )
            def log_timeout(self) -> None:
                self.logger.warning("timeout")
        ```

    Args:
        method (Callable | None, optional): The method to be decorated.\
            Usually, this argument should not be provided explicitly.\
            If None, the decorator prepares to be applied when the method\
            is passed in a subsequent call.
        change_to (str | Iterable[str] | TestStatus | Iterable[TestStatus] |
        None, optional): Status value(s) that trigger the action. If None,\
            the action is executed when the test status changes to any value.\
        priority (int, optional): Priority of the action within all actions\
            triggered by the same status change event. Lower values indicate\
            higher priority. Actions with the same priority are executed in\
            alphabetical order of their method names. Defaults to 999.
        log (LogFilter, optional): Specifies the logging behavior for the\
            action execution. See `LogFilter` enumeration for possible values.\
            Defaults to LogFilter.ALWAYS. Note: Current implementation\
            does not alter logging behavior.
        description (str | None, optional): Description of the purpose of\
            the action. Defaults to None.

    Returns:
        Callable: A decorated method with the attached description tag when\
            the decorator is applied directly, or the decorator itself\
            when used with parentheses.
    """
    tags = [
        TagInfo(TagType.ON_STATUS_CHANGE, target, priority, log, description)
        for target in test_status_to_list(change_to)
        ]
    return TagDecorator.new(method, tags=tags)
