from __future__ import annotations
from typing import List, Dict
from pipelineparser.variable import Variable


class GlobalVariables:

    def __init__(self, variables: Dict[str, str|int|None|bool]):
        self._variables = [
            Variable(
                name=key,
                value=variables[key],
                comment=c[2].value if (c := variables.ca.items.get(key, None)) else ''
            ) for key in variables
        ]

    @property
    def variables(self) -> List[Variable]:
        return self._variables
