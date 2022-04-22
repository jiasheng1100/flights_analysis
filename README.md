# flights_analysis

## Table of contents
* [General info](#general-info)
* [Technology](#technologies)
* [Instruction](#instruction)
* [Sample program calls](#Sample-program-calls)

## General info
THis program allows users to run simple, pre-defined statistical analyses of a data set containing information on flights through the command line.
	
## Technology
Program is created with:
* Python 3.7.3 
	
## Description
The program accepts three mandatory arguments in the following order:\
statistic: ```min``` (minimal value), ```max``` (maximal value), ```avg``` (average) and ```sum```.\
variable: ```distance``` (flight distance in miles) and ```delay``` (arrival delay in minutes).\
file: the filename or filepath that contains the data set.\
\
Besides, it is able to filter the data set before performing the computations by the following optional arguments:\
```--carriers``` (one or more airline carrier codes from column 'OP_CARRIER')\
```--from-airport``` (a departure airport from column 'ORIGIN')\
```--to-airport``` (a destination airport from column 'DEST')\
```--from-date``` (an earliest scheduled departure date in format 'YYYY-MM-DD' or 'DD.MM.YYYY')\
```--to-date``` (a latest scheduled depature date, in format 'YYYY-MM-DD' or 'DD.MM.YYYY')\

## Sample program calls
```
python3 flights.py --carriers AA --to-airport LAX avg delay flights.tsv
9.7
```

```
python3 flights.py --to-airport RST --from-date 2019-01-09 --to-date 2019-01-10 min distance flights.tsv
76
```

Lastly modified on September 13, 2021\
Jia Sheng