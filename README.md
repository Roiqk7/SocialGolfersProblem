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

Total count of $X_{r,p,g}$ variables is $N \cdot G \cdot R$

2. Pair of players $\{p_1, p_2\}$ meet in group $g$ during round $r$:

Boolean variable $Z_{r,\{p_1,p_2\},g}$, defined as:

$$
Z_{r,\{p_1,p_2\},g} =
\begin{cases}
1, & \text{if both players } p_1 \text{ and } p_2 \text{ are in group } g \text{ during round } r, \\
0, & \text{otherwise.}
\end{cases}
$$

Total count of $Z_{r,\{p_1,p_2\},g}$ variables is $R \cdot \binom{N}{2} \cdot G$

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

This means we have a total of $R \cdot N + R \cdot N \cdot \binom{G}{2}$ clauses.

2. Each group has exactly $S$ golfers:

$$
\bigwedge_{\substack{U\subseteq\{1,\dots,N\}\\|U|=N-(S-1)}}
\left(
  \bigvee_{p\in U} X_{r,p,g}
\right)
$$

The total of clauses here is $R \cdot G \cdot \binom{N}{S+1}$

*Note:* Here we actually just ensure that each group has at most $S$ players, which in combination with constraint 1 is enough.

3. No pair of players plays together more than $T$ times:

$$
\bigwedge_{\substack{U\subseteq\{1,\dots,R\}\\|U|=T+1}}
\left(
  \bigvee_{r\in U} \neg Y_{r,\{p_1,p_2\}}
\right)
$$

The total of clauses here is $\binom{N}{2} \cdot \Big[ R(4G+1) + \binom{R}{T+1} \Big]$

Which gives us the total number of all clauses:

$$
R \cdot N + R \cdot N \cdot \binom{G}{2} + R \cdot G \cdot \binom{N}{S+1} + \binom{N}{2} \cdot \Big[ R(4G+1) + \binom{R}{T+1} \Big]
$$

Here is an orientation table:

| Scenario | $N$ | $R$ | $G$ | $T$ | Clauses without $Y,Z$                                       | Clauses with $Y,Z$                                             |
| :---: | :---: | :---: | :---: | :---: |-------------------------------------------------------------|----------------------------------------------------------------|
| Small | 16 | 5 | 4 | 1 | $\binom{5}{2}\cdot \binom{16}{2}\cdot 4^2 = 19.200$         | $\binom{16}{2}\cdot[5(4\cdot4+1)+\binom{5}{2}] = 11.400$       |
| Medium | 32 | 10 | 8 | 1 | $\binom{10}{2}\cdot \binom{32}{2}\cdot 8^2 = 1.428.480$     | $\binom{32}{2}\cdot[10(4\cdot8+1)+\binom{10}{2}] = 186.000$    |
| Large | 64 | 20 | 16 | 2 | $\binom{20}{3}\cdot \binom{64}{2}\cdot 16^3 = 9.413.591.040$ | $\binom{64}{2}\cdot[20(4\cdot16+1)+\binom{20}{3}] = 4.919.040$ |

## State of application

* Core
  * Improve core functionality
    * Check individual clause encoders for their clause count
    * Also check variables etc.
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
