import argparse
import sys
import datetime

# Parse arguments. DO NOT MODIFY THESE LINES!
parser = argparse.ArgumentParser()
parser.add_argument("statistic", choices=["sum", "avg", "min", "max"], help="Which measure do you want to compute")
parser.add_argument("variable", choices=["distance", "delay"], help="Which variable should be used for the calculation")
parser.add_argument("tsvfile", help="Name/path of TSV file containing data set")
parser.add_argument("--carriers", dest="carriers", help="Comma-separated list of airline codes to be used for the calculation")
parser.add_argument("--from-date", dest="from_date", help="The earliest date to be used for calculation")
parser.add_argument("--to-date", dest="to_date", help="The latest date to be used for calculation")
parser.add_argument("--from-airport", dest="from_airport", help="Departure airport for flights to be used for calculation")
parser.add_argument("--to-airport", dest="to_airport", help="Arrival airport for flights to be used for calculation")
args = parser.parse_args()



# import the data frame
import pandas as pd
try:
    data = pd.read_csv(args.tsvfile, sep = "\t", header = 0)
#print the error message when file does not exist
except FileNotFoundError:
    print("ERROR_INVALID_FILE")
    quit()



#apply optional arguments to filter data
#define the functions to apply to the arguments
def arg_check(data, col, arg, err):
    """a function to check whether a given argument can be found in
    the corresponding collumn of a dataframe, and prints out an error
    message if not."""
    if not data[col].str.contains(arg).any():
        sys.exit(err)

def data_filter(data, col, arg):
    """a function that filters the data frame and only keeps the rows
    that contains the given arguments"""
    data = data[data[col]==arg]
    return data

if args.carriers:
    #check whether one or more values are passed to this argument
    if "," in args.carriers:
        #if it contains more values, convert it to a list
        arg_list = args.carriers.split(",")
        data_list = list()
        for carrier in arg_list:
            arg_check(data, "OP_CARRIER", str(carrier), "ERROR_INVALID_CARRIER")
            data_list.append(data_filter(data, "OP_CARRIER", str(carrier)))
        data = pd.concat(data_list)
    else:
        arg_check(data, "OP_CARRIER", args.carriers, "ERROR_INVALID_CARRIER")
        data = data_filter(data, "OP_CARRIER", args.carriers)

#check which arguments are given and apply the functions to them
if args.from_airport:
    arg_check(data, "ORIGIN", args.from_airport, "ERROR_INVALID_AIRPORT")
    data = data_filter(data, "ORIGIN", args.from_airport)

if args.to_airport:
    arg_check(data, "DEST", args.to_airport, "ERROR_INVALID_AIRPORT")
    data = data_filter(data, "DEST", args.to_airport)

#define the function to deal with dates in the argument
def date_check(date):
    """a function to convert the given string to datetime, or prints out
    an error message if the given string is not in the right date format
    ("%Y-%m-%d" or "%d.%m.%Y")"""
    try:
        date = datetime.datetime.strptime(date, "%Y-%m-%d")
        return date
    except ValueError:
        try:
            date = datetime.datetime.strptime(date, "%d.%m.%Y")
            return date
        except ValueError:
            sys.exit("ERROR_INVALID_DATE")

#convert the corresponding column in the dataframe to datetime to
#enable the comparison with the given date
data["FL_DATE"] = pd.to_datetime(data["FL_DATE"])

if args.from_date:
    start_date = date_check(args.from_date)
    data = data[data["FL_DATE"]>=start_date]
    

if args.to_date:
    end_date = date_check(args.to_date)
    data = data[data["FL_DATE"]<=end_date]

#Finally, check whether there are flights that match the given criteria
#and print out an error message if not
if len(data) == 0:
        print("NO_MATCHING_FLIGHTS")
        quit()
    


#define the variables and calculations based on the mandatory arguments

#variables
v = args.variable

#define the function that counts negative values in arrival delays as zero
def modify_delay(x):
    """a function that equals the given value to zero when it is less than zero """
    if x < 0:
        x = 0
    return x

if v == "distance":
    x = data["DISTANCE"]

if v == "delay":
    #calculate the arrival delay in minutes
    data["DELAY"] = data["ACTUAL_ELAPSED_TIME"] - data["CRS_ELAPSED_TIME"] + data["DEP_DELAY"]
    #apply the function to transform negative values
    data["DELAY"] = data["DELAY"].apply(modify_delay)
    x = data["DELAY"]

#calculation methods
s = args.statistic

if s == "sum":
    print(int(x.sum()))

if s == "avg":
    if v == "distance":
        #round the output to an integer
        print(int(round(x.mean())))
    if v == "delay":
        #round the output to a float with one decimal point
        print("{:.1f}".format(x.mean()))

if s == "min":
    print(int(x.min()))

if s == "max":
    print(int(x.max()))