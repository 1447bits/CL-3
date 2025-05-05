AH SHIT HERE WE GO AGAIN 
AI SLOP HELPING YOU OUT:

PRESS CTRL+SHIFT+V for better viewing experience. Dhanyawad

---

## 1. Theory: Genetic Algorithms (GAs)

1. **Biological Metaphor**
   GAs emulate natural evolution. A *population* of candidate solutions (individuals) evolves over generations under the forces of selection, recombination (crossover), and mutation.

2. **Representation**
   Each individual encodes a solution—here, a list of three real‐valued “genes.” The complete population explores the search space in parallel.

3. **Fitness Evaluation**
   A *fitness* function scores individuals by how well they solve the task. Our example minimizes

   $$
     f(x_1,x_2,x_3) = x_1^2 + x_2^2 + x_3^2,
   $$

   so the ideal solution is $(0,0,0)$.

4. **Selection**
   Better‐scoring individuals are preferentially chosen to reproduce. Tournament selection (here, size 3) repeatedly pits small groups against each other, advancing the best each time. This balances exploration (giving weaker individuals occasional chances) and exploitation (favoring strong ones).

5. **Crossover (Recombination)**
   Pairs of parents exchange genetic material to produce offspring. Blend crossover (`cxBlend` with α=0.5) takes each gene as a convex combination of the two parents:

   $$
     \text{offspring}_i = (1-\lambda)\,\text{parent1}_i + \lambda\,\text{parent2}_i,\quad \lambda\in[-\alpha,1+\alpha].
   $$

6. **Mutation**
   Each gene of each offspring may be perturbed by adding Gaussian noise (`mutGaussian`):

   $$
     x_i \leftarrow x_i + \mathcal{N}(\mu=0,\sigma=1)
   $$

   with probability 0.2 per gene. Mutation introduces new variation and helps escape local minima.

7. **Generational Loop**
   Over a fixed number of generations, we:

   * **Generate** offspring by applying crossover (with probability 0.5 between random pairs) and mutation (with probability 0.1 per individual).
   * **Evaluate** their fitness.
   * **Select** a new population of the same size via tournament selection on the offspring.
     At the end, the best individual is returned.

---

## 2. Code Walkthrough

```python
import random
from deap import base, creator, tools, algorithms
```

* **Imports**:

  * `random` for uniform sampling.
  * DEAP’s core modules:

    * `base` to build the GA toolbox,
    * `creator` to define custom Fitness and Individual classes,
    * `tools` for built-in operators,
    * `algorithms` for utility functions (here only `varAnd`).

```python
# Define the evaluation function (minimize a simple mathematical function)
def eval_func(individual):
    # Example evaluation function (minimize a quadratic function)
    return sum(x ** 2 for x in individual),
```

* **Fitness**: returns a 1-tuple (note the trailing comma) equal to the sum of squares of the three genes. Lower is better.

```python
# DEAP setup
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)
```

* **FitnessMin**: a subclass of `base.Fitness` with a single objective to *minimize* (weight = −1.0).
* **Individual**: a subclass of Python’s `list` that carries a `.fitness` attribute of type `FitnessMin`.

```python
toolbox = base.Toolbox()
```

* A container for registering all GA components.

```python
# Define attributes and individuals
toolbox.register("attr_float", random.uniform, -5.0, 5.0)
toolbox.register("individual",
                 tools.initRepeat,
                 creator.Individual,
                 toolbox.attr_float,
                 n=3)
toolbox.register("population",
                 tools.initRepeat,
                 list,
                 toolbox.individual)
```

* **attr\_float**: draws one gene uniformly in \[−5,5].
* **individual**: constructs an `Individual` by repeating `attr_float` three times.
* **population**: builds a `list` of such individuals.

```python
# Evaluation function and genetic operators
toolbox.register("evaluate", eval_func)
toolbox.register("mate", tools.cxBlend, alpha=0.5)
toolbox.register("mutate", tools.mutGaussian,
                 mu=0, sigma=1, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)
```

* **evaluate**: links to our `eval_func`.
* **mate**: blend crossover with α=0.5.
* **mutate**: Gaussian mutation (μ=0, σ=1) applied gene-wise with independent probability 0.2.
* **select**: tournament selection of size 3.

```python
# Create population
population = toolbox.population(n=50)

# Genetic Algorithm parameters
generations = 20
```

* **population**: 50 random individuals.
* **generations**: we’ll run 20 evolution cycles.

```python
# Run the algorithm
for gen in range(generations):
    # a) Generate offspring from current population
    offspring = algorithms.varAnd(population,
                                 toolbox,
                                 cxpb=0.5,
                                 mutpb=0.1)

    # b) Evaluate the fitness of the offspring
    fits = list(map(toolbox.evaluate, offspring))
    for fit, ind in zip(fits, offspring):
        ind.fitness.values = fit

    # c) Select the next generation population
    population = toolbox.select(offspring,
                                k=len(population))
```

* **algorithms.varAnd** applies:

  * Crossover with overall probability `cxpb=0.5` between random mates.
  * Mutation with overall probability `mutpb=0.1` per individual.
* We then **evaluate** all offspring and set their `.fitness.values`.
* Finally, we **select** 50 individuals (with replacement) via tournament to form the next generation.

```python
# Get the best individual after generations
best_ind = tools.selBest(population, k=1)[0]
best_fitness = best_ind.fitness.values[0]

print("Best individual:", best_ind)
print("Best fitness:", best_fitness)
```

* **selBest** retrieves the top‐scoring individual.
* We print its gene tuple (ideally close to `[0.0,0.0,0.0]`) and its minimal sum of squares.

---

## 3. Hyperparameters & Tuning

| Parameter        | Meaning                                              | Effect of Increasing                                          |
| ---------------- | ---------------------------------------------------- | ------------------------------------------------------------- |
| Population size  | Number of individuals per generation                 | More exploration, slower                                      |
| Generations      | Number of evolution cycles                           | Better convergence, slower                                    |
| cxpb (crossover) | Probability of mating pairs                          | More mixing, risk of loss of good building blocks if too high |
| mutpb (mutation) | Probability of mutating each offspring               | More exploration, but noise can disrupt fine tuning           |
| indpb (gene p.)  | Probability of mutating each gene within an mutation | Controls extent of mutation per individual                    |

Tuning balances exploration (finding global minima) against exploitation (refining good solutions).

---

### In Summary

This DEAP script implements a classic real-valued genetic algorithm to *minimize* a quadratic function. You define how to encode solutions, measure their quality, and apply biologically inspired operators—selection, crossover, and mutation—iteratively refining the population toward the optimal $(0,0,0)$.
