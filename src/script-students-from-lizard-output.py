from operator import methodcaller
import os
import csv
import subprocess
import re


# absolute path to input  CSV, för repoes to be analyzed
input = "../data/inda-data-test-by-ta.csv"
output = "../data/inda-data-test-by-ta-sorted.csv"
#command = "lizard -o lizard_analytics.numbers --exclude \"./*Test*\" --csv"
lizard_headers = ["NLOC", "CCN", "token", "PARAM", "length", "verbose", "input", "class::method", "class::method(args)", "start line", "end line"]
output_headers = ["NLOC", "CCN", "token", "PARAM", "length", "TA", "student", "task", "class", "method"]

regex = {
    "task": "(task-[0-9]+)",
    "class": "^[A-Za-z0-9]*",
    "TA": "(?<=repos\/)[A-Za-z]+(?=\/)",
    "student": "((?<=\/)([a-zA-Z0-9]+)(?=-task))",
    "method": "((?<=::)[A-Za-z0-9].*$)"
}



# Först sparas allt i en lista, varje ny rad är en dictionary
rows = []
attribute_errors = 0
with open(input, newline='') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=lizard_headers)
    for row in reader:
        try:
            ta = re.search(regex["TA"], row['verbose']).group(0)
            student = re.search(regex["student"], row['verbose']).group(0)
            task = re.search(regex["task"], row['verbose']).group(0)
            clss = re.search(regex["class"], row['class::method']).group(0)
            method = re.search(regex["method"], row['class::method']).group(0)
        except AttributeError:
            # eftersom lösningar som ej kompilerar pajar regexen är detta nödvändigt
	# Kanske vill sätta till NaN för att kunna filtrera ut i Pandas
            attribute_errors = attribute_errors + 1
            continue
        new_row = { # dictionary
                    "NLOC": row['NLOC'], 
                    "CCN": row['CCN'], 
                    "token": row['token'], 
                    "PARAM": row['PARAM'], 
                    "length": row['length'],
                    "TA": ta,
                    "student": student, 
                    "task": task, 
                    "class": clss, 
                    "method": method
                    }
        rows.append(new_row)

# Nu skapar jag en ny CSV-filjävel
with open(output, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=output_headers)
    writer.writeheader()
    writer.writerows(rows)

print(f"Done parsing a total of {len(rows)} rows, with {attribute_errors} faulty lines! That's a felmariginal of {attribute_errors/len(rows)}")
