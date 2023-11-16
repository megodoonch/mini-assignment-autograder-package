# Mini-assignment autograder

Version 0.1.0

An autograder for small python assignments

Author: Meaghan Fowlie

## Quickstart

To get started, install this repo as a Python package. A sample assignment is provided. 

```bash
pip install path/to/mini-assignment-autograder-package/directory
```

Copy the script `check_script.py` into the parent folder of your assignments.

Create an assignment as a folder of your main homework folder. An example is provided: `favourite_number`.

## Running autograder

Run the autograder from the command line by running `check_script.py`. Use `-h` for help.

```bash
python check_script.py -h
```

```
usage: check_script.py [-h] -p PROJECT [-s SPREADSHEET] [-z ZIP] [-e EXTRA_FILES]

options:
  -h, --help            show this help message and exit
  -p PROJECT, --project PROJECT
                        local path to assignment folder (e.g. digital_tools_1)
  -s SPREADSHEET, --spreadsheet SPREADSHEET
                        absolute path to downloaded BB spreadsheet for marks
  -z ZIP, --zip ZIP     path to zip file of submissions
  -e EXTRA_FILES, --extra-file EXTRA_FILES
                        path to extra file to copy into the working directory (use more than once if needed)
```

`--project` is for the name of the directory where the particular homework lives. Submissions will be unzipped into a subfolder of the project called `submissions`.
Marks will be saved in `marks.csv`, which should be uploadable to Blackboard.

You can update a couple of local variables in `check_script.py` such as where you want it to copy the output spreadsheet to, if you want them to end up somewhere else.



### Running the autograder on an assignment




This is meant to be a package to provide the groundwork. The actual assignments are made separately.

## Licence
Licensed under GNU GENERAL PUBLIC LICENSE,  Version 3

## Citation

Please [cite this project as described here](./CITATION.md).
