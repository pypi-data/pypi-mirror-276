import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import argparse
import docsgen


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ci-file', default='.gitlab-ci.yml', help='Path to gitlab-ci.yml')
    parser.add_argument('--doc-file', default='README.md', help='Path to the file in the docs are injected to')
    parser.add_argument('--include-all-rules', '-a', action='store_true', help='If set, include all workflow rules. Otherwise only rules with $CI_PIPELINE_SOURCE=web|pipeline|api are included')
    parser.add_argument('--include-global-vars', '-g', action='store_true', help='If set, global variables section is included')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    docsgen.create_docs(
        args.ci_file, args.doc_file, args.include_all_rules, args.include_global_vars
    )
