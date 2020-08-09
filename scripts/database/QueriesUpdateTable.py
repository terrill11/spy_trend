#!/Users/terrill/OneDrive/Documents/work/projects/spy/venv_spy/bin/python

class QueriesUpdateTable():
    def insert_data_equities(self, ticker):
        query = f'''INSERT Equities.dbo.{ticker} (Date, HighPrice, LowPrice, OpenPrice, ClosePrice, Volume)
                        VALUES (?,?,?,?,?,?)'''
        return query

    def insert_data_equities_bonds(self, ticker):
        query = f'''INSERT Equities.dbo.{ticker} (Date, HighPrice, LowPrice, OpenPrice, ClosePrice)
                        VALUES (?,?,?,?,?)'''
        return query

    def insert_data_equities_vix(self, ticker):
        query = f'''INSERT Equities.dbo.{ticker} (Date, HighPrice, LowPrice, OpenPrice, ClosePrice)
                        VALUES (?,?,?,?,?)'''
        return query

    def insert_data_economics_rates(self, ticker):
        query = f'''INSERT Economics.dbo.{ticker} (Date, Rate)
                        VALUES (?,?)'''
        return query

    def insert_data_economics_regs(self, ticker):
        query = f'''INSERT Economics.dbo.{ticker} (Date, Value)
                        VALUES (?,?)'''
        return query

    def insert_data_forex(self, ticker):
        query = f'''INSERT Forex.dbo.{ticker} (Date, ClosePrice, OpenPrice, HighPrice, LowPrice)
                        VALUES (?,?,?,?,?)'''
        return query

    def insert_data_futures(self, ticker):
        query = f'''INSERT Futures.dbo.{ticker} (Date, ClosePrice, OpenPrice, HighPrice, LowPrice, Volume)
                        VALUES (?,?,?,?,?,?)'''
        return query

    def insert_data_dix(self):
        query = f'''INSERT Equities.dbo.I_DIX (Date, SPX, DIX, GEX)
                        VALUES (?,?,?,?)'''
        return query