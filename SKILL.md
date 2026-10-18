---
name: diagram4papers
description: Turn research methods into compact, illustrated, editable method diagrams, architecture diagrams and workflows. Use for mechanism-rich paper/code figures and reference-driven refinement; not statistical plots, slide decks or generic infographics.
license: MIT
---

# Diagram4Papers

Explain a research mechanism through a designed visual example. Deliver one editable `.drawio` and one independent native-rendered `.png` per figure. A combined preview is optional only when requested.

The default style is dense, orderly illustrated research diagrams: unequal but aligned regions, Comic Sans MS, pale module backgrounds, coordinated multicolor contents, professionally designed icons, clearly tiered rounded dashed frames, and substantial readable objects. These are adjustable defaults. The user's current requirements take priority.

## 1. Find the explanation and its example

For a new method figure, read [content-and-reference.md](references/content-and-reference.md). Read the actual method, relevant paper figures and enough public code to resolve operations, object roles, branches and state changes. Separate evidence from illustrative choices. A style reference supplies visual rules, not scientific content.

Write a short content plan in the figure workspace: reader's question; central mechanism; source evidence; one coherent example; visible intermediate changes; diagram forms; space allocation. Choose a familiar, small example that exposes the method's distinctive decision. Carry its objects through the figure so the reader can check what changes and why. Introduce parameters beside the objects they denote; use ordinary action names for reader-facing headings.

An Agent figure often benefits from tools, a trace, feedback, memory or a decision branch. Choose detail supported by the actual method; a simple encoder architecture can use an appropriately compact composition.

## 2. Learn the reference's design decisions

Read [visual-contract.md](references/visual-contract.md). Inspect the reference at whole-canvas and detail scale. Identify what each region teaches, why its area is needed, and how an icon, diagram, formula and short label work together locally. Record typography, palette roles and areas, frame hierarchy, icon mass and connector grammar. If an unfamiliar style is difficult to translate into drawing decisions, independently rebuild a representative region: its grid, text, scientific geometry and spacing. This teaches construction; copying extracted PDF paths does not.

Inspect the bundled public examples: [AutoGPS](examples/autogps.png) with [geometry/proof design notes](examples/design-notes.md), and [Voyager](examples/voyager.png) with [embodied-agent design notes](examples/voyager-notes.md). They share a visual vocabulary while changing palette, main scene and layout. Use the closer mechanism to inform the explanation; neither is a layout to relabel. The user's explicit style takes priority.

## 3. Compose the mechanism at two scales

First design each local explanation as **objects + operation + visible consequence**. Retrieval can show candidate entries and a selected subset; parameter instantiation can show aligned correspondences beside one instance; verification can show a condition, evidence and verdict. Mix open diagrams, small mappings, comparison rows and compact payloads according to the operation. Let icons identify the actors and actions within these compositions as well as beside headings. Use a detailed input scene once, then show the relevant change in a smaller form.

Then fit these compositions into an unequal but aligned major grid. Give the difficult mechanism the largest region; compress supporting library entrances, loading actions and result summaries into strips when appropriate. Align sibling boundaries and title baselines, then organize the interior into clear rows or columns. Visible internal dashed sections give dense contents stable ownership. A substantial scene can remain open within its section; every label does not need another card.

Build at readable text and illustration sizes, then reclaim idle area by reflowing content and fitting the canvas. Removing a caption or connector also frees its reserved space. A sparse region may need more supported intermediate detail; a region with sufficient content may simply need a narrower column. The intended fullness comes from substantial objects and close, orderly relationships.

## 4. Resolve assets, color and weight together

Read [icons-and-licensing.md](references/icons-and-licensing.md) whenever icons are used. Search Flaticon live by semantic role and illustrated color style; inspect and select actual candidates. Use legitimate SVG when available; trace an available PNG when appropriate and inspect the result.

Choose professionally designed, suitably licensed assets of comparable visual quality when a candidate is unavailable. The bundled Streamline Ultimate Colors subset supplies an open-source alternative. Intentionally original icons can suit a specific visual brief when reviewed to the same standard. Author scientific graphs, mappings, code cards, geometry and state diagrams for the method and keep them editable where practical.

Select real candidates before finalizing their slots. Compare visible icon mass, contour/detail and perspective at final display size, then size the neighboring text and scientific scene with them. Preserve their multicolor artwork. Use a pale module ground and a stronger heading/frame to establish identity; coordinate local blue, violet, amber, cyan or rose accents by lightness, saturation, area and position. Inspect one representative local composition before propagating the treatment across the figure.

Keep accurate source, author, exact file/license, intended distribution and transformations in an asset ledger. Separate skill code licensing from example artwork licensing. Dark text and mature icon contours provide visual substance; pale surfaces and subordinate frames keep it readable.

## 5. Author and render

Author draw.io XML with explicit geometry, editable text and native explanatory shapes. `scripts/figure.py` provides low-level helpers only; it does not select content, choose layouts or guarantee visual quality. Use `Figure.asset()` for ledger-backed external art. Keep related annotations beside their objects instead of adding a card for every sentence.

Run `scripts/check_figure.py FIGURE.drawio --assets ASSET_LEDGER.json --require-font` before native rendering. It catches structural, font and provenance errors, not composition quality. Render with `scripts/preview.py FIGURE.drawio --port 8765 --scale 2` in an available browser, or use desktop draw.io export. Inspect the actual full canvas and dense regions at comparable display scale to the style target. Confirm Comic Sans MS loaded; the font is not bundled. Report missing capabilities honestly and retain editable work.

## 6. Refine through visible comparisons

Read [iteration.md](references/iteration.md). Compare the new render and the reference at the same display width, then inspect corresponding local regions. Explain the largest visible gap in terms of a design decision: content form, region proportion, grouping, object scale, asset quality or colored area. Make that change and inspect the result. Static passes validate the file; the image comparison evaluates its design.

Preserve improvements already established while refining another dimension. Translate feedback such as "fuller," "more orderly" or "more harmonious" into a local operation using the repair examples in `iteration.md`. Judge the whole composition after a local change: removing an arrow can shorten a gutter; strengthening a section frame can make a crowded group readable; restoring a colorful icon can require a quieter neighboring fill.

Fix scientific errors, clipping, collisions and unclear reading order before handoff. Repeat native rendering after meaningful changes. Stop when the intended explanation and requested visual standard are met, with proportionate verification for small edits. Describe any material remaining quality gap concretely.

## Public package and handoff

For open-source distribution, read [publication.md](references/publication.md). Build synthetic or publicly sourced examples independently; no private diagrams, coordinates, traces, screenshots, identifiers or workstation paths may enter the package. Run the release audit on the exact distributable tree, including decoded assets. Do not publish remotely without a request.

Deliver figure files, concise explanation, necessary attribution and material limitations. When testing this skill, first complete one mechanism-rich case and compare it to the visual target, then test a different method. Fix observed failures in the relevant rules rather than repeatedly changing papers or adding a checklist for every past comment.
