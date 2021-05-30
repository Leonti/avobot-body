import os
import sys

from solid import *
from solid.utils import *

screw_hole_diameter_2_5 = 2.35

lcd_depth = 27.5
lcd_width = 25.5

case_depth = 29.5
case_width = 27.5
height = 8

ear = (
    cylinder(d = 6, h = 1.5) 
    + translate([0, -3, 0])(cube([4, 6, 1.5]))
    - translate([0, 0, -1])(cylinder(d = 3, h = 10))
)

def ears(use_placeholders = False):
    front = (
        translate([-4, 3, 0])(ear)
        + translate([-4, case_width - 3, 0])(ear)
    )

    back = translate([case_depth, 0, 0])(mirror([1, 0, 0])(front))

    return front + back

def stands_base():
    stand = cylinder(d = 5, h = 5.5) - cylinder(d = screw_hole_diameter_2_5, h = 10)

    return (
        translate([-4, 3, 1.5])(stand)
        + translate([-4, 24.5, 1.5])(stand)
        + translate([33.5, 24.5, 1.5])(stand)
        + translate([33.5, 3, 1.5])(stand)
    )

skirt = translate([-1.4, -1.4, height - 3])(
    cube([case_depth + 2.8, case_width + 2.8, 1.5])
    - translate([1.4, 1.4, -1])(cube([case_depth, case_width, 10]))
    )

lcd = (
    cube([lcd_depth, lcd_width, height])
    + translate([8.8, (lcd_width - 24) / 2.0, 0])(cube([12, 24, 13]))
)

def case(use_placeholders = False):
    real_case = (
            cube([case_depth, case_width, height + 0.5]) - translate([1, 1, 0])(lcd)
            + ears() 
            + skirt
        )
    if use_placeholders:
        return translate([-0.05, -0.05, 0])(cube([case_depth + 0.1, case_width + 0.1, height + 20])) + real_case
    else:    
        return real_case

stands = translate([15, -63, 65])(rotate([0, 0, 180])(stands_base()))

def full(use_placeholders = False):
    return translate([15, -63, 65])(rotate([0, 0, 180])(case(use_placeholders)))

