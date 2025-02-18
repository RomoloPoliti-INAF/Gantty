# Gantty
Build simple Gantt diagram from CSV file

Based on Thiago Carvalho's [article](https://towardsdatascience.com/gantt-charts-with-pythons-matplotlib-395b7af72d72) 

## Install
You can install the software by pip:

```bash
python3 -m pip install gantty
```


## Usage

gantty [OPTIONS]

### Optional arguments:
Option| Description
---|---
**--input**, **-i**  *<FILE\>*| The CSV input file. The default is gantt.csv
**--output**, **-o** *<FILE\>*| The PNG output file. The default is gantt.png
**-t**, **--title** *<TITLE\>*| Title of the plot. To include more than word, please, use the quetemarks
**--xticks**, **-x** *<NUM\>* | Set the x Thicks frequency to NUM. The default is every month (1)
**--show**, **-s**            | Print the input data and the computed one and exit
**--display**, **-d**,        | Show the plot on an interactive window. No output will be saved
**--no-sessions**, **-n**     | Do not change the background for different session.
**-h**, **--help**            | Show this help message and exit


### Example
Create a Gantt diamgram using the data in the file *time.csv* and save it in the file *doc/example.png*
```bash
$ gantty -i time.csv -o doc/example.png
```
The result is:
![Example Gantt Diagram](doc/example.png)
