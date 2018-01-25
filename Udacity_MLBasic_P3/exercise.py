from decimal import Decimal
from vector import Vector
from line import Line
from plane import Plane
from linsys import LinearSystem

p0 = Plane(normal_vector=Vector(['1','1','1']), constant_term='1')
p1 = Plane(normal_vector=Vector(['0','1','0']), constant_term='2')
p2 = Plane(normal_vector=Vector(['1','1','-1']), constant_term='3')
p3 = Plane(normal_vector=Vector(['1','0','-2']), constant_term='2')

s = LinearSystem([p0,p1,p2,p3])
s.swap_rows(0,1)
if not (s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3):
    print '\ntest case 1 failed'

s.swap_rows(1,3)
if not (s[0] == p1 and s[1] == p3 and s[2] == p2 and s[3] == p0):
    print '\ntest case 2 failed'

s.swap_rows(3,1)
if not (s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3):
    print '\ntest case 3 failed'

s.multiply_coefficient_and_row(1,0)
if not (s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3):
    print '\ntest case 4 failed'

s.multiply_coefficient_and_row(-1,2)
if not (s[0] == p1 and
        s[1] == p0 and
        s[2] == Plane(normal_vector=Vector(['-1','-1','1']), constant_term='-3') and
        s[3] == p3):
    print '\ntest case 5 failed'

print "\nafter test case 5: s.multiply_coefficient_and_row(-1,2)"
print s

s.multiply_coefficient_and_row(10,1)
if not (s[0] == p1 and
        s[1] == Plane(normal_vector=Vector(['10','10','10']), constant_term='10') and
        s[2] == Plane(normal_vector=Vector(['-1','-1','1']), constant_term='-3') and
        s[3] == p3):
    print '\ntest case 6 failed'

print "\nafter test case 6: s.multiply_coefficient_and_row(10,1)"
# print s
print "s[1]: ",s[1]
print "Plane(normal_vector=Vector(['10','10','10']), constant_term='10'): ", Plane(normal_vector=Vector(['10','10','10']), constant_term='10')

s.add_multiple_times_row_to_row(0,0,1)
if not (s[0] == p1 and
        s[1] == Plane(normal_vector=Vector(['10','10','10']), constant_term='10') and
        s[2] == Plane(normal_vector=Vector(['-1','-1','1']), constant_term='-3') and
        s[3] == p3):
    print '\ntest case 7 failed'

print "\nafter test case 7: s.add_multiple_times_row_to_row(0,0,1)"
print s

s.add_multiple_times_row_to_row(1,0,1)
if not (s[0] == p1 and
        s[1] == Plane(normal_vector=Vector(['10','11','10']), constant_term='12') and
        s[2] == Plane(normal_vector=Vector(['-1','-1','1']), constant_term='-3') and
        s[3] == p3):
    print '\ntest case 8 failed'

print "\nafter test case 8: s.add_multiple_times_row_to_row(1,0,1)"
print s

s.add_multiple_times_row_to_row(-1,1,0)
if not (s[0] == Plane(normal_vector=Vector(['-10','-10','-10']), constant_term='-10') and
        s[1] == Plane(normal_vector=Vector(['10','11','10']), constant_term='12') and
        s[2] == Plane(normal_vector=Vector(['-1','-1','1']), constant_term='-3') and
        s[3] == p3):
    print '\ntest case 9 failed'

print "\nafter test case 9:s.add_multiple_times_row_to_row(-1,1,0)"
print s

"""
p1 = Plane(Vector([-7.926,8.625,-7.212]),-7.95)
p2 = Plane(Vector([-2.642,2.875,-2.404]),-2.443)
if p1 == p2:
	print "equal"
elif p1.parallel(p2):
	print "parallel"
else:
	print "not parallel"


p1 = Plane(Vector([-2.611,5.528,0.283]),4.6)
p2 = Plane(Vector([7.715,8.306,5.342]),3.76)
if p1 == p2:
	print "equal"
elif p1.parallel(p2):
	print "parallel"
else:
	print "not parallel"


p1 = Plane(Vector([-0.412,3.806,0.728]),-3.46)
p2 = Plane(Vector([1.03,-9.515,-1.82]),8.65)
print p1 == p2

# exercise for line
L1 = Line(Vector([4.046,2.836]),1.21)
L2 = Line(Vector([10.115,7.09]),3.025)
print L1.intersection(L2) #infinite

L1 = Line(Vector([7.204,3.182]),8.68)
L2 = Line(Vector([8.172,4.114]),9.883)
print L1.intersection(L2)


L1 = Line(Vector([1.182,5.562]),6.744)
L2 = Line(Vector([1.773,8.343]),9.525)
print L1.intersection(L2)


# 10.cross product
v = Vector([8.462, 7.893, -8.187])
w = Vector([6.984, -5.975, 4.778])
for k, item in enumerate(v.coordinates):
        print k,item
print v.cross(w)

v = Vector([-8.987,-9.838,5.031])
w = Vector([-4.268,-1.861,-8.866])
print v.area_p(w)

v = Vector([1.5,9.547,3.691])
w = Vector([-6.007,0.124,5.772])
print v.area_t(w)


# get the projection
v = Vector([3.039,1.879])
b = Vector([0.825,2.036])
print v.proj(b)

v = Vector([-9.88,-3.264,-8.159])
b = Vector([-2.155,-9.353,-9.473])
print v.trans(b)

v = Vector([3.009,-6.172,3.692,-2.51])
b = Vector([6.404,-9.144,2.759,8.718])
print v.proj(b)
print v.trans(b)

# check parallel or orthogona
v=Vector([-7.579,-7.88])
w=Vector([22.737,23.64])
print v.poro(w)

v=Vector([-2.029,9.97,4.172])
w=Vector([-9.231,-6.639,-7.245])
print v.poro(w)

v=Vector([-2.328,-7.284,-1.214])
w=Vector([-1.821,1.072,-2.94])
print v.poro(w)

v=Vector([2.118,4.827])
w=Vector([0,0])
print v.poro(w)


v = Vector([-0.221,7.437])
v_m = v.magnitude()
v = Vector([8.813,-1.331,-6.247])
v_m2 = v.magnitude()
print v_m
print v_m2

v = Vector([1.996,3.108,-4.554])
v = Vector([5.581,-2.136])
m = v.magnitude()
r = v.times(1/m)
print "r:",v.normalized()

# check dotproduct and angle

v = Vector([7.887,4.138])
w = Vector([-8.802,6.776])
print v.dotproduct(w)

v = Vector([-5.955,-4.904,-1.874])
w = Vector([-4.496,-8.775,7.103])
print v.dotproduct(w)

v = Vector([3.183,-7.627])
w = Vector([-2.668,5.319])
print v.angle(w)

v=Vector([7.35,0.221,5.188])
w=Vector([2.751,8.259,3.985])
print v.angle(w)
"""


