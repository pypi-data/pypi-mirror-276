import re
from typing import List
from errors import VariableCommentFormatError


class Variable:

    _regex_value_regex = '[a-zA-Z0-9-_\.]'
    _regex_group_req = '(?P<required>required\s?)?'
    _regex_group_type = '(?P<type>:[a-zA-Z]+)?'
    _regex_group_opt = property(lambda s: f'(?P<options>{s._regex_value_regex}+(\|{s._regex_value_regex}+)*)?')
    _regex = property(lambda s: f'^#\s*{s._regex_group_req}{s._regex_group_type}{s._regex_group_opt}$')

    def __init__(self, name: str, value: str, comment: str, const: bool = False):
        self._name = name
        self._value = value
        self._required = False
        self._choices = []
        self._typename = ''
        self._is_const = const
        self._is_described = False

        if (comment := comment.strip()) and comment != '#':
            if (matched := re.fullmatch(self._regex, comment)) is None:
                raise VariableCommentFormatError(f'Variable comment ({comment}) has invalid format. Valid format: {self._regex}')
            if matched['options'] and matched['type']:
                raise VariableCommentFormatError(f'Variable comment ({comment}) has invalid format. Valid format: {self._regex}')

            self._is_described = True
            self._required = bool(matched['required'])
            self._choices = list(set(matched['options'].split('|'))) if matched['options'] else []
            self._typename = matched['type'][1:] if matched['type'] else None

    @property
    def name(self) -> str:
        return self._name

    @property
    def key(self) -> str:
        return self._name

    @property
    def value(self) -> str:
        return self._value

    @property
    def required(self) -> bool:
        return self._required

    @property
    def required_str(self) -> str:
        return 'Yes' if self._required else 'No'

    @property
    def optional(self) -> bool:
        return not self._required

    @property
    def choices(self) -> List[str]:
        return self._choices

    @property
    def choices_str(self) -> str:
        return ', '.join(self._choices) if self._choices else ''

    @property
    def typename(self) -> str:
        return self._typename

    @property
    def is_const(self) -> bool:
        return self._is_const or self.name.startswith('_')

    @property
    def is_described(self) -> bool:
        return self._is_described
