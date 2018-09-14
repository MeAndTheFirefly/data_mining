r"""
Simple CSV parsing functions.

Warning: Only works with simple CSV.
In particular, fields cannot contain the separator, quotes, or newlines.
Use Python's standard csv module if you want a more robust solution.

When reading:
    Quoted fields are treated as string type even if they contain numbers.
    Unquoted numbers are treated as float type.
    Unquoted non-numeric values are treated as strings.

When writing:
    String values are quoted even if they contain numbers.
    Float and int types are written unquoted.
"""

# convert CSV field to Python value
def field2val(field):
    if field[:1] == '"':
        return field[1:-1]
    try:
        return float(field)
    except ValueError:
        return field

# convert Python value to CSV field
def val2field(val):
    if type(val) == float or type(val) == int:
        return str(val)             # return bare number
    else:
        return '"' + str(val) + '"' # wrap in quotes

# generator function to parse rows of simple CSV
#   does not handle fields with embedded separators, quotes, or newlines
def csv_rows(lines, sep=","):
    for line in lines:
        # split at sep, return one row at a time as a list
        yield [ field2val(p) for p in line.strip().split(sep) ]

# generator function to create dict records from CSV rows
def csv_records(rows, fields=None):
    # get field names from first line if not provided
    if not fields: fields = next(rows)
    # combine each row into a dict keyed on field names
    for row in rows: yield dict(zip(fields,row))

# make a line of CSV for output from a list of values
def row2csv(row, sep=","):
    return sep.join(val2field(v) for v in row)

# make a line of CSV for output from a record and list of fields
def rec2csv(rec, fields, sep=","):
    return row2csv([ rec[f] for f in fields ], sep)
