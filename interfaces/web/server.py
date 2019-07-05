import argparse
import json
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os.path
import subprocess
import netifaces
from tornado.options import define, options
from wifi import Cell, Scheme
from datetime import datetime


CONFIG_FILE = '/var/www/config/config.json'
EVENTS_FILE = '/var/www/logs/events.log'


class Application(tornado.web.Application):
    def __init__(self, model):
        self.model = model
        handlers = [
            (r"/server/system", SystemHandler),
            (r"/server/wifi-status", WifiStatusHandler),
            (r"/server/wifi", WifiHandler),
            (r"/server/logs", LogHandler),
            (r"/server/events", EventHandler),
            (r"/server/intelligence", IntelligenceHandler),
        ]
        tornado.web.Application.__init__(self, handlers)


class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')


def add_event(new_line):
    with open(EVENTS_FILE, 'a+') as events_file:
        events_file.write(datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S.%f") + ' - ' + str(new_line) + '\n')


def update_config_file(new_dict):
    '''
    Schema:
        {
            'wifi': {
                'ssid': '',
                'password': ''
            },
            'intelligence': {
                'voice-command': True,
                'autonomous-driving': True,
                'nightvision-camera': True,
                'ultrasonic-distance-meter': True,
            }
        }
    '''
    add_event('Updated Config File...')
    with open(CONFIG_FILE, 'r+') as config_file:
        data = json.load(config_file)
        for k, v in new_dict.items():
            data[k] = v
        config_file.seek(0)
        json.dump(data, config_file, indent=4)
        config_file.truncate()


def get_config_file():
    config = {}
    with open(CONFIG_FILE, 'r') as config_f:
        config = json.load(config_f)
    return config


def cmd(command):
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    log, _err = proc.communicate()
    try:
        log = log.decode("utf-8")
    except Exception as e:
        return e
    else:
        return log


def tail(filename, lines=20):
    return cmd(['tail', '-%d' % lines, filename])


class LogHandler(BaseHandler):
    def get(self):
        self.write(json.dumps(tail('/var/log/syslog', lines=100)))


class EventHandler(BaseHandler):
    def get(self):
        self.write(json.dumps(tail(EVENTS_FILE)))


class IntelligenceHandler(BaseHandler):
    def get(self):
        config = get_config_file()
        self.write(json.dumps(config.get('intelligence')))

    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        print(data)
        intelligence_conf = {
            'intelligence': {
                'voice-command': data.get('voice-command', False) == 'on',
                'autonomous-driving': data.get('autonomous-driving', False) == 'on',
                'nightvision-camera': data.get('nightvision-camera', False) == 'on',
                'ultrasonic-distance-meter': data.get('ultrasonic-distance-meter', False) == 'on',
            }
        }
        add_event(intelligence_conf)
        update_config_file(intelligence_conf)


class SystemHandler(BaseHandler):
    def get(self):
        self.write(json.dumps(os.uname()))

    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        if data['command'] == 'shutdown':
            self._shutdown()
        elif data['command'] == 'reboot':
            self._reboot()
        elif data['command'] == 'reset_factory':
            self._reset_factory()

    def _shutdown(self):
        add_event('Shutting Down')
        cmd(['shutdown', '-h', 'now'])

    def _reboot(self):
        add_event('Rebooting')
        cmd(['reboot'])

    def _reset_factory(self):
        add_event('Restarting to Factory')
        print('Reset to Factory...')


class WifiStatusHandler(BaseHandler):
    def get(self):
        access_point_mode = True
        connected = True
        if not access_point_mode and connected:
            self.write(json.dumps({
                'access_point_mode': False,
                'ssid': 'GET IT FROM /etc/netplan/wireless.yaml'
            }))
        elif access_point_mode:
            self.write(json.dumps({
                'access_point_mode': True,
                'ssid': 'TheGreenBot'
            }))


class WifiHandler(BaseHandler):
    WIRELESS_YAML_TEMPLATE = '''
network:
  version: 2
  renderer: networkd
  wifis:
    wlan0:
      dhcp4: yes
      dhcp6: yes
      access-points:
        "%(ssid)s":
          password: "%(password)s"
'''

    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        add_event('Connecting to WiFi: %s' % data['ssid'])
        update_config_file({
            'wifi': {
                'ssid': data['ssid'],
                'password': data['password'],
            }
        })
        new_ip = self.configure_netplan(data)
        self.write(json.dumps(new_ip))


    def get(self):
        wifis = Cell.all('wlan0')
        SSIDs = [wifi.ssid for wifi in wifis]
        self.write(json.dumps(SSIDs))

    def configure_netplan(self, data):
        wireless_yaml = WifiHandler.WIRELESS_YAML_TEMPLATE.format(data)
        with open('/etc/netplan/wireless.yaml', 'w+') as wirelesss_yaml_f:
            wirelesss_yaml_f.write(wireless_yaml)
            cmd(['netplan', 'generate'])
            cmd(['netplan', 'apply'])
            ip = netifaces.ifaddresses('wlan0')[netifaces.AF_INET][0]['addr']
            return ip
        

def main(args):
    http_server = tornado.httpserver.HTTPServer(Application({}))
    http_server.listen(args.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Web Interface Server')

    parser.add_argument('--port', type=int, help="port to run on. Must be supplied.")
    args = parser.parse_args()
    main(args)
