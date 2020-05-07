class Camera:

    def __init__(self, camera_id, station_id, show_image, resize_image, width, height, fps):
        self.id = camera_id
        self.station_id = station_id
        self.show_image = show_image
        self.resize_image = resize_image
        self.width = width
        self.height = height
        self.fps = fps

    def __repr__(self):
        return '<Camera> {} ({}x{}) FPS:{} SIZE:{}'.format(self.station_id, self.width, self.height, self.fps, self.resize_image)
    

