import os
import sys

from solid import *
from solid.utils import *

import mounts

nop = import_scad('lib.scad')
nano = import_stl('nano.stl')
nano_holder = translate([2, 2, -33])(rotate([0, 0, 90])
                                     (import_stl('nano_holder.stl')))

raspberry_pie = nop.rpi()

motor_driver = color("red")(cube([20.05, 20.05, 1.6]))

raspberry_pie_stand = cylinder(d=2.3, h=9)


def raspberry_pie_stands(stand):
    return (
        translate([0, 0])(stand)
        + translate([0, 58])(stand)
        + translate([49, 58])(stand)
        + translate([49, 0])(stand)
    )


rpi_stands = (
    raspberry_pie_stands(cylinder(d=2.5, h=12))
    + raspberry_pie_stands(cylinder(d=6, h=6))
)

motor_driver_stand = (
    cube([25, 25, 7])
    - translate([(25 - 18.5)/2, -3, -1])(cube([18.5, 25, 10]))
    - translate([(25 - 22)/2, -3, 3])(cube([22, 25, 2.2]))
)

powerstrip_stands = (
    translate([0, 40, 0])(cylinder(d=7, h=10))
    - translate([0, 40, 0])(cylinder(d=2.3, h=11))
    + translate([0, -20, 4])(cylinder(d=7, h=6))
    + translate([-3, -10, 0])(cube([6, 6, 4]))
    + translate([-3, -19, 4])(cube([6, 15, 4]))
    - translate([0, -20, 0])(cylinder(d=2.3, h=11))
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
    + translate([17, ELECTRONICS_STAND_WIDTH + 5, 0])(cylinder(d=10, h=5))
    + translate([12, ELECTRONICS_STAND_WIDTH - 5, 0])(cube([10, 10, 2]))
    - translate([17, ELECTRONICS_STAND_WIDTH + 5, 2])(mounts.nut_hole)
    + translate([3.5, 81, 2])(rpi_stands)
    + translate([31, 25, 2])(motor_driver_stand)
    + translate([ELECTRONICS_STAND_HEIGHT - 8, 55, 2])(cube([8, 49, 4]))
    - translate([ELECTRONICS_STAND_HEIGHT - 12, 58, -1])(cube([13, 43, 5]))
    + translate([0, 7, 2])(nano_holder_cut)
    + translate([25, 25, 2])(cylinder(d=10, h=3))
    - translate([25, 25, 2])(mounts.nut_hole)
    + translate([26.5, 12, 2])(powerstrip_stands)
    - translate([8, 65, -1])(cube([40, 70, 4]))
)


full = translate([26, -75, 3])(
    translate([0, 0, 0])(electronics_stand)
    + translate([28, 100, 7])(rotate([0, 0, -90])(raspberry_pie))
    + translate([33, 26, 5])(motor_driver)
    + translate([11, 31, 11])(rotate([0, 0, 90])(nano))
)
