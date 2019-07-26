import RPi.GPIO as GPIO


class Motor:
    def __init__(self, pins, frequency=20):
        self.frequency = frequency
        GPIO.setmode(GPIO.BCM)

        self.forward_pin = pins['forward']
        self.reverse_pin = pins['reverse']
        self.control_pin = pins['control']

        GPIO.setup(self.forward_pin, GPIO.OUT)
        GPIO.setup(self.reverse_pin, GPIO.OUT)
        GPIO.setup(self.control_pin, GPIO.OUT)

        self._speed = GPIO.PWM(self.control_pin, frequency)

    def _clip(self, value, minimum=0, maximum=100):
        """Ensure value is between minimum and maximum."""

        if value < minimum:
            return minimum
        elif value > maximum:
            return maximum
        return value

    def _set_speed(self, speed):
        self._speed.start(speed)

    def stop(self):
        self._speed.start(0)

    def forward(self, speed_percent=100):
        speed = self._clip(abs(speed_percent))
        self._set_speed(speed)

        GPIO.output(self.forward_pin, GPIO.HIGH)
        GPIO.output(self.reverse_pin, GPIO.LOW)

        return speed

    def reverse(self, speed_percent=100):
        speed = self._clip(abs(speed_percent))
        self._set_speed(speed)

        GPIO.output(self.forward_pin, GPIO.LOW)
        GPIO.output(self.reverse_pin, GPIO.HIGH)

        return speed
