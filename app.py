from flask import Flask, render_template, send_from_directory, request, redirect, Response, send_file, flash
from conneciton.database import DataBase
from loguru import logger
from controller.camera import CameraController
from controller.communication import CommunicationController
from controller.project import ProjectController
from controller.user import UserController
from controller.wifi import WifiController
from models.camera import Camera
from models.communication import Communication
from models.wifi import Wifi
from time import sleep
from pyzbar import pyzbar
import jinja2.exceptions
import imutils
import os
import cv2

from flask_login import LoginManager, login_user, logout_user, login_required

app = Flask(__name__)
app.secret_key = os.urandom(97)

login_manager = LoginManager()
login_manager.init_app(app)

db = DataBase(data_base='/home/pi/prod/s-config/config.db')

cameraController = CameraController(db=db)
communicationController = CommunicationController(db=db)
projectController = ProjectController(db=db)
userController = UserController(db=db)
wifiController = WifiController(db=db)


def read_qr(frame):
    text = ''

    image = pyzbar.decode(frame)

    for data in image:
        text = data.data.decode('utf-8')
        text = '{}'.format(text)

    return text


def check_database():
    if os.path.exists('./config.db'):
        logger.info('Database exist')
    else:
        db.create_data_base()

        with open('create_tables.sql', 'r') as s:
            sql = s.read()

        db.execute_sql(sql)


def read_config():
    configs = {

        'camera': cameraController.consult()[0],
        'communication': communicationController.consult()[0],
        'project': projectController.consult()[0],
        'user': userController.consult()[0],
        'wifi': wifiController.consult()[0]
    }

    return configs


# analise
def gen():
    configs = read_config()

    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, img = cap.read()
        if ret:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = imutils.resize(img, width=configs['camera'].resize_image)

            code = read_qr(frame=img)

            if code != '':
                logger.debug('Code: {}'.format(code))
                cv2.putText(img, code, (25, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            0.8, (255, 255, 255), 1)

            frame = cv2.imencode('.jpg', img)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            sleep(0.1)
        else:
            break


@app.route('/reboot_system')
@login_required
def reboot_system():
    logger.info('Reboot System')
    os.system('sudo reboot')

    return render_template('index.html')


@app.route('/download')
@login_required
def download_database():
    f = './config.db'

    return send_file(f, as_attachment=True)


@login_manager.user_loader
def load_user(user_id):
    configs = read_config()
    return configs['user']


@app.route('/login', methods=['GET', 'POST'])
def login():
    configs = read_config()

    if request.method == "POST":
        data = request.form

        if data['user'] == configs['user'].name and data["password"] == configs['user'].password:

            login_user(configs['user'])
            flash("Welcome {}!".format(data['user']))

            return render_template('dashboard.html', configs=configs)

        else:
            flash("Invalid user or password.")
            return render_template('index.html')

    return render_template('index.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('index.html')


@app.route('/camera', methods=['GET', 'POST'])
@login_required
def update_camera():
    configs = read_config()

    if request.method == "POST":
        data = request.form

        camera = Camera(camera_id=data["id"], station_id=data["station_id"], show_image=data["show_image"],
                        resize_image=data["resize_image"], width=data["width"], height=data["height"], fps=data["fps"])

        cameraController.update(camera)

        configs = read_config()

        flash("changes saved successfully :)")

        return render_template('camera.html', configs=configs)

    return render_template('camera.html', configs=configs)


@app.route('/serial', methods=['GET', 'POST'])
@login_required
def update_communication():
    configs = read_config()

    if request.method == "POST":
        data = request.form

        communication = Communication(communication_id=data["id"], port=data["port"], baudrate=data["baudrate"],
                                      timeout=data["timeout"],
                                      preamble=data["preamble"])

        communicationController.update(communication)

        configs = read_config()

        flash("changes saved successfully :)")

        return render_template('serial.html', configs=configs)

    return render_template('serial.html', configs=configs)


@app.route('/wifi', methods=['GET', 'POST'])
@login_required
def update_wifi():
    configs = read_config()

    if request.method == "POST":
        data = request.form

        wifi = Wifi(wifi_id=data["id"], name=data["name"], password=data["password"])

        wifiController.update(wifi)

        configs = read_config()

        flash("changes saved successfully :)")

        return render_template('wifi.html', configs=configs)

    return render_template('wifi.html', configs=configs)


@app.route('/video_feed')
@login_required
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/<pagename>')
@login_required
def admin(pagename):
    configs = read_config()

    return render_template(pagename, configs=configs)


@app.route('/<path:resource>')
def serveStaticResource(resource):
    return send_from_directory('static/', resource)


@app.errorhandler(jinja2.exceptions.TemplateNotFound)
def template_not_found(e):
    return not_found(e)


@app.errorhandler(404)
@login_required
def not_found(e):
    configs = read_config()
    return render_template('404.html', configs=configs)


@app.errorhandler(401)
def unauthorized(e):
    flash('Unauthorized access.')
    return render_template('index.html')


if __name__ == '__main__':
    check_database()
    app.run(host='0.0.0.0', debug=True)
