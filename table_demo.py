#!/bin/env python3.10

from table import Table, DefaultTableFormatter

skus = [ 4775635, 4807340, 4926455, 4936280, 4991265, 5060117, 5128277, 5137233, 5159326, 5159334 ]

class DB2Provider(object):

    def __init__(self, skus):
        self._skus = skus
        self._curr = 0

    def sku(self):
        if self._curr >= len(self._skus):
            return None
        else:
            return self._skus[self._curr]

    def mcr(self):
        if self._curr >= len(self._skus):
            return None
        else:
            return self._skus[self._curr] % 2 == 0


    def agp(self):
        if self._curr >= len(self._skus):
            return None
        else:
            value = self._skus[self._curr] % 3 == 0
            return value


    def slq(self):
        if self._curr >= len(self._skus):
            return None
        else:
            value = self._skus[self._curr] % 5 == 0
            self._curr += 1
            return value


class DataAggregator(object):

    def __init__(self, *providers):
        self._providers = providers

    def _all_none(self, lst):
        for v in lst:
            if v != None:
                return False

        return True


    def lines(self):
        while True:
            all_none = True

            values = list()
            for p in self._providers:
                value = p()
                values.append(value)

                if value != None:
                    all_none = False

            from time import sleep
            sleep(0.5)
            if all_none:
                return
            else:
                yield values


db2 = DB2Provider(skus)
aggregator = DataAggregator(db2.mcr, db2.agp, db2.slq)

table = Table()

table.column(header='SKU', provider=db2.sku, width=12, alignment='left')
table.column(header='MCR', provider=db2.mcr, width=12, alignment='left')
table.column(header='AGP', provider=db2.agp, width=12, alignment='center')
table.column(header='SLQ', provider=db2.slq, width=12, alignment='right')

formatter = DefaultTableFormatter(
        column_separators={'before': '| ', 'cell':' ', 'after': '|'},
        section_separator_char='-',
        section_separator={'before_header': True, 'header->body': True, 'after_body': True},
        cell_padding={'left': 1, 'right': 4})


# column_separators={'before': ' ', 'cell': '|', 'after': ''},
# section_separator_char='-',
# section_separator={'before_header': False, 'header->body': True, 'after_body': False},
# cell_padding={'left': 1, 'right': 1}):

table.print(formatter)


