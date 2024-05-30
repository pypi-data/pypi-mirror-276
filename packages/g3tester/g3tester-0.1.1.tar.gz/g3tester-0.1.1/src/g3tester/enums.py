import enum


class TestStatus(enum.StrEnum):
    """Test status enumeration."""
    UNKNOWN = enum.auto()
    """Test status is unknown."""
    PENDING = enum.auto()
    """Test is pending for execution."""
    QUEUED = enum.auto()
    """Test is queued for execution."""
    RUNNING = enum.auto()
    """Test is running."""
    PASSED_WITH_WARNING = enum.auto()
    """Test passed with warning."""
    PASSED = enum.auto()
    """Test passed."""
    FAILED = enum.auto()
    """Test failed."""
    TIMEOUT = enum.auto()
    """Test timed out."""
    ABORTED = enum.auto()
    """Test was aborted."""


class TestType(enum.StrEnum):
    """Test type enumeration."""
    OTHER = enum.auto()
    """Other test type."""
    SINGLETEST = enum.auto()
    """Single test."""
    MULTITEST = enum.auto()
    """Multitest."""
    MULTITEST_SEQUENTIAL = enum.auto()
    """Sequential multitest."""
    MULTITEST_PARALLEL = enum.auto()
    """Parallel multitest."""
