class User:

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __init__(self, user_id, name, password):
        self.id = user_id
        self.name = name
        self.password = password

    def __repr__(self):
        return '<User> {}: {}'.format(self.id, self.name)
