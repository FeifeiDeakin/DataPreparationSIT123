import csv, re

processed = []
with open('input-fixed.csv', 'rb') as f:
    reader = csv.reader(f)
    data = list(reader)

# Column 1 should only contain numerical characters
# Column 1 should always be greater than 999
# Column 2 should only contain numerical characters
# Should always be between 9 and 11 characters in length
# Column 3 should always look like %year%/%month%/%date%/ %H%:%M%:%S%
# Column 4 should always be a decimal number >= 0 <= 100
# And there are some other rules included below
def inconsistency(row, message):
    print "Inconsistency at row " + str(row) + " " + message

floatString = re.compile('\d+(\.\d+)?')

row = 1
prev_line = False
nf = 0;
for line in data:

    # Skip the column name row
    if row == 1:
        row += 1
        continue;

    line[0] = line[0].strip();
    if not line[0].isdigit():
        inconsistency(row, 'in column 1 (non-digit string)')
        nf += 1

    if line[0] < 999:
        inconsistency(row, 'in column 1 (value is >= 999)')
        nf += 1

    line[1] = line[1].strip();
    if not line[1].isdigit():
        inconsistency(row, 'in column 2 (non-digit string)')
        nf += 1

    if len(line[1]) < 9 or len(line[1]) > 11:
        inconsistency(row, 'in column 2 (value < 9 or > 11)')
        nf += 1

    # Has more or less than one second passed?
    if not prev_line == False:
        if line[1].isdigit() and prev_line[1].isdigit():
            if (not int(line[1]) - int(prev_line[1])) == 1:
                inconsistency(row, 'in column 1 (time since last record != 1)')
                nf += 1

    line[2] = line[2].strip();
    if ("/" not in line[2]):
        inconsistency(row, 'in column 3 (value is not y/m/d h:m:s)')
        nf += 1

    if (line[2].count("/") < 2):
        inconsistency(row, 'invalid number of / in column 3');
        nf += 1

    if (line[2].count(":") < 2):
        inconsistency(row, 'invalid number of : in column 3');
        nf += 1

    line[3] = line[3].strip()
    if floatString.match(line[3]) == None:
        inconsistency(row, 'in column 4 (non-digit string)')
        nf += 1
    elif (float(line[3]) > 100) or (float(line[3]) <= 0 ):
        inconsistency(row, 'in column 4 (value is <= 0 or > 100)')
        nf += 1

    # Find duplicate entries
    x = 2
    for i in processed:
        if i[0] == line[0] and i[1] == line[1] and i[2] == line[2] and i[3] == line[3]:
            inconsistency(row, 'duplicate entry with line ' + str(x))
        x += 1

    prev_line = line
    processed.append(line)
    row += 1

print "Finished. Found " + str(nf) + " inconsistencies."
