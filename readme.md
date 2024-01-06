# Operational Research UWM

### Task 1 - Basic Problem

### Task 2 - Transportation Problem
The problem objective is to minimize the total shipping cost to all customers from all sources. 

$$\mbox{minimize:}\quad \mbox{Cost} = \sum_{c \in Customers}\sum_{s \in Sources} T[c,s] x[c,s]$$

Shipments from all sources can not exceed the manufacturing capacity of the source.

$$\sum_{c \in Customers} x[c,s] \leq \mbox{Supply}[s] \qquad \forall s \in Sources$$

Shipments to each customer must satisfy their demand.

$$\sum_{s\in Sources} x[c,s] = \mbox{Demand}[c] \qquad \forall c \in Customers$$

### Sources
* [Operational Research Course](https://www.youtube.com/playlist?list=PLgA4wLGrqI-ll9OSJmR5nU4lV4_aNTgKx) a greate YouTube course by 
Yong Wang.
* [ND Pyomo Cookbook](https://jckantor.github.io/ND-Pyomo-Cookbook/README.html) a collection of notebooks showing the use Pyomo to solve modeling and optimization problems.
