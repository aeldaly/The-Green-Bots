from . import constants
from .motor import Motor
from .direction_resolver import DirectionResolver
from .speed_resolver import SpeedResolver


class Driver:
    _SPEED_INCREMENT = 10

    def __init__(self, left_motor_pins, right_motor_pins):
        # Assign pins to motors.
        self._left_motor = Motor(left_motor_pins)
        self._right_motor = Motor(right_motor_pins)

        self.direction_resolver = DirectionResolver()
        self.speed_resolver = SpeedResolver(Driver._SPEED_INCREMENT)

        self.stop()

    def _current_direction(self):
        ml = self._state['left_speed']
        mr = self._state['right_speed']

        return self.direction_resolver.resolve(ml, mr)

    def _set_speed(self, target_action):
        speeds = self.speed_resolver.resolve(self._state, target_action)
        self._set_state(speeds['left_motor_speed'],
                        speeds['right_motor_speed'])

    def _set_state(self, left_speed, right_speed):
        self._state = {
            'left_speed': left_speed,
            'right_speed': right_speed
        }

        self._state['current_direction'] = self._current_direction()

        return self._state

    def stop(self):
        self._left_motor.move(0)
        self._right_motor.move(0)

        return self._set_state(0, 0)

    def forward(self):
        self._set_speed(constants.TARGET_ACTION_FORWARD)

        return self._state

    def reverse(self):
        self._set_speed(constants.TARGET_ACTION_REVERSE)

        return self._state

    def left(self):
        self._set_speed(constants.TARGET_ACTION_LEFT)

        return self._state

    def right(self):
        self._set_speed(constants.TARGET_ACTION_RIGHT)

        return self._state

    # def _velocity_received_callback(self, message):
    #     """Handle new velocity command message."""

    #     self._last_received = rospy.get_time()

    #     # Extract linear and angular velocities from the message
    #     linear = message.linear.x
    #     angular = message.angular.z

    #     # Calculate wheel speeds in m/s
    #     left_speed = linear - angular*self._wheel_base/2
    #     right_speed = linear + angular*self._wheel_base/2

    #     # Ideally we'd now use the desired wheel speeds along
    #     # with data from wheel speed sensors to come up with the
    #     # power we need to apply to the wheels, but we don't have
    #     # wheel speed sensors. Instead, we'll simply convert m/s
    #     # into percent of maximum wheel speed, which gives us a
    #     # duty cycle that we can apply to each motor.
    #     self._left_speed_percent = (100 * left_speed/self._max_speed)
    #     self._right_speed_percent = (100 * right_speed/self._max_speed)

    # def run(self):
    #     """The control loop of the driver."""

    #     rate = rospy.Rate(self._rate)

    #     while not rospy.is_shutdown():
    #         # If we haven't received new commands for a while, we
    #         # may have lost contact with the commander-- stop
    #         # moving
    #         delay = rospy.get_time() - self._last_received
    #         if delay < self._timeout:
    #             self._left_motor.move(self._left_speed_percent)
    #             self._right_motor.move(self._right_speed_percent)
    #         else:
    #             self._left_motor.move(0)
    #             self._right_motor.move(0)

    #         rate.sleep()
