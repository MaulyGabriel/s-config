from models.project import Project


class ProjectController:

    def __init__(self, db):
        self.db = db

    def insert(self, project):
        sql = "INSERT INTO project(name, version) VALUES('{}', '{}');".format(project.name, project.version)
        self.db.execute_sql(sql=sql)

    def update(self, project):
        sql = "UPDATE project SET name='{}', version='{}' WHERE id={};".format(project.name, project.version, project.id)
        self.db.execute_sql(sql)

    def delete(self, project):
        sql = 'DELETE FROM project WHERE id={}'.format(project.id)
        self.db.execute_sql(sql)

    def consult(self):
        projects = list()

        sql = 'SELECT * FROM project'
        result = self.db.consult(sql)

        if result is None:
            return None

        for p in result:
            projects.append(Project(project_id=p[0], name=p[1], version=p[2]))

        return projects

    def consult_by(self, condition, project):

        sql = ''

        if condition == 'id':
            sql = "SELECT * FROM project WHERE id={}".format(project.id)
        elif condition == 'name':
            sql = "SELECT * FROM project WHERE name LIKE '%{}%';".format(project.name)

        result = self.db.consult(sql)

        if result is None:
            return None

        for p in result:
            project = Project(project_id=p[0], name=p[1], version=p[2])

        return project
