from pyomo.environ import *
from pyomo.environ import Var, Constraint, SolverFactory, Objective, maximize, NonNegativeReals
import matplotlib.pyplot as plt
import numpy as np


# Function to plot the constraints and the solution
def plot(model):
    x1 = np.linspace(-10, 10, 400)
    x2 = np.linspace(-10, 10, 400)  # Adjusted range for x2 based on constraints

    # Constraints
    c1 = (10 - x1) / 2
    c2 = 1 - x1

    # Objective function
    z = lambda x1, x2: x1 + 2 * x2

    # Create meshgrid
    X1, X2 = np.meshgrid(x1, x2)
    Z = z(X1, X2)

    plt.figure(figsize=(8, 6))
    plt.plot(x1, c1, label=r'$x_1 + 2x_2 \leq 10$', color='blue')
    # plt.plot(x1, np.maximum(c2, np.ones_like(c2)), label=r'$x_1 + x_2 \geq 1$', color='green')
    plt.plot(x1, c2, label=r'$x_1 + x_2 \geq 1$', color='green')
    plt.axhline(y=1, color='red')
    plt.axhline(y=4, color='red')

    plt.fill_between(x1, 1, 4, color='gray', alpha=0.3, label=r'$1 \leq x_2 \leq 4$')  # Fill feasible region for x2

    # Optimal solution
    plt.plot(model.x1.value, model.x2.value, 'ro')  # Red dot
    plt.text(model.x1.value, model.x2.value, f'  Optimal\n  ({model.x1.value:.2f}, {model.x2.value:.2f})',
             verticalalignment='bottom')

    plt.xlim(-2, 10)
    plt.ylim(-2, 6)
    plt.xlabel('$x_1$')
    plt.ylabel('$x_2$')
    plt.title('Linear Programming Solution')
    plt.legend()

    plt.savefig('../plots/plot_task1.png', dpi=300)


# Function to run the optimization model
def run(verbose: bool = False):
    model = ConcreteModel()
    model.x1 = Var(domain=NonNegativeReals)
    model.x2 = Var(bounds=(1, 4))  # Adjusted bounds for x2

    # Objective
    model.objective_function = Objective(expr=model.x1 + 2 * model.x2, sense=maximize)

    # Constraints
    model.c1 = Constraint(expr=model.x1 + 2 * model.x2 <= 10)
    model.c2 = Constraint(expr=model.x1 + model.x2 >= 1)
    model.c3 = Constraint(expr=model.x1 >= 0)
    model.c4 = Constraint(expr=model.x2 >= 1)
    model.c5 = Constraint(expr=model.x2 <= 4)

    # Solve
    SolverFactory('glpk').solve(model).write()

    print('*** *** *** ***')
    model.objective_function.display()
    model.x1.display()
    model.x2.display()
    if verbose:
        plot(model)


if __name__ == '__main__':
    run(verbose=True)
