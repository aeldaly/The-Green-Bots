from expects import equal, expect
import os
import sys

parent = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent)

from classes.direction_resolver import DirectionResolver


def test_forward():
    expect(DirectionResolver().resolve(50, 50)).to(equal('F'))


def test_forward_right():
    expect(DirectionResolver().resolve(70, 50)).to(equal('FR'))


def test_forward_left():
    expect(DirectionResolver().resolve(50, 70)).to(equal('FL'))


def test_reverse():
    expect(DirectionResolver().resolve(-50, -50)).to(equal('Rv'))


def test_reverse_right():
    expect(DirectionResolver().resolve(-50, -70)).to(equal('RvR'))


def test_reverse_left():
    expect(DirectionResolver().resolve(-70, -50)).to(equal('RvL'))


def test_right():
    expect(DirectionResolver().resolve(50, -50)).to(equal('R'))


def test_left():
    expect(DirectionResolver().resolve(-50, 50)).to(equal('L'))
