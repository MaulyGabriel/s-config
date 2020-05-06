class Project:

    def __init__(self, project_id, name, version):
        self.id = project_id
        self.name = name
        self.version = version

    def __repr__(self):
        return '<Project> {}:{}'.format(self.name, self.version)
