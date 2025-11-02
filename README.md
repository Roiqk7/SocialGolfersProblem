# [Social Golfers Problem](https://en.wikipedia.org/wiki/Social_golfer_problem)

Can $N$ golfers be scheduled to play in $G$ groups of size $S$ over $R$ rounds so that no pair of golfers plays together more than $T$ times?

## Problem description

Given $N, G, S, R, T \in \mathbb{N}$, where $N = G \cdot S$ is the following statement $true$?

There exists a valid schedule in which $N$ golfers play in $G$ groups of size $S$ over $R$ rounds so that no pair of golfers plays together more than $T$ times.

The problem is to find a valid assignment of players to groups across all rounds that satisfies the following conditions:

1. **Group partition** - In every round all $N$ golfers must be in exactly one group.
2. **Group size** - In every round all groups must contain exactly $S$ players.
2. **Pairing constraint** - Across all rounds, each pair of golfers share the same group at most $T$ times.

## Encoding

We encode the [Social Golfers Problem](https://en.wikipedia.org/wiki/Social_golfer_problem) as a [boolean satisfiability problem](https://en.wikipedia.org/wiki/Boolean_satisfiability_problem).

### Variables

1. Player $p$ is in group $g$ during round $r$:

Boolean variable $X_{r,p,g}$ which is defined as follows:

$$
X_{r,p,g} =
\begin{cases}
1, & \text{if player } p \text{ is in group } g \text{ during round } r, \\
0, & \text{otherwise.}
\end{cases}
$$

2. Pair of players $\{p_1, p_2\}$ meet in group $g$ during round $r$:

Boolean variable $Z_{r,\{p_1,p_2\},g}$, defined as:

$$
Z_{r,\{p_1,p_2\},g} =
\begin{cases}
1, & \text{if both players } p_1 \text{ and } p_2 \text{ are in group } g \text{ during round } r, \\
0, & \text{otherwise.}
\end{cases}
$$

This gives us the total number of all variables:

$$
R \cdot \Big[N \cdot G + \binom{N}{2} \cdot (1 + G) \Big]
$$

### Constraints

1. Each player is exactly in one group per round. That can be written as follows:

$$
\left( \bigvee_{g=1}^{G} X_{r, p, g} \right) \land
\left( \bigwedge_{1 \le g_1 < g_2 \le G} (\neg X_{r, p, g_1} \lor \neg X_{r, p, g_2}) \right)
$$

2. Each group has exactly $S$ golfers:

$$
\bigwedge_{\substack{U\subseteq\{1,\dots,N\}\\|U|=N-(S-1)}}
\left(
  \bigvee_{p\in U} X_{r,p,g}
\right)
$$

*Note:* Here we actually just ensure that each group has at most $S$ players, which in combination with constraint 1 is enough.

3. No pair of players plays together more than $T$ times:

$$
\bigwedge_{\substack{U\subseteq\{1,\dots,R\}\\|U|=T+1}}
\left(
  \bigvee_{r\in U} \neg Y_{r,\{p_1,p_2\}}
\right)
$$

## State of application

### TODO:

* Frontend
  * Create new project (C#)
  * Create the static pages
  * Write backend - basic workflow
  * Refactor

### What the application cannot do:

* Optimisation
  * There are probably better ways to generate less clauses
  * The clause generation could be multi-threadeds
    * Each constraint would be written to its own file, then they would be synthesized at the end
  * I might want to rewrite it to C# and make this a full C# project
