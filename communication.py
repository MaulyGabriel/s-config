from digi.xbee.devices import XBeeDevice
from conneciton.database import DataBase
from controller.communication import CommunicationController
from loguru import logger
from time import sleep
import serial


class Communication:

    def __init__(self, port, rate):

        self.port = port
        self.rate = rate

    def open_connection(self):

        conn = XBeeDevice(self.port, self.rate)

        return conn

    def test_communication(self):

        conn = self.open_connection()

        conn.open()

        while True:

            def data_receive_callback(xbee_message):
                answer = xbee_message.data.decode('utf-8')

                print(answer)


            conn.add_data_received_callback(data_receive_callback)



if __name__ == '__main__':
    logger.info('Open connection...')

    db = DataBase(data_base='/home/pi/prod/s-config/config.db')

    communicationController = CommunicationController(db=db)

    communication = communicationController.consult()[0]

    print(communication)

    try:
        c = Communication(communication.port, communication.baudrate)
        c.test_communication()

    except Exception as e:
        logger.error('Erro: {}'.format(e))
