# Hawaii Climate
<p>This repository contains a Python project that implements a Flask API that retrieve climate information from Hawaii area that helps to perform climate analysis.
The current implementation implements the following objectives:
- USe Python and SQLAlchemy to perform basic climate analysis and data exploration of a climate database.
- Implement a Flask API to retrieve the climate observations and the daily normals for a give time range. 
## Data
[Hawaii Climate Data](https://github.com/aidinhass/surfpy/blob/master/surfpy/data/int/hawaii.sqlite)

## Report

## Requirements
- numpy 1.14.5
- pandas 0.23.1
- jupyter 1.0.0
- nb_conda 2.2.1
- matplotlib 2.2.2
- sqlalchemy 1.2.8 
 
## Directory Structure
```
.
├── docs                <- Documents related to this project.
├── images              <- Images for README.md files.
├── notebooks           <- Ipythoon Notebook files
├── reports             <- Generated analysis as HTML, PDF, Latex, etc.
│   ├── figures         <- Generated graphics and figures used in reporting.
│   └── logs            <- Generated log files.  
└── surfpy
    ├── conf
    ├── data            <- data utilized in this project.
    │   ├── ext
    │   ├── int
    │   └── raw
    ├── src             <- Source files used in this project.
    ├── static          <- CSS files.
    └── templates       <- Flask templates 
```
## Installation
Install python dependencies from  `requirements.txt` using conda.
```bash
conda install --yes --file requirements.txt
```

Or create a new conda environment `<new-env-name>` by importing a copy of a working conda environment at the project root directory :`surfpy.yml`.
```bash
conda env create --name <new-env-name> -f surfpy.yml
```
## Usage
```bash
python run.py

```
## References

## To Do

## License
MIT License 
