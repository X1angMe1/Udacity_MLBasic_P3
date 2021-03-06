from decimal import Decimal, getcontext
from vector import Vector

getcontext().prec = 30

class Plane(object):

    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    def __init__(self, normal_vector=None, constant_term=None):
        self.dimension = 3

        if not normal_vector:
            all_zeros = ['0']*self.dimension
            normal_vector = Vector(all_zeros)
        self.normal_vector = normal_vector

        if not constant_term:
            constant_term = Decimal('0')
        self.constant_term = Decimal(constant_term) if abs(Decimal(constant_term)) > 1e-10 else Decimal('0')

        self.set_basepoint()

    def set_basepoint(self):
        try:
            n = self.normal_vector.coordinates # mei: add coordinates
            c = self.constant_term
            basepoint_coords = ['0']*self.dimension

            initial_index = Plane.first_nonzero_index(n)
            initial_coefficient = Decimal(n[initial_index]) # mei: add Decimal

            basepoint_coords[initial_index] = c/initial_coefficient
            self.basepoint = Vector(basepoint_coords)

        except Exception as e:
            if str(e) == Plane.NO_NONZERO_ELTS_FOUND_MSG:
                self.basepoint = None
            else:
                raise e

    def __str__(self):
        num_decimal_places = 3

        def write_coefficient(coefficient, is_initial_term=False):
            coefficient = round(coefficient, num_decimal_places)
            if coefficient % 1 == 0:
                coefficient = int(coefficient)

            output = ''

            if coefficient < 0:
                output += '-'
            if coefficient > 0 and not is_initial_term:
                output += '+'

            if not is_initial_term:
                output += ' '

            if abs(coefficient) != 1:
                output += '{}'.format(abs(coefficient))

            return output

        n = self.normal_vector.coordinates # mei: add coordinates

        try:
            initial_index = Plane.first_nonzero_index(n)
            terms = [write_coefficient(n[i], is_initial_term=(i==initial_index)) + 'x_{}'.format(i+1)
                     for i in range(self.dimension) if round(n[i], num_decimal_places) != 0]
            output = ' '.join(terms)

        except Exception as e:
            if str(e) == self.NO_NONZERO_ELTS_FOUND_MSG:
                output = '0'
            else:
                raise e

        constant = round(self.constant_term, num_decimal_places)
        if constant % 1 == 0:
            constant = int(constant)
        output += ' = {}'.format(constant)

        return output

    @staticmethod
    def first_nonzero_index(iterable):
        for k, item in enumerate(iterable):
            if not MyDecimal(item).is_near_zero():
                return k
        raise Exception(Plane.NO_NONZERO_ELTS_FOUND_MSG)
        
    def parallel(self,plane2):
        return self.normal_vector.parallel(plane2.normal_vector)        
        
    def __eq__(self,plane2):
        if not self.parallel(plane2):
            return False
        x0 = self.basepoint
        y0 = plane2.basepoint
        if x0 is None or y0 is None:
            return x0 is None and y0 is None
        diff = x0.minus(y0)
        return diff.orthogonal(self.normal_vector)

    def intersection(self,plane2):
        if self == plane2:
            return "infinite" #Decimal('infinite')
        elif self.parallel(plane2):
            return Decimal('NaN')
        else:
            a,b=self.normal_vector.coordinates
            c,d=plane2.normal_vector.coordinates
            k1 = self.constant_term
            k2 = plane2.constant_term
            
            x=d*k1-b*k2
            y=-c*k1+a*k2
            one_over_denom = Decimal('1')/(a*d-b*c)
            return Vector([x,y]).times(one_over_denom)

    def times(self, n):
        self.normal_vector = self.normal_vector.times(n)
        self.constant_term *= n
        return self

    def plus(self, plane2):
        self.normal_vector = self.normal_vector.plus(plane2.normal_vector)
        self.constant_term += plane2.constant_term
        return  Plane(self.normal_vector, self.constant_term) # new Plane to avoid basepoint change

class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps
