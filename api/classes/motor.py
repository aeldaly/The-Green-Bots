import RPi.GPIO as GPIO


class Motor:
    def __init__(self, pins):
        GPIO.setmode(GPIO.BCM)

        [forward_pin, backward_pin, control_pin] = pins

        GPIO.setup(forward_pin, GPIO.OUT)
        GPIO.setup(backward_pin, GPIO.OUT)
        GPIO.setup(self.control_pin, GPIO.OUT)

        self._FREQUENCY = 20

        self._forward_pwm = GPIO.PWM(forward_pin, _FREQUENCY)
        self._backward_pwm = GPIO.PWM(backward_pin, _FREQUENCY)
        self._speed = GPIO.PWM(self.control_pin, _FREQUENCY)

    def _clip(value, minimum, maximum):
    """Ensure value is between minimum and maximum."""

    if value < minimum:
        return minimum
    elif value > maximum:
        return maximum
    return value

    def move(self, speed_percent):
        speed = _clip(abs(speed_percent), 0, 100)

        # Positive speeds move wheels forward
        # Negative speeds move wheels backward
        if speed_percent < 0:
            self._backward_pwm.start(speed)
            self._forward_pwm.start(0)
        else:
            self._forward_pwm.start(speed)
            self._backward_pwm.start(0)
