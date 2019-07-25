from . import constants


class SpeedResolver:
    def __init__(self, speed_increment):
        self._speed_increment = speed_increment

    def _increase_forward_speed(self):
        self.ml_speed += self._speed_increment
        self.mr_speed += self._speed_increment

    def _decrease_forward_speed(self):
        self.ml_speed -= self._speed_increment
        self.mr_speed -= self._speed_increment

    def _increase_right_speed(self):
        self.ml_speed += self._speed_increment

    def _increase_left_speed(self):
        self.mr_speed += self._speed_increment

    def _decrease_right_speed(self):
        self.ml_speed -= self._speed_increment

    def _decrease_left_speed(self):
        self.mr_speed -= self._speed_increment

    def _equalise_speed(self, operation='max'):
        if operation == 'max':
            speed = max(self.ml_speed, self.mr_speed)
        else:
            speed = min(self.ml_speed, self.mr_speed)

        self.ml_speed = self.mr_speed = speed

    def _reverse(self):
        self.ml_speed = self.mr_speed = (-1 * self._speed_increment)

    def _move_forward(self):
        self.ml_speed = self.mr_speed = self._speed_increment

    def _move_forward_right(self):
        self.ml_speed = self._speed_increment
        self.mr_speed = 0

    def _move_forward_left(self):
        self.ml_speed = 0
        self.mr_speed = self._speed_increment

    def _resolve_forward_direction(self):
        if self._target_action == constants.TARGET_ACTION_FORWARD:
            self._increase_forward_speed()
        elif self._target_action == constants.TARGET_ACTION_REVERSE:
            self._decrease_forward_speed()
        elif self._target_action == constants.TARGET_ACTION_LEFT:
            self._increase_right_speed()
        else:
            self._increase_left_speed()

    def _resolve_forward_right_direction(self):
        if self._target_action == constants.TARGET_ACTION_FORWARD:
            self._equalise_speed()
        elif self._target_action == constants.TARGET_ACTION_REVERSE:
            self._reverse()
        elif self._target_action == constants.TARGET_ACTION_LEFT:
            self._increase_left_speed()
        else:
            self._increase_right_speed()

    def _resolve_forward_left_direction(self):
        if self._target_action == constants.TARGET_ACTION_FORWARD:
            self._equalise_speed()
        elif self._target_action == constants.TARGET_ACTION_REVERSE:
            self._reverse()
        elif self._target_action == constants.TARGET_ACTION_LEFT:
            self._increase_left_speed()
        else:
            self._increase_right_speed()

    def _resolve_right_direction(self):
        if self._target_action == constants.TARGET_ACTION_FORWARD:
            self._move_forward()
        elif self._target_action == constants.TARGET_ACTION_REVERSE:
            self._reverse()
        elif self._target_action == constants.TARGET_ACTION_LEFT:
            self._move_forward_left()
        else:
            self._move_forward_right()

    def _resolve_left_direction(self):
        if self._target_action == constants.TARGET_ACTION_FORWARD:
            self._move_forward()
        elif self._target_action == constants.TARGET_ACTION_REVERSE:
            self._reverse()
        elif self._target_action == constants.TARGET_ACTION_LEFT:
            self._move_forward_left()
        else:
            self._move_forward_right()

    def _resolve_reverse_direction(self):
        if self._target_action == constants.TARGET_ACTION_FORWARD:
            self._move_forward()
        elif self._target_action == constants.TARGET_ACTION_REVERSE:
            self._decrease_forward_speed()
        elif self._target_action == constants.TARGET_ACTION_LEFT:
            self._decrease_right_speed()
        else:
            self._decrease_left_speed()

    def _resolve_reverse_right_direction(self):
        if self._target_action == constants.TARGET_ACTION_FORWARD:
            self._move_forward()
        elif self._target_action == constants.TARGET_ACTION_REVERSE:
            self._equalise_speed('min')
        elif self._target_action == constants.TARGET_ACTION_LEFT:
            self._decrease_right_speed()
        else:
            self._decrease_left_speed()

    def _resolve_reverse_left_direction(self):
        if self._target_action == constants.TARGET_ACTION_FORWARD:
            self._move_forward()
        elif self._target_action == constants.TARGET_ACTION_REVERSE:
            self._equalise_speed('min')
        elif self._target_action == constants.TARGET_ACTION_LEFT:
            self._decrease_left_speed()
        else:
            self._decrease_right_speed()

    def resolve(self, state, target_action):
        self._target_action = target_action
        current_direction = state['current_direction']
        self.ml = state['left_motor']
        self.ml = state['right_motor']

        if current_direction == constants.DIRECTION_FORWARD:
            self._resolve_forward_direction()
        elif current_direction == constants.DIRECTION_FORWARD_RIGHT:
            self._resolve_forward_right_direction()
        elif current_direction == constants.DIRECTION_FORWARD_LEFT:
            self._resolve_forward_left_direction()
        elif current_direction == constants.DIRECTION_REVERSE:
            self._resolve_reverse_direction()
        elif current_direction == constants.DIRECTION_REVERSE_RIGHT:
            self._resolve_reverse_right_direction()
        elif current_direction == constants.DIRECTION_REVERSE_LEFT:
            self._resolve_reverse_left_direction()
        elif current_direction == constants.DIRECTION_RIGHT:
            self._resolve_right_direction()
        else:
            self._resolve_left_direction()

        return {
            'left_motor_speed': self.ml_speed,
            'right_motor_speed': self.mr_speed
        }
