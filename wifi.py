from conneciton.database import DataBase
from controller.wifi import WifiController
from PyAccessPoint import pyaccesspoint as pa
from loguru import logger


class Wifi:

    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.service = 'wifi_solinftec.service'

    def create_network(self):
        logger.info('Configurando o ponto de acesso...')

        w = pa.AccessPoint(ssid=self.name, password=self.password)

        logger.info('Iniciando o ponto de acesso...')

        w.stop()
        w.start()

        logger.success('Processo concluído.')

    def run(self):
        self.create_network()


if __name__ == '__main__':
    
    db = DataBase(data_base='/home/pi/prod/s-config/config.db')

    wifiController = WifiController(db=db)

    wifi = wifiController.consult()[0]

    print(wifi)

    w = Wifi(name=wifi.name, password=wifi.password)
    w.run()
