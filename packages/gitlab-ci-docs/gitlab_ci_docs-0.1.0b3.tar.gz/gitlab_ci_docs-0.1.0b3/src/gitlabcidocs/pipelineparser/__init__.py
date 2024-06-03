from ruamel.yaml import YAML
from pipelineparser.workflow import Workflow
from pipelineparser.globalvariables import GlobalVariables


class CiFileParser:

    def __init__(self, filepath: str):
        with open(filepath) as f:
            self._pipeline = YAML().load(f)

    def get_workflow(self, include_all_rules: bool) -> Workflow:
        return Workflow(self._pipeline['workflow'], include_all_rules)

    def get_global_variables(self) -> GlobalVariables:
        return GlobalVariables(self._pipeline.get('variables', {}))
