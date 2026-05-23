# Vickrey Auction Allocation

**Also known as:** Second-Price Sealed-Bid Allocation, Strategy-Proof Task Auction

**Category:** Multi-Agent  
**Status in practice:** mature

## Intent

Allocate a task to the lowest sealed bidder but pay them the second-lowest bid, making truthful cost reporting a dominant strategy.

## Context

Multiple agents have heterogeneous private costs to perform a task — they know their own cost of compute, opportunity cost, or implementation cost. The allocator wants to assign the task to the cheapest agent. The agents are self-interested and will misreport if it gets them better payment.

## Problem

A first-price sealed-bid auction (allocator picks the lowest bidder, pays them what they bid) gives agents an incentive to shade — bid higher than true cost. The winner makes more, but the allocator can't tell whether they paid the actual minimum cost. Worse, shading is itself uncertain, so agents waste cycles modelling each other's likely shading. The auction's clean economic property of allocating to the cheapest agent collapses under strategic behaviour.

## Forces

- Sealed-bid eliminates direct collusion during the auction.
- First-price schemes incentivise strategic shading.
- Truthful reporting is the right input for the allocator.
- Payment difference (paid second-price, not own bid) is the bribe to be honest.

## Applicability

**Use when**

- Self-interested agents have private costs and the allocator wants truthful reporting.
- Allocator can absorb the second-price premium in exchange for strategy-proofness.
- Single-task or VCG-tractable combinatorial allocation.

**Do not use when**

- Agents are cooperative — truthfulness is given without a mechanism.
- Collusion among bidders is feasible and would distort the second price.
- Combinatorial structure makes VCG computationally infeasible.

## Therefore

Therefore: run a sealed-bid auction where the lowest bidder wins but is paid the second-lowest bid, so truthful cost reporting is a dominant strategy and the allocator gets the cheapest assignment.

## Solution

The allocator broadcasts the task and a sealed bid window. Each candidate agent submits a sealed bid representing its true cost. The allocator picks the lowest bidder and pays the second-lowest bid. Vickrey's classical result: truthful bidding is the dominant strategy because bidding higher than true cost only loses opportunities while bidding lower lowers the payment without helping win. For multi-task generalisations, use Vickrey-Clarke-Groves (VCG) mechanisms. Distinct from contract-net (which doesn't specify the payment rule) and from first-price auctions (which incentivise shading).

## Example scenario

A research-task allocator broadcasts 'analyse this 30-page filing' to five specialist agents who self-report cost (compute + opportunity). Bids come back at 50, 60, 65, 80, 100 credits. The 50-credit agent wins and is paid 60 (second-price). The next time around the agent has no incentive to bid above 50 — that risks losing the task without raising payment if it does win.

## Diagram

```mermaid
sequenceDiagram
  participant Al as Allocator
  participant A as Agent A
  participant B as Agent B
  participant C as Agent C
  Al->>A: call for sealed bids
  Al->>B: call for sealed bids
  Al->>C: call for sealed bids
  A->>Al: bid 50 (truthful cost)
  B->>Al: bid 60 (truthful cost)
  C->>Al: bid 80 (truthful cost)
  Note over Al: Lowest = A; second-lowest = 60
  Al->>A: award + pay 60
```

## Consequences

**Benefits**

- Truthful bidding is the dominant strategy — allocator gets honest cost reports.
- Allocator achieves cheapest assignment without modelling agent shading.
- Composes with contract-net as the bid-evaluation step.

**Liabilities**

- Allocator pays more than the winner's actual cost (the second-price premium).
- Susceptible to collusion among bidders (one agrees to be the dummy high-bid to inflate second price).
- VCG generalisations have known computational hardness for combinatorial settings.

## What this pattern constrains

Task auctions among self-interested agents must not use first-price payment when strategy-proofness matters; the winner pays the second-lowest bid so truthful reporting is dominant.

## Known uses

- **Google AdSense (Vickrey-style auctions on display ads)** — *Available* — <https://en.wikipedia.org/wiki/Vickrey_auction>
- **Multiagent Systems (Weiss) — Auctions and mechanism design chapter (Sandholm)** — *Available* — <https://mitpress.mit.edu/9780262731317/multiagent-systems/>
- **Sponsored search and ad-auction platforms running VCG variants** — *Available*

## Related patterns

- *complements* → [contract-net-protocol](contract-net-protocol.md) — Vickrey is one payment rule for contract-net allocation.
- *specialises* → [tool-agent-registry](tool-agent-registry.md)
- *complements* → [coalition-formation](coalition-formation.md)
- *complements* → [trust-and-reputation-routing](trust-and-reputation-routing.md)

## References

- (book) *Multiagent Systems, 2nd ed.*, Gerhard Weiss (ed.), 2013, <https://mitpress.mit.edu/9780262731317/multiagent-systems/>
- (doc) *Vickrey auction*, <https://en.wikipedia.org/wiki/Vickrey_auction>

**Tags:** multi-agent, auction, mechanism-design
