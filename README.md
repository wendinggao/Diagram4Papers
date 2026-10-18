<div align="center">

# Diagram4Papers

### Editable diagrams for research methods.

A skill for turning papers and code into compact, illustrated explanations.

[English](README.md) · [简体中文](README_zh-CN.md)

[![Code license: MIT](https://img.shields.io/badge/code-MIT-77995C?style=flat-square)](LICENSE)
[![Output: draw.io + PNG](https://img.shields.io/badge/output-draw.io%20%2B%20PNG-5D8FB0?style=flat-square)](#examples)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-9274BE?style=flat-square)](#rebuild-the-examples)

[Examples](#examples) · [Get started](#get-started) · [How it draws](#how-it-draws) · [Credits](#credits-and-license)

</div>

---

Diagram4Papers helps a coding agent decide **what a figure should explain and how to draw it**. It reads the method, follows a concrete example, and makes intermediate changes visible through diagrams, mappings, code excerpts and evidence. The result is an editable `.drawio` file with a native-rendered PNG.

The default style is full and orderly: substantial illustrations, precise alignment, light panel backgrounds, coordinated accent colors, Comic Sans MS, and rounded dashed sections with a clear hierarchy. Layout follows the method. Supporting inputs can fit in a narrow strip while a difficult mechanism gets room to unfold.

## Examples

These figures were independently composed to explain published research. They illustrate the skill's visual approach; they are not copies of the papers' original figures or recorded system executions.

### AutoGPS · Geometry reasoning

From a geometry problem to multimodal formalization, symbolic validation, proof-graph expansion and a concise explanation.

![Independently designed AutoGPS method diagram](examples/autogps.png)

[Paper](https://arxiv.org/abs/2505.23381) · [Editable draw.io](examples/autogps.drawio) · [Full-size PNG](examples/autogps.png) · [Sources and design notes](examples/design-notes.md)

The public 13–13–10 triangle provides a running example. The figure exposes premise bundles, atomic algebraic operations and the dependencies retained for the goal proof. The derivation is a checked teaching illustration.

### Voyager · Embodied lifelong learning

A chest-crafting example connects automatic curriculum, code revision, execution feedback, verification and skill memory.

![Independently designed Voyager method diagram](examples/voyager.png)

[Paper](https://arxiv.org/abs/2305.16291) · [Editable draw.io](examples/voyager.drawio) · [Full-size PNG](examples/voyager.png) · [Sources and design notes](examples/voyager-notes.md)

An apricot, lavender and teal composition gives the code/environment interaction most of the area. The world, recipe and inventory changes are schematic; model responses and retrieved entries are illustrative. The program excerpt adapts public MIT-licensed code. Offline checks do not run Minecraft or an LLM.

<sub>Icons in both examples: <a href="https://www.streamlinehq.com/">Free icons from Streamline</a>, <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>. Method credit belongs to the cited paper authors. See <a href="THIRD_PARTY_NOTICES.md">third-party notices</a> for sources and code attribution.</sub>

## Get started

### Install in Codex

Clone the repository into your skills directory:

```sh
git clone https://github.com/wendinggao/Diagram4Papers.git "${CODEX_HOME:-$HOME/.codex}/skills/diagram4papers"
```

The skill is available from your next turn. Its entry point is [SKILL.md](SKILL.md); the callable name is `diagram4papers`.

### Give it a paper and a drawing task

```text
$diagram4papers
Read this paper and the relevant implementation, then draw a method overview.
Use one concrete example to show the important intermediate changes.
Refer to the bundled examples for visual style, choose a layout and palette
that suit this method, and inspect the actual draw.io render.
Deliver an editable .drawio file and a separate PNG.

Paper: <URL or file>
Code: <optional repository>
Reference: <optional figure>
```

You can also give it an existing `.drawio` file and describe a local change. State the content or layout that should remain fixed. For a new composition, venue dimensions and a preferred reference help set the intended scale.

**Scope:** method diagrams, architectures and workflows. Statistical plots and presentation decks need a different workflow. Codex is the tested environment; the core instructions are Markdown and can be read by other agents, with tool-specific steps adapted to their environment.

## How it draws

| Design decision | What the skill does |
|---|---|
| Content | Reads the method and relevant code; chooses a coherent example and the changes worth showing. |
| Local composition | Pairs objects, operations and visible consequences using forms suited to each relationship. |
| Layout | Gives explanatory mechanisms the space they need, aligns sections and reclaims idle area. |
| Illustration | Selects professional assets for actual objects and actions, alongside editable scientific shapes. |
| Color and hierarchy | Coordinates pale large surfaces with smaller multicolor details; groups related contents with tiered frames. |
| Revision | Compares the native render with the reference at a common scale and revises the underlying design decision. |

The bundled examples are visual anchors. New papers need their own content and composition. Their final appearance still depends on the agent's source understanding, asset choices and rendered-image review.

## Rebuild the examples

**Requirements:** Python 3.9+, a modern browser with access to the diagrams.net embed, or desktop draw.io for export. Exact typography requires Comic Sans MS installed on the rendering system; the font is not bundled. Pillow is optional for font-width checks. Node.js is only needed for the optional Voyager resource-mock test.

From the repository root:

```sh
python3 -B scripts/build_demo.py --out demo-output/autogps.drawio
python3 -B scripts/check_figure.py demo-output/autogps.drawio --assets assets/streamline/ledger.json --require-font
python3 -B scripts/preview.py demo-output/autogps.drawio --port 0 --scale 2
```

Open the printed local URL. The preview exports a native PNG beside the figure. It runs a temporary loopback server and requires the rendering browser to reach `embed.diagrams.net`. Desktop draw.io export is an alternative.

For Voyager, use `scripts/build_voyager.py` and `demo-output/voyager.drawio` in the same commands. Builders also save the illustrative traces beside their outputs. The low-level [drawing helper](scripts/figure.py) is available for new compositions; it does not choose content or layout.

<details>
<summary><strong>Validation and repository guide</strong></summary>

```sh
python3 -B -m unittest discover -s tests -v
node tests/test_voyager_program.js
```

Run the release audit on an exported working tree without Git metadata. An optional `--deny-file` can supply private terms from outside that tree. Tooling checks geometry, style consistency, provenance and release contents; actual visual review is a separate step. See [validation notes](RELEASE-CHECKS.md) for what has been checked and its limits.

| Path | Purpose |
|---|---|
| [SKILL.md](SKILL.md) | The skill's drawing workflow and reference routing. |
| [references/](references/) | Content planning, composition, color, asset selection and revision guidance. |
| [scripts/](scripts/) | Native draw.io helpers, example builders, checks and browser export. |
| [examples/](examples/) | Editable diagrams, PNGs and source/design notes. |
| [assets/streamline/](assets/streamline/) | Licensed professional icons with a source ledger. |

</details>

## Credits and license

**Contributor:** [wendinggao](https://github.com/wendinggao) · `wending.gao25@student.xjtlu.edu.cn`

The skill's code is [MIT licensed](LICENSE). The AutoGPS and Voyager methods belong to their respective authors; each example links its scientific sources. The shortened Voyager program retains the [MineDojo Team MIT notice](references/voyager-code-license.txt).

Bundled Streamline icons are licensed separately under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Retain **Free icons from Streamline**, a link to [Streamline](https://www.streamlinehq.com/), the license and any applicable modification notice when redistributing the artwork. The [asset ledger](assets/streamline/ledger.json) records exact files and sources. No font is distributed.

Suggestions and example results are welcome through [Issues](https://github.com/wendinggao/Diagram4Papers/issues). If Diagram4Papers is useful in your work, a Star is appreciated.
