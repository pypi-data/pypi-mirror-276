## Overview

The CI/CD solution by gitlba is great, however it has some limitations. The way how a pipeline is defined is definitelly one of thme. There's nothing woring about YAML itself, but gitlab pipeline is so complex to be written in a markup language.

For instance, let's assume there is the design where we want to trigger a pipeline from web UI or by API call. The pipeline consumes variables as input. There is no way how to define variable's type, options or if it's required or if it shouldn't be overriden. This sort of information is always part of a documentation. This package provides functionality to create simple documentation of *workflow* section, which can contain all of these infromation.

In my opinion, the *workflow* section should be part of every clean/nice pipeline definition ("code").
Let's define the naming convention, which covers some scenarios, and all other information write to comment. I know, comments sound awful, but it is the most safe way to achieve what we need.

## How does it work
The output of this script is simple description (documentation) of *workflow* section. It parses workflow section and inserts it to readme file. Currently, output documentation is only as html table.

### Readme file
By default, the script inserts generated table in the beggining of the file. However, it is possible to mark position in the file where the table will be inserted. The mark token is *\<!--PIPELINE_DOCS-->*

If token is present, the table is insreted below it.

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

## Usage
The tool can be used from command line or imported as module in a code. It requires only two parameters on input:
- path to yaml file containing thw *workflow* section
- path to documentation file where generated table is inserted to

### Command line
The packegs is called **gitlabcidocs** and consumes following arguments:
- **--ci-file [**_optional_**]**
<br>Path to the file containing workflow section.
<br>Default value is *.gitlab-ci.yml*
- **--doc-file [**_optional_**]**
<br>Path to the output file.
<br>Default value is *README.md*

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