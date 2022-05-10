from functools import reduce
import mounts
import motors_stand
from solid import *
from solid.utils import *
import lcd_case
import power_button_case

nuts_n_bolts = import_scad('/home/leonti/3d/openscad_libraries/nutsnbolts')

elastic_angle = 24
rover_diameter = 220
acrylic_plate_diameter = 208

acrylic_plate = translate([0, 0, 1.75])(
    cylinder(d=acrylic_plate_diameter, h=3))

back_left_holes = (
    translate([45, -85, -1])(cylinder(d=3.5, h=10))
    + translate([87, -45, -1])(cylinder(d=3.5, h=10))
)

back_base_mounts = (
    cylinder(d=acrylic_plate_diameter, h=1.5)
    - translate([-140, 0, -1])(cube([300, 150, 5]))
    - translate([-140, -140, -1])(cube([150, 150, 5]))
    - translate([0, -140, -1])(cube([35, 150, 5]))
    - translate([0, -80, -1])(cube([82, 81, 5]))
    - translate([0, -40, -1])(cube([97, 41, 5]))
    - translate([0, -11, -1])(cube([102, 12, 5]))
    - back_left_holes
)

nut_catch = (
    cylinder(d=9, h=3)
    - translate([0, 0, 4]
                )(nuts_n_bolts.cyl_head_bolt.nutcatch_parallel("M3", l=10, clk=0.6))
)

back_base = (
    cylinder(d=rover_diameter, h=6.5)
    - translate([-140, 0, -1])(cube([300, 150, 10]))
    - translate([-140, -140, -1])(cube([150, 150, 10]))
    - translate([0, -140, -1])(cube([35, 150, 10]))
    - translate([0, 0, -1])(cylinder(d=acrylic_plate_diameter, h=8))
    + back_base_mounts
    + translate([0, 0, 5])(back_base_mounts)
    + translate([45, -85, 6.5])(nut_catch)
    + translate([87, -45, 6.5])(nut_catch)
)

back_top_cover_holes_left_coords = [
    (103, -20),
    (68, -80),
    (45, -94.5)
]

back_top_cover_holes_left = reduce(lambda a, b: a + b, map(
    lambda xy: translate([xy[0], xy[1], -1])(cylinder(d=3.5, h=4)),
    back_top_cover_holes_left_coords)
)

back_top_cover_nut_catches = reduce(lambda a, b: a + b, map(
    lambda xy: translate([xy[0], xy[1], -3])((
        cylinder(d=10, h=3)
        - translate([0, 0, -1])(mounts.nut_hole)
    )),
    back_top_cover_holes_left_coords)
)

back_top_cover_rim_left = (
    cylinder(d=rover_diameter, h=1.5)
    - translate([0, 0, -1])(cylinder(d=rover_diameter - 18, h=8))
    - translate([-140, 0, -1])(cube([300, 150, 10]))
    - translate([-140, -140, -1])(cube([150, 150, 10]))
    - translate([0, -140, -1])(cube([35, 150, 10]))
    - back_top_cover_holes_left
    + back_top_cover_nut_catches
)

back_top_plate = translate([0, 0, 72])(
    cylinder(d=rover_diameter, h=1.5)
    - translate([-195, -125, -1])(cube([250, 250, 4]))
    - back_top_cover_holes_left
    - mirror([0, 1, 0])(back_top_cover_holes_left)
)

right_side_plate = (translate([0, 0, 72])(
    cylinder(d=rover_diameter, h=1.5)
    - translate([55, -125, -1])(cube([250, 250, 4]))
    - mirror([1, 0, 0])(translate([55, -125, -1])(cube([250, 250, 4])))
    - translate([-125, -(250 - 80/2), -1])(cube([250, 250, 4]))
    - mirror([0, 1, 0])(back_top_cover_holes_left)
    - mirror([1, 0, 0])(mirror([0, 1, 0])(back_top_cover_holes_left))
)
    - motors_stand.full_for_holes)

usb_connector_hole = rotate([270, 0, 0])(cylinder(d = 3.7, h = 10))

usb_connector_holes = (
    usb_connector_hole
    + translate([8.5, 0, 0])(usb_connector_hole)
)

usb_connector = (
    cube([15, 1.6, 15])
    + translate([3.5, 1.6, 10.5])(cube([8, 3, 10]))
    - translate([3.2, -2, 5.8])(usb_connector_holes)
)

usb_connector_holder = translate([0, -4, 3])(
    cube([15, 4, 12])
    + translate([6.5, -7, 6])(cube([2, 7, 6]))
    - translate([3.2, -2, 2.8])(usb_connector_holes)
)

def usb_connector_translate(part):
    return translate([-7.5, -67, 57])(part)

left_side_plate = (
    mirror([0, 1, 0])(right_side_plate)
#    - translate([45, -70, 71])(cylinder(d=7, h=4))
#    - usb_connector_translate(usb_connector)
#    + usb_connector_translate(usb_connector_holder)
) - lcd_case.full(True) + lcd_case.stands() - power_button_case.full(True) + power_button_case.stands

front_top_plate = mirror([1, 0, 0])(back_top_plate)

outer_shell_left = (
    cylinder(d=rover_diameter, h=64)
    - translate([-140, 0, -1])(cube([300, 150, 100]))
    - translate([-140, -140, -1])(cube([150, 150, 100]))
    - translate([0, -140, -1])(cube([35, 150, 100]))
    - translate([0, 0, -1])(cylinder(d=rover_diameter - 3, h=100))
)

cut_out_ring = (
    cylinder(d=rover_diameter + 20, h=64)
    - translate([0, 0, -1])(cylinder(d=rover_diameter - 3, h=100))
)

back_left_shell_base = (
    translate([0, 0, 6.5])(outer_shell_left)
    + translate([rover_diameter/2 - 8.5, -1.5, 6.5])((
        cube([7.5, 1.5, 64])
        - translate([-0.5, -2, 0])(cube([2, 5, 6]))
    ))
    - translate([105, 1, 25])(rotate([90, 0, 0])((
        cylinder(d=3.5, h=50)
        + translate([0, 0, 10])(cylinder(d=4.5, h=40))
    )))
    - translate([105, 1, 55])(rotate([90, 0, 0])((
        cylinder(d=3.5, h=50)
        + translate([0, 0, 10])(cylinder(d=4.5, h=40))
    )))
    + translate([0, 0, 70.5])(back_top_cover_rim_left)
)

back_left = (
    back_base
    + back_left_shell_base
)

back_right = mirror([0, 1, 0])(back_left)

front_left_support_hole = (
    translate([0, 0, 15])(
        nuts_n_bolts.cyl_head_bolt.nutcatch_parallel("M3", l=15, clk=0.6))
    + translate([0, 0, -20])(cylinder(d=3.5, h=20))
)


def generate_front_left_support(hole_placeholders=False):
    bottom_holes = translate([-(42 + 10), -77, 1.5 + 0.4 + 3])(
        translate([5, 5, 2])(front_left_support_hole)
        + translate([5, 25, 2])(front_left_support_hole)
    )
    support_base = (translate([-(42 + 10), -77, 1.5 + 0.4 + 3])(
        cube([10, 30, 4])
        + translate([16, 13, 4])(rotate([0, 0, 150])(cube([10, 37, 10])))
        - translate([10, 0, 0])(cube([10, 40, 40]))
        + translate([5, 25, 4])(cylinder(d=10, h=2))
        - translate([5, 5, 6])(cylinder(d=8, h=20))
    )
        - cut_out_ring
    )

    if hole_placeholders is True:
        return (support_base
                + translate([-54.5, -86.5, 14]
                            )(rotate([90, 90, -30])(cylinder(d=3.5, h=30)))
                + bottom_holes
                )
    else:
        return (support_base
                - translate([-54.5, -86.5, 14])(rotate([90, 90, -30])
                                                (mounts.inner_mount_hole))
                - bottom_holes
                )


front_left_support = generate_front_left_support()
front_right_support = mirror([0, 1, 0])(front_left_support)


def generate_front_support(hole_placeholders=False):
    fork_left_hole = translate([0, 7, 0])(
        rotate([0, -90, 4])(mounts.inner_mount_hole))

    front_fork = (
        cube([15, 25, 10])
        - translate([-1, 11.5 - (3.5/2), -1])(cube([9, 3.5, 20]))
        - translate([5.5, -2, 5])(fork_left_hole)
    )

    left_side = translate([-95, -5, 3 + 0.4 + 1.5])(
        cube([35, 10, 4])
        + translate([-3.5, 0, 4])((
            cube([20, 10, 10])
            + translate([-10, -7.5, 0])(front_fork)
        )
        )
        - translate([-20, 5, 0-1])(cube([70, 20, 30]))
    )

    front_support_base = (
        left_side
        + mirror([0, 1, 0])(left_side)
        + translate([-66, 0, 9])(cylinder(d=10, h=2))
        - translate([-66, 0, 8])(mounts.nut_hole)
        - cut_out_ring)

    placeholder_left = translate(
        [-100, -7.25, 14])(rotate([0, -90, 4])(mounts.cylinder(d=3.5, h=40)))
    placeholders = (
        placeholder_left
        + mirror([0, 1, 0])(placeholder_left)
    )

    if hole_placeholders is True:
        return front_support_base + placeholders + translate([-66, 0, 8])(mounts.nut_hole)
    else:
        return front_support_base


front_left = (
    mirror([1, 0, 0])(back_left_shell_base)
    - cylinder(d=rover_diameter + 10, h=9)
    - generate_front_left_support(True)
    - generate_front_support(True)
)

front_right = mirror([0, 1, 0])(front_left)

front_support = generate_front_support()


def connector(length, type='all'):
    outer = (
        cube([4, 4.5, length])
        - translate([-1, (4.5 - 1.7)/2, -1])(cube([3, 1.7, length + 2]))
        - translate([2, 4.5/2, -1])(cylinder(d=2.7, h=length + 2))
    )
    inner = translate([-1.6, -1.55, 0])((
        cube([5.6, 4.5, length])
        - translate([1.5, (4.5 - 1.7)/2, -1])(cube([10, 1.7, length + 2]))
        - translate([3, 3, -1])(cube([10, 2, length + 2]))
        + translate([3.6, 3.8, 0])(cylinder(d=2.2, h=length))
    ))
    connectors = {
        'inner': inner,
        'outer': outer
    }

    return connectors.get(type, (
        inner + outer
    ))


connector_test = connector(length=15, type='all')

def create_lidar_cover():
    outer_cover = hull()(translate([-1, 0, 0])(cylinder(d = 90, h = 29))
        + translate([-46.5, 0, 0])(cylinder(d = 44, h = 29)))
    
    skirt = hull()(translate([-1, 0, 0])(cylinder(d = 90 + 35, h = 1.5))
        + translate([-26.5, -55, 0])(cylinder(d = 15, h = 1.5))
        + translate([-26.5, 55, 0])(cylinder(d = 15, h = 1.5))
        + translate([-46.5, 0, 0])(cylinder(d = 44 + 35, h = 1.5)))

    upper_skirt = (translate([-1, 0, 29-5])(hull()(translate([-1, 0, 0])(cylinder(d = 90 + 10, h = 5))
        + translate([-46.5, 0, 0])(cylinder(d = 44 + 10, h = 5)))))

    cover = (
  #  translate([-67, -40, 0])(
  #      cube([105, 80, 29])
  #      - translate([1.5, 1.5, -1])(cube([105 - 3, 80 - 3, 29 - 1.5 + 1]))
  #  )
  #  + translate([-82, -60, 0])(
  #      cube([120, 120, 1.5])
  #      - translate([16, 21.5, -1])(cube([105, 80 - 3, 10]))
  #  )
  #  - translate([-1, 0, 25])(cylinder(d=75, h=7))
    skirt
    + outer_cover
    + upper_skirt
    - hull()(translate([-1, 0, -1])(cylinder(d = 90 - 3, h = 29 - 0.5))
        + translate([-46.5, 0, -1])(cylinder(d = 44 - 3, h = 29 - 0.5)))
    - translate([-1, 0, 25])(cylinder(d=75, h=7))
    )

    return translate([7, 0, 73.5])(cover) - motors_stand.full_for_holes 

lidar_cover = create_lidar_cover()

full = (
    back_left
    + back_right
    + back_top_plate
    + left_side_plate
    + right_side_plate
    + front_top_plate
    + front_left_support
    + front_right_support
    + front_left
    + front_right
    #  + acrylic_plate
    + front_support
    + lidar_cover
)

for_holes = (
    back_left_holes
    + mirror([0, 1, 0])(back_left_holes)
    + generate_front_left_support(True)
    + mirror([0, 1, 0])(generate_front_left_support(True))
    + generate_front_support(True)
)

explode_distance = 40
full_exploded = (
    translate([explode_distance, -explode_distance, 0])(back_left)
    + translate([explode_distance, explode_distance, 0])(back_right)
    + translate([explode_distance*2, explode_distance *
                 2, explode_distance*2])(back_top_plate)
    + translate([explode_distance*2, explode_distance *
                 2, explode_distance*2])(left_side_plate)
    + translate([explode_distance*2, explode_distance *
                 2, explode_distance*2])(right_side_plate)
    + translate([explode_distance*2, explode_distance *
                 2, explode_distance*2])(front_top_plate)
    + translate([explode_distance*2, explode_distance *
                 2, explode_distance*2])(lidar_cover)
    + translate([-explode_distance, -explode_distance, 0])(front_left)
    + translate([-explode_distance, explode_distance, 0])(front_right)
    + front_left_support
    + front_right_support
    #  + acrylic_plate
    + front_support

)
