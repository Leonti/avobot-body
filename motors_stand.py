#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import os
import sys

from solid import *
from solid.utils import *

nuts_n_bolts = import_scad('/home/leonti/3d/openscad_libraries/nutsnbolts')

MOTOR_DIAMETER = 25.2
WALL_WIDTH = 1.75
HALF_HEIGHT = 70

motor_base = cylinder(d=MOTOR_DIAMETER, h=70)
motor_shaft = cylinder(d=7, h=10)
motor_hole = cylinder(d=3.5, h=10)

motor = (
    translate([0, 0, -10])(motor_shaft)
    + translate([0, 8.5, -10])(motor_hole)
    + translate([0, -8.5, -10])(motor_hole)
    + motor_base
)
# 8mm longer for cutouts
def stepper_motor(hole_placeholders=False):
    width = 42.6 if hole_placeholders is True else 42
    length = 46.7 if hole_placeholders is True else 38.7

    hole = cylinder(d = 3.5, h = 20)
    holes = translate([-31/2, -31/2, 30])(
      #  hole
         translate([31, 31, 0])(hole)
      #  + translate([31, 0, 0])(hole)
        + translate([0, 31, 0])(hole)
    )
    base = (
        translate([-width/2, -width/2, 0])(cube([width, width, length]))
        + cylinder(d = 22.5 if hole_placeholders is True else 22, h = 51 if hole_placeholders is True else 39.6)
        + cylinder(d = 5, h = 61.6)
        )
    if hole_placeholders is True:
        return base + holes + cylinder(d = 22.5, h = 39.6)
    else:
        return base - holes

outer_width = MOTOR_DIAMETER + (WALL_WIDTH * 2)

outer_case = (
    translate([0, 0, -WALL_WIDTH])(cylinder(d=outer_width, h=HALF_HEIGHT))
    + translate([-outer_width/2.0, 0, -WALL_WIDTH]
                )(cube([outer_width, outer_width/2.0, HALF_HEIGHT]))
    + translate([-30/2.0, outer_width/2.0 - WALL_WIDTH, -WALL_WIDTH]
                )(cube([30, WALL_WIDTH, HALF_HEIGHT]))
)

cylindrical_case = (
    outer_case
    + motor
    - translate([-MOTOR_DIAMETER/2.0, 0, 0]
                )(cube([MOTOR_DIAMETER, MOTOR_DIAMETER/2.0 + 0.5, HALF_HEIGHT]))
    - translate([-MOTOR_DIAMETER/2.0, 0, 5]
                )(cube([MOTOR_DIAMETER, 20, HALF_HEIGHT]))
)

full_holder = rotate([90, 0, 90])(translate([0, 0, WALL_WIDTH])(
    cylindrical_case
    + translate([0, 0, HALF_HEIGHT * 2 - WALL_WIDTH * 2]
                )(rotate([180, 0, 180])(cylindrical_case))
))

STAND_WIDTH = outer_width + 20
STAND_HEIGHT = outer_width + 3
STAND_DEPTH = 10

STAND_LEG_DEPTH = 30
STAND_LEG_WIDTH = 10
STAND_LEG_HEIGHT = 6

stand_leg = cube([STAND_LEG_DEPTH, STAND_LEG_WIDTH, STAND_LEG_HEIGHT])

mount_hole = (
    nuts_n_bolts.cyl_head_bolt.nutcatch_parallel("M3", l=2, clk=0.6)
    + translate([0, 0, -20])(cylinder(d=3.5, h=20))
)


def lower_stand_leg(hole_placeholders=False):

    if hole_placeholders is True:
        return (
            stand_leg
            + translate([STAND_LEG_WIDTH / 2.0, STAND_LEG_WIDTH /
                         2.0, STAND_LEG_HEIGHT])(mount_hole)
            + translate([STAND_LEG_DEPTH - STAND_LEG_WIDTH / 2.0,
                         STAND_LEG_WIDTH / 2.0, STAND_LEG_HEIGHT])(mount_hole)
        )
    else:
        return (
            stand_leg
            - translate([STAND_LEG_WIDTH / 2.0, STAND_LEG_WIDTH /
                         2.0, STAND_LEG_HEIGHT])(mount_hole)
            - translate([STAND_LEG_DEPTH - STAND_LEG_WIDTH / 2.0,
                         STAND_LEG_WIDTH / 2.0, STAND_LEG_HEIGHT])(mount_hole)
        )


inner_mount_hole = (
    translate([-3, -10, 0])(cube([6, 20, 3]))
    + translate([0, 0, -20])(cylinder(d=3.5, h=27))
)


def upper_stand_leg(hole_placeholders=False):
    leg_base = cube([STAND_DEPTH, STAND_DEPTH, 35.25])

    if hole_placeholders is True:
        return (
            cube([STAND_DEPTH, STAND_DEPTH, 35.25])
            + translate([STAND_DEPTH/2, STAND_DEPTH/2, 29.5]
                        )(cylinder(d=3.5, h=100))
        )
    else:
        return (
            cube([STAND_DEPTH, STAND_DEPTH, 35.25])
            - translate([STAND_DEPTH/2, STAND_DEPTH/2, 29.5])(inner_mount_hole)
        )

def stand(hole_placeholders=False):
    return color("red")(
        cube([STAND_DEPTH, STAND_WIDTH, STAND_HEIGHT])
        + translate([-STAND_LEG_DEPTH / 2.0 + STAND_DEPTH / 2.0,
                     0, 0])(lower_stand_leg(hole_placeholders))
        + translate([-STAND_LEG_DEPTH / 2.0 + STAND_DEPTH / 2.0, STAND_WIDTH -
                     STAND_LEG_WIDTH, 0])(lower_stand_leg(hole_placeholders))
        + translate([0, 0, STAND_HEIGHT])(upper_stand_leg(hole_placeholders))
        + translate([0, 38.75, STAND_HEIGHT]
                    )(upper_stand_leg(hole_placeholders))
    )



def stepper_motor_left(hole_placeholders=False):
    return translate([0, -10.5, 42/2 + 3.4])(rotate([90, 0, 0])(stepper_motor(hole_placeholders)))

def lower_stand_leg_stepper(hole_placeholders=False):
    stand_leg_stepper = cube([75, STAND_LEG_WIDTH, STAND_LEG_HEIGHT])
    if hole_placeholders is True:
        return (
            stand_leg_stepper
            + translate([STAND_LEG_WIDTH / 2.0, STAND_LEG_WIDTH /
                         2.0, STAND_LEG_HEIGHT])(mount_hole)
            + translate([65 - STAND_LEG_WIDTH / 2.0,
                         STAND_LEG_WIDTH / 2.0, STAND_LEG_HEIGHT])(mount_hole)
        )
    else:
        return (
            stand_leg_stepper
            - translate([STAND_LEG_WIDTH / 2.0, STAND_LEG_WIDTH /
                         2.0, STAND_LEG_HEIGHT])(mount_hole)
            - translate([75 - STAND_LEG_WIDTH / 2.0,
                         STAND_LEG_WIDTH / 2.0, STAND_LEG_HEIGHT])(mount_hole)
        )

motor_side_support = rotate([90, 0, 0])(linear_extrude(height=3.15)(
        polygon([
            [0, 0],
            [0, 45],
            [45, 0]
        ])
    ))

SELF_SCREW_DIAMETER = 3.1
stand_lidar_support = (
    cube([20, 10, 5])
    + translate([10, 0,  0])(rotate([270, 0, 0])(linear_extrude(height=10)(
        polygon([
            [0, 0],
            [0, 10],
            [10, 0]
        ])
    )))
    - translate([15, 5, -10])(cylinder(d = SELF_SCREW_DIAMETER, h = 30))
)

def stand_left(hole_placeholders=False):
    return color("magenta")(translate([STAND_WIDTH/2, -60, 3.4])(rotate([0, 0, 90])( # 90
        cube([STAND_DEPTH, STAND_WIDTH, STAND_HEIGHT + 14])
        + translate([-STAND_LEG_DEPTH / 2.0 + STAND_DEPTH / 2.0,
                     0, 0])(lower_stand_leg_stepper(hole_placeholders))
        + translate([-STAND_LEG_DEPTH / 2.0 + STAND_DEPTH / 2.0, STAND_WIDTH -
                     STAND_LEG_WIDTH, 0])(lower_stand_leg_stepper(hole_placeholders))
        + translate([0, 0, STAND_HEIGHT])(upper_stand_leg(hole_placeholders))
        + translate([0, 38.70, STAND_HEIGHT]
                    )(upper_stand_leg(hole_placeholders))
        + translate([0, 3.15, 0])(motor_side_support)
        + translate([0, 48.7, 0])(motor_side_support) 
        + translate([0, 0, 46])(stand_lidar_support)
        + translate([0, STAND_WIDTH - 10, 46])(stand_lidar_support)
    )))

def stand_full(hole_placeholders=False):
    return (
        translate([0, - STAND_WIDTH/2.0, - STAND_HEIGHT/2.0 - (STAND_HEIGHT -
                                                               outer_width)/2 - WALL_WIDTH])(stand(hole_placeholders))
        - rotate([90, 0, 90])(outer_case)
    )

def stand_full_steppers(hole_placeholders=False):
    return stand_left_full(hole_placeholders) + mirror([0, 1, 0])(stand_left_full(hole_placeholders))

def stand_left_full(hole_placeholders=False):
    return stand_left(hole_placeholders) - stepper_motor_left(True)

def generate_full(hole_placeholders=False):
    return translate([0, -70, 22.5])(rotate([0, 0, 90])((
        translate([10, 0, 0])(stand_full(hole_placeholders))
        + translate([120, 0, 0])(stand_full(hole_placeholders))
        + full_holder
    )))

full = generate_full()

full_for_holes = generate_full(True)

step_up = (cube([51.1, 28.4, 2.0])
    + translate([9, 0.8, 0])(cube([32, 27, 13.2]))
)

steppers_board_hole = cylinder(d = 3, h = 15)
steppers_board_holes = (
    steppers_board_hole
    + translate([0, 29.7, 0])(steppers_board_hole)
    + translate([45, 29.7, 0])(steppers_board_hole)
    + translate([45, 0, 0])(steppers_board_hole)
)

steppers_board = (cube([51.6, 35.2, 2.0])
    + translate([6, 2, 0])(cube([40, 31, 20]))
    + translate([(51.6 - 45)/2.0, (35.2 - 29.7) / 2.0, -7])(steppers_board_holes)
)

steppers_electronics = color("green")(translate([-(51.6 - 49)/2.0, 1.5, 0])(
    translate([0, (35.2 - 28.4)/2.0, 7])(step_up)
    + translate([0.5, 0, 15 + 7])(steppers_board)
))

steppers_case = (
    cube([49, 38, 25.7])
    - cube([12, 38, 6])
    - translate([49-12, 0, 0])(cube([12, 38, 6]))
    - translate([-1, 1.5, 7])(cube([60, 38-3, 50]))
    - translate([-1, (38-24)/2.0, 6])(cube([60, 24, 1.0]))
    + translate([0, 0, 7])(cube([49, 5.7, 3]))
    + translate([0, (38-5.2), 7])(cube([49, 5.2, 3]))
    + translate([(49 - 34)/2.0, 0, 20.5])(cube([34, 3.5, 5.2]))
    + translate([(49 - 34)/2.0, (38-3.5), 20.5])(cube([34, 3.5, 5.2]))
    + translate([0, 0, 23.85])(cube([5.3, 8, 1.9]))
    + translate([0, (38-8), 23.85])(cube([5.3, 8, 1.9]))
    - translate([49/2.0, 38/2, 5.4])(cylinder(d = 15, h = 0.8))
    - translate([49/2.0, 38/2, 5.4])(mount_hole)
) - steppers_electronics

testing_rig = translate([-STAND_WIDTH/2.0, -120/2, 71])(
    cube([STAND_WIDTH, 120, 1])
    + translate([STAND_WIDTH/2.0, 120/2, 0])(cylinder(d = 3, h = 20))
    - translate([(STAND_WIDTH - 25)/2.0, 0, -1])(cube([25, 50, 4]))
    - translate([(STAND_WIDTH - 25)/2.0, 120 - 50, -1])(cube([25, 50, 4]))
) - stand_full_steppers(True)

#full = stand_full_steppers() + testing_rig
full = stand_full_steppers(False)
#full = steppers_case #+ steppers_electronics
#full = lower_stand_leg_stepper()