# Real Estate Services Plugins

Claude Code plugins for real estate investing and operations -- acquisitions, asset management, capital markets, development, property operations, leasing, and ESG. Built as a monorepo with a shared core plugin for MCP connectors, underwriting, valuation, and reporting standards.

## Quick Start

```bash
# Add the marketplace
claude plugin marketplace add <org>/realestate-services-plugins

# Install core plugin (required first)
claude plugin install real-estate-analysis@realestate-services-plugins

# Install add-ons for your role
claude plugin install acquisitions-investments@realestate-services-plugins
claude plugin install asset-management@realestate-services-plugins
```

## Plugins

### v1 (Current)

| Plugin | Commands | Who it's for |
|--------|----------|-------------|
| **real-estate-analysis** (core) | `/underwrite-asset`, `/value-asset`, `/rent-roll-qc`, `/ops-variance`, `/market-snapshot`, `/investment-memo-draft` | Everyone -- install first |
| **acquisitions-investments** | `/screen-deal`, `/bid-envelope`, `/acq-comps`, `/ic-memo`, `/diligence-punchlist`, `/downside-case`, `/deal-structure`, `/close-readiness` | Acquisitions teams, PE investors, REIT investment groups |
| **asset-management** | `/monthly-asset-report`, `/quarterly-portfolio-review`, `/reforecast`, `/hold-sell`, `/asset-business-plan`, `/capital-plan`, `/fund-performance`, `/attribution`, `/investor-update` | Asset managers, portfolio managers, fund managers |

### Planned (v1.1+)

- **capital-markets** -- borrower-side debt sizing, refinancing, covenant surveillance
- **leasing** -- pipeline, proposals, lease abstracting, renewals
- **property-operations** -- budgets, CAM reconciliation, expense management
- **esg-sustainability** -- GRESB prep, emissions, climate risk, certifications
- **development-construction** -- feasibility, entitlements, draws, GMP comparison

## Architecture

- **Core plugin** owns shared MCP connectors and cross-cutting skills (underwriting, valuation, metrics, memo-writing)
- **Add-on plugins** provide role-specific workflows that invoke core skills
- **Validated Python calculation library** for precision-sensitive math (IRR, waterfall, amortization) -- the LLM calls tested code, never reasons through financial math
- **Auditable Excel templates** with named ranges for standard deliverables
- **Deal context directories** with `_manifest.json` for cross-command state management

See [docs/spec.md](docs/spec.md) for the full specification.

## Data Input

v1 works primarily with **manual data input** (uploaded rent rolls, T-12s, OMs). MCP integrations are planned but not required. Only Egnyte has a native MCP server today; all other data providers (CoStar, Yardi, Trepp, etc.) require wrapper development.

## Industry Standards

Plugins assist with preparation of standards-aligned outputs (not submission-ready):
NCREIF, NCREIF/PREA Reporting Standards, IREM, BOMA, GRESB, TCFD/IFRS S2, UNPRI, GRI, Green Lease Leaders, ENERGY STAR.

## License

Apache 2.0
