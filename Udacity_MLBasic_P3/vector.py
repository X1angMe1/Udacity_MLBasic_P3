import math
from decimal import Decimal
class Vector(object):
    """docstring for ClassName"""
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            coordinates = [Decimal(x) for x in coordinates]
            self.coordinates = tuple(coordinates)
            self.dimension = len(coordinates)
        except ValueError:
            raise ValueError('The coordinates must be non-empty')
        except TypeError:
            raise TypeError('The coordinates must be an iterable')

    def __str__(self):
        self.coordinates = [round(x,10) for x in self.coordinates]
        return 'Vector: {}'.format(self.coordinates)

    def __eq__(self,v):
        return  self.coordinates == v.coordinates

    def plus(self,v):
        result = [ x+y for (x,y) in zip(self.coordinates,v.coordinates)]
        return Vector(result)
        
    def minus(self,v):
        result =  [x-y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(result)

    def times(self,n):
        n = Decimal(n)
        result = [x * n for x in self.coordinates]
        return Vector(result)

    def magnitude(self):
        # result is number
        result = [x*x for x in self.coordinates]
        return math.sqrt(sum(result))

    def normalized(self):
        # return the normalized vector of self
        try:
            return self.times(1./self.magnitude())
        except ZeroDivisionError:
            raise Exception("Cannot normalize the zero vector")

    def dot(self,v):
        # result is number
        result = [x * y for x,y in zip(self.coordinates, v.coordinates)]
        return sum(result)

    def angle(self,v,degree=False):
        if self.is_zero() or v.is_zero():
            raise Exception("Cannot compute an aggle with the zero vector")
        u1 = self.normalized()
        u2 = v.normalized()
        temp = u1.dot(u2)
        if temp > 1:
            temp =1
        if temp < -1:
            temp = -1
        result = math.acos(temp)
        if degree:
            degree_per_radian = 180. / math.pi
            return result  * degree_per_radian
        return result

    def parallel(self,v):
        # check whether self is parallel to v
        return(self.is_zero() or 
               v.is_zero() or 
               self.angle(v) == 0 or 
               self.angle(v) == math.pi)

    def orthogonal(self,v,tolerance = 1e-10):
        # check whether self is orthogonal to v
        return abs(self.dot(v)) < tolerance

    def poro(self,v):
        # check whether self is parallel or orthogonal to v
        return self.parallel(v),self.orthogonal(v)
        
    def is_zero(self, tolerance=1e-10):
        return self.magnitude() < tolerance

    def proj(self,b):
        # return the component vector of self that parallel to b
        ub = b.normalized()
        n = self.dot(ub)
        result = ub.times(n)
        return result
        
    def trans(self,b):
        # return the component vector of self that orthogonal to b
        proj = self.proj(b)
        result = self.minus(proj)
        return result
        
    def cross(self,w):
        # the cross product of self and w, self and w are 3D
        x1,y1,z1 = self.coordinates
        x2,y2,z2 = w.coordinates
        result = [y1*z2-y2*z1,-(x1*z2-x2*z1),x1*y2-x2*y1]
        return Vector(result)

    def area_p(self,w):
        # return the parallelogram area of self and w
        c = self.cross(w)
        result = c.magnitude()
        return result
        
    def area_t(self,w):
        # return the triangle area of self and w
        return 0.5 * self.area_p(w)