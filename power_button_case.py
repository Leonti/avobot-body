import os
import sys

from solid import *
from solid.utils import *

screw_hole_diameter_2_5 = 2.35

def stands_base(stand):
    return (
        translate([9.5, 0,0])(stand)
        + translate([0, 9.5, 0])(stand)
        + translate([-9.5, 0, 0])(stand)
        + translate([0, -9.5, 0])(stand)
    )

stands_positioned = translate([0, 0, - 1.5 - 5.5])(stands_base(cylinder(d = 5, h = 5.5) - cylinder(d = screw_hole_diameter_2_5, h = 10)))

#stands = translate([15, -63, 65])(rotate([0, 0, 180])(stands_base()))

def full(use_placeholders = False):
    return translate([15, -63, 65])(rotate([0, 0, 180])(case(use_placeholders)))

button = color("grey")(
    translate([-8/2.0, -6.9/2.0, -12.6])(cube([8, 6.9, 10]))
    + translate([0, 0, -2.6])(cylinder(d = 10.3, h = 2.6))
    + cylinder(d = 6.7, h = 1)
)

case_base = (
    translate([0, 0, - 1.55 - 6])(cylinder(d = 10.1 + 3.8, h = 6))
    + translate([0, 0, -9])(cylinder(d = 24, h = 2))
    - translate([0, 0, -10])(stands_base(cylinder(d = 3, h = 10)))
    - button
)

case = translate([40, -70, 73.5])(case_base)
stands = translate([40, -70, 73.5])(stands_positioned)

def full(use_placeholder = False):
    if use_placeholder:
        return translate([40, -70, 73.5])(button)
    else:
        return case #button
