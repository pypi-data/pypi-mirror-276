from typing import List, Dict
from pipelineparser import Workflow, Rule, Variable


class HTMLBuilder:

    def __init__(self, workflow: Workflow):
        self._show_pipelinename_column = False
        headers = ['Trigger', 'Variable', 'Default value', 'Required', 'Type', 'Choices']
        if workflow.pipeline_name_in_rules:
            headers.insert(0, 'Pipeline name')
            self._show_pipelinename_column = True
        self._docs = self.table(headers, workflow.rules)

    @property
    def docs(self) -> str:
        return self._docs

    def get_variable_cells(self, variable: Variable, is_mutable: bool) -> List[Dict[str, str]]:
        cells = [
            {'value': variable.name},
            {'value': variable.value}
        ]
        if is_mutable:
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

    def create_rule_rows(self, rule: Rule) -> str:
        rowspan = len(rule.variables) if rule.variables else 1
        pipeline_name_cell = [{'value': rule.pipeline_name, 'rowspan': rowspan}] if self._show_pipelinename_column else []

        first_row = self.row(
            pipeline_name_cell
            + [{'value': self.get_trigger_cell(rule), 'rowspan': rowspan}]
            + (self.get_variable_cells(rule.variables[0], rule.is_mutable) if rule.variables else [])
        )
        other_rows = '\n'.join([self.row(self.get_variable_cells(v, rule.is_mutable)) for v in rule.variables[1:]])

        return first_row + other_rows

    def table(self, headers: List[str], rules: List[Rule]) -> str:
        return '\n'.join([
            '<table>',
            self.headers(headers),
            '\n'.join([self.create_rule_rows(r) for r in rules]),
            '</table>'
        ])

    def headers(self, headers: List[str]) -> str:
        return f'<tr>{"".join([f"<th>{h}</th>" for h in headers])}</tr>'

    def row(self, data: List[Dict[str, str]]) -> str:
        return f'<tr>{"".join([self.cell(v["value"], v.get("rowspan", None)) for v in data])}</tr>'

    def cell(self, value: str, rowspan=None) -> str:
        rowspan = f' rowspan="{rowspan}"' if rowspan and rowspan > 1 else ''
        return f'<td{rowspan}>{value}</td>'
