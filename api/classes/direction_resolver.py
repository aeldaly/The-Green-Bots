

class DirectionResolver:
    _FORWARD_DIRECTION = 'F'
    _FORWARD_RIGHT_DIRECTION = 'FR'
    _FORWARD_LEFT_DIRECTION = 'FL'
    
    _REVERSE_DIRECTION = 'Rv'
    _REVERSE_RIGHT_DIRECTION = 'RvR'
    _REVERSE_LEFT_DIRECTION = 'RvL'

    _RIGHT_DIRECTION = 'R'
    _LEFT_DIRECTION = 'L'

    def __init__(self):
        self._ml_speed = 0
        self._mr_speed = 0

    def _resolve_forward_direction(self):
        diff = self._ml_speed - self._mr_speed
        if diff == 0:
            self.direction = DirectionResolver._FORWARD_DIRECTION   
        elif diff < 0:
            self.direction = DirectionResolver._FORWARD_LEFT_DIRECTION
        else:
            self.direction = DirectionResolver._FORWARD_RIGHT_DIRECTION

    def _resolve_reverse_direction(self):
        diff = self._ml_speed - self._mr_speed
        if diff == 0:
            self.direction = DirectionResolver._REVERSE_DIRECTION
        elif diff < 0:
            self.direction = DirectionResolver._REVERSE_LEFT_DIRECTION
        else:
            self.direction = DirectionResolver._REVERSE_RIGHT_DIRECTION

    def _resolve_in_place_direction(self):
        if self._ml_speed < 0:
            self.direction = DirectionResolver._LEFT_DIRECTION
        else:
            self.direction = DirectionResolver._RIGHT_DIRECTION

    def resolve(self, motor_left_speed, motor_right_speed):
        self._ml_speed = motor_left_speed
        self._mr_speed = motor_right_speed

        if self._ml_speed > 0 and self._mr_speed > 0:
            self._resolve_forward_direction()
        elif self._ml_speed < 0 and self._mr_speed < 0:
            self._resolve_reverse_direction()
        else:
            self._resolve_in_place_direction()

        return self.direction
