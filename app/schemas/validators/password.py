from app.schemas.validators.base.str_validator import StrValidator

SPECIAL_CHARS: set[str] = {
    '@',
    '#',
    '%',
    '!',
    '&',
    '*',
    '(',
    ')',
    '_',
    '+',
    '=',
    '{',
    '}',
    '[',
    ']',
    '.',
}


MIN_LENGTH: int = 8
MAX_LENGTH: int = 20
INCLUDES_SPECIAL_CHARS: bool = True
INCLUDES_NUMBERS: bool = True
INCLUDES_LOWERCASE: bool = True
INCLUDES_UPPERCASE: bool = True


class PasswordStr(StrValidator):
    @classmethod
    def _validate(cls, value: str) -> str:
        if not MIN_LENGTH <= len(value) <= MAX_LENGTH:
            raise ValueError(
                f'Password length should be at least {MIN_LENGTH} and at most {MAX_LENGTH} characters'
            )  # noqa: E501

        has_upper = has_lower = has_digit = has_special = False

        for char in value:
            if char.isupper():
                has_upper = True
            elif char.islower():
                has_lower = True
            elif char.isdigit():
                has_digit = True
            elif char in SPECIAL_CHARS:
                has_special = True

        if INCLUDES_NUMBERS and not has_digit:
            raise ValueError('Password should have at least one numeral')
        if INCLUDES_UPPERCASE and not has_upper:
            raise ValueError('Password should have at least one uppercase letter')
        if INCLUDES_LOWERCASE and not has_lower:
            raise ValueError('Password should have at least one lowercase letter')
        if INCLUDES_SPECIAL_CHARS and not has_special:
            raise ValueError(
                f'Password should have at least one symbol: {"".join(SPECIAL_CHARS)}'
            )

        return value
