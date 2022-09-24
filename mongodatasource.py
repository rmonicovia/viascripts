from abstractdatasource import AbstractDataSource
import urllib

try:
    import pymongo
except ImportError:
    error('Module "pymongo" is required')


class MongoDataSource(AbstractDataSource):

    def __init__(self, configs, *args, **kwargs):
        super(MongoDataSource, self).__init__(*args, **kwargs)
    
        self.configs = configs

        user, password, host, params = configs.values()
    
        user = urllib.parse.quote_plus(user)
        password = urllib.parse.quote_plus(password)
    
        self.connection_string = f'mongodb://{user}:{password}@{host}/{params}'


    def produtos(self):
        client = pymongo.MongoClient(self.connection_string)

        try:
            database = client.catalogo
    
            collection = database.produtos
    
            int_skus = [ int(s) for s in self.skus ]
            produtos = collection.find({ "_id.sku": { "$in": int_skus } })
    
            try:
                # breakpoint()
                i = 0
                for produto in produtos:
                    while str(produto['_id']['sku']) != self.skus[i]:
                        yield False
                        i += 1

                    yield True
                    i+= 1

            finally:
                produtos.close()
    
        finally:
            client.close()


