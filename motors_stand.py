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

motor_base = cylinder(d = MOTOR_DIAMETER, h = 70)
motor_shaft = cylinder(d = 7, h = 10)
motor_hole = cylinder(d = 3.5, h = 10)

motor = (
    translate([0, 0, -10])(motor_shaft)
    + translate([0, 8.5, -10])(motor_hole)
    + translate([0, -8.5, -10])(motor_hole)  
    + motor_base
    )

outer_width = MOTOR_DIAMETER + (WALL_WIDTH * 2)

outer_case = (
    translate([0, 0, -WALL_WIDTH])(cylinder(d = outer_width, h = HALF_HEIGHT))
    + translate([-outer_width/2.0, 0, -WALL_WIDTH])(cube([outer_width, outer_width/2.0, HALF_HEIGHT]))
    + translate([-30/2.0, outer_width/2.0 - WALL_WIDTH, -WALL_WIDTH])(cube([30, WALL_WIDTH, HALF_HEIGHT]))
)

cylindrical_case = (
    outer_case
    - motor
    - translate([-MOTOR_DIAMETER/2.0, 0, 0])(cube([MOTOR_DIAMETER, MOTOR_DIAMETER/2.0 + 0.5, HALF_HEIGHT]))
    - translate([-MOTOR_DIAMETER/2.0, 0, 5])(cube([MOTOR_DIAMETER, 20, HALF_HEIGHT]))
    )

full_holder = rotate([90, 0, 90])(translate([0, 0, WALL_WIDTH])(
    cylindrical_case
    + translate([0, 0, HALF_HEIGHT * 2 - WALL_WIDTH * 2])(rotate([180, 0, 180])(cylindrical_case))
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
    + translate([0, 0, -20])(cylinder(d = 3.5, h = 20))
)

def lower_stand_leg(hole_placeholders = False):

    if hole_placeholders is True:
        return (
            stand_leg
            + translate([STAND_LEG_WIDTH / 2.0, STAND_LEG_WIDTH / 2.0, STAND_LEG_HEIGHT])(mount_hole)
            + translate([STAND_LEG_DEPTH - STAND_LEG_WIDTH / 2.0, STAND_LEG_WIDTH / 2.0, STAND_LEG_HEIGHT])(mount_hole)
        )
    else:    
        return (
            stand_leg
            - translate([STAND_LEG_WIDTH / 2.0, STAND_LEG_WIDTH / 2.0, STAND_LEG_HEIGHT])(mount_hole)
            - translate([STAND_LEG_DEPTH - STAND_LEG_WIDTH / 2.0, STAND_LEG_WIDTH / 2.0, STAND_LEG_HEIGHT])(mount_hole)
        )

inner_mount_hole = (
    translate([-3, -10, 0])(cube([6, 20, 3]))
    + translate([0, 0, -20])(cylinder(d = 3.5, h = 27))
)

def upper_stand_leg(hole_placeholders = False):
    leg_base = cube([STAND_DEPTH, STAND_DEPTH, 35.25])

    if hole_placeholders is True:
        return (
            cube([STAND_DEPTH, STAND_DEPTH, 35.25])
            + translate([STAND_DEPTH/2, STAND_DEPTH/2, 29.5])(cylinder(d = 3.5, h = 100))
        )
    else:
        return (
            cube([STAND_DEPTH, STAND_DEPTH, 35.25])
            - translate([STAND_DEPTH/2, STAND_DEPTH/2, 29.5])(inner_mount_hole)
        )          

def stand(hole_placeholders = False): 
    return color("red")(
        cube([STAND_DEPTH, STAND_WIDTH, STAND_HEIGHT])
        + translate([-STAND_LEG_DEPTH / 2.0 + STAND_DEPTH / 2.0, 0, 0])(lower_stand_leg(hole_placeholders))
        + translate([-STAND_LEG_DEPTH / 2.0 + STAND_DEPTH / 2.0, STAND_WIDTH - STAND_LEG_WIDTH, 0])(lower_stand_leg(hole_placeholders))
        + translate([0, 0, STAND_HEIGHT])(upper_stand_leg(hole_placeholders))
        + translate([0, 38.75, STAND_HEIGHT])(upper_stand_leg(hole_placeholders))    
        )

def stand_full(hole_placeholders = False): 
    return (
        translate([0, - STAND_WIDTH/2.0, - STAND_HEIGHT/2.0 - (STAND_HEIGHT - outer_width)/2 - WALL_WIDTH])(stand(hole_placeholders))
        - rotate([90, 0, 90])(outer_case)    
    )

def generate_full(hole_placeholders = False):
    return translate([0, -70, 22.5])(rotate([0, 0, 90])((
        translate([10, 0, 0])(stand_full(hole_placeholders))
        + translate([120, 0, 0])(stand_full(hole_placeholders))
        + full_holder
    )))

full = generate_full()

full_for_holes = generate_full(True)