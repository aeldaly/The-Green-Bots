import argparse
import json
import tornado.httpserver, tornado.ioloop, tornado.options, tornado.web, os.path
from tornado.options import define, options
from wifi import Cell, Scheme
from datetime import datetime


define("port", default=8000, help="run on the given port", type=int)
CONFIG_FILE = '../../config/config.json'
EVENTS_FILE = '../../logs/events.log'

class Application(tornado.web.Application):
    def __init__(self, model):
        self.model = model
        handlers = [
            (r"/system", SystemHandler),
            (r"/wifi-status", WifiStatusHandler),
            (r"/wifi", WifiHandler),
            (r"/logs", LogHandler),
            (r"/events", EventHandler),
            (r"/intelligence", IntelligenceHandler),
        ]
        tornado.web.Application.__init__(self, handlers)

class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

def add_event(new_line):
    with open(EVENTS_FILE, 'a+') as events_file:
        events_file.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")+ ' - ' + str(new_line) + '\n')

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
        for k,v in new_dict.items():
            data[k] = v
        config_file.seek(0)
        json.dump(data, config_file, indent=4)
        config_file.truncate()


def get_config_file():
    config = {}
    with open(CONFIG_FILE, 'r') as config_f:
        config = json.load(config_f)
    return config


def tail(f, lines=20):
    total_lines_wanted = lines

    BLOCK_SIZE = 1024
    f.seek(0, 2)
    block_end_byte = f.tell()
    lines_to_go = total_lines_wanted
    block_number = -1
    blocks = [] # blocks of size BLOCK_SIZE, in reverse order starting
                # from the end of the file
    while lines_to_go > 0 and block_end_byte > 0:
        if (block_end_byte - BLOCK_SIZE > 0):
            # read the last block we haven't yet read
            f.seek(block_number*BLOCK_SIZE, 2)
            blocks.append(f.read(BLOCK_SIZE))
        else:
            # file too small, start from begining
            f.seek(0,0)
            # only read what was not read
            blocks.append(f.read(block_end_byte))
        lines_found = blocks[-1].count('\n')
        lines_to_go -= lines_found
        block_end_byte -= BLOCK_SIZE
        block_number -= 1
    all_read_text = ''.join(reversed(blocks))
    return '\n'.join(all_read_text.splitlines()[-total_lines_wanted:])


class LogHandler(BaseHandler):
    def get(self):
        # syslog_f = open('/var/log/syslog', 'r') # linux
        syslog_f = open('/var/log/system.log', 'r') # mac TEST
        self.write(json.dumps(tail(syslog_f, lines=100)))

class EventHandler(BaseHandler):
    def get(self):
        event_f = open(EVENTS_FILE, 'r')
        self.write(json.dumps(tail(event_f, lines=20)))


class IntelligenceHandler(BaseHandler):
    def get(self):
        config = get_config_file()
        self.write(json.dumps(config['intelligence']))

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
        print('Shutting down...')

    def _reboot(self):
        add_event('Rebooting')
        print('Rebooting...')

    def _reset_factory(self):
        add_event('Restarting to Factory')
        print('Reset to Factory...')

class WifiStatusHandler(BaseHandler):
    def get(self):
        access_point_mode = True
        connected = True
        if not access_point_mode and connected:
            status = '''
<p>
Status: <span data-feather="cloud" style="color:green;">Connected</span><br><br>
You can access your Green Bot web interface by clicking on:<br> <a href="http://thegreenbot" style="color:green;">http://thegreenbot</a>
</p>
'''
        elif access_point_mode:
            status = '''
<p>
Status: <span data-feather="cloud-off" style="color:orange;">Access Point Mode</span><br><br>
You can access your Green Bot web interface by clicking on:<br> <a href="http://thegreenbot" style="color:green;">http://thegreenbot</a>
</p>
'''
        self.write(status)

class WifiHandler(BaseHandler):

    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        add_event('Connecting to WiFi: %s' % data['ssid'])
        update_config_file({
            'wifi': {
                'ssid': data['ssid'],
                'password': data['password'],
            }
        })
        print(data)
        # scheme = Scheme.find('wlan0', ssid_name)
        # scheme.save()
        # scheme.activate()
        self.write(json.dumps({
        }))
    
    def get(self):
        # wifis = Cell.all('wlan0')
        # print(wifis)
        wifis = [
            'BELL884-ng5',
            'home'
        ]
        self.write(json.dumps(wifis))


def main(args):
    http_server = tornado.httpserver.HTTPServer(Application({}))
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Web Interface Server')
    args = parser.parse_args()
    main(args)

