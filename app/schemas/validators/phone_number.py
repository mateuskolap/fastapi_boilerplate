import re
from typing import Any

from phonenumbers import (
    PhoneNumberFormat,
    format_number,
    is_possible_number,
    is_valid_number,
    parse,
)
from phonenumbers.phonenumberutil import NumberParseException

from app.schemas.validators.base.str_validator import StrValidator
from app.settings import settings


class PhoneNumberStr(StrValidator):
    @classmethod
    def _validate(cls, value: Any) -> str:
        if not isinstance(value, str):
            raise TypeError('string required')

        phone_number = re.sub(r'[^\d+]', '', value)
        parsed_phone_number = parse(phone_number, settings.LOCAL)

        try:
            if not is_possible_number(parsed_phone_number):
                raise ValueError('Incorrect phone number')
            if not is_valid_number(parsed_phone_number):
                raise ValueError('Invalid phone number')
        except NumberParseException as e:
            raise ValueError(f'Invalid phone number: {e}')

        return format_number(parsed_phone_number, PhoneNumberFormat.E164)
