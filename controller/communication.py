from models.communication import Communication


class CommunicationController:

    def __init__(self, db):
        self.db = db

    def insert(self, communication):
        sql = "INSERT INTO communication(port, baudrate, timeout, preamble) VALUES('{}', '{}', '{}', '{}');".format(
            communication.port,
            communication.baudrate, communication.timeout, communication.preamble)
        self.db.execute_sql(sql=sql)

    def update(self, communication):
        sql = "UPDATE communication SET port='{}', baudrate='{}', timeout='{}', preamble='{}' WHERE id='{}';".format(
            communication.port,
            communication.baudrate,
            communication.timeout,
            communication.preamble,
            communication.id)

        self.db.execute_sql(sql)

    def delete(self, communication):
        sql = 'DELETE FROM communication WHERE id={}'.format(communication.id)
        self.db.execute_sql(sql)

    def consult(self):
        communications = list()

        sql = 'SELECT * FROM communication'
        result = self.db.consult(sql)

        if result is None:
            return None

        for c in result:
            communications.append(
                Communication(communication_id=c[0], port=c[1], baudrate=c[2], timeout=c[3], preamble=c[4]))

        return communications

    def consult_by(self, condition, communication):

        sql = ''

        if condition == 'id':
            sql = "SELECT * FROM communication WHERE id={}".format(communication.id)
        elif condition == 'name':
            sql = "SELECT * FROM communication WHERE port LIKE '%{}%';".format(communication.port)

        result = self.db.consult(sql)

        if result is None:
            return None

        for c in result:
            communication = Communication(communication_id=c[0], port=c[1], baudrate=c[2], timeout=c[3], preamble=c[4])

        return communication
