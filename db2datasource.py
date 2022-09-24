from abstractdatasource import AbstractDataSource
import ibm_db


class DB2DataSource(AbstractDataSource):

    def __init__(self, configs, *args, **kwargs):
        super(DB2DataSource, self).__init__(*args, **kwargs)

        self.configs = configs
    
        host, port, database, self.schema, user, password = self.configs.values()
    
        connection_string = f'HOSTNAME={host};PORT={port};DATABASE={database};PROTOCOL=TCPIP;UID={user};PWD={password};'

        # log('Connection on DB2 with string:', connection_string)
    
        self.connection = ibm_db.connect(connection_string, '', '')


    def mcr(self):
        mcr_stmt = self._make_mcr_stmt()

        i = 0
        while (mercadoria := ibm_db.fetch_assoc(mcr_stmt)):
            while str(mercadoria['CD_MCR']) != self.skus[i]:
                yield False
                i += 1

                if i == len(self.skus):
                    return

            yield True
            i += 1

            if i == len(self.skus):
                return


    def agp_mcr_anc(self):
        cnj_stmt = self._make_cnj_stmt()
    
        i = 0
        while (conjunto := ibm_db.fetch_assoc(cnj_stmt)):
            while str(conjunto['CD_AMANC']) != self.skus[i]:
                yield False
                i += 1

                if i == len(self.skus):
                    return

            yield True
            i += 1

            if i == len(self.skus):
                return

    
    def _make_mcr_stmt(self):
        query = f'''
    select
        *
    from
        {self.schema}.mcr
    where
        cd_mcr in ({",".join(self.skus)})
    '''
    
        return self._run_query(query)
    
    
    def _make_cnj_stmt(self):
        query = f'''
    select
        *
    from
        nsvp.agp_mcr_anc
    where
        cd_amanc in ({",".join(self.skus)})
    '''
    
        return self._run_query(query)
    
    
    def _run_query(self, query):
        # log('Running query:', query)
    
        return ibm_db.exec_immediate(self.connection, query)


    def __exit__(self, exc_type, exc_value, traceback):
        ibm_db.close(self.connection)

