from __future__ import annotations
from pathlib import Path
from typing import List
import pipelineparser
import docsbuilder


def read_doc_file(file_path: str|Path) -> List[str]:
    with open(file_path, 'r') as f:
        return [line for line in f]


def write_doc_file(file_path: str|Path, data: str) -> None:
    with open(file_path, 'w') as f:
        f.write(data)


def insert_to_doc_file(docs: str, doc_file_path: str|Path) -> None:
    docs_token = '<!--PIPELINE_DOCS-->'

    begin_docs_line_idx = None
    end_docs_line_idx = None

    out_lines = read_doc_file(doc_file_path)

    for i in range(len(out_lines)):
        if docs_token in out_lines[i]:
            if begin_docs_line_idx is None:
                begin_docs_line_idx = i
            else:
                end_docs_line_idx = i

    if begin_docs_line_idx is None:
        out_lines.insert(0, f'{docs_token}\n{docs}\n{docs_token}\n\n')
    elif end_docs_line_idx is None:
        out_lines.insert(begin_docs_line_idx+1, f'{docs}\n{docs_token}\n\n')
    else:
        out_lines = out_lines[:begin_docs_line_idx+1] + [docs+'\n'] + out_lines[end_docs_line_idx:]

    write_doc_file(doc_file_path, ''.join(out_lines))


def create_docs(ci_file_path: str|Path, doc_file_path: str|Path, include_all_rules: bool) -> str:
    workflow = pipelineparser.CiFileParser(ci_file_path).get_workflow(include_all_rules)
    docs = docsbuilder.HTMLBuilder(workflow).docs
    insert_to_doc_file(docs, doc_file_path)
    return docs



