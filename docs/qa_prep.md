# Q&A preparation — Group A1

Draft answers for the live Q&A. **Numbers: always quote `results/summary.md`** (default
mode), never this file. "→ summary: X" says which table to read.

---

## Correctness

### Q1. Why is your exhaustive search guaranteed to find the optimum?
Take any optimal packing with k bins. Write down the items of bin 1, then bin 2, …, bin k.
That order is one of the n! permutations we try. First Fit on that order never needs more
than k bins: every item fits in its own optimal bin, so FF puts it there or in an earlier
bin with room. So the minimum over all orders equals OPT.
It really tries all n! orders — no pruning, no symmetry removal — so the name matches the code.

### Q2. Why is the bitmask DP correct?
State `dp[S] = (bins used, fill of the last bin)` for item set S, minimized lexicographically.
Each step adds one item: into the open bin if it fits, else into a new bin (Next Fit on some order).
1. **Some order reaches OPT.** List items bin by bin as in Q1. By induction, after
   the items of optimal bins 1..j, Next Fit uses at most j bins: when bin j+1's items come,
   some may still fit the open bin; the first one that does not fit opens a new bin, and
   all remaining items of bin j+1 fit there because they are a subset of a feasible bin.
2. **Keeping only the best state per S loses nothing.** For the same S, fewer bins is never
   worse. With equal bins, a less-filled last bin accepts everything a fuller one accepts.
   Closed bins never matter again.
Complexity O(2ⁿ·n) time and O(2ⁿ) memory — that is why it stops around n ≈ 22–24.

### Q3. How do you know your exact methods are not buggy?
On every instance, exhaustive, DP and MIP are cross-checked; any disagreement aborts the
experiment. → summary: "Do the exact methods agree?" (number of instances, 0 disagreements).
Unit tests also check n ≤ 8 for all three, plus hand examples.

### Q4. How do you check 3D packings are valid?
Every answer is validated: each item exactly once, allowed orientation, inside the container,
no two items overlapping (half-open intervals, so touching faces are fine), and when switched
on, no support or heavy-below violations. A failing check stops the experiment.

## Theory

### Q5. No algorithm can beat ratio 3/2 unless P = NP, but FFD is 11/9. Contradiction?
No. 3/2 is an **absolute** bound: deciding whether 2 bins suffice is PARTITION (NP-hard), so
any poly-time algorithm must sometimes answer 3 when OPT = 2. FFD's 11/9·OPT + 6/9 has an
**additive constant**: for OPT = 2 it allows 28/9 ≈ 3.1, i.e. 3 bins — ratio 3/2. The 11/9
only dominates as OPT grows (asymptotic ratio).

### Q6. FFD is almost always optimal in your results — so why does the worst case matter?
Random instances are easy; the 11/9 bound is reached only on crafted inputs. Our claim is
"on these distributions" → summary: "FFD / OPT" (share optimal, median, max per distribution).
We do not generalize beyond the distributions we tested.

## Practical choices

### Q7. You have a MIP solver. Why use heuristics at all?
Three reasons, all measured:
1. **Time.** Within the time limit the MIP proves optimality only for small n; on uniform and
   large items it often finds no solution at all from n ≈ 100. → summary A "Where each method
   gives up", B "mip" rows.
2. **Memory.** The assignment model has n × (#bins) binary variables; beyond n = 1000 we do not
   even build it (`skipped`).
3. **Quality.** FFD is within a few percent of the lower bound in milliseconds. → summary B.
Fairness note: our model is the textbook assignment formulation, which is weak (symmetric,
weak LP bound). Stronger formulations (arc-flow, Gilmore–Gomory column generation) solve far
larger instances; we say so instead of claiming "MIP is slow".

### Q8. Is the runtime comparison fair?
Same instance for every algorithm. `perf_counter` around the algorithm call only. Exhaustive
and DP run in a child process that is killed at the limit; process start-up is excluded.
MIP time **includes** model building (also reported separately). Box recommendation time
**includes** all multi-start attempts (reported as `tries`). All code is pure Python except
the MIP solver (C++), so the MIP has a language advantage, not a disadvantage.

### Q9. Do two reps / one seed prove anything?
Presentation numbers use 5 reps (`--full`: 30) per (algorithm, distribution, n), and we report
medians. Where a ranking flips between distributions we say when it flips (e.g. constraint
cost differs strongly between flat and long items → summary C "Cost of loading constraints").

## 3D and loading

### Q10. Why is 3D Naive so much worse than Extreme Point?
Naive never revisits space: a row is as deep as its deepest item and a layer as tall as its
tallest item, and everything above short items is wasted. It also never rotates. EP sorts
items, keeps candidate corners in all open bins and goes back to fill gaps.
Part of the gap is rotation, so we also ran the same EP **without** rotation. That run shows
how much is rotation and how much is the algorithm. → summary C "How much of the Naive → EP gap
is rotation?" (in the quick run, rotation explained only a small part; the algorithm explained
most of it — check the default-mode table before saying this).

### Q11. Where does the 70% support value come from?
It is our assumption, not a standard; 70% is a middle value between "fully supported" and
"anything goes". So we also ran 50% and 90% on the same instances to show how much the
choice matters. → summary C "Sensitivity of the support threshold". The cost grows with the
threshold and depends strongly on item shape (flat items are hit hardest, long items barely).

### Q12. Why does heavy-below cost so many more bins than support?
Heavy-below forbids stacking whenever the item below is lighter — with random weights that
is about half of all stacking options. Support only forbids overhangs. → summary C.
Implementation detail worth mentioning: we check both directions — an item placed on top of
lighter items, and a light item slid **under** an overhanging heavy one (the bug we found
and fixed during development).

**Can the cost be reduced?** Yes, by the order alone: sorting items heaviest first lets heavy
items take the floor before light ones, so the rule blocks fewer positions. Same rule, same
instances, fewer extra bins → summary C "Cost of loading constraints", row
`ep_weight_support_weight` vs `ep_support_weight`.

### Q12b. Is "heavy below" how it is done in practice?
Partly. The practical version is a **load-bearing (stacking) constraint**: how much weight a
box's top can carry, which depends on its strength, not only on whether it is heavier — a
sturdy light box can carry a heavy one, a fragile heavy one cannot. Bortfeldt & Wäscher (2013,
EJOR) list stacking/load-bearing among the practical constraints of container loading and
note that much of the literature ignores such constraints. Real loading also considers
delivery order (last stop loaded first), centre of gravity and axle loads, which we do not
model. Our heavy-below is a simple proxy for load-bearing; we do not claim it is what any
specific company uses. "Load heavy items first, at the bottom" is a common rule of thumb,
but we only report what we measured.

### Q13. Does the EP sort rule matter?
On our distributions, barely: volume, height and base-area sorting give nearly identical bin
counts. → summary C rows `ep_volume / ep_height / ep_area`. The box recommendation still tries
all three (multi-start), because on a single small order a different rule can fit a smaller box.

### Q14. What is the difference between your box recommendation and CJ Logistics' system?
Ours is a simplified version inspired by the same idea (pick the box per order automatically).
We do not know their algorithm; our items, catalog and orders are synthetic. We do **not**
compare our void ratio or speed with their press-release figures (~0.04 s per order, ~36% void).

### Q15. The naive box baseline splits many orders into several boxes. Isn't it a straw man?
It is the simplest rule a person might use (smallest box by volume, stack in arrival order,
no turning). It fails often because layer stacking without rotation wastes space in small
boxes. We show it to make the gap visible, not as a realistic competitor.
→ summary C "Box choice per order" (`share_split`).

## Limitations (say these before being asked)
- Pure-Python implementations; absolute times would be smaller in C++.
- Synthetic, uniformly random instances; real parcel data is more regular.
- 3D EP is simplified (see README "Simplifications").
- No load-bearing limits, centre of gravity, fragility or delivery-order constraints.
