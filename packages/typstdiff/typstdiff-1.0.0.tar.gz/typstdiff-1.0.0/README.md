# TypstDiff
### Dominika Ferfecka, Sara Fojt, Małgorzata Kozłowska

## Introduction
Tool created with Pandoc to compare two typst files. It marks things
deleted from first file and marks differently things added to the second file.

## Run documentation
All information about tool, its working process and how to use it is located
in documentation written in mkdocs. To run documentation server use command
`mkdocs serve` 
in the folder `documentation`.
If mkdocs is not installed use command `pip install mkdocs` or run virtual environment
`poetry shell` and install all dependencies with `poetry install` (poetry can be installed
with `pip install poetry`)

### Issues
As both tools - Pandoc and Typst are new and still developing there is no full support
for typst in Pandoc. Because of that it is not possible to notice all changes made
in files, but tool will be developed.