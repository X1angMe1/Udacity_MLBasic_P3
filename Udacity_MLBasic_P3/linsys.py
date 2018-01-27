from decimal import Decimal, getcontext
from copy import deepcopy

from vector import Vector
from plane import Plane

getcontext().prec = 30


class LinearSystem(object):

    ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG = 'All planes in the system should live in the same dimension'
    NO_SOLUTIONS_MSG = 'No solutions'
    INF_SOLUTIONS_MSG = 'Infinitely many solutions'

    def __init__(self, planes):
        try:
            d = planes[0].dimension
            for p in planes:
                assert p.dimension == d

            self.planes = planes
            self.dimension = d

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)

    def compute_rref(self):
        tf = self.compute_triangular_form()

        # Step1: set c of x/y/z to 1
        l = len(tf)
        if len(tf) > 3:
            l = 3
        for i in range(l):
            tf = tf.set_c_to_1(i)
        
        # step2: z into x/y row
        non_zero = tf.indices_of_first_nonzero_terms_in_each_row()
        y = -1
        z = -1
        if 1 in non_zero:
            y = non_zero.index(1)
        if 2 in non_zero:
            z = non_zero.index(2)
        if z != -1:
            if y != -1:
                y_z_c = tf[y].normal_vector.coordinates[2]
                tf = tf.add_multiple_times_row_to_row(-y_z_c, z,y) # add z to y row

            x_z_c = tf[0].normal_vector.coordinates[2]
            tf = tf.add_multiple_times_row_to_row(-x_z_c, z,0) # add z to x row

        # step3: y into x row
        if y != -1:
            x_y_c = tf[0].normal_vector.coordinates[1]
            tf = tf.add_multiple_times_row_to_row(-x_y_c, y, 0)
        return tf

    def set_c_to_1(self,row):
        non_zero = self.indices_of_first_nonzero_terms_in_each_row()
        r = -1
        if row in non_zero:
            r = non_zero.index(row)
        if r != -1:
            c = self[r].normal_vector.coordinates[row]
            self = self.multiply_coefficient_and_row(1/c,row)
        return self

    def compute_triangular_form(self):
        system = deepcopy(self)
        for i in range(len(system) - 1):
            system = system.temp(i)
        return system

    def temp(self, row):
        non_zero = self.indices_of_first_nonzero_terms_in_each_row()
        if non_zero[row] > row:
            n = non_zero.index(row)
            self = self.swap_rows(row, n)

        c = self[row].normal_vector.coordinates[row] 
        for i in range(row + 1, len(self)):
            n = self[i].normal_vector.coordinates[row]
            self = self.add_multiple_times_row_to_row(-n/c,row,i)
        return self

    def swap_rows(self, row1, row2):
        self[row1],self[row2] = self[row2],self[row1]
        return self

    def multiply_coefficient_and_row(self, coefficient, row):
        self[row].times(coefficient)
        return self


    def add_multiple_times_row_to_row(self, coefficient, row_to_add, row_to_be_added_to):
        temp = Plane(self[row_to_add].normal_vector, self[row_to_add].constant_term)
        self[row_to_be_added_to] = self[row_to_be_added_to].plus(temp.times(coefficient))
        return self

    def indices_of_first_nonzero_terms_in_each_row(self):
        num_equations = len(self)
        num_variables = self.dimension

        indices = [-1] * num_equations

        for i,p in enumerate(self.planes):
            try:
                indices[i] = p.first_nonzero_index(p.normal_vector.coordinates) # mei: add coordinates
            except Exception as e:
                if str(e) == Plane.NO_NONZERO_ELTS_FOUND_MSG:
                    continue
                else:
                    raise e

        return indices


    def __len__(self):
        return len(self.planes)


    def __getitem__(self, i):
        return self.planes[i]


    def __setitem__(self, i, x):
        try:
            assert x.dimension == self.dimension
            self.planes[i] = x

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)

    def removeItem(self,index):
        result = []
        for i in range(len(self)):
            if i != index:
                result.append(self[i])
        self = LinearSystem(result)
        return self

    def __str__(self):
        ret = 'Linear System:\n'
        temp = ['Equation {}: {}'.format(i+1,p) for i,p in enumerate(self.planes)]
        ret += '\n'.join(temp)
        return ret


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps



