from collections import defaultdict

# This supports multiple variables
class Polynomial:
    def __init__(self, terms=None):
        self.terms = defaultdict(int)
        if terms:
            # We want to remove 0 coefficient monomials because they mess with eq
            for m, c in terms.items():
                if c != 0:
                    self.terms[m] = c

    def __add__(self, other):
        output = Polynomial(self.terms)

        for m, c in other.terms.items():
            output.terms[m] += c

            # Deleting monomials with 0 coefficients is necessary for equals
            if output.terms[m] == 0:
                del output.terms[m]

        return output

    def __mul__(self, other):
        output = Polynomial()

        for m1, c1 in self.terms.items():
            for m2, c2 in other.terms.items():
                new_monomial = tuple(a + b for a, b in zip(m1, m2))
                output.terms[new_monomial] += c1 * c2

                # Again, we need to delete monomials with 0 coefficients
                if output.terms[new_monomial] == 0:
                    del output.terms[new_monomial]
        return output

    def __eq__(self, other):
        return self.terms == other.terms

    def __str__(self):
        return str(dict(self.terms))
