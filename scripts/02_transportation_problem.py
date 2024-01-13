from pyomo.environ import *

Demand = {
    'Customer1': 50,
    'Customer2': 80,
    'Customer3': 50,
    'Customer4': 70,
    'Fictional_Customer': 40,
}

Supply = {
    'Supplier1': 80,
    'Supplier2': 140,
    'Supplier3': 70
}

# T = {
#     ('Supplier1', 'Customer1'): 4,
#     ('Supplier1', 'Customer2'): 2,
#     ('Supplier1', 'Customer3'): 3,
#     ('Supplier1', 'Customer4'): 1,
#     ('Supplier1', 'Fictional_Customer'): 0,
#     ('Supplier2', 'Customer1'): 6,
#     ('Supplier2', 'Customer2'): 3,
#     ('Supplier2', 'Customer3'): 5,
#     ('Supplier2', 'Customer4'): 6,
#     ('Supplier2', 'Fictional_Customer'): 0,
#     ('Supplier3', 'Customer1'): 3,
#     ('Supplier3', 'Customer2'): 2,
#     ('Supplier3', 'Customer3'): 6,
#     ('Supplier3', 'Customer4'): 3,
#     ('Supplier3', 'Fictional_Customer'): 0,
# }
#
# T_swapped = {(c, s): T[(s, c)] for s, c in T}
# print(T_swapped)
T = {
    ('Customer1', 'Supplier1'): 4,
    ('Customer2', 'Supplier1'): 2,
    ('Customer3', 'Supplier1'): 3,
    ('Customer4', 'Supplier1'): 1,
    ('Fictional_Customer', 'Supplier1'): 0,
    ('Customer1', 'Supplier2'): 6,
    ('Customer2', 'Supplier2'): 3,
    ('Customer3', 'Supplier2'): 5,
    ('Customer4', 'Supplier2'): 6,
    ('Fictional_Customer', 'Supplier2'): 0,
    ('Customer1', 'Supplier3'): 3,
    ('Customer2', 'Supplier3'): 2,
    ('Customer3', 'Supplier3'): 6,
    ('Customer4', 'Supplier3'): 3,
    ('Fictional_Customer', 'Supplier3'): 0
}

# Step 0: Create an instance of the model
model = ConcreteModel()
model.dual = Suffix(direction=Suffix.IMPORT)

# Step 1: Define index sets
CUS = list(Demand.keys())
SRC = list(Supply.keys())

# Step 2: Define the decision
model.x = Var(CUS, SRC, domain=NonNegativeReals)


# Step 3: Define Objective
@model.Objective(sense=minimize)
def cost(m):
    return sum([T[c, s] * model.x[c, s] for c in CUS for s in SRC])


# Step 4: Constraints
@model.Constraint(SRC)
def src(m, s):
    return sum([model.x[c, s] for c in CUS]) <= Supply[s]


@model.Constraint(CUS)
def dmd(m, c):
    return sum([model.x[c, s] for s in SRC]) == Demand[c]


results = SolverFactory('glpk').solve(model)

# for c in CUS:
#     for s in SRC:
#         print(c, s, model.x[c,s]())
if 'ok' == str(results.Solver.status):
    print("Total Shipping Costs = ", model.cost())
    print("\nShipping Table:")
    for s in SRC:
        for c in CUS:
            if model.x[c, s]() > 0:
                print("Ship from ", s, " to ", c, ":", model.x[c, s]())
else:
    print("No Valid Solution Found")
