from abstractdatasource import AbstractDataSource
import solr


class SolrDataSource(AbstractDataSource):

    def __init__(self, configs, *args, **kwargs):
        super(SolrDataSource, self).__init__(*args, **kwargs)
 
        self.configs = configs

        self.host = configs['host']


    def solr(self):
        s = solr.SolrConnection(self.host)

        params = {
            'q': self.make_query(),
            'fields': ['sku'],
            'sort': 'sku asc',
        }
        response = s.query(**params)

        i = 0
        for result in response.results:
            while str(result['sku']) != self.skus[i]:
                yield False
                i += 1

            yield True
            i += 1


    def make_query(self):
        return f'sku:({" ".join(self.skus)})'
    
    
    # def field_list(self):
    #     fields = list()
    # 
    #     fields.append('sku')
    # 
    #     for filial in filiais:
    #         fields.append(f'filial_preco_*_{filial}')
    #         fields.append(f'filial_estoque_*_{filial}')
    #         fields.append(f'filial_comercializacao_*_{filial}')
    # 
    #     return fields


