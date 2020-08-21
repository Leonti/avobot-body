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
import json
from functools import reduce

nuts_n_bolts = import_scad('/home/leonti/3d/openscad_libraries/nutsnbolts')
rplidar = import_stl('rplidar.stl')

SEGMENTS = 200

ACRYLIC_HEIGHT = 3

wheel = color("blue")(cylinder(d=67, h=27))
diff_drive = (
    translate([0, (177 + 27) / 2.0, 22.5])(rotate([90, 0, 0])
                                           (wheel + translate([0, 0, 177])(wheel)))
    + motors_stand.full
)

usb_connector = cube([18, 35, 8])
micro_usb_connector = cube([40, 10, 7])
BATTERY_WIDTH = 75.5
BATTERY_HEIGHT = 14.3
battery = (
    color("brown")(cube([BATTERY_WIDTH, 144, BATTERY_HEIGHT]))
    + color("black")(translate([11, 144, 3])(usb_connector))
    + color("black")(translate([47, 144, 3])(usb_connector))
    + color("black")(translate([75, 121, 3])(micro_usb_connector))
)
BATTERY_VERTICAL_POSTITION = 42

battery_stand_width = BATTERY_WIDTH + 8
battery_stand_height = BATTERY_VERTICAL_POSTITION + BATTERY_HEIGHT + 2

mount_hole = (
    nuts_n_bolts.cyl_head_bolt.nutcatch_parallel("M3", l=3, clk=0.5)
    + nuts_n_bolts.cyl_head_bolt.hole_through(name="M3", l=10, cld=0.5, h=0, hcld=0.4)
)


def battery_rear_stand(hole_placeholders=False):
    base = (
        cube([10, battery_stand_width, battery_stand_height])
        - translate([-1, 2, BATTERY_VERTICAL_POSTITION]
                    )(cube([10, BATTERY_WIDTH, BATTERY_HEIGHT]))
        - translate([-1, 12, 4])(cube([15, BATTERY_WIDTH - 20, 30]))
        + translate([0, (battery_stand_width / 2) - 10, 0])(cube([17, 20, 4]))
    )

    mount_holes_coords = [
        (5, 15),
        (5, 64),
        (13, (battery_stand_width / 2))
    ]

    mount_holes = reduce(lambda a, b: a + b, map(
        lambda xy: translate([xy[0], xy[1], 5])(mount_hole), mount_holes_coords)
    )

    if hole_placeholders is True:
        return base + mount_holes
    else:
        return base - mount_holes


def battery_front_stand(hole_placeholders=False):
    return (
        battery_rear_stand(hole_placeholders)
        - translate([-1, 2, BATTERY_VERTICAL_POSTITION]
                    )(cube([20, BATTERY_WIDTH, BATTERY_HEIGHT]))
    )


caster = (
    cylinder(d=17, h=15)
    + translate([0, -8, 0])(cylinder(d=6.5, h=15))
    + translate([0, 8, 0])(cylinder(d=6.5, h=15))
)

caster_holes = (
    translate([0, -8, 0])(cylinder(d=2.8, h=20))
    + translate([0, 8, 0])(cylinder(d=2.8, h=20))
    + translate([0, -8, 2])(cylinder(d=4.5, h=20))
    + translate([0, 8, 2])(cylinder(d=4.5, h=20))
)

RPLIDAR_WIDTH = 70.28
rplidar_full = (
    rotate([90, 0, 180])(rplidar)
    + translate([-45, 60, -3])(cube([20, 5, 12]))
)

rplidar_leg_hole = cylinder(d=6, h=5)
rplidar_leg = (
    cylinder(d=10, h=7)
    - translate([0, 0, 9])(nuts_n_bolts.cyl_head_bolt.hole_through(name="M3",
                                                                   l=10, cld=0.5, h=0, hcld=0.4))
    - translate([0, 0, 2])(cylinder(d=5.5, h=10))
)

rplidar_battery_wrap = (
    cube([10, battery_stand_width, BATTERY_HEIGHT + 4])
    - translate([-1, (battery_stand_width - BATTERY_WIDTH)/2, 2]
                )(cube([12, BATTERY_WIDTH, BATTERY_HEIGHT]))
)


def rplidar_legs(element, z=0):
    return (
        translate([0, 0, z])(element)
        + translate([0, 56, z])(element)
        + translate([-70, 8, z])(element)
        + translate([-70, 48, z])(element)
    )


rplidar_stand = (
    rplidar_legs(rplidar_leg)
    + translate([-25, -(battery_stand_width - 56)/2, -
                 (BATTERY_HEIGHT + 4)])(rplidar_battery_wrap)
    + translate([-75, -(battery_stand_width - 56)/2, -
                 (BATTERY_HEIGHT + 4)])(rplidar_battery_wrap)
    + translate([-20, -7.5, -2])(cube([25, 15, 2]))
    + translate([-20, 48.5, -2])(cube([25, 15, 2]))
    + translate([-70, (56 - 15)/2, -2])(cube([55, 15, 2]))
    - rplidar_legs(cylinder(d=6, h=20), -20.5)
    - rplidar_legs(cylinder(d=3, h=30), -20)
)


def battery_rear_stand_with_caster(hole_placeholders=False):

    base = color([1.0, 1.0, 1.0, 0.7])(
        battery_rear_stand(hole_placeholders)
        + translate([-10, battery_stand_width / 2 - 20, 0])(cube([10, 40, 4]))
        - translate([0, battery_stand_width / 2, -14])(caster)
        - translate([0, battery_stand_width / 2, 0])(caster_holes)
    )

    if hole_placeholders is True:
        return (base
                + translate([0, battery_stand_width / 2, -14])(caster)
                + translate([0, battery_stand_width / 2, 0])(caster_holes)
                )
    else:
        return base


def battery_with_lidar(hole_placeholders=False):
    return translate([-9, 0, 0])((
        translate([100, -BATTERY_WIDTH/2.0, ACRYLIC_HEIGHT +
                   BATTERY_VERTICAL_POSTITION])(rotate([0, 0, 90])(battery))
        + translate([92, -(battery_stand_width / 2), ACRYLIC_HEIGHT]
                    )(battery_rear_stand_with_caster(hole_placeholders))
        + translate([-35, (battery_stand_width / 2), ACRYLIC_HEIGHT]
                    )(rotate([0, 0, 180])(battery_front_stand(hole_placeholders)))
        + translate([65, -RPLIDAR_WIDTH/2, 66])(color("grey")(rplidar_full))
        + translate([58, -28, 61])(rplidar_stand)
    ))


wheel_cutout_right = translate([-35, 70, -1])(cube([70, 40, 5]))
acrylic_base = color([1.0, 1.0, 1.0, 0.9])(
    cylinder(d=208, h=ACRYLIC_HEIGHT)
    - wheel_cutout_right
    - mirror([0, 1, 0])(wheel_cutout_right)
    - cover.for_holes
    - motors_stand.full_for_holes
    - bumper.for_holes
    - battery_with_lidar(True)
)

full = (
    acrylic_base
    + translate([0, 0, 0])(diff_drive)
    + battery_with_lidar()
    + electronics.full
    + translate([0, 0, -2.6])(bumper.bumper)
    + translate([0, 0, -1.5])(cover.full)
)

full_exploded = (
    acrylic_base
    + translate([0, 0, 0])(diff_drive)
    + translate([-9, 0, 0])(battery_with_lidar())
    + electronics.full
    + translate([0, 0, -2.6])(bumper.bumper)
    + translate([0, 0, -1.5])(cover.full_exploded)
)

stls = [
    {'name': 'motors_stand', 'obj': motors_stand.full,
     'title': 'Motors holder',
     'desc': '''Central part of the robot body, make sure to either print with 100%% infill or
     with sufficiently thick walls. I used 1.2mm.
     Slide m3 screws at the top and use BlueTak or some glue to keep them from moving.   
    '''},
    {'name': 'battery_rear_holder', 'obj': battery_rear_stand_with_caster(),
        'title': 'Battery holder (rear)',
        'desc': 'Use screws that come with the caster to screw it to the PLA'},
    {'name': 'battery_front_stand', 'obj': battery_front_stand(),
        'title': 'Battery holder (front)',
        'desc': ''
     },
    {'name': 'rplidar_stand', 'obj': rplidar_stand,
        'title': 'Lidar Stand',
        'desc': 'Be careful when removing supports as it is pretty thin and might break'},
    {'name': 'cover_back_left', 'obj': cover.back_left,
        'title': 'Rear cover (left)',
        'desc': ''},
    {'name': 'cover_back_right', 'obj': cover.back_right,
        'title': 'Rear cover (right)',
        'desc': ''},
    {'name': 'cover_back_top_plate', 'obj': cover.back_top_plate,
        'title': 'Top plate for rear cover',
        'desc': ''},
    {'name': 'cover_front_left', 'obj': cover.front_left,
        'title': 'Front cover (left)',
        'desc': ''},
    {'name': 'cover_front_right', 'obj': cover.front_right,
        'title': 'Front cover (right)',
        'desc': ''},
    {'name': 'cover_front_top_plate', 'obj': cover.front_top_plate,
        'title': 'Top plate for front cover',
        'desc': ''},
    {'name': 'cover_left_side_plate', 'obj': cover.left_side_plate,
        'title': 'Left top cover',
        'desc': 'The LED hole is for 5mm LED, might need gentle filing for a tight fit'},
    {'name': 'cover_right_side_plate', 'obj': cover.right_side_plate,
        'title': 'Right top cover',
        'desc': ''},
    {'name': 'cover_front_left_support', 'obj': cover.front_left_support,
        'title': 'Left front cover support leg',
        'desc': ''},
    {'name': 'cover_front_right_support', 'obj': cover.front_right_support,
        'title': 'Right front cover support leg',
        'desc': ''},
    {'name': 'cover_front_support', 'obj': bumper.bumper_base + cover.front_support,
        'title': 'Bumper base',
        'desc': 'Make sure to clean up supports and file space underneth the switches so bumpers can move smoothly'
     },
    {'name': 'left_bumper', 'obj': bumper.bumper_left,
        'title': 'Left bumper',
        'desc': ''
     },
    {'name': 'right_bumper', 'obj': bumper.bumper_right,
        'title': 'Right bumper',
        'desc': ''
     },
    {'name': 'left_bumper_stopper', 'obj': bumper.bumper_stopper_left,
        'title': 'Left bumper stopper',
        'desc': 'Make sure to clean it up as it is a tight fit'
     },
    {'name': 'right_bumper_stopper', 'obj': bumper.bumper_stopper_right,
        'title': 'Right bumper stopper',
        'desc': ''
     },
    {'name': 'cover_lidar_cover', 'obj': cover.lidar_cover,
        'title': 'Lidar cover',
        'desc': 'It\'s wider on top to easily grab the robot by hand and move it if necessary'
     },
    {'name': 'acrylic_base', 'obj': acrylic_base,
     'title': 'Acrylic plate base',
     'desc': 'If you have a big enough printer print this, otherwise cut it out of an acrylic plate'
     }
]


def save_stl_defs():
    with open('stls.json', 'w') as fh:
        fh.write(json.dumps(list(map(lambda x: {
                 'name': x['name'], 'title': x['title'], 'desc': x['desc']}, stls)), indent=2))


def render_stls():
    for stl in stls:
        name = stl['name']
        print(f'Rendering {name}')
        scad_render_to_file(stl['obj'], os.path.join(
            out_dir, 'to_render.scad'), file_header='$fn = %s;' % SEGMENTS)
        os.system(f'openscad -o stl/{name}.stl ./to_render.scad')


if __name__ == '__main__':
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.curdir
    file_out = os.path.join(out_dir, 'chassis.scad')

    a = full
    save_stl_defs()
#    render_stls() # run to render all stls
#    a = projection(cut = True)(acrylic_base)

    print("%(__file__)s: SCAD file written to: \n%(file_out)s" % vars())

    # Adding the file_header argument as shown allows you to change
    # the detail of arcs by changing the SEGMENTS variable.  This can
    # be expensive when making lots of small curves, but is otherwise
    # useful.
    scad_render_to_file(a, file_out, file_header='$fn = %s;' % SEGMENTS)
