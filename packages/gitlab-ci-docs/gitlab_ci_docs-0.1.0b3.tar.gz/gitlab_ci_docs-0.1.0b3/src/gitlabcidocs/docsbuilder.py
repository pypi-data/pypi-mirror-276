from typing import List, Dict
from pipelineparser.workflow import Workflow
from pipelineparser.rule import Rule
from pipelineparser.variable import Variable
from pipelineparser.globalvariables import GlobalVariables


class HTMLBuilder:

    def get_workflow_table(self, workflow: Workflow) -> str:
        headers = ['Trigger', 'Variable', 'Default value', 'Required', 'Type', 'Choices']
        if workflow.pipeline_name_in_rules:
            headers.insert(0, 'Pipeline name')

        return '\n'.join([
            '<b>Pipeline worflow</b>',
            '<table>',
            self.headers(*headers),
            '\n'.join([self.create_rule_rows(r, workflow.pipeline_name_in_rules) for r in workflow.rules]),
            '</table>'
        ])

    def get_global_vars_table(self, globalvars: GlobalVariables) -> str:
        return '\n'.join([
            '<b>Global variables</b>',
            '<table>',
            self.headers('Name', 'Value', 'Required', 'Type', 'Choices'),
            '\n'.join([self.row(self.get_variable_cells(v)) for v in globalvars.variables]),
            '</table>'
        ])

    def get_variable_cells(self, variable: Variable) -> List[Dict[str, str]]:
        cells = [
            {'value': variable.name},
            {'value': variable.value}
        ]
        if not variable.is_const and variable.is_described:
            cells += [
                {'value': variable.required_str},
                {'value': variable.typename if variable.typename else '-'},
                {'value': variable.choices_str if variable.choices_str else '-'}
            ]
        return cells

    def get_trigger_cell(self, rule: Rule) -> str:
        return '<br>'.join([i for i in [
            f'<b>if:</b> {rule.condition}' if rule.condition else '',
            f'<b>when:</b> {rule.when}' if rule.when else ''
        ] if i])

    def create_rule_rows(self, rule: Rule, pipelinename_column: bool) -> str:
        rowspan = len(rule.variables) if rule.variables else 1
        pipeline_name_cell = [{'value': rule.pipeline_name, 'rowspan': rowspan}] if pipelinename_column else []

        first_row = self.row(
            pipeline_name_cell
            + [{'value': self.get_trigger_cell(rule), 'rowspan': rowspan}]
            + (self.get_variable_cells(rule.variables[0]) if rule.variables else [])
        )
        other_rows = '\n'.join([self.row(self.get_variable_cells(v)) for v in rule.variables[1:]])

        return first_row + other_rows

    def headers(self, *headers: List[str]) -> str:
        return f'<tr>{"".join([f"<th>{h}</th>" for h in headers])}</tr>'

    def row(self, data: List[Dict[str, str]]) -> str:
        return f'<tr>{"".join([self.cell(v["value"], v.get("rowspan", None)) for v in data])}</tr>'

    def cell(self, value: str, rowspan=None) -> str:
        rowspan = f' rowspan="{rowspan}"' if rowspan and rowspan > 1 else ''
        return f'<td{rowspan}>{value}</td>'
