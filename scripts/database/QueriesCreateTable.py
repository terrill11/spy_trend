#!/Users/terrill/OneDrive/Documents/work/projects/spy/venv_spy/bin/python

class QueriesCreateTable():
    def create_table_equities(self, ticker):
        query = f'''CREATE TABLE Equities.dbo.{ticker} (
                                Date DATE,
                                HighPrice DECIMAL(16,6),
                                LowPrice DECIMAL(16,6),
                                OpenPrice DECIMAL(16,6),
                                ClosePrice DECIMAL(16,6),
                                Volume INT
                            )'''
        return query

    def create_table_equities_indexes(self, ticker):
        query = f'''CREATE TABLE Equities.dbo.{ticker} (
                                Date DATE,
                                HighPrice DECIMAL(26,6),
                                LowPrice DECIMAL(26,6),
                                OpenPrice DECIMAL(26,6),
                                ClosePrice DECIMAL(26,6),
                                Volume BIGINT
                            )'''
        return query

    def create_table_equities_bonds(self, ticker):
        query = f'''CREATE TABLE Equities.dbo.{ticker} (
                                Date DATE,
                                HighPrice DECIMAL(6,2),
                                LowPrice DECIMAL(6,2),
                                OpenPrice DECIMAL(6,2),
                                ClosePrice DECIMAL(6,2)
                            )'''
        return query

    def create_table_equities_vix(self, ticker):
        query = f'''CREATE TABLE Equities.dbo.{ticker} (
                                Date DATE,
                                HighPrice DECIMAL(10,6),
                                LowPrice DECIMAL(10,6),
                                OpenPrice DECIMAL(10,6),
                                ClosePrice DECIMAL(10,6)
                            )'''
        return query

    def create_table_economics_rate(self, ticker):
        query = f'''CREATE TABLE Economics.dbo.{ticker} (
                                Date DATE,
                                Rate DECIMAL(11,10))'''
        return query

    def create_table_economics_value(self, ticker):
        query = f'''CREATE TABLE Economics.dbo.{ticker} (
                                Date DATE,
                                Value DECIMAL(14,4)
                                )'''
        return query

    def create_table_forex(self, ticker):
        query = f'''CREATE TABLE Forex.dbo.{ticker} (
                                Date DATE,
                                ClosePrice DECIMAL(14,4),
                                OpenPrice DECIMAL(14,4),
                                HighPrice DECIMAL(14,4),
                                LowPrice DECIMAL(14,4)
                                )'''
        return query

    def create_table_futures(self, ticker):
        query = f'''CREATE TABLE Futures.dbo.{ticker} (
                                Date DATE,
                                ClosePrice DECIMAL(14,4),
                                OpenPrice DECIMAL(14,4),
                                HighPrice DECIMAL(14,4),
                                LowPrice DECIMAL(14,4),
                                Volume BIGINT
                            )'''
        return query