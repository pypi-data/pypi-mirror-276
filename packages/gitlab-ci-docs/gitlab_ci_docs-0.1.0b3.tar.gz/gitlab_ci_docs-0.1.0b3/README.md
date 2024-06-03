## Motivation
Let's assume the design when we want to trigger a pipeline from web UI or by an API call. The pipeline consumes variables as input. It would be very helpful to know the type of a variable or its valid options. This kind of information is usually part of the documentation. This package provides functionality to automate the creation of this documentation.

<img alt="Generated table example" src="doc/table_sample.PNG">

## Overview
The output of this script is simple description (documentation) of *workflow* section. It parses workflow section and inserts it to readme file. Currently, output documentation is only as html table.
<br>Properties of variables are defined in comment using the format described in following section.

### Variable definition
As mentioned before, we write all parameters of a variable to a comment. Format of a comment is very simple.
1. **first part** describes if variable is required on input. By default a variable is considered as optional. To "set" is as required, put *required* to the comment - *# required*
1. **second part** descibes variable's type or valid options.
    - **type** - starts with colon. Typename can be whatever made up. *:type*
    - **choices** - dev|test

These parts are separated by space. Type and choices must not by combined.

#### Example
```yaml
ENV: dev  # required dev|test|prod
ACCOUNT_ALIAS: null  # required :str
IMAGE_TAG: 0.1.0  # :version
```

### Pipeline name
Using of the pipeline name improves readability of pipeline runs and also describes the task executed by the pipeline.

Variable **PIPELINE_NAME** is showed in the separated column of the table.

## Usage
The tool can be used from command line or imported as module in a code. Output is written to the readme file.

### Insert to the Readme
By default, the script inserts generated table in the beggining of the file. However, it is possible to mark position in the file where the table will be inserted. The mark token is <br>*\<!--PIPELINE_DOCS-->*

If token is present, the table is insreted below it.

### Command line
The package  **gitlabcidocs** consumes following arguments:
<ul>
    <li><b>--ci-file</b> <i>[optional]</i></li>
    <ul style="list-style-type:none;">
        <li>Path to the file containing workflow section.</li>
        <li>Default value is <i>.gitlab-ci.yml</i></li>
    </ul>
</ul>
<ul>
    <li><b>--doc-file</b> <i>[optional]</i></li>
    <ul style="list-style-type:none;">
        <li>Path to the output file.</li>
        <li>Default value is <i>README.md</i></li>
    </ul>
</ul>
<ul>
    <li><b>--include-all-rules, -a</b> <i>[optional]</i></li>
    <ul style="list-style-type:none;">
        <li>If set to *true*, all rules in the workflow section are included. Otherwise only rules which includes $CI_PIPELINE_SOURCE==web|api|pipeline in the if statement are documented.</li>
        <li>Default is <i>true</i></li>
    </ul>
</ul>
<ul>
    <li><b>--include-global-vars, -g</b> <i>[optional]</i></li>
    <ul style="list-style-type:none;">
        <li>If set, global variables section is included.</li>
        <li>Default value is <i>false</i></li>
    </ul>
</ul>

```bash
python -m gitlabcidocs --ci-file my_workflow.yml --doc-file myREADME.md
```

### Import in code
The module *gitlab-ci-docs* contains *create_docs* function. The functions consumes the same arguments as cli tool, but there are no default values set.
```python
import gitlabcidocs


def run_create_docs():
    docs = gitlabcidocs.create_docs(
        ci_file_path='my_workflow.yml',
        docs_file_path='README.md'
    )
```