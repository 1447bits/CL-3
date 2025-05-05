def fuzzy_union(A, B):
    return {x: max(A.get(x, 0), B.get(x, 0)) for x in set(A) | set(B)}

def fuzzy_intersection(A, B):
    return {x: min(A.get(x, 0), B.get(x, 0)) for x in set(A) & set(B)}

def fuzzy_complement(A):
    return {x: 1 - A[x] for x in A}

def fuzzy_difference(A, B):
    return {x: min(A.get(x, 0), 1 - B.get(x, 0)) for x in set(A)}

def cartesian_product(A, B):
    return {(x, y): min(A[x], B[y]) for x in A for y in B}

def max_min_composition(R, S):
    T = {}
    for (x, y1) in R:
        for (y2, z) in S:
            if y1 == y2:
                T[(x, z)] = max(T.get((x, z), 0), min(R[(x, y1)], S[(y2, z)]))
    return T

A = {'a': 0.5, 'b': 0.7, 'c': 0.2}
B = {'b': 0.6, 'c': 0.8, 'd': 0.4}

# Fuzzy set operations
union = fuzzy_union(A, B)
intersection = fuzzy_intersection(A, B)
complement_A = fuzzy_complement(A)
difference = fuzzy_difference(A, B)

# Fuzzy relations
R = cartesian_product(A, B)
S = cartesian_product(B, A)

# Max-min composition
composition = max_min_composition(R, S)

print("Union:", union)
print("Intersection:", intersection)
print("Complement of A:", complement_A)
print("Difference (A - B):", difference)
print("Cartesian Product R:", R)
print("Max-Min Composition:", composition)
