#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import os
import sys

from solid import *
from solid.utils import *
import bumper

nuts_n_bolts = import_scad('/home/leonti/3d/openscad_libraries/nutsnbolts')
nop = import_scad('lib.scad')
#print(dir(nop))
nano = import_stl('nano.stl')
nano_holder = translate([2, 2, -33])(rotate([0, 0, 90])(import_stl('nano_holder.stl')))
rplidar = import_stl('rplidar.stl')

SEGMENTS = 48

ACRYLIC_HEIGHT = 3
acrylic_base = color("green")(cylinder(d = 210, h = ACRYLIC_HEIGHT))

wheel = color("blue")(cylinder(d = 67, h = 27))
diff_drive = (
    wheel
    + translate([-50/2.0, -35/2.0, 33])(color("black")(cube([50, 35, 140])))
    + translate([0, 0, 177])(wheel)
)

usb_connector = cube([18, 35, 8])
micro_usb_connector = cube([40, 10, 7])
BATTERY_WIDTH = 75.2
BATTERY_HEIGHT = 14.1
battery = (
    color("brown")(cube([BATTERY_WIDTH, 144, BATTERY_HEIGHT]))
    + color("black")(translate([11,144,3])(usb_connector))
    + color("black")(translate([47,144,3])(usb_connector))
    + color("black")(translate([75,121,3])(micro_usb_connector))
)
BATTERY_VERTICAL_POSTITION = 42

battery_stand_width = BATTERY_WIDTH + 4
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

battery_rear_stand_with_caster = color([1.0, 1.0, 1.0, 0.7])(
    battery_rear_stand
    + translate([-10, battery_stand_width / 2 - 20, 0])(cube([10, 40, 4]))
    - translate([0, battery_stand_width / 2, -14])(caster)
    - translate([0, battery_stand_width / 2, 0])(caster_holes)
    - translate([-5, 25, 5])(mount_hole)
    - translate([-5, 55, 5])(mount_hole)
    )

raspberry_pie = nop.rpi()

motor_driver = color("red")(cube([20.05, 20.05, 1.6]))

RPLIDAR_WIDTH = 70.28
rplidar_full = (
    rotate([90, 0, 180])(rplidar)
    + translate([-45, 60, -3])(cube([20, 5, 12]))
    )

rplidar_leg_hole = cylinder(d = 6, h = 5)
rplidar_leg = (
    cylinder(d = 10, h = 10)
    - translate([0, 0, 10])(nuts_n_bolts.cyl_head_bolt.hole_through(name="M3", l=10, cld=0.5, h=0, hcld=0.4))
    - translate([0, 0, -4])(rplidar_leg_hole)
    - translate([0, 0, 5])(cylinder(d = 5.5, h = 10))
    )

rplidar_battery_wrap = (
    cube([10, battery_stand_width, BATTERY_HEIGHT + 4])
    - translate([-1, 2, 2])(cube([12, BATTERY_WIDTH, BATTERY_HEIGHT]))
)

def rplidar_legs(element): 
    return ( 
    element 
    + translate([0, 56, 0])(element)
    + translate([-70, 8, 0])(element)
    + translate([-70, 48, 0])(element)  
    )

rplidar_stand = color([1.0, 1.0, 1.0, 0.7])(
    rplidar_legs(rplidar_leg)
    + translate([-5,-(battery_stand_width - 56)/2,-(BATTERY_HEIGHT + 4)])(rplidar_battery_wrap)
    - translate([0, 0, -69])(cylinder(d = 6, h = 70))
    - translate([0, 56, -69])(cylinder(d = 6, h = 70))
    + translate([-75,-(battery_stand_width - 56)/2,-(BATTERY_HEIGHT + 4)])(rplidar_battery_wrap)
    - translate([-70, 8, -69])(cylinder(d = 6, h = 70))
    - translate([-70, 48, -69])(cylinder(d = 6, h = 70))
    + translate([-70, (56- 15)/2, -2])(cube([70, 15, 2]))
)

raspberry_pie_stand = cylinder(d = 2.3, h = 9)
def raspberry_pie_stands(stand): 
    return (
        translate([0, 0])(stand)
        + translate([0, 58])(stand)
        + translate([49, 58])(stand)
        + translate([49, 0])(stand)
    )

rpi_stands = (
    raspberry_pie_stands(cylinder(d = 2.5, h = 12))
    + raspberry_pie_stands(cylinder(d = 6, h = 6))
)

motor_driver_stand = (
    cube([25, 25, 7])
    - translate([(25 - 18.5)/2, -3, -1])(cube([18.5, 25, 10]))
    - translate([(25 - 22)/2, -3, 3])(cube([22, 25, 2.1]))
)

powerstrip_stands = (
    cylinder(d = 6, h = 8)
    + translate([0, 40, 0])(cylinder(d = 6, h = 10))
    - translate([0, 40, 0])(cylinder(d = 2.5, h=11))
)

nano_holder_cut = translate([0, 0, -4])((
    nano_holder
    - translate([-1, -1, 0])(cube([100, 100, 4]))
    ))

ELECTRONICS_STAND_WIDTH = 143
ELECTRONICS_STAND_HEIGHT = 56
electronics_stand = color([1.0, 1.0, 1.0, 0.7])(
    linear_extrude(height=2)(
        polygon([
            [0, 7],
            [0, ELECTRONICS_STAND_WIDTH],
            [ELECTRONICS_STAND_HEIGHT - 3, ELECTRONICS_STAND_WIDTH],
            [ELECTRONICS_STAND_HEIGHT, ELECTRONICS_STAND_WIDTH - 3],
            [ELECTRONICS_STAND_HEIGHT, 20],
            [35, 0],
            [15, 0],
            [15, 7]
            ])
    )
#    + translate([25, ELECTRONICS_STAND_WIDTH, 0])(cylinder(d = 10, h = 2))
    + translate([3.5, 81, 2])(rpi_stands)
    + translate([31, 25, 2])(motor_driver_stand)
    + translate([ELECTRONICS_STAND_HEIGHT - 8, 55, 2])(cube([8, 49, 4]))
    - translate([ELECTRONICS_STAND_HEIGHT - 12, 58, -1])(cube([13, 43, 5]))
    + translate([0, 7, 2])(nano_holder_cut)
    + translate([26.5, 12, 2])(powerstrip_stands)
    
#    - translate([25, ELECTRONICS_STAND_WIDTH + 1, -1])(cylinder(d = 2.9, h = 4))
#    - translate([50, 20, -1])(cylinder(d = 2.9, h = 4))
    - translate([8, 65, -1])(cube([40, 70, 4]))
)


electronics = (
    translate([0, 0, 0])(electronics_stand)
    + translate([28, 100, 7])(rotate([0, 0, -90])(raspberry_pie))
    + translate([33, 26, 5])(motor_driver)
    + translate([11, 31, 11])(rotate([0, 0, 90])(nano))
)

battery_with_lidar = (
    translate([100, -BATTERY_WIDTH/2.0, ACRYLIC_HEIGHT + BATTERY_VERTICAL_POSTITION])(rotate([0, 0, 90])(battery))
    + translate([92, -(battery_stand_width / 2), ACRYLIC_HEIGHT])(battery_rear_stand_with_caster)
    + translate([-35, (battery_stand_width / 2), ACRYLIC_HEIGHT])(rotate([0, 0, 180])(battery_front_stand))
    + translate([65, -RPLIDAR_WIDTH/2, 66])(rplidar_full)
    + translate([58, -28, 61])(rplidar_stand)
)

full = (
    acrylic_base
    + translate([0, (177 + 27) / 2.0, 35/2.0 + ACRYLIC_HEIGHT])(rotate([90, 0, 0])(diff_drive))
    + translate([-7, 0, 0])(battery_with_lidar)
    + translate([26, -75, 3])(electronics)
    + translate([0, 0, -4.5])(bumper.bumper)

)

if __name__ == '__main__':
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.curdir
    file_out = os.path.join(out_dir, 'chassis.scad')

    a = bumper.bumper

    print("%(__file__)s: SCAD file written to: \n%(file_out)s" % vars())

    # Adding the file_header argument as shown allows you to change
    # the detail of arcs by changing the SEGMENTS variable.  This can
    # be expensive when making lots of small curves, but is otherwise
    # useful.
    scad_render_to_file(a, file_out, file_header='$fn = %s;' % SEGMENTS)