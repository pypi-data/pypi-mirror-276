from typing import Dict, List
from pipelineparser.rule import Rule


class Workflow:

    def __init__(self, workflow: Dict, include_all_rules: bool):
        self._pipeline_name = workflow.get('name', '')
        self._rules = [rule for rule in [Rule(r) for r in workflow['rules']] if include_all_rules or rule.has_mutable_vars]

    @property
    def rules(self) -> List[Rule]:
        return self._rules

    @property
    def pipeline_name(self) -> str:
        return self._pipeline_name

    @property
    def pipeline_name_in_rules(self):
        return any(r.pipeline_name for r in self.rules)
