# Mini-assignment autograder

Version 0.1.0

An autograder for small python assignments

Author: Meaghan Fowlie

## Quick Start

First time, where `project_path` is one of `favourite_number`, `alice`, `nth`, and `module_script`

```commandline
python check_script.py -p project_path -z path_to_zip_file_of_raw_submissions -s path_to_spreadsheet_from_blackboard 
```

If you need to rerun it, just use `-p` and `-s`

```commandline
python check_script.py -p project_path -s path_to_spreadsheet_from_blackboard 
```

If you're testing it out and don't want to write to the spreadsheet yet, just use `-p`


## Under construction warning

These ones work:

* alice
* favourite_number   
* module_script
* nth

These aren't updated yet:

* categories
* every_nth_word (is this just nth?)
* id_printer (maybe this is obsolete?)
* tags
* pickling (is this tags?)


## Project organization

```
Legend:
PG: Project Generated
RO: Read Only
HW: Human Written

.
├── .gitignore
├── CITATION.md
├── LICENSE.md
├── README.md
├── requirements.txt
├── bin                <- Compiled and external code, ignored by git (PG)
│   └── external       <- Any external source code, ignored by git (RO)
├── config             <- Configuration files (HW)
├── data               <- All project data, ignored by git
│   ├── processed      <- The final, canonical data sets for modeling. (PG)
│   ├── raw            <- The original, immutable data dump. (RO)
│   └── temp           <- Intermediate data that has been transformed. (PG)
├── docs               <- Documentation notebook for users (HW)
│   ├── manuscript     <- Manuscript source, e.g., LaTeX, Markdown, etc. (HW)
│        └── reports        <- Other project reports and notebooks (e.g. Jupyter, .Rmd) (HW)
├── results
│   ├── figures        <- Figures for the manuscript or reports (PG)
│       └── output         <- Other output for the manuscript or reports (PG)
└── autograder             <- Source code for this project (HW)

```


## License

This project is licensed under the terms of the [MIT License](./LICENSE.md)

## Citation

Please [cite this project as described here](./CITATION.md).
