# Dense illustrated method-diagram contract

This is a design vocabulary, not a universal template. Use the user's reference and explicit requirements first. Inspect the bundled public exemplar at full-canvas and detail scale before using the defaults. Values in `assets/style.json` are adjustable starting tokens, not measurements attributed to a source paper.

## Composition: content fills space, the grid provides order

Identify the figure's dominant mechanism. Allocate unequal region sizes around it, then align major boundaries, heading baselines, sibling rows and local gutters. Combine a substantial explanatory scene with compact entry/output strips and small comparison areas. Avoid turning every paragraph or operation into an equally prominent card. The grid should organize the explanation rather than become its subject.

Build the objects at useful text/illustration sizes, then fit the canvas to them. Treat long unused strips, broad one-word cells, repeated unchanged scenes and excess header height as reflow signals. Fill a region with meaningful detail or enlarge/rearrange the explanatory objects; do not merely enlarge the frame. When narrowing columns, reduce the whole canvas when appropriate instead of transferring empty space. Clearances must protect glyphs, strokes, connectors and group ownership; fullness never permits collisions.

A useful starting rhythm in authored pixels: outer margin 18–24, major gutters 12–18, section padding 10–16, functional local gaps 6–12. These are not reasons to spread an already coherent design. Inspect silhouette and negative space; there is no universal occupancy quota, required icon count or fixed number of modules.

Compare density across the individual regions as well as across the whole canvas. A rich input illustration cannot compensate for a sparse reasoning or output section. As relevant to the method, expose actual premise bundles, atomic transformations, retained/discarded dependencies and evidence-bearing output rows. Increase the visible footprint of operation icons with the explanatory objects; a larger count of tiny icons does not create the intended illustrated density. Preserve readable body text and clear ownership while tightening space.

### Reflow for fullness and order

Start with the local scientific composition, then draw its boundary. Inside each section, align shared row baselines, mapping columns, comparison cells and result strips. Let the largest useful object set the row height. Use the remaining space for adjacent evidence or a compact explanatory inset, rather than scattering small labels across an empty surface.

When a figure feels loose, inspect where the area went. Remove redundant header bands and production notes; close the space they occupied. Reduce oversized containers and long connector corridors. Narrow a supporting column while retaining useful text and icon sizes, and move neighboring columns inward. Reallocate height within the column that actually needs it. These are changes to geometry, not uniform scaling of the image.

Dense does not mean every area has equal weight. A short resource strip, a large selection/instantiation scene, a regular check grid and a compact state sequence can sit together on a strict major grid. Their different proportions make the mechanism prominent; their shared edges and small consistent gaps make it orderly.

## Type and visual weight

Use Comic Sans MS for labels, IDs, numbers and simple formulas unless explicitly overridden. A genuinely complex formula can use a deliberate consistent exception. Give module titles, local headings, body and secondary notes a visible hierarchy. Typical starts: title 34–40, local heading 27–31, body 24–28, secondary 20–23. Design size and detail for the intended publication width; don't shrink all text to fit an oversized diagram.

Use native font weight rather than artificial outline strokes. Match peer results exactly in family, size, weight and centering. Dark ink and confident icon contours give substance; not every label needs bold. Keep optional captions outside the explanation rather than scattering tiny implementation footnotes inside panels. Large branding titles are optional, not a way to fill an empty band.

Visual substance comes from the combined footprint of readable text, substantial illustrated subjects and close composition. Coordinate those first; then tune heading weight and object outlines. Heavy solid frames around every large region can overpower the contents. Use clear dashed grouping for those regions and crisp solid outlines for actual data/results. Compare peer icons by their opaque subject rather than their nominal image dimensions, including transparent padding.

## Palette: coordinated plural colors within a region

A module ground, its heading band and its outside frame establish family identity. Contents may use blue, violet, amber, cyan, rose and green together, in controlled areas. Preserve natural multicolor icons. Neither recoloring every element to the panel hue nor importing large bright unrelated blocks reproduces this style.

Give large surfaces very light fills; use stronger colors on smaller meaningful objects. Pair each fill with a related slightly darker outline. Compare adjacent fills for value and saturation, not just hex-name difference. Across a local mechanism, colors can distinguish object identity or state consistently; across unrelated modules, do not force a semantic scheme that makes the palette unnatural. Labels must carry meaning without color.

Before rendering, describe the palette's jobs: ground, heading, content surface, normal object, selected/pending object, verified result, and icon. After rendering, check color area: a matrix, code card or long ribbon can dominate despite sharing a nominal pastel palette. Rebalance area and saturation together. A new paper may use apricot/lavender/teal while maintaining the same grammar.

Work outward from one local group: establish the very pale ground, add the heading tint, place an original multicolor icon, and choose light auxiliary fills for the payloads beside it. Review the group as a color composition before applying it elsewhere. Large code surfaces and long state boxes usually need quieter fills than small selected tokens. A related outline can carry the hue while the fill stays light. Distinguish a pending value and a verified result through both text and a modest accent; unrelated scenes can use different auxiliary combinations when this improves harmony.

## Rounded dashed frame hierarchy

Assign frame tier by semantic containment, not by physical box size. Two peers keep identical framing even if one contains a long trace and the other a narrow saved artifact. Round containers, not scientific geometry, graph nodes whose shape is meaningful, arrows or data marks.

| Tier | Stroke | Dash pattern | Radius | Treatment |
|---|---:|---|---:|---|
| Outside module | 2.7 | 5 3 | 12 | Clear family color |
| Peer internal section | 1.6 | 4 3 | 9 | Visible muted family color |
| Actual nested local group | 1.3 | 3 2 | 7 | Lighter neutral/family color |
| Data/variable/result object | 1.45 / emphasized 1.65 | solid | 7 | Related readable outline |
| Heading ribbon | 0 | solid fill | 8 | Medium family tint |

Patterns are stroke-width multiples with `fixDash=0`; do not mix fixed-pixel dash modes. Use explicit colors and `strokeOpacity=100`. In draw.io set `rounded=1;absoluteArcSize=1;arcSize=2*radius`. Internal frames must remain visible enough to group the contents at normal display size. Adding a dashed frame to every icon creates clutter; shared boundaries, light surfaces and alignment can define a section where appropriate.

## Illustrations and arrows

A professional icon introduces an operation or object. The scientific scene explains it: candidates enter a filter, a tool returns an error, a symbol maps to an object, a selected entry yields a specific payload. Compare the alpha-visible subject, not nominal image boxes. Use deliberate scale variation for hierarchy, consistent visual mass for peers, no stretched icons and no automatic module tint.

Draw necessary local connectors with modest filled heads and clear ownership. Use straight or short orthogonal routes where suitable; give a feedback loop its own planned route. Avoid frame-hugging tours. A full-page reading path need not have an arrow between every pair of numbered modules. Distinguish workflow edges from geometric edges, equality symbols and evidence correspondences.

Use row order, adjacency, numbering and shared identifiers to carry obvious progression. Reserve an arrow for a relationship whose direction or branch would otherwise be unclear. Local process arrows can be short neutral filled arrows; logical or scientific edges can be finer. When a route is removed, reclaim its dedicated gutter. After reflowing, inspect arrowheads and endpoints in the native render: moving a group can alter a bend, the final segment or apparent ownership.

## Style-target check

At common display width compare the new render against the approved style target/public exemplar. Look for (1) a mechanism visible before reading all prose; (2) a substantial primary scene, not uniformly weighted cards; (3) full but orderly space use; (4) professional asset detail; (5) multicolor harmony; (6) visible internal grouping; (7) consistent typography. Superficial agreement in font and background colors is insufficient. See `iteration.md` for repair decisions and honest reporting.
