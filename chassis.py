#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import os
import sys

from solid import *
from solid.utils import *
import bumper
import cover
import motors_stand
import electronics
import mounts

nuts_n_bolts = import_scad('/home/leonti/3d/openscad_libraries/nutsnbolts')
rplidar = import_stl('rplidar.stl')

SEGMENTS = 200

ACRYLIC_HEIGHT = 3

wheel_cutout_right = translate([-35, 70, -1])(cube([70, 40, 5]))
acrylic_base = color([1.0, 1.0, 1.0, 0.9])(
    cylinder(d = 208, h = ACRYLIC_HEIGHT)
    - wheel_cutout_right
    - mirror([0, 1, 0])(wheel_cutout_right)
    - cover.for_holes 
    - motors_stand.full_for_holes
    - bumper.for_holes
    )
wheel = color("blue")(cylinder(d = 67, h = 27))
diff_drive = (
    translate([0, (177 + 27) / 2.0, 22.5])(rotate([90, 0, 0])(wheel + translate([0, 0, 177])(wheel)))
    + motors_stand.full
)

usb_connector = cube([18, 35, 8])
micro_usb_connector = cube([40, 10, 7])
BATTERY_WIDTH = 75.5
BATTERY_HEIGHT = 14.3
battery = (
    color("brown")(cube([BATTERY_WIDTH, 144, BATTERY_HEIGHT]))
    + color("black")(translate([11,144,3])(usb_connector))
    + color("black")(translate([47,144,3])(usb_connector))
    + color("black")(translate([75,121,3])(micro_usb_connector))
)
BATTERY_VERTICAL_POSTITION = 42

battery_stand_width = BATTERY_WIDTH + 8
battery_stand_height = BATTERY_VERTICAL_POSTITION + BATTERY_HEIGHT + 2

mount_hole = (
    nuts_n_bolts.cyl_head_bolt.nutcatch_parallel("M3", l=3, clk=0.5)
    + nuts_n_bolts.cyl_head_bolt.hole_through(name="M3", l=10, cld=0.5, h=0, hcld=0.4)
)
battery_rear_stand = color([1.0, 1.0, 1.0, 0.7])(
    cube([10, battery_stand_width, battery_stand_height])
    - translate([-1, 2, BATTERY_VERTICAL_POSTITION])(cube([10, BATTERY_WIDTH, BATTERY_HEIGHT]))
    - translate([-1, 12, 4])(cube([15, BATTERY_WIDTH - 20, 30]))
    + translate([0, (battery_stand_width / 2) - 10, 0])(cube([17, 20, 4]))
    - translate([5, 15, 5])(mount_hole)
    - translate([5, 64, 5])(mount_hole)
    - translate([13, (battery_stand_width / 2), 5])(mount_hole)
    )

battery_front_stand = (
    battery_rear_stand
    - translate([-1, 2, BATTERY_VERTICAL_POSTITION])(cube([20, BATTERY_WIDTH, BATTERY_HEIGHT])) 
)

caster = (
    cylinder(d=17, h = 15)
    + translate([0,-8,0])(cylinder(d = 6.5, h = 15))
    + translate([0,8,0])(cylinder(d = 6.5, h = 15))
)

caster_holes = (
    translate([0,-8,0])(cylinder(d=2.8, h=20))
    + translate([0,8,0])(cylinder(d=2.8, h=20))
    + translate([0,-8,2])(cylinder(d=4.5, h=20))
    + translate([0,8,2])(cylinder(d=4.5, h=20))
)

RPLIDAR_WIDTH = 70.28
rplidar_full = (
    rotate([90, 0, 180])(rplidar)
    + translate([-45, 60, -3])(cube([20, 5, 12]))
    )

rplidar_leg_hole = cylinder(d = 6, h = 5)
rplidar_leg = (
    cylinder(d = 10, h = 7)
    - translate([0, 0, 9])(nuts_n_bolts.cyl_head_bolt.hole_through(name="M3", l=10, cld=0.5, h=0, hcld=0.4))
    - translate([0, 0, 2])(cylinder(d = 5.5, h = 10))
    )

rplidar_battery_wrap = (
    cube([10, battery_stand_width, BATTERY_HEIGHT + 4])
    - translate([-1, (battery_stand_width - BATTERY_WIDTH)/2, 2])(cube([12, BATTERY_WIDTH, BATTERY_HEIGHT]))
)

def rplidar_legs(element, z = 0): 
    return ( 
    translate([0, 0, z])(element) 
    + translate([0, 56, z])(element)
    + translate([-70, 8, z])(element)
    + translate([-70, 48, z])(element)  
    )

rplidar_stand = (
    rplidar_legs(rplidar_leg)
    + translate([-25,-(battery_stand_width - 56)/2,-(BATTERY_HEIGHT + 4)])(rplidar_battery_wrap)
    + translate([-75,-(battery_stand_width - 56)/2,-(BATTERY_HEIGHT + 4)])(rplidar_battery_wrap)
    + translate([-20, -7.5, -2])(cube([25, 15, 2]))
    + translate([-20, 48.5, -2])(cube([25, 15, 2]))
    + translate([-70, (56- 15)/2, -2])(cube([55, 15, 2]))
    - rplidar_legs(cylinder(d = 6, h = 20), -20.5)
    - rplidar_legs(cylinder(d = 3, h = 30), -20)
)

battery_rear_stand_with_caster = color([1.0, 1.0, 1.0, 0.7])(
    battery_rear_stand
    + translate([-10, battery_stand_width / 2 - 20, 0])(cube([10, 40, 4]))
    - translate([0, battery_stand_width / 2, -14])(caster)
    - translate([0, battery_stand_width / 2, 0])(caster_holes)
    - translate([-5, 25, 5])(mount_hole)
    - translate([-5, 55, 5])(mount_hole)
    )

battery_with_lidar = (
    translate([100, -BATTERY_WIDTH/2.0, ACRYLIC_HEIGHT + BATTERY_VERTICAL_POSTITION])(rotate([0, 0, 90])(battery))
    + translate([92, -(battery_stand_width / 2), ACRYLIC_HEIGHT])(battery_rear_stand_with_caster)
    + translate([-35, (battery_stand_width / 2), ACRYLIC_HEIGHT])(rotate([0, 0, 180])(battery_front_stand))
    + translate([65, -RPLIDAR_WIDTH/2, 66])(color("grey")(rplidar_full))
    + translate([58, -28, 61])(rplidar_stand)
)

full = (
    acrylic_base
    + translate([0, 0, 0])(diff_drive)
    + translate([-9, 0, 0])(battery_with_lidar)
    + electronics.full
    + translate([0, 0, -2.6])(bumper.bumper)
    + translate([0, 0, -1.5])(cover.full)
)

full_exploded = (
    acrylic_base
    + translate([0, 0, 0])(diff_drive)
    + translate([-9, 0, 0])(battery_with_lidar)
    + electronics.full
    + translate([0, 0, -2.6])(bumper.bumper)
    + translate([0, 0, -1.5])(cover.full_exploded)
)

to_render = {
  'cover_back_left': cover.back_left,
  'cover_back_right': cover.back_right,
  'cover_back_top_plate': cover.back_top_plate,
  'cover_left_side_plate': cover.left_side_plate,
  'cover_right_side_plate': cover.right_side_plate,
  'cover_front_top_plate': cover.front_top_plate,
  'cover_front_left_support': cover.front_left_support,
  'cover_front_right_support': cover.front_right_support,
  'cover_front_left': cover.front_left,
  'cover_front_right': cover.front_right,
  'cover_front_support': cover.front_support,
  'cover_lidar_cover': cover.lidar_cover,
  'motors_stand': motors_stand.full,
  'battery_rear_holder': battery_rear_stand_with_caster,
  'battery_front_stand': battery_front_stand,
  'rplidar_stand': rplidar_stand,
  'bumper_base': bumper.bumper_base,
  'left_bumper': bumper.bumper_left,
  'right_bumper': bumper.bumper_right,
  'left_bumper_stopper': bumper.bumper_stopper_left,
  'right_bumper_stopper': bumper.bumper_stopper_right
}

def render_stls():
    for key in to_render:
        print(f'Rendering {key}')
        scad_render_to_file(to_render[key], os.path.join(out_dir, 'to_render.scad'), file_header='$fn = %s;' % SEGMENTS)
        os.system(f'openscad -o rendered/{key}.stl ./to_render.scad')

if __name__ == '__main__':
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.curdir
    file_out = os.path.join(out_dir, 'chassis.scad')

    a = rplidar_stand
#    render_stls() # run to render all stls

    print("%(__file__)s: SCAD file written to: \n%(file_out)s" % vars())

    # Adding the file_header argument as shown allows you to change
    # the detail of arcs by changing the SEGMENTS variable.  This can
    # be expensive when making lots of small curves, but is otherwise
    # useful.
    scad_render_to_file(a, file_out, file_header='$fn = %s;' % SEGMENTS)