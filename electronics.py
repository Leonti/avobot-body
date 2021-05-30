import os
import sys

from solid import *
from solid.utils import *

import mounts

import cover

nop = import_scad('lib.scad')
raspberry_pie = nop.rpi()

motor_driver = color("red")(cube([20.05, 20.05, 1.6]))

raspberry_pie_stand = cylinder(d=2.3, h=9)

screw_hole_diameter_2_5 = 2.35
screw_hole_diameter_3 = 2.85
screw_hole_diameter_2 = 1.85

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

def buck_converter_stands(stand):
    return (
        translate([15, 5.7, -1])(stand)
        + translate([4, 41, -1])(stand)
        + translate([27, 41, -1])(stand)
    )

def buck_converter_base():
    pcb = color("green")(cube([31, 45.5, 1.8]))
    capacitor = color("black")(cylinder(d = 10, h = 13))
    inductor = color("grey")(cube([15, 14, 8]))
    connector = color("blue")(cube([15, 8, 10]))
    hole = cylinder(d = 3.1, h = 10)

    return (
        pcb
        + translate([6.2, 6, 1.8])(capacitor)
        + translate([25.2, 6, 1.8])(capacitor)
        + translate([14, 12, 1.8])(inductor)
        + translate([8, 37, 1.8])(connector)
        - buck_converter_stands(hole)
    )

buck_converter = buck_converter_base()

def ina219_stands(stand):
    return (
        translate([4, 2.5, 0])(stand)
        + translate([4, 17.8, 0])(stand)
    )

def ina219_base():
    pcb = color("purple")(cube([21, 20.4, 1.8]))
    hole = cylinder(d = 3.1, h = 10)

    return (
        pcb
        - translate([0, 0, -1])(ina219_stands(hole))
    )
ina219 = ina219_base()

def relay_stands(stand):
    return (
        translate([4, 10.4, 0])(stand)
        + translate([4, 15.3 + 10.4, 0])(stand)        
    )

def relay_base():
    pcb = color("brown")(cube([28, 34, 1.8]))
    hole = cylinder(d = 3.1, h = 10)
    relay = color("white")(cube([10, 20, 11]))

    return (
        pcb
        + translate([16, 5.5, 1.8])(relay)
        - translate([0, 0, -1])(relay_stands(hole))
    )

relay = relay_base()

def pico_stands(stand):
    return translate([2, (21 - 11.4)/2.0, 0])(
        stand
        + translate([47, 0, 0])(stand)
        + translate([47, 11.4, 0])(stand)
        + translate([0, 11.4, 0])(stand)
    )

def pico_base():
    pcb = color("green")(cube([51, 21, 1.5]))
    usb = color("white")(cube([6, 8, 3]))
    hole = cylinder(d = 2.1, h = 10)

    return (
        pcb
        + translate([-1.3, (21 - 8)/2.0, 1.5])(usb)
        - translate([0, 0, -1])(pico_stands(hole))
    )

pico = pico_base()

powerstrip_stands = (
    translate([0, 40, 0])(cylinder(d=7, h=10))
    - translate([0, 40, 0])(cylinder(d=screw_hole_diameter_2_5, h=11))
    + translate([0, -20, 5])(rotate([0, 0, 30])(
        cylinder(d=7, h=5)
        + translate([0, -7/2.0, 0])(
            cube([9, 7, 3])
            + translate([6, 0, -7])(cube([3, 7, 8]))
        )
    ))
    - translate([0, -20, 5])(cylinder(d=screw_hole_diameter_2_5, h=6))

)

ELECTRONICS_STAND_WIDTH = 143
ELECTRONICS_STAND_HEIGHT = 56
electronics_stand = color([1.0, 1.0, 1.0, 0.7])(
    translate([0, 0, 26])(linear_extrude(height=2)(
        polygon([
            [0, ELECTRONICS_STAND_WIDTH],
            [ELECTRONICS_STAND_HEIGHT - 3, ELECTRONICS_STAND_WIDTH],
            [ELECTRONICS_STAND_HEIGHT, ELECTRONICS_STAND_WIDTH - 3],
            [ELECTRONICS_STAND_HEIGHT, 49],
            [ELECTRONICS_STAND_HEIGHT + 10, 49],
            [ELECTRONICS_STAND_HEIGHT + 10, 30],
            [ELECTRONICS_STAND_HEIGHT, 30],
            [ELECTRONICS_STAND_HEIGHT, 20],
            [35, 0],
            [12, -11.5],
            [13, 5],
            [0, 5]    
        ])
    ))
    + translate([0, 33, 0])(cube([ELECTRONICS_STAND_HEIGHT, 2, 26]))
    + translate([0, 2, 0])(cube([49, 33, 2]))
    - translate([39, 2, -1])(linear_extrude(height=10)(polygon([
        [0, 0],
        [10, 0],
        [10, 10]
    ])))
    + translate([0, 115, 0])(cube([ELECTRONICS_STAND_HEIGHT, 2, 26]))
    + translate([0, 115, 0])(cube([45, 38, 2]))
    - translate([0, 138, -1])(cube([7, 15, 4]))
    + translate([12, ELECTRONICS_STAND_WIDTH - 5, 0])(cube([10, 10, 2]))
    + translate([28, ELECTRONICS_STAND_WIDTH + 5, 0])(cylinder(d=10, h=5))
    - translate([28, ELECTRONICS_STAND_WIDTH + 5, 2])(mounts.nut_hole)
    + translate([3.5, 81, 27])(raspberry_pie_stands(cylinder(d=6, h=6)))
    - translate([3.5, 81, 20])(raspberry_pie_stands(cylinder(d=screw_hole_diameter_2_5, h=20)))
    + translate([25, 22, 0])(cylinder(d=10, h=5))
    - translate([25, 22, 2])(mounts.nut_hole)
    + translate([10, 12, 28])(powerstrip_stands)
    + translate([50, 1, 3])(rotate([0, 0, 90])(buck_converter_stands(cylinder(d = 8, h = 7))))
    - translate([50, 1, 0])(rotate([0, 0, 90])(buck_converter_stands(cylinder(d = screw_hole_diameter_3, h = 20))))
    - translate([50, 1, 20])(rotate([0, 0, 90])(buck_converter_stands(cylinder(d = 8, h = 20))))
    + translate([17, 0, 26])(ina219_stands(cylinder(d = 8, h = 4)))
    - translate([17, 0, 20])(ina219_stands(cylinder(d = screw_hole_diameter_3, h = 20)))
    + translate([10, 146, 0])(rotate([0, 0, 270])(relay_stands(cylinder(d = 7, h = 9))))
    - translate([10, 146, -1])(rotate([0, 0, 270])(relay_stands(cylinder(d = screw_hole_diameter_3, h = 20))))
    - translate([10, 146, 10])(rotate([0, 0, 270])(relay_stands(cylinder(d = 8, h = 20))))
    + translate([65, 50, 26])(rotate([0, 0, 180])(pico_stands(cylinder(d = 5, h = 6))))
    - translate([65, 50, 20])(rotate([0, 0, 180])(pico_stands(cylinder(d = screw_hole_diameter_2, h = 20))))
)

batteries = cube([66, 79, 21])

outer_shell = (
    cylinder(d = 217, h = 40)
    - translate([0, 0, -1])(cylinder(d = 216, h = 100))
    - translate([-150 + 22, -200, -1])(cube([150, 400, 100]))
)

hole_test = (
    cube([10, 30, 2])
    + translate([5, 5, 0])(cylinder(d = 8, h = 6))
    + translate([5, 15, 0])(cylinder(d = 8, h = 6))
    + translate([5, 25, 0])(cylinder(d = 8, h = 6))
    - translate([5, 5, -1])(cylinder(d = screw_hole_diameter_2, h = 20))
    - translate([5, 15, -1])(cylinder(d = screw_hole_diameter_2_5, h = 20))
    - translate([5, 25, -1])(cylinder(d = screw_hole_diameter_3, h = 20))
)

full = translate([26, -75, 3])(
    translate([0, 0, 0])(electronics_stand)
    + translate([1, 35.5, 6])(batteries)
    + translate([28, 100, 7 + 26])(rotate([0, 0, -90])(raspberry_pie))
    + translate([50, 1, 9])(rotate([0, 0, 90])(buck_converter))
    + translate([65, 50, 32])(rotate([0, 0, 180])(pico))
    + translate([10, 146, 9])(rotate([0, 0, 270])(relay))
    + translate([17, 0, 30])(ina219)
) #+ outer_shell

full = electronics_stand

#full = translate([26, -75, 3])(
#    translate([1, 35.5, 6])(batteries)
#)

#full = hole_test