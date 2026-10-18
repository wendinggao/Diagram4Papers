# Public release boundary

A skill derived from private work must transfer general reasoning and visual rules, not private artifacts. Start a clean package tree. Independently author scientific diagrams, reusable code/templates and synthetic test fixtures. Reuse properly licensed professional artwork with clear provenance; retain notices for adapted public code. Do not rename and ship an old project's diagram or copy its coordinates, labels, programs, traces, counts, data, logs or screenshots.

Release checks:
- Only files intentionally listed for distribution are included. No symlinks, caches, original downloads, hidden credentials, transcripts, local exports, absolute workstation paths or external local-file dependencies.
- Every reference points to a bundled relative file or a deliberate public service/documentation URL. Scripts run from an arbitrary directory; no project import, proprietary API, private host or unbundled helper is required.
- Inspect draw.io XML values, metadata and decoded embedded SVGs. Inspect PNG text metadata/compressed text chunks. An innocent filename does not prove a clean binary.
- Identify each example as synthetic or publicly sourced. Freshly construct synthetic data; cite public problem instances and distinguish them from measured results. Review visual similarity for accidental reuse of a private illustration, not just string leakage.
- Check code and artwork licensing separately. Do not bundle a proprietary font. Do not assume an attributed icon may be redistributed as a template asset.
- Use `scripts/audit_release.py ROOT --deny-file EXTERNAL_FILE` with sensitive terms supplied outside the tree. The report records only locations/counts, not the secret terms. Keep this external list private. Inspect every finding and resolve it before publishing.
- Build the example in a fresh temporary directory using only the copied package. Run the structural tests and inspect a native render. Record what still depends on internet, system fonts or optional tools.

The checker is a useful detector, not a proof of non-disclosure. Finish with a human/agent review of all public files and intended archive members. Do not publish automatically or message third parties unless the user explicitly asks.
