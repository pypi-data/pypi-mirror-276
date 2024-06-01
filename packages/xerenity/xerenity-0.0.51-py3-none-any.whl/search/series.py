class Series:

    def __init__(self, connection):
        self.sup = connection

    def portfolio(self):
        return self.sup.get_all_series()

    def search(self, serie_id):
        return self.sup.read_serie(serie_id=serie_id)
