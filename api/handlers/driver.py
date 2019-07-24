import tornado.websocket
import json


class DriverHandler(tornado.websocket.WebSocketHandler):
    clients = set()

    def check_origin(self, origin):
        # Allow access from every origin
        return True

    def open(self):
        DriverHandler.clients.add(self)
        print("WebSocket opened from: " + self.request.remote_ip)

    def on_message(self, message):
        print('Receiveed msg from Driver Websocket: %s' % message)
        if message == 'forward':
            self.application.driver.forward()
        elif message == 'reverse':
            self.application.driver.reverse()
        elif message == 'left':
            self.application.driver.left()
        elif message == 'right':
            self.application.driver.right()
        elif message == 'stop':
            self.application.driver.stop()
        self.write_message(json.dumps(message))

    def on_close(self):
        DriverHandler.clients.remove(self)
        print("WebSocket closed from: " + self.request.remote_ip)
        if len(DriverHandler.clients) == 0:
            self.application.driver.stop()
