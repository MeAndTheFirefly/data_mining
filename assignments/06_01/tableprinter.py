"""This module provides the TablePrinter class"""

__author__ = 'James Taylor'
__version__ = '0.1'
__date__ = '8th September 2018'

# import as private attributes so objects from other modules
# do not clutter the documentation for this one
from sys import stdout as _stdout
from math import ceil as _ceil
from re import sub as _sub, match as _match, fullmatch as _fullmatch

class TablePrinter:
    r"""
    Class for neatly printing textual tables to the console.

    The data to display must be provided as a list of dict records.
    The print() method does all the work. Other methods are for setting
    what the printed table will contain and how it will be formatted.

    Here is an example of typical usage:

        from tableprinter import TablePrinter

        my_data = [
            { 'item': 'Book',      'price': 8.50,   'stock': 12 },
            { 'item': 'Chocolate', 'price': 5.25,   'stock': 27 },
            { 'item': 'Music',     'price': 12.50,  'stock': 7 },
            { 'item': 'Ferrari',   'price': 249150, 'stock': 0 },
        ]

        tp = TablePrinter()
        tp.num(1).indent(" " * 4)
        tp.fields([ 'item', 'price' ])
        tp.forms( [ '^',    ',.2f'  ])
        tp.print(my_data)

    The output looks like this:

        ╭───┬───────────┬────────────╮
        │ # │   Item    │      Price │
        ├───┼───────────┼────────────┤
        │ 1 │   Book    │       8.50 │
        │ 2 │ Chocolate │       5.25 │
        │ 3 │   Music   │      12.50 │
        │ 4 │  Ferrari  │ 249,150.00 │
        ╰───┴───────────┴────────────╯

    An instance of the TablePrinter class should first be created:

        from tableprinter import TablePrinter
        tp = TablePrinter()

    The output may be confgured using the methods described below,
    and then the data can be printed by calling the print() method.
    The methods are:

    data()   Optionally load the data before calling print() without args.
    print()  Print given data, or the data already loaded by data().
    fields() Set fields of the dict records to print as table columns.
    heads()  Set headings for the table columns corresponding to each field.
    forms()  Set format and alignment for each field to be printed.
    num()    Enable automatic numbering of rows given the first row number.
    parts()  Split the table into several parts horizintally on screen.
    indent() String to use for indenting the table from the left margin.
    sep()    String to use as separator between multiple part tables.
    ascii()  Use simple ASCII characters for the table borders.
    utf8()   Use nice utf8 characters for the table borders (the default).
    file()   Set an alternative file handle for the printed output to go.

    For conveniece all methods may be chained like this:

        TablePrinter().ascii().num(1).parts(3).print(my_data)

    See the documentation for each method for more usage details.
    """

    _ascii_box = {
        'nw': '+-', 'n': '-', 'nt': '-+-', 'ne': '-+',
        'w':  '| ', ' ': ' ', 'v':  ' | ', 'e':  ' |',
        'wt': '+-', 'h': '-', 'x':  '-+-', 'et': '-+',
        'sw': '+-', 's': '-', 'st': '-+-', 'se': '-+',
    }

    _utf8_box = {
        'nw': '╭─', 'n': '─', 'nt': '─┬─', 'ne': '─╮',
        'w':  '│ ', ' ': ' ', 'v':  ' │ ', 'e':  ' │',
        'wt': '├─', 'h': '─', 'x':  '─┼─', 'et': '─┤',
        'sw': '╰─', 's': '─', 'st': '─┴─', 'se': '─╯',
    }

    def __init__(self):
        r"""Just use tp = TablePrinter() without arguments."""
        self._data = []
        self._fields = None
        self._forms = None
        self._heads = None
        self._start = None
        self._parts = 1
        self._indent = ''
        self._sep = '  '
        self._box = TablePrinter._utf8_box
        self._file = _stdout

    def data(self, records):
        r"""
        Set list of dict records to use if print() is called without args.

        When the print() method is called with an argument then that is
        used instead of the one set by this data() method.
        """
        self._data = records
        return self

    def fields(self, names):
        r"""
        Set the field names and the order they will appear in the table.

        This takes the field names as a list of strings. The fields names
        should be the same as the dict keys in the data records, or the
        subset that you wish to print as columns in the table. The order
        that they appear in the list will be used when printing the table.

        If the field names are not given before the print() method is
        called then the alphabetical order of the fields in the first
        record of the data will be used instead.
        """
        self._fields = names
        return self

    def forms(self, formats):
        r"""
        Set the format and/or alignment for each field to be printed.

        This method takes either a dict or a list. If given a dict the
        dict should have field names for keys and string values for the
        corresponding format codes. If given a list of strings to use as
        format codes then the order must match the order of the field
        names previously given to the fields() method.

        The format codes this understands are the same as Python's
        standard "format_spec" mini language which is documented here:

        https://docs.python.org/3/library/string.html#formatspec

        Some example format codes:

            d       decimal integers, column width is automatic 
            4d      integers in a space at least 4 characters wide
            ,d      integers with commas separating thousands
            f       floating point values, column width automatic
            6f      floats within a space at least 6 chars wide
            6.2f    floats at least 6 wide, with 2 decimal places
            .2f     floats with 2 decimal places, auto column width
            8,.2f   floats 8 wide, 2 decimals, commas at thousands
            12s     strings in a space at least 12 chars wide
            ^12s    strings centered within a space at least 12 wide
            >s      strings right aligned in automatic column width
            <d      integers left aligned in the automatic width

        It is not necessary to provide a format code for every field
        because default formatting will be quite sensible when Python
        knows the types of numeric values. Often only floating point
        decimal places will need to be set.

        If there are many fields but only a few need format codes then
        it is easier to use a dict to set a few formats. Example:

            tp.forms({ 'grams': '.4f', 'atoms': ',d' })

        might be all that is needed in a large table of chemical data
        where most fields can be displayed in their default format.

        When print() is called, any fields for which no format was set
        will be formatted automatically according to the type of the
        values in the data. Strings will be left aligned, and numbers
        will be right aligned. Floating point numbers will be aligned by
        the decimal point. Other types will just be shown as strings.

        Headings will get the same alignment as each column in the
        data so that they appear neatly above most of the data values.
        """
        self._forms = formats
        return self

    def heads(self, headings):
        r"""
        Set the headings to display above each table column.

        This method takes either a dict or a list. If given a dict the
        dict should have field names for keys and string values for the
        corresponding headings. If given a list of strings to use as
        headings then the order must match the order of the field names
        previously given to the fields() method.

        When print() is called, any fields for which no heading was set
        will get a heading made by capitalizing the field name and
        converting any underscores to spaces.
        """
        self._heads = headings
        return self

    def num(self, start):
        r"""
        Enable row numbering in an extra column left of the table.

        This method takes an integer to use as the start number.
        Typically this would be 1 but you can start row numbers from any
        number if, for example, you are printing a continuation table.
        The heading for the numbering column is always just a '#' symbol.

        By default row numbering is disabled. After enabling it you can
        disable it by calling this method with None as the start value.
        """
        self._start = start
        return self

    def indent(self, indent_str):
        r"""
        Set the string to indent the table from the left margin.

        By default tables are printed next to the left side of the
        screen with no indentation. For small tables this can look odd
        so it may be better to indent them away from the left margin.

        This methd takes a single string. Typically this will just be
        a few spaces, such as " " * 4 or perhaps a tab character "\t"
        to position small tables more centrally on the screen.

        See the sep() method for spacing between multi part tables.
        """
        self._indent = indent_str
        return self

    def parts(self, num_parts):
        r"""
        Set the number of parts to split the table horizontally on screen.

        By default there is just one part, so the table is displayed in
        a single vertical column on screen. This may not be the best use
        of available screen space and the top of the table may scroll
        out of view. In this situation it could be better to split the
        table into several parts displayed side by side.

        When the number of parts is 2 or more the rows will be as evenly
        balanced as possible between the parts. If the number of rows is
        not exactly divisible by the number of parts then there will be
        some blank rows at the end of the last part so it lines up neatly.
        """
        self._parts = num_parts
        return self

    def sep(self, sep_str):
        r"""
        Set the string to use to separate parts of multi part tables.

        By default this is two space characters. Increasing the
        separation may improve the appearance of some multi part tables
        in a similar way to the indent() method.
        """
        self._sep = sep_str
        return self

    def file(self, out_file):
        r"""
        Set the output file handle used for printing the table.

        By default output goes to sys.stdout as normal. If you wish to
        redirect output to another file (or file-like stream) then pass
        the file handle to this method.
        """
        self._file = out_file
        return self

    def utf8(self):
        r"""
        Use utf8 box drawing characters for the table borders.

        This is the default display mode because it is better looking
        on most modern terminal software. For plain ASCII table borders
        use the ascii() method.
        """
        self._box = TablePrinter._utf8_box
        return self

    def ascii(self):
        r"""
        Use ASCII box drawing characters + - | for the table borders.

        By default nicer looking utf8 box drawing characters are used
        for the table borders. In some situations it is not possible to
        display utf8 characters so this method can be used to switch to
        the alternative plain ASCII box characters plus, hypen, and bar. 

        You can switch back to utf8 chars with the utf8() method.
        """
        self._box = TablePrinter._ascii_box
        return self

    def print(self, records=None):
        r"""
        Print the data as a textual table.

        If the records are provided as an argument to the print() method
        then those will be printed. If print() is called without an
        argument then data must have already been provided to the data()
        method. If neither of these has any data, print() will do nothing.

        Typically print() will be the last method called after configuring
        the TablePrinter object using the other methods. It is recommended
        to at least set the field order with fields() and the column
        headings with heads() and perhaps some of the formats with forms().
        """
        data = records or self._data
        if not data: return

        fields = self._fields
        forms = self._forms
        heads = self._heads
        parts = self._parts
        indent = self._indent
        sep = self._sep
        box = self._box
        outfile = self._file
        start = self._start

        if not fields:
            fields = sorted(data[0].keys())

        if heads and type(heads) == dict:
            heads = heads.copy()
        if heads and type(heads) == list:
            heads = dict(zip(fields,heads))
        if not heads:
            heads = {}
        for f in fields:
            if f not in heads:
                heads[f] = _sub('_', ' ', f).title()

        if forms and type(forms) == dict:
            forms = forms.copy()
        if forms and type(forms) == list:
            forms = dict(zip(fields,forms))
        if not forms:
            forms = {}

        widths = { f: len(heads[f]) for f in fields }
        types  = { f: '' for f in fields }
        magn   = { f: None for f in fields }
        pres   = { f: None for f in fields }
        hform  = {}
        for f in fields:
            fmt = '{:'+forms[f]+'}' if f in forms else '{}'
            magn[f], pres[f] = 0, 0
            for rec in data:
                val = rec[f]
                valstr = fmt.format(val)
                widths[f] = max(widths[f], len(valstr))
                types[f] = max(types[f],
                    {int: 'd', float: 'f', str: 's'}[type(val)])
                if types[f] != 'f': continue
                valstr = valstr.strip()
                point = valstr.find('.') + 1
                if point:
                    pres[f] = max(pres[f], len(valstr)-point)
                    magn[f] = max(magn[f], point-1)


            if f in forms:
                fmt = forms[f]
                # first char of format_spec can be any fill char but
                # only when there is an alignment char <^>= present
                fi = ''
                if _match(r'.[<^>=]', fmt):
                    fi, fmt = fmt[0], fmt[1:]
                # parts of the format_spec are:
                # fill align sign pad width group precision type
                al, si, pa, wi, gr, pr, ty = _fullmatch(
                  r'([<^>=]?)([+ -]?)([#0]*)(\d*)([,_]?)((?:\.\d+)?)(\w?)',
                  fmt).groups()
                # type letters include:
                # b=binary, c=character, d=int, e=exponent, f=float,
                # g=general, n=int with commas, o=octal, s=string, x=hex
                ty = ty or types[f]
                al = al or '<' if ty == 's' else '>'
                if wi: widths[f] = max(widths[f], int(wi))
                wi = str(widths[f])
                forms[f] = fi + al + si + pa + wi + gr + pr + ty
            else:
                al = '<' if types[f] == 's' else '>'
                if types[f] == 'f':
                    widths[f] = max(widths[f], magn[f] + 1 + pres[f])
                    forms[f] = al + str(widths[f]) +'.'+ str(pres[f]) +'f'
                else:
                    forms[f] = al + str(widths[f]) + types[f]
            hform[f] = al + str(widths[f]) + 's'

        if start is not None:
            numlen = max(len(str(start)), len(str(start+len(data)-1)))
            fields = [ '#' ] + fields
            heads['#'] = '#'
            widths['#'] = numlen
            forms['#'] = '>' + str(numlen) + 'd'
            hform['#'] = '>' + str(numlen) + 's'

        toprule  = ( box['nw']
                   + box['nt'].join([box['n'] * widths[f] for f in fields])
                   + box['ne'] )
        midrule  = ( box['wt']
                   + box['x'].join([box['h'] * widths[f] for f in fields])
                   + box['et'] )
        botrule  = ( box['sw']
                   + box['st'].join([box['s'] * widths[f] for f in fields])
                   + box['se'] )
        blankrow = ( box['w']
                   + box['v'].join([box[' '] * widths[f] for f in fields])
                   + box['e'] )
        rowfmt   = ( box['w']
                   + box['v'].join(['{:'+forms[f]+'}' for f in fields ])
                   + box['e'] )
        headfmt  = ( box['w']
                   + box['v'].join(['{:'+hform[f]+'}' for f in fields ])
                   + box['e'] )

        header = headfmt.format(*[ heads[f] for f in fields ])
        print(indent + sep.join([ toprule ] * parts), file=outfile)
        print(indent + sep.join([ header  ] * parts), file=outfile)
        print(indent + sep.join([ midrule ] * parts), file=outfile)
        step = _ceil(len(data) / parts)
        for r in range(0, step):
            print(indent, end='', file=outfile)
            for c in range(0, parts):
                i = step*c+r
                if c: print(sep, end='', file=outfile)
                if i < len(data):
                    rowdat = [ data[i][f] for f in fields if f != '#' ]
                    if start is not None:
                        rowdat = [ start + i ] + rowdat
                    row = rowfmt.format(*rowdat)
                else:
                    row = blankrow
                print(row, end='', file=outfile)
            print('', file=outfile)
        print(indent + sep.join([ botrule ] * parts), file=outfile)
        return self

