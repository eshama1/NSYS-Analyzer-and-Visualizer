# NSYS Analyzer & Visualizer (NAV)

These scripts are designed to extract and generate tables and figures from an NSYS Trace database (*sqlite*). 
These scripts also have the ability to create comparative tables and figures when more than one database or *NAV* formatted json file are provided.

NOTE these scripts extract the raw data from the *sqlite* files which means the duration of extraction is relative to the size and frequency of the metrics.
For ~1GB files expect a few minutes, for ~100GB expect a few hours. 

## Requirements

### Required Trace Flags 
 ```bash
 nsys profile --trace=cuda,mpi,ucx,nvtx 
 ```

Extracting *sqlite* file from *nsys-rep* file. Alternative: If you open the nsys-rep file in NSight GUI it may generate *sqlite* file.
```bash
nsys export --type sqlite <nsys.rep file>
```

### Required Python Library's 
Please ensure that local python ENV has all the required library's 
```python
pip install absl_py contourpy cycler fonttools joblib kiwisolver matplotlib numpy packaging pillow pyparsing python_dateutil scikit_learn scipy six sklearn threadpoolctl
```

## Script Usage

### Generating *NAV* *json* file
Extracting data from *.sqlite* and create tables and figures
```python
python3 main.py -df file.sqlite
```
Extracting data from *.sqlite* without creating tables and figures (This method is useful when you want to extract data from many files first that create tables and figures after)
```python
python3 main.py -df file.sqlite -nmo
```
Extracting data from multiple *.sqlite* and create tables and figures sequentially (NOT RECOMMENDED!! VERY SLOW)
```python
python3 main.py -df "file1.sqlite file2.sqlite file3.sqlite" -mdl "Label1,Label2,Label3"
```
### Recommend method to create NAV *json* files from multiple *sqlite* files
Extracting data from multiple *.sqlite* without create tables and figures
```python
# Run in seperate Nodes or Jobs in parallel
python3 main.py -df "file1.sqlite" -nmo
python3 main.py -df "file2.sqlite" -nmo
python3 main.py -df "file3.sqlite" -nmo
```
### Generating Tables and Figures from *NAV json* file(s)
Create tables and figures from *NAV json*
```python
python3 main.py -jf file.json
```
Create tables and figures from multiple *NAV json* with comparison tables and figures
```python
python3 main.py -jf "file1.json file2.json file3.json" -mdl "Label1,Label2,Label3"
```

## Flags Overview

### General Flags
- **output_dir** (`-o`): Name of directory to save generated NAV files and export Tables and Figures (default: ./output)
- **multi_data_label** (`-mdl`): *(REQUIRED for multi-files)* Labels for each database/JSON file provided to distinguish in statistics. Example: (1 GPU, 2 GPU, 3 GPU). Use commas to split names, and ensure the order matches the provided files.
- **max_workers** (`-mw`): Specifies the number of threads to split work (Defaults to CPU count if not set).

### Extraction Flags
- **data_file** (`-df`): Specifies the database file for extraction (sqlite).
- **json_file** (`-jf`): Specifies the JSON file containing extracted statistics.
- **no_kernel_metrics** (`-nkm`): If set, kernel metrics will not be exported.
- **no_transfer_metrics** (`-ntm`): If set, transfer metrics will not be exported.
- **no_communication_metrics** (`-ncm`): If set, communication metrics will not be exported.
- **no_save_data** (`-nsd`): If set, metrics will not be saved to a *NAV json* file.

### Graphics and Table Flags
- **no_metrics_output** (`-nmo`): If set, disables metrics export after extraction.
- **no_compare_metrics_output** (`-ncmo`): If set, disables comparison metrics export (applicable for multi-file only).
- **no_general_metrics_output** (`-ngmo`): If set, disables general metrics export (Kernel, Transfer, Communication).
- **no_specific_metrics_output** (`-nsmo`): If set, disables specific metrics export (Duration, Size, Slack, Overhead, etc).
- **no_individual_metrics_output** (`-nimo`): If set, disables individual metrics export (individual kernel, transfer, communication statistics).
