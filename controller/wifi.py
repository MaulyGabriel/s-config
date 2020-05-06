from models.wifi import Wifi


class WifiController:

    def __init__(self, db):
        self.db = db

    def insert(self, wifi):
        sql = "INSERT INTO wifi(name, password) VALUES('{}', '{}');".format(wifi.name, wifi.password)
        self.db.execute_sql(sql=sql)

    def update(self, wifi):
        sql = "UPDATE wifi SET name='{}', password='{}' WHERE id='{}';".format(wifi.name, wifi.password, wifi.id)
        self.db.execute_sql(sql)

    def delete(self, wifi):
        sql = 'DELETE FROM wifi WHERE id={}'.format(wifi.id)
        self.db.execute_sql(sql)

    def consult(self):
        nets = list()

        sql = 'SELECT id, name, password FROM wifi'
        result = self.db.consult(sql)

        if result is None:
            return None

        for w in result:
            nets.append(Wifi(wifi_id=w[0], name=w[1], password=w[2]))

        return nets

    def consult_by(self, condition, wifi):

        sql = ''

        if condition == 'id':
            sql = "SELECT * FROM wifi WHERE id={}".format(wifi.id)
        elif condition == 'name':
            sql = "SELECT * FROM wifi WHERE name LIKE '%{}%';".format(wifi.name)

        result = self.db.consult(sql)

        if result is None:
            return None

        for w in result:
            wifi = Wifi(wifi_id=w[0], name=w[1], password=w[2])

        return wifi
