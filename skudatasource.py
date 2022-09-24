from abstractdatasource import AbstractDataSource


class SKUDataSource(AbstractDataSource):

    def sku(self):
        for sku in self.skus:
            yield sku

