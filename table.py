
class Table(object):

    def __init__(self):
        self._columns = list()


    def column(self, *args, **kwargs):
        col = Column(*args, **kwargs)

        self._columns.append(col)


    def print(self, formatter):
        formatter.table = self

        for line in formatter.header():
            print(line)

        for data in self.lines():
            print(formatter.line(data))

        for line in formatter.footer():
            print(line)


    def lines(self):
        generators = [ c.provider() for c in self._columns ]

        while True:
            values = list()
            some_running = False
            for g in generators:
                try:
                    values.append(next(g))
                    some_running = True
                except StopIteration as e:
                    values.append(None)
                
            if some_running:
                yield values
            else:
                break
            # try:
            #     values = [ next(g) for g in generators ]
            # except StopIteration as e:
            #     return

            # yield values


class Column(object):

    def __init__(self, header, provider, width=12, separator='|', alignment='left', formatter=str):
        self.header = header
        self.provider = provider
        self.width = width
        self.separator = separator
        self.alignment = alignment
        self.formatter = formatter


class TableFormatter(object):

    def __init__(self):
        pass


    def header(self, headers):
        return list()


    def footer(self):
        return list()


class DefaultTableFormatter(TableFormatter):

    def __init__(self,
            column_separators={'before': ' ', 'cell': '|', 'after': ''},
            section_separator_char='-',
            section_separator={'before_header': False, 'header->body': True, 'after_body': False},
            cell_padding={'left': 1, 'right': 1}):
        self.column_separators = column_separators
        self.section_separator_char = section_separator_char
        self.section_separator = section_separator
        self.cell_padding = cell_padding


    def header(self):
        self.headers_line, headers_body_separator = self._make_header_line()

        lines = list()

        if self.section_separator['before_header']:
            lines.append(self.section_separator_char * len(self.headers_line))

        lines.append(self.headers_line)

        if self.section_separator['header->body']:
            lines.append(headers_body_separator)

        return lines


    def _make_header_line(self):
        formatted = self.format_cells([ col.header for col in self.table._columns ], True)

        return self.format_line(formatted, True)


    def line(self, data):
        formatted = self.format_cells(data, False)
        
        return self.format_line(formatted)


    def format_cells(self, data_line, skipcolformatter):
        formatted = list()

        for col, data_cell in zip(self.table._columns, data_line):
            formatted.append(self.format_cell(col, data_cell, skipcolformatter))

        return formatted

    
    def format_cell(self, column, data, skipcolformatter):
        datastr = data if skipcolformatter else column.formatter(data)
        spacer = column.width - len(datastr) - self.cell_padding['left'] - self.cell_padding['right']

        cell = ' ' * self.cell_padding['left']

        match column.alignment:
            case 'right':
                cell += ' ' * spacer

            case 'center':
                cell += ' ' * (spacer // 2)


        cell += datastr

        match column.alignment:
            case 'left':
                cell += ' ' * spacer

            case 'center':
                cell += ' ' * (spacer // 2)
                
                if spacer % 2 == 1:
                    cell += ' '

        cell += ' ' * self.cell_padding['right']

        return cell
    

    def format_line(self, data, make_separator=False):
        def append(value, filler=' '):
            nonlocal line
            line += value

            if make_separator:
                nonlocal separator
                separator += filler * len(value)

        line = ''
        separator = ''

        append(self.column_separators['before'])

        for cellno, cell in enumerate(data):
            append(cell, self.section_separator_char)

            if cellno < len(data) - 1:
                append(self.column_separators['cell'])

        append(self.column_separators['after'])

        if make_separator:
            return line, separator
        else:
            return line


    def footer(self):
        if self.section_separator['after_body']:
            return [ self.section_separator_char * len(self.headers_line) ]
        else:
            return list()

