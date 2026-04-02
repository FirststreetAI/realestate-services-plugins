# CLAUDE.md - Contributor Guidelines

## Repository Structure

This is a monorepo of Claude Code plugins for real estate. See `docs/spec.md` for the full specification.

- `real-estate-analysis/` -- core plugin, install first. Owns shared MCP connectors and cross-cutting skills.
- `acquisitions-investments/` -- deal screening through close
- `asset-management/` -- portfolio surveillance, fund performance, investor reporting
- Other verticals are planned (capital-markets, leasing, property-operations, esg-sustainability, development-construction)

## Key Rules

### Commands vs Skills

All components live in `skills/` (the `commands/` directory is legacy). The distinction is conceptual:
- **Commands** = thin orchestrators. Their SKILL.md sequences skill invocations and handles user interaction.
- **Skills** = domain logic. Their SKILL.md contains the actual analytical methodology, formulas, and standards references.

### Canonical Skill Ownership

Every analytical domain has a single canonical skill owner. Commands invoke skills; they do NOT reimplement logic. See the ownership table in `docs/spec.md` Section 6.

### Computational Trust

The LLM must NEVER perform precision-sensitive financial calculations by reasoning in natural language. It must call validated Python functions in `skills/*/scripts/`.

Precision-sensitive: IRR, XIRR, NPV, waterfall/promote, amortization, DSCR, TWRR, TGER, GHG emissions, CAM allocation.
LLM-appropriate: cap rate selection, comp selection, memo narratives, risk identification, workflow structuring.

### Excel Output

Standard deliverables use pre-formatted Excel templates in `skills/*/assets/`. The LLM fills data into named ranges; it does NOT generate novel spreadsheet structures. Every output includes a "Sources & Assumptions" tab.

### Deal Context

Multi-command workflows use deal context directories with `_manifest.json`. Commands read from and write to the manifest. See `docs/spec.md` Section 5.5.

### Data Conflict Resolution

- State the as-of date for each data source
- Flag when source dates differ by more than one quarter
- Never silently resolve disagreements between sources -- present both and ask the user
- Respect freshness gates (market rents: 6mo, valuations: 1 quarter, rent rolls: 3mo)

## Testing

All calculation functions in `scripts/` must have unit tests with known-answer inputs verified against Excel. Tests live in `scripts/tests/`.

## MCP

v1 uses manual data input as the primary path. Only Egnyte has a native MCP server. Do not add MCP connectors to `.mcp.json` unless the wrapper has been built and tested.
