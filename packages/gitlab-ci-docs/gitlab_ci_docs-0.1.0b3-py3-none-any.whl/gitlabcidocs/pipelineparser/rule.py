import re
from typing import List, Dict
from pipelineparser.variable import Variable


class Rule:

    _regex_pipeline_source = '\$CI_PIPELINE_SOURCE\s==\s[\'"]?(web|pipeline|api|trigger)[\'"]?'

    def __init__(self, rule: Dict):
        self._pipeline_name = ''
        self._condition = rule.get('if', '')
        self._when = rule.get('when', None)
        self._variables = [
            Variable(
                name=key,
                value=rule['variables'][key],
                comment=c[2].value if (c := rule['variables'].ca.items.get(key, None)) else '',
                const=not self.has_mutable_vars
            ) for key in rule.get('variables', {}) if key != 'PIPELINE_NAME'
        ]
        self._pipeline_name = rule.get('variables', {}).get('PIPELINE_NAME', '')

    @property
    def has_mutable_vars(self) -> bool:
        return bool(re.search(self._regex_pipeline_source, self.condition))

    @property
    def condition(self) -> str:
        return self._condition

    @property
    def when(self):
        return self._when

    @property
    def variables(self) -> List[Variable]:
        return self._variables

    @property
    def pipeline_name(self) -> str:
        return self._pipeline_name
