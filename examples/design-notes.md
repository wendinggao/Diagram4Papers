# Public example: AutoGPS

## Evidence and scope

[AutoGPS: Automated Geometry Problem Solving via Multimodal Formalization and Deductive Reasoning](https://arxiv.org/abs/2505.23381), ICLR 2026. The figure is independently designed from Sections 3.3–3.4, Algorithm 1, and the public geometry instance in Figure 3. Its layout, editable shapes and typography are newly authored; no source-paper raster, extracted vector artwork or original coordinates are embedded.

Implementation references use the [official repository](https://github.com/Jayce-Ping/AutoGPS), revision `f2095a26dbe7539eeb502b0de5b2d0afd8595164`: `multimodal_formalizer/main.py` describes alignment inputs; `symbolic_reasoner/proof_graph.py` implements isosceles reasoning, algebraic transformations, predecessor tracking and `find_minimal_subgraph_for_goal`; `proof_graph_format.py` translates predicates and theorems into readable descriptions. Source code is consulted, not redistributed.

The Multimodal Problem Formalizer (MPF) annotates points, pre-parses diagram and text, aligns their meaning with an MLLM and checks syntax. The Deductive Symbolic Reasoner (DSR) checks geometric consistency, completes implied relations, returns error feedback when needed, alternates geometric deductions with atomic algebraic transformations, and extracts a concise goal proof.

## Content plan

| Reader question | Visible payload and transformation |
|---|---|
| What information must be understood? | An initially unlabeled isosceles triangle, 13/13/10, and an area request |
| Why are both diagram and text needed? | Point annotation; segment/incidence/perpendicularity records; an unresolved `Shape($)` target |
| What does alignment change? | `$` becomes `Triangle(A,D,C)`; the problem gains concrete premises and a typed target |
| What can validation do? | Reject a collinear triangle assertion; complete a perpendicular relation; refine through feedback |
| What is a derivation hyperedge? | Several premise records feed one theorem application and a resulting relation |
| How does algebra participate? | Separate substitution, evaluation, nonlinear and linear-system examples with explicit inputs and outputs |
| Why is the final explanation short? | Necessary goal dependencies are retained while equal-angle and subtriangle-area branches are gray; readable rows expose premises, rule and conclusion |

## Mathematical and representational limits

The public example has `AC=10`, `AD=CD=13`, `B` on `AC`, and `BD` perpendicular to the base. Hence `BC=5`, `BD=12`, and `Area(ADC)=60`. `S` abbreviates this area. The builder checks these values exactly. A test independently checks the area using Heron's formula. The gray equal-angle branch is valid for the isosceles triangle, and `Area(ABD)=30` is a valid unused result, also illustrated by the paper's overview.

This is a compressed teaching diagram, not a recorded AutoGPS execution. Common validated geometry is shared across rows instead of copied into every premise bundle. Point/segment/triangle construction, equality substitutions and numeric evaluations are grouped where appropriate. The four readable rows do not claim a four-edge minimum for the actual implementation. Algebra cards demonstrate engine capabilities; they are not four parallel independent routes to the answer. The contradiction is an illustrative rejected formalization, not a claim that a particular model made that error on this run. The adjacent trace JSON explicitly records `autogps_execution=false`.

## Composition and density

A narrow blue entrance contains the original problem and the concrete tool library. The rose column explains annotation, partial records, alignment and the feedback boundary. The wider green column gives most of its area to deductions, atomic transformations and proof selection. Modules 3 and 4 use compact fact rows, visible professional operation icons, branching dependencies, a four-operation matrix, a target/continue strip, and premise-bearing proof rows. Density comes from explanatory objects and substantial icon silhouettes; tiny notes and enlarged empty cards are avoided.

The two triangles express an actual change: unlabeled input versus labeled geometry. Other regions use graphs, formula transformations, a selection contrast and proof records. Pale blue, lavender, amber, cyan and green separate object roles within the green modules; large surfaces stay light. Comic Sans MS, aligned sibling regions and semantic frame tiers keep the full composition ordered.

## Assets and transfer

Professional Streamline Ultimate Colors SVGs are embedded from the exact original bytes listed in the asset ledger. They retain natural multicolor artwork and dark contours. Credit: [Free icons from Streamline](https://www.streamlinehq.com/), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). No font is bundled.

For another paper, transfer the content-first planning, illustrated hierarchy, controlled color areas, visible asset scale and native rendering loop. Choose new scientific objects and a new spatial design. This example is not a mandatory four-module template or a substitute for reading the next paper.
