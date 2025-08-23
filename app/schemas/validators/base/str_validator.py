from typing import Any

from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema


class StrValidator(str):
    @classmethod
    def _validate(cls, value: Any) -> str:
        raise NotImplementedError('You must implement _validate method')

    @classmethod
    def __get_pydantic_core_schema__(  # noqa: PLW3201
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ):
        return core_schema.no_info_after_validator_function(
            cls._validate, core_schema.str_schema()
        )
