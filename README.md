# [Social Golfers Problem](https://en.wikipedia.org/wiki/Social_golfer_problem)

Can $N$ golfers be scheduled to play in $G$ groups of size $S$ over $R$ rounds so that no pair of golfers plays together more than $T$ times?

## Problem description

Given $N, G, S, R, T \in \mathbb{N}$, where $N = G \cdot S$ is the following statement $true$?

There exists a valid schedule in which $N$ golfers play in $G$ groups of size $S$ over $R$ rounds so that no pair of golfers plays together more than $T$ times.

The problem is to find a valid assignment of players to groups across all rounds that satisfies the following conditions:

1. **Group partition** - In every round all $N$ golfers must be in $G$ groups of size $S$.
2. **Pairing constraint** - Across all rounds, each pair of golfers share the same group at most $T$ times.

## Encoding

We encode the [Social Golfers Problem](https://en.wikipedia.org/wiki/Social_golfer_problem) as a [boolean satisfiability problem](https://en.wikipedia.org/wiki/Boolean_satisfiability_problem).

### Variables

We introduce the boolean variable $X_{r,p,g}$ which is defined as follows:

$$
X_{r,p,g} =
\begin{cases}
1, & \text{if player } p \text{ is in group } g \text{ during round } r, \\
0, & \text{otherwise.}
\end{cases}
$$

### Constraints

1. Each player is exactly in one group per round. That can be written as follows:

$$
\forall r \in \{1, \dots, R\}, \forall p \in \{1, \dots, N\}: \left( \left( \bigvee_{g=1}^{G} X_{r,p,g} \right) \land \left( \bigwedge_{g_1=1}^{G} \bigwedge_{g_2=g_1+1}^{G} \neg (X_{r,p,g_1} \land X_{r,p,g_2}) \right) \right)
$$

2. Each group has exactly $S$ golfers:

$$
\forall r \in \{1, \dots, R\}, \forall g \in \{1, \dots, G\}: \sum_{p=1}^{N} X_{r,p,g} = S
$$

3. No pair of players plays together more than T times

$$
\forall 1 \le p_1 < p_2 \le N:
\quad
\sum_{r=1}^{R} \sum_{g=1}^{G} (X_{r,p_1,g} \land X_{r,p_2,g}) \le T
$$


## State of application

* Core
  * Improve core functionality
    * Add correct clause generation
    * Add correct clause counter
  * Add result interpreter
  * Add basic tests + instances
  * Code refactoring
* Test
  * Write tests for the Core
* Frontend
  * Create new project (C#, why not?)
  * Create the static pages
  * Write backend - basic workflow
  * Refactor
