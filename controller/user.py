from models.user import User


class UserController:

    def __init__(self, db):
        self.db = db

    def insert(self, user):
        sql = "INSERT INTO user(name, password) VALUES('{}', '{}');".format(user.name, user.password)
        self.db.execute_sql(sql=sql)

    def update(self, user):
        sql = "UPDATE user SET name='{}', password='{}' WHERE id='{}';".format(user.name, user.password, user.id)
        self.db.execute_sql(sql)

    def delete(self, user):
        sql = 'DELETE FROM user WHERE id={}'.format(user.id)
        self.db.execute_sql(sql)

    def consult(self):
        users = list()

        sql = 'SELECT id, name, password FROM user'
        result = self.db.consult(sql)

        if result is None:
            return None

        for u in result:
            users.append(User(user_id=u[0], name=u[1], password=u[2]))

        return users

    def consult_by(self, condition, user):

        sql = ''

        if condition == 'id':
            sql = "SELECT * FROM user WHERE id={}".format(user.id)
        elif condition == 'name':
            sql = "SELECT * FROM user WHERE name LIKE '%{}%';".format(user.name)

        result = self.db.consult(sql)

        if result is None:
            return None

        for u in result:
            user = User(user_id=u[0], name=u[1], password=u[2])

        return user
