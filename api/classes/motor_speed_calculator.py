from . import constants


class MotorAbstraction:
    def __init__(self):
        self.speed = 0

    def forward_increase(self, turning=True):
        self.speed = ForwardMotorCommands.increase_speed(self.speed, turning)

    def forward_decrease(self, turning=True):
        self.speed = ForwardMotorCommands.decrease_speed(self.speed, turning)

    def reverse_increase(self, turning=True):
        self.speed = ReverseMotorCommands.increase_speed(self.speed, turning)

    def reverse_decrease(self, turning=True):
        self.speed = ReverseMotorCommands.decrease_speed(self.speed, turning)


class LeftMotor(MotorAbstraction):
    pass


class RightMotor(MotorAbstraction):
    pass

STRAIGHT_SPEED_INCREMENT = constants.SPEED_INCREMENT
TURNING_SPEED_INCREMENT = STRAIGHT_SPEED_INCREMENT / 2


class ForwardMotorCommands:
    @staticmethod
    def increase_speed(speed, turning):
        incremental_speed = TURNING_SPEED_INCREMENT if turning is True else STRAIGHT_SPEED_INCREMENT
        speed += incremental_speed
        return speed

    @staticmethod
    def decrease_speed(speed, turning):
        incremental_speed = TURNING_SPEED_INCREMENT if turning is True else STRAIGHT_SPEED_INCREMENT
        speed -= incremental_speed
        return speed


class ReverseMotorCommands:
    @staticmethod
    def increase_speed(speed, turning):
        incremental_speed = TURNING_SPEED_INCREMENT if turning is True else STRAIGHT_SPEED_INCREMENT
        speed -= incremental_speed
        return speed

    @staticmethod
    def decrease_speed(speed, turning):
        incremental_speed = TURNING_SPEED_INCREMENT if turning is True else STRAIGHT_SPEED_INCREMENT
        speed += incremental_speed
        return speed


class MotorSpeedCalculator:
    def __init__(self):
        self._speed_increment = constants.SPEED_INCREMENT
        self.left_motor = LeftMotor()
        self.right_motor = RightMotor()

    def equalise_speed(self, operation='max'):
        if operation == 'max':
            speed = max(self.left_motor.speed, self.right_motor.speed)
        else:
            speed = min(self.left_motor.speed, self.right_motor.speed)

        self.left_motor.speed = self.right_motor.speed = speed

    def increase_forward_speed(self):
        self.left_motor.forward_increase(False)
        self.right_motor.forward_increase(False)

    def decrease_forward_speed(self):
        self.left_motor.forward_decrease(False)
        self.right_motor.forward_decrease(False)

    def increase_reverse_speed(self):
        self.left_motor.reverse_increase(False)
        self.right_motor.reverse_increase(False)

    def decrease_reverse_speed(self):
        self.left_motor.reverse_decrease(False)
        self.right_motor.reverse_decrease(False)

    def move_more_forward_right(self):
        self.left_motor.forward_increase()
        self.right_motor.forward_decrease()

    def move_more_forward_left(self):
        self.left_motor.forward_decrease()
        self.right_motor.forward_increase()

    def move_more_reverse_left(self):
        self.left_motor.reverse_decrease()
        self.right_motor.reverse_increase()

    def move_more_reverse_right(self):
        self.left_motor.reverse_increase()
        self.right_motor.reverse_decrease()

    def move_more_inplace_left(self):
        self.left_motor.reverse_increase(False)
        self.right_motor.forward_increase(False)

    def move_more_inplace_right(self):
        self.left_motor.forward_increase(False)
        self.right_motor.reverse_increase(False)

    def move_less_inplace_right(self):
        self.left_motor.forward_decrease(False)
        self.right_motor.reverse_decrease(False)

    def move_less_inplace_left(self):
        self.left_motor.reverse_decrease(False)
        self.right_motor.forward_decrease(False)

    # absolute drive commands
    def reverse(self):
        self.left_motor.speed = self.right_motor.speed = (-1 * self._speed_increment)

    def move_forward(self):
        self.left_motor.speed = self.right_motor.speed = self._speed_increment

    def move_inplace_left(self):
        self.left_motor.speed = -1 * self._speed_increment
        self.right_motor.speed = self._speed_increment

    def move_inplace_right(self):
        self.left_motor.speed = self._speed_increment
        self.right_motor.speed = -1 * self._speed_increment
