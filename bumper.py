from solid import *
from solid.utils import *

elastic_angle = 24

bumper_elastic_stands = (
  translate([0, 0, 0])(cylinder(d = 10, h = 15))
  + translate([0, 70, 0])(cylinder(d = 10, h = 15))
)

elastic_stands_positioned = translate([-60, -63.8, 0])(rotate([0, 0, elastic_angle])(bumper_elastic_stands))

bumper_stopper_guides = translate([3.5, -15, 0])(
  translate([0, 5, 0])(cylinder(d = 2.7, h = 5))
  + translate([0, 25, 0])(cylinder(d = 2.7, h = 5))
)

bumper_stopper_guides_positioned = translate([-86, -38, 1])(rotate([0, 0, elastic_angle])(bumper_stopper_guides))

bumper_stopper_screw_hole = translate([-86, -38, -1])(rotate([0, 0, elastic_angle])(translate([3.5, 0, 0])
  (cylinder(d=3, h = 10))))

switch_base = (
  color("black")(cube([10.7, 20, 6.4]))
  + color("red")(translate([17.5, 16.4, 0.7])(cylinder(d = 4.7, h = 5)))
  - translate([2.7, 5.4, -1])(cylinder(d = 2.4, h = 10))
  - translate([2.7, 14.6, -1])(cylinder(d = 2.4, h = 10))
)

switch_poles = (
  cylinder(d = 2.2, h = 7)
  + translate([0, 9.2, 0])(cylinder(d = 2.2, h = 7))
)

switch_stand = color([1.0, 1.0, 1.0, 0.7])((
  translate([2.7, 5.4, 0])(switch_poles)
  + translate([0, -1.5, -1.5])(cube([10.7, 23, 1.5]))
  + translate([0, -6, -4])(cube([10.7, 6, 2.5]))
  + translate([0, 20, -4])(cube([10.7, 6, 2.5]))
))

switch_stand_left = translate([-49.5, -12.5, 5.5])(
  rotate([0, 0, 180])(switch_stand)
  )

switch_left = translate([-49.5, -12.5, 13])(
  rotate([0, 0, 180])(switch_base)
  ) 

switch_right = mirror([0, 1, 0])(switch_left)  

bumper_base = (
  cylinder(d = 190, h = 1.5)
  - translate([-55, -200, -50])(cube([400, 400, 100]))
  + elastic_stands_positioned
  + mirror([0, 1, 0])(elastic_stands_positioned)
  + bumper_stopper_guides_positioned
  + mirror([0, 1, 0])(bumper_stopper_guides_positioned)
  - bumper_stopper_screw_hole
  - mirror([0, 1, 0])(bumper_stopper_screw_hole)
  + switch_stand_left
  + mirror([0, 1, 0])(switch_stand_left)
#  - translate([-70, -20, -1])(cube([40, 40, 40]))
)

bumper_elastic_though = (
    cube([12, 44, 10])
    - translate([2, -1, 4])(cube([8, 100, 2]))
    - translate([2, 2, -1])(cube([8, 40, 100]))
    + translate([-20, 0, 0])(
      cube([30, 44, 2])
      - translate([3, 3, -1])(cube([27, 38, 4]))  
      )
      + translate([10, 20, 0])(cube([15, 4, 1.8]))
)

bumper_brim = (
    cylinder(d = 226, h = 1.5)
    - translate([0, 0, -1])(cylinder(d = 220, h = 20))
    - translate([-40, -200, -1])(cube([400, 400, 5]))
)

bumper_left = (
    cylinder(d = 220, h = 9)
    - translate([0, 0, -0.1])(cylinder(d = 217, h = 7.6))
    - translate([0, 0, -1])(cylinder(d = 200, h = 20))
    + translate([0, 0, 0])(bumper_brim)
    - translate([-35, -200, -1])(cube([400, 400, 20]))
    - translate([-120,-5,-1])(cube([400, 400, 20]))
    + translate([-70.5, -55, 9])(rotate([0, 0, elastic_angle])(bumper_elastic_though))
)

bumper_stopper_holes = (
  translate([0, 5, 0])(cylinder(d = 3, h = 10))
  + translate([0, 15, 0])(cylinder(d = 3, h = 10))
  + translate([0, 25, 0])(cylinder(d = 3, h = 10))
)

bumper_stopper = (
  translate([0, -15, 0])(cube([7, 30, 2.5]))
  + translate([4, -15-9, 2.5])(cube([3, 12, 1.5]))
  + translate([4, 15-3, 2.5])(cube([3, 12, 1.5]))
  - translate([3.5, -15, -1])(bumper_stopper_holes)
)

bumper_stopper_left = translate([-86, -38, 9])(rotate([0, 0, elastic_angle])(bumper_stopper))
bumper_stopper_right = mirror([0, 1, 0])(bumper_stopper_left)

bumper_right = mirror([0, 1, 0])(bumper_left)

bumper_base = translate([0, 0, 7.5])(bumper_base)

 

bumper = (
    bumper_base
    + color("green")(bumper_left)
    + color("green")(bumper_right)
    + switch_left 
    + switch_right
    + bumper_stopper_left
    + bumper_stopper_right
)
