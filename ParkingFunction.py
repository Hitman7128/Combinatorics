# Parking functions have multiple forms to go back and forth between and this stores each of them
class ParkingFunction(object):
    def __init__(self, car_formation, area_vector, n):
        self.car_formation = car_formation
        self.area_vector = area_vector
        self.n = n

    def get_car_formation(self):
        return self.car_formation

    def get_area_vector(self):
        return self.area_vector

    def get_occupants_vector(self):
        occ = []

        # When reading the car formation from left to right, whenever we see a car, we go up a row
        car_formation = self.car_formation
        for i in range(len(car_formation)):
            for j in range(len(car_formation[i])):
                k = car_formation[i][j]
                occ.append(k)
        return occ

    def dinv(self):
        occ = self.get_occupants_vector()
        a = self.get_area_vector()
        n = self.n
        count = 0
        for i in range(n-1):
            for j in range(i+1, n):
                # Type 1 dinv pair
                if a[i] == a[j] and occ[i] < occ[j]:
                    count += 1
                # Type 2 dinv pair
                if a[i] == a[j] + 1 and occ[i] > occ[j]:
                    count += 1
        return count

    def area(self):
        return sum(self.area_vector)

    def rise_set(self):
        a = self.get_area_vector()
        n = self.n
        rises = set()
        for i in range(1, n):
            if a[i] > a[i-1]:
                rises.add(i)
        return rises

    # Row i has a moveable valley iff you can move the car in row i one spot to the left and still have a valid PF
    def moveable_valleys(self):
        a = self.get_area_vector()
        occ = self.get_occupants_vector()
        n = self.n

        valleys = set()
        for i in range(1, n):
            # If row i has less area than row i-1, you can always do the shift
            if a[i] < a[i-1]:
                valleys.add(i)
            # This is the case when shifting the car in row i will cause it to be on top of the car in row i-1
            if a[i] == a[i-1] and occ[i] > occ[i-1]:
                valleys.add(i)
        return valleys

# Outputs an iterator of all area vectors of length n that correspond to Dyck paths
# The number of valid vectors of length n is equal to the nth Catalan number
def generate_area_sequences(n):
    def extend(seq):
        if len(seq) == n:
            yield tuple(seq)
        # This is the base case where a[0] = 0 always
        elif not seq:
            yield from extend([0])
        # Then, a[i] is between 0 to a[i-1] + 1, inclusive
        else:
            for x in range(seq[-1] + 2):
                yield from extend(seq+[x])

    yield from extend([])

# Converts the area vector into a column vector, letting us know how many car spots are in each column
def get_column_vector(area_vector):
    n = len(area_vector)
    heights = [0]*n

    # The column number containing the N move in row i can be deduced from the area vector
    for i in range(n):
        col = i - area_vector[i]
        heights[col] += 1

    return heights

# A recursive DFS style method of placing the cars
# m is the car number we're about to place
def place_cars(capacities, placement, m, n):
    # This is the base case when we placed all cars
    if m > n:
        yield placement
        return

    # We iterate over all columns with a car spot left and try all placements for car m
    for i in range(n):
        if capacities[i] > 0:
            new_capacities = capacities[:]
            new_capacities[i] -= 1
            new_placement = [col[:] for col in placement]
            new_placement[i].append(m)
            yield from place_cars(new_capacities, new_placement, m + 1, n)

# Now, we generate all parking functions
# For a sanity check, there are (n+1)^(n-1) parking functions of size n
def generate_parking_functions(n):
    # We first find all area vectors
    for area_vector in generate_area_sequences(n):
        empty_placement = [[] for _ in range(n)]
        column_vector = get_column_vector(area_vector)

        # Then we try to place the cars
        for placement in place_cars(column_vector, empty_placement, 1, n):
            yield ParkingFunction(placement, area_vector, n)
