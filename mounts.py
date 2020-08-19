from solid import *
from solid.utils import *
nuts_n_bolts = import_scad('/home/leonti/3d/openscad_libraries/nutsnbolts')

inner_mount_hole = (
    translate([-3, -10, 0])(cube([6, 20, 3]))
    + translate([0, 0, -20])(cylinder(d = 3.5, h = 27))
)

nut_hole = (
  translate([0, 0, 15])(nuts_n_bolts.cyl_head_bolt.nutcatch_parallel("M3", l=15, clk=0.6))
  + translate([0, 0, -20])(cylinder(d = 3.5, h = 20))
)