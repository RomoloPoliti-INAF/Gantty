# PyGantt
Build simple Gantt diagram from CSV file
## Usage

PyGantt [-h] [-i FILE] [-o FILE] [-t TITLE] [-x NUM] [-s] [-d]

### Optional arguments:
Option| Description
---|---
**-h**, **--help**|    show this help message and exit
**-i**, **--input** *FILE*|    The CSV input file. The default is gantt.csv
**-o**, **--output** *FILE*|   The PNG output file. The default is gantt.png
**-t**, **--title** *TITLE*|   Title of the plot
**-x**, **--xticks** *NUM*|  Set the x Thicks frequency to NUM. The default is every month (1)
**-s**, **--show**| Display the plot. No output will be saved
**-d**, **--display**|         Display the input data and the computed one and exit
