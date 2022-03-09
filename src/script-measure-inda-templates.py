import csv
import subprocess
import re
from pathlib import Path


from executing import Source


# Find which data to analyze
input = "../data/inda-templates.csv"
output = "../data/inda-templates-sorted.csv"

#command = "lizard -o lizard_analytics.numbers --exclude \"./*Test*\" --csv"
lizard_headers = ["NLOC", "CCN", "token", "PARAM", "length", "verbose", "input", "class::method", "class::method(args)", "start line", "end line"]
output_headers = ["NLOC", "CCN", "token", "PARAM", "length", "task", "class", "method"]

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
            task = re.search(regex["task"], row['verbose']).group(0)
            clss = re.search(regex["class"], row['class::method']).group(0)
            method = re.search(regex["method"], row['class::method']).group(0)
        except AttributeError:
            # eftersom lösningar som ej kompilerar pajar regexen är detta nödvändigt
	# Kanske vill sätta till NaN för att kunna filtrera ut i Pandas
            attribute_errors = attribute_errors + 1
            new_row = { # dictionary
                    "NLOC": row['NLOC'], 
                    "CCN": row['CCN'], 
                    "token": row['token'], 
                    "PARAM": row['PARAM'], 
                    "length": row['length'],            
                    "task": "NaN", 
                    "class": "NaN", 
                    "method": "Nan"
                    }            
            continue
        new_row = { # dictionary
                    "NLOC": row['NLOC'], 
                    "CCN": row['CCN'], 
                    "token": row['token'], 
                    "PARAM": row['PARAM'], 
                    "length": row['length'],            
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
