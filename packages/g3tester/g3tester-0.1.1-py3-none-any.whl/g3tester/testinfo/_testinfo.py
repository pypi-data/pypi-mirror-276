from __future__ import annotations

from datetime import datetime
from typing import Self
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from .._test import TestABC, MultiTestABC, TestType, TestStatus


class TestInfoABC(BaseModel):
    """
    Test info model ABC.
    """
    model_config = ConfigDict(
        alias_generator=lambda s: to_camel(s.rstrip('_')),
        populate_by_name=True,
        validate_assignment=True,
        validate_default=True
        )


class TestInfo(TestInfoABC):
    """
    Test info model.
    """
    id_: int
    name: str
    type_: TestType
    status: TestStatus
    started_at: datetime | None
    finished_at: datetime | None
    duration_sec: float

    @classmethod
    def model_validate_test(cls, test: TestABC) -> Self:
        return cls.model_validate(
            {
                'id_': id(test),
                'name': test.name,
                'type_': test.type,
                'status': test.status,
                'started_at': test.started_at,
                'finished_at': test.finished_at,
                'duration_sec': test.duration_sec
            }
        )


class MultiTestInfo(TestInfoABC):
    """
    Multitest info model.
    """
    id_: int
    name: str
    type_: TestType
    status: TestStatus
    started_at: datetime | None
    finished_at: datetime | None
    duration_sec: float
    tests: list[TestInfo | MultiTestInfo]

    @classmethod
    def model_validate_test(cls, test: MultiTestABC) -> Self:
        return cls.model_validate(
            {
                'id_': id(test),
                'name': test.name,
                'type_': test.type,
                'status': test.status,
                'started_at': test.started_at,
                'finished_at': test.finished_at,
                'duration_sec': test.duration_sec,
                'tests': [
                    MultiTestInfo.model_validate_test(t)
                    if isinstance(t, MultiTestABC) else
                    TestInfo.model_validate_test(t)
                    for t in test
                ]
            }
        )
