from imutils.video import VideoStream
from conneciton.database import DataBase
from controller.camera import CameraController
from time import localtime, sleep
from loguru import logger
from pyzbar import pyzbar
import pandas as pd
import imutils
import cv2


class Recognition:

    def __init__(self, camera):
        self.camera = camera
        self.cart_log = list()

    def start_camera(self):

        camera = VideoStream(usePiCamera=True,
                             resolution=(self.camera.width, self.camera.height),
                             framerate=self.camera.fps).start()

        sleep(0.8)

        return camera

    @staticmethod
    def scanner(frame):

        code = ''

        image = pyzbar.decode(frame)

        for data in image:
            text = data.data.decode('utf-8')
            code = '{}'.format(text)

        return code

    def process_image(self, frame):

        frame = imutils.resize(frame, self.camera.resize_image)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        return frame

    @staticmethod
    def get_format_date():

        date = localtime()

        year, month, day, hour, minutes, seconds = date[0], date[1], date[2], date[3], date[4], date[5]

        def verify_number(number):
            if len(str(number)) == 1:
                number = '0{}'.format(number)

            return number

        year = str(year)
        year = year[2:]
        day = verify_number(day)
        month = verify_number(month)
        hour = verify_number(hour)
        minutes = verify_number(minutes)
        seconds = verify_number(seconds)

        format_data = '{}/{}/{} {}:{}:{}'.format(day, month, year, hour, minutes, seconds)

        return format_data

    @staticmethod
    def save_log(logs):

        df = pd.DataFrame(logs, index=[0])

        logger.success(logs)

        with open('/home/pi/prod/s-config/logs/logs.csv', 'a') as f:
            df.to_csv(f, header=False)

            logger.success('Saved logs')

    def reader(self):

        camera = self.start_camera()

        truck = 0

        while True:

            try:

                frame = camera.read()
                frame = self.process_image(frame)

                code = self.scanner(frame)

                if code != '':

                    if code in self.cart_log:
                        pass
                    else:

                        self.cart_log.append(code)

                        logger.info(self.cart_log)

                        if len(self.cart_log) > 0:

                            carts = ''

                            for c in self.cart_log:
                                carts += '{} '.format(c)

                            logs = {

                                'number_truck': truck,
                                'total_cart': len(self.cart_log),
                                'carts': carts,
                                'data': self.get_format_date(),
                            }

                            self.save_log(logs=logs)

                            if len(self.cart_log) == 4:
                                self.cart_log = list()

                if bool(int(self.camera.show_image)):
                    cv2.imshow('Image', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

                else:
                    pass
            except Exception as e:
                logger.error(e)

                with open('/home/pi/prod/s-config/logs/error.txt', 'a') as f:
                    f.write('\n{}'.format(str(e)))

        camera.stop()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    db = DataBase(data_base='/home/pi/prod/s-config/config.db')

    cameraController = CameraController(db=db)
    camera_config = cameraController.consult()[0]

    print(camera_config)

    r = Recognition(camera=camera_config)
    r.reader()
