# Runtime Compatibility Test Results

Tested against: Claude Code plugin system (April 2026)
Reference repo: [anthropics/financial-services-plugins](https://github.com/anthropics/financial-services-plugins)

## Results

| # | Assumption | Result | Confidence | Evidence |
|---|-----------|--------|------------|----------|
| R1 | Plugin discovery from `.claude-plugin/plugin.json` | **PASS** | High | Official docs confirm. Reference repo uses this pattern across 8 plugins. |
| R2 | Command discovery from `commands/` directory | **PASS (with caveat)** | High | Auto-discovered, but docs label `commands/` as **legacy**. Recommend using `skills/` for new development. Both work. |
| R3 | Skill discovery from `skills/` with `SKILL.md` | **PASS** | High | Official docs confirm. Folder name becomes skill name, namespaced under plugin. |
| R4 | Marketplace manifest registers plugins | **PASS** | High | Official docs + reference repo `marketplace.json` confirm full schema. |
| R5 | Multi-plugin install in same session | **PASS** | High | `--plugin-dir` supports multiple values. Plugins are namespaced to prevent conflicts. Reference repo install flow confirms. |
| R6 | Cross-plugin MCP sharing | **LIKELY PASS** | Medium-High | Not explicitly documented as a guarantee, but reference repo architecture requires it (core plugin owns all 11 MCP connectors, add-ons use them). MCP tools appear in flat namespace alongside Claude's tools. No per-plugin isolation documented. |

## Architecture Decision

**Use the primary model** (multi-plugin monorepo with core owning shared MCP connectors).

Rationale:
- R1-R5 confirmed
- R6 is the architecture Anthropic themselves use in financial-services-plugins
- Fallback (single-plugin with command packs) remains available if R6 fails in practice

## Key Finding: `commands/` is legacy

The official docs label the `commands/` directory as legacy and recommend `skills/` for all new components. Both directories are auto-discovered, but new plugins should prefer `skills/`.

This does NOT affect the spec's command/skill distinction (thin orchestration wrappers vs. domain logic). It only affects file placement -- both types can live in `skills/`.

## Remaining Verification

One empirical test would close the R6 gap completely: install `financial-analysis` + one add-on from the reference repo and confirm the add-on's commands can access the core's MCP tools. This should be done before building MCP-dependent workflows, but is NOT a blocker for v1 since v1's primary data path is manual input (only Egnyte has a native MCP server).

## Date

2026-04-02
