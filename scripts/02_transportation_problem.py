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

model = ConcreteModel()
model.dual = Suffix(direction=Suffix.IMPORT)

customers = list(Demand.keys())
suppliers = list(Supply.keys())

model.x = Var(customers, suppliers, domain=NonNegativeReals)


@model.Objective(sense=minimize)
def cost(m):
    return sum([T[c, s] * model.x[c, s] for c in customers for s in suppliers])


@model.Constraint(suppliers)
def src(m, s):
    return sum([model.x[c, s] for c in customers]) <= Supply[s]


@model.Constraint(customers)
def dmd(m, c):
    return sum([model.x[c, s] for s in suppliers]) == Demand[c]


results = SolverFactory('glpk').solve(model)

if 'ok' == str(results.Solver.status):
    print("Total Shipping Costs = ", model.cost())
    print("\nShipping Table:")
    for s in suppliers:
        for c in customers:
            if model.x[c, s]() > 0:
                print("Ship from ", s, " to ", c, ":", model.x[c, s]())
else:
    print("No Valid Solution Found")
