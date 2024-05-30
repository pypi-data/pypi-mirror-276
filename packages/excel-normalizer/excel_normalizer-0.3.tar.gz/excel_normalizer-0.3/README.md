# excel_normalizer
A CLI tool to force an entire Excel spreadsheet, CSV, or tab-delimited TXT file to be treated as text. I was getting extremely annoyed at Excel for automattically formatting large numbers into scientific notation with no way to disable the behavior. I made a python script to treat the whole file as text, fueled by spite and rage. I decided a CLI would be more convenient for myself, and if I'm going that far I might as well publish it. So here ya go. 

## Install
```
pip install excel_normalizer
```

## Usage
```
normalize /path/to/file.csv
```
A new Excel (.xlsx) file will be saved in the same directory as the source file with the source file name appended with "_NORMALIZED."
I may or may not add the option to specify an output filename and location. Or you can, I don't really care. MIT licsense, do what you want. 

## Supported File Types
.xlsx
.csv
.txt (tab-delimited)

