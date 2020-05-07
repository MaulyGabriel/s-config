from models.camera import Camera


class CameraController:

    def __init__(self, db):
        self.db = db

    def insert(self, camera):
        sql = "INSERT INTO camera(station_id, show_image, resize_image, width, height, fps) VALUES('{}', '{}', '{}', '{}', '{}', '{}');".format(
            camera.station_id, camera.show_image, camera.resize_image, camera.width, camera.height, camera.fps)
        self.db.execute_sql(sql=sql)

    def update(self, camera):
        sql = "UPDATE camera SET station_id='{}', show_image='{}', resize_image='{}', width='{}', height='{}', fps='{}' WHERE id='{}';".format(
            camera.station_id, camera.show_image, camera.resize_image, camera.width, camera.height, camera.fps,
            camera.id)
        self.db.execute_sql(sql)

    def delete(self, camera):
        sql = 'DELETE FROM camera WHERE id={}'.format(camera.id)
        self.db.execute_sql(sql)

    def consult(self):
        cameras = list()

        sql = 'SELECT * FROM camera'
        result = self.db.consult(sql)

        if result is None:
            return None

        for c in result:
            cameras.append(
                Camera(camera_id=c[0], station_id=c[1], show_image=c[2], resize_image=c[3], width=c[4], height=c[5],
                       fps=c[6]))

        return cameras

    def consult_by(self, condition, camera):

        sql = ''

        if condition == 'id':
            sql = "SELECT * FROM camera WHERE id={}".format(camera.id)
        elif condition == 'name':
            sql = "SELECT * FROM camera WHERE station_id LIKE '%{}%';".format(camera.station_id)

        result = self.db.consult(sql)

        if result is None:
            return None

        for c in result:
            camera = Camera(camera_id=c[0], station_id=c[1], show_image=c[2], resize_image=c[3], width=c[4],
                            height=c[5],
                            fps=c[6])

        return camera
