# Real Estate Services Plugins — Specification v2.2

## Overview

A monorepo of Claude Code plugins purpose-built for real estate owners, operators, investors, lenders, and development teams. Each plugin targets a specific vertical and provides slash commands, skills, and MCP integrations that map directly to day-to-day business workflows.

Modeled after [anthropics/financial-services-plugins](https://github.com/anthropics/financial-services-plugins). The architecture follows a **hub-and-spoke** layout: one core plugin owns shared MCP connectors and cross-cutting skills, with vertical add-on plugins for role-specific workflows.

---

## 1. Repository Structure

```
realestate-services-plugins/
├── .claude-plugin/
│   └── marketplace.json                  # Marketplace manifest (registers all plugins)
├── CLAUDE.md                             # Contributor guidelines
├── README.md
├── LICENSE                               # Apache 2.0
├── .gitignore
├── docs/
│   └── spec.md                           # This file
│
├── real-estate-analysis/                 # CORE plugin (install first)
├── acquisitions-investments/             # Add-on: deal screening through close
├── asset-management/                     # Add-on: portfolio surveillance & reporting
├── capital-markets/                      # Add-on: debt, refinancing, covenant tracking
├── development-construction/             # Add-on: ground-up & value-add development
├── property-operations/                  # Add-on: budgets, CAM, expense management
├── leasing/                              # Add-on: pipeline, proposals, renewals
├── esg-sustainability/                   # Add-on: GRESB, emissions, climate risk, certifications
│
└── partner-built/                        # Partner-contributed plugins
    ├── costar/                           # CoStar Group (additional skills on top of core MCP)
    └── yardi/                            # Yardi Systems (additional skills on top of core MCP)
```

---

## 2. Runtime Compatibility (Verified)

Runtime assumptions have been tested against the Claude Code plugin system and documented in `docs/runtime-compatibility.md`. Results:

| # | Assumption | Result | Notes |
|---|-----------|--------|-------|
| R1 | Plugin discovery from `.claude-plugin/plugin.json` | **PASS** | Each directory with plugin.json is independently installable. |
| R2 | Command/skill discovery from directory structure | **PASS** | Auto-discovered. **Note**: `commands/` is labeled **legacy** in official docs. `skills/` is the recommended location for all new components. |
| R3 | Skill discovery from `skills/` with `SKILL.md` | **PASS** | Folder name becomes skill name, namespaced under plugin. |
| R4 | Marketplace manifest registers plugins | **PASS** | `marketplace.json` schema confirmed. |
| R5 | Multi-plugin install in same session | **PASS** | Plugins are namespaced (e.g., `/plugin-name:command-name`). |
| R6 | Cross-plugin MCP sharing | **LIKELY PASS** | Not explicitly documented, but Anthropic's own financial-services-plugins repo is built on this assumption (core owns all MCP, add-ons use them). MCP tools appear in flat namespace. |

### Architecture decision: multi-plugin monorepo confirmed

R1-R5 are confirmed. R6 is the architecture Anthropic uses in their reference repo. We proceed with the **primary model** (separate plugins, core owns shared MCP connectors).

R6 is not a blocker for v1 regardless, since v1's primary data path is manual input (only Egnyte has a native MCP server). By the time MCP wrappers are built, R6 will have been empirically verified through usage.

### Key finding: `commands/` is legacy

The official docs recommend `skills/` for all new components. Both directories are auto-discovered, but new plugins should use `skills/` exclusively. This does not change the spec's conceptual distinction between commands (thin workflow orchestrators) and skills (domain logic) -- it only means both live under `skills/` in the file system.

Updated plugin directory layout:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json
├── .mcp.json
├── skills/                          # ALL components live here
│   ├── underwrite-asset/            # "Command" -- thin orchestrator
│   │   └── SKILL.md
│   ├── underwriting-standards/      # "Skill" -- domain logic
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   │   ├── proforma.py
│   │   │   ├── returns.py
│   │   │   └── tests/
│   │   ├── references/
│   │   └── assets/
│   │       └── proforma-template.xlsx
│   └── ...
├── hooks/
│   └── hooks.json
└── .claude/
    └── *.local.md
```

### Fallback (retained but not expected)

If R6 is disproven in practice, the fallback is a single plugin with all skills in one `skills/` directory, namespaced by vertical via subdirectory prefixes. This remains available but is not the planned path.

---

## 3. Target Personas

"Real estate" is not one buyer. The plugins should support these operating models without requiring a separate plugin per persona -- differences are handled through **skills, templates, and command variants**.

### Public and semi-public owners

- **Equity REITs** — public company reporting cadence, same-store NOI, FFO/AFFO framing, occupancy and leasing spread tracking.

### Private capital owners

- **Private equity real estate / opportunity funds** — deal screening, underwriting, IC memos, business plan execution, realized/unrealized returns.
- **Core / core-plus / open-end funds** — stabilized asset monitoring, income durability, benchmark and portfolio analytics, NCREIF/ODCE submissions.
- **Family offices / private investors** — simpler acquisition, hold-sell, financing, and reporting workflows.
- **Separate accounts / institutional asset managers** — mandate-specific reporting, portfolio review, and asset-plan governance.

### Operators

- **Owner-operators / regional operators** — property operations, leasing, capex, vendor management.
- **Developers** — entitlement, design coordination, GMP/draw tracking, lease-up monitoring.

> **v1 persona exclusion**: Mortgage REITs and real estate credit/debt platforms are excluded from v1. Their core workflow -- lender-side debt portfolio surveillance (monitoring a book of originated loans, collateral tracking, credit watchlists) -- is not covered by v1 commands. The capital-markets plugin serves **borrower-side** debt workflows only (sizing, refinancing, covenant compliance for loans the firm has taken, not originated). Debt portfolio surveillance can be added as a capital-markets extension post-v1 if demand warrants it.

---

## 4. Plugin Architecture Standard

### 4.1 Standard directory layout

Every plugin uses `skills/` for all components (see Section 2 -- `commands/` is legacy). Commands and domain skills are distinguished by their SKILL.md content, not by directory:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest (name, version, description, author)
├── .mcp.json                # MCP server connections (empty {} for add-ons)
├── skills/                  # ALL components: commands and domain skills
│   ├── command-name/        # "Command" -- thin orchestrator
│   │   └── SKILL.md
│   └── skill-name/          # "Skill" -- domain logic
│       ├── SKILL.md
│       ├── scripts/         # Validated calculation functions (Section 5.4)
│       │   └── tests/       # Unit tests
│       ├── references/      # Supporting reference docs (formulas, standards)
│       └── assets/          # Templates, checklists, Excel templates
├── hooks/
│   └── hooks.json           # Event hooks (initially empty [])
└── .claude/
    └── *.local.md           # Per-user/firm-specific settings (gitignored)
```

### 4.2 plugin.json schema

Follows Anthropic's actual pattern -- minimal fields only:

```json
{
  "name": "plugin-name",
  "version": "0.1.0",
  "description": "One-line description of the plugin.",
  "author": {
    "name": "Anthropic"
  }
}
```

### 4.3 .mcp.json pattern and cross-plugin MCP strategy

**Primary model (if runtime assumption R6 holds -- cross-plugin MCP sharing works):**

The core plugin declares all shared MCP connectors. Add-on plugins have `.mcp.json` with empty `"mcpServers": {}`. When a user installs both core and an add-on, the runtime merges MCP namespaces and add-on commands can reference core connectors.

**Defensive model (if R6 fails or is unverified):**

Every add-on plugin declares the specific MCP connectors it actually uses, duplicating entries from the core plugin's `.mcp.json` as needed. This creates redundancy but guarantees each plugin is self-contained.

> **Decision rule**: Run the R1-R6 runtime compatibility tests (Section 2) first. If R6 passes, use the primary model. If R6 fails, use the defensive model. Do not commit to either until the test results are documented. Either way, the command and skill logic is identical -- only the `.mcp.json` files change.

If an add-on needs a connector **not** in core (e.g., Procore for development, Measurabl for ESG), it declares that connector in its own `.mcp.json` regardless of which model is used.

### 4.4 .claude/*.local.md (firm customization)

Each plugin supports per-firm settings via gitignored local files:

- Firm-specific templates and branding
- Default assumptions (cap rate ranges, expense ratios, market preferences)
- LP/investor reporting conventions
- Naming conventions for output files
- Preferred MCP sources when multiple are available
- GRESB entity mapping (which funds/accounts submit, under which entity names)
- NCREIF/ODCE submission identifiers and property-type classifications

### 4.5 hooks/hooks.json

Initially empty (`[]`) for all plugins. Future uses:

- Pre-command validation (e.g., confirm rent roll file exists before `/underwrite`)
- Post-command QA triggers (e.g., run model audit after pro forma generation)
- Approval gates for sensitive deliverables (IC memos, investor updates)

---

## 5. Artifact Strategy

Commands claim outputs in Excel, Word, and PowerPoint formats. This section defines what that actually means in a markdown/JSON plugin with no build tooling.

### 5.1 What commands actually produce

Commands do **not** generate binary Office files directly. Claude Code operates in a conversational and file-generation context. Commands produce:

1. **Structured markdown** — The primary output for memos, reports, and narratives. Formatted for readability in the terminal and easy copy-paste into Word/Google Docs.

2. **CSV / TSV data** — For tabular outputs (comp sets, debt sizing, budgets, utility data). Can be opened directly in Excel or imported into Google Sheets. Commands should write these to named files in the working directory.

3. **Python scripts for Excel generation** — For complex financial models that require formulas, multiple tabs, and formatting (pro formas, underwriting models, waterfall structures). See Section 5.4 for the critical distinction between validated library code and generated-from-scratch scripts.

4. **Conversational output** — For quick analyses, checklists, and advisory outputs that don't need a file artifact.

### 5.2 Output format mapping

| Spec says | What the command actually produces | File artifact? |
|-----------|-----------------------------------|---------------|
| **Excel** | CSV for simple tables; template-filled .xlsx for models with formulas/tabs | Yes (.csv or .xlsx) |
| **Word** | Structured markdown written to .md file | Yes (.md) |
| **PPT** | Structured markdown with section headers suitable for deck conversion | Yes (.md) |
| **Excel + Word** | Both a data file and a narrative file | Yes (both) |

### 5.3 Implications for skills and templates

- Skills should define **output structure** (sections, tables, required fields) not visual formatting
- Template files in `skills/*/assets/` are **content templates** (markdown with placeholders), not Office file templates
- QA checklists in commands validate **content completeness and accuracy**, not formatting
- If a firm needs branded Office output, they configure conversion tooling outside the plugin (e.g., Pandoc, firm-specific scripts referenced in `.claude/*.local.md`)

### 5.4 Computational trust: validated code vs. LLM reasoning

Real estate is a basis-point business. A $0.01\%$ error in an IRR calculation or a rounding mistake in a waterfall destroys institutional trust. This creates a hard rule:

> **The LLM must never perform precision-sensitive financial calculations by reasoning through them in natural language.** It must call validated, tested code.

#### What this means in practice

**Precision-sensitive calculations** (must use validated code):
- IRR, XIRR, NPV, XNPV
- Waterfall / promote calculations (preferred return, catch-up, carry splits)
- Loan amortization schedules
- DSCR, debt yield, LTV (when derived from amortization)
- TWRR, money-weighted returns
- TGER
- GHG emissions (Scope 1/2/3 with emission factors)
- CAM pro-rata share allocation with gross-up

**Judgment calls** (LLM reasoning is appropriate):
- Selecting cap rates, discount rates, growth assumptions
- Choosing comparable properties
- Writing memo narratives
- Identifying risk factors
- Structuring workflows

#### Implementation pattern

The repo must ship a **validated calculation library** -- a set of tested Python functions that live in `skills/*/scripts/`:

```
skills/underwriting-standards/
├── SKILL.md
├── scripts/
│   ├── proforma.py           # NOI projection, cash flow waterfall
│   ├── returns.py            # IRR, equity multiple, cash-on-cash
│   ├── debt_sizing.py        # DSCR/DY/LTV constraint solver, amortization
│   └── tests/
│       ├── test_proforma.py
│       ├── test_returns.py
│       └── test_debt_sizing.py
└── references/
    └── ...
```

**Rule**: When a command needs an IRR, it calls `returns.calculate_irr(cashflows, dates)`. It does **not** ask the LLM to "compute the IRR of these cash flows." The SKILL.md must instruct the LLM to import and call the function, not to replicate the math.

**Rule**: Every calculation function must have unit tests with known-answer inputs (e.g., IRR of a known cash flow series verified against Excel's XIRR). Tests live alongside the functions and run as part of any CI.

#### Auditability and templates

For Excel output specifically, the LLM must not generate a novel spreadsheet structure from scratch each time. Instead:

1. **Template-based models**: Skills ship pre-formatted Excel templates in `skills/*/assets/` (e.g., `proforma-template.xlsx`, `waterfall-template.xlsx`). These templates have named ranges, standard tab structure, and documented formulas that a Senior VP can audit once and trust repeatedly.

2. **The LLM's job is data, not structure**: The LLM gathers inputs, validates them, calls the calculation library to compute results, and then fills values into the template's named ranges using `openpyxl`. It does not invent new tabs, columns, or formula structures.

3. **Traceability**: Every generated Excel file should include a "Sources & Assumptions" tab that documents: which data came from which source, as-of dates, any manual assumptions the user provided, and which calculation functions were called.

> **Exception**: For one-off or exploratory analyses where no template exists, the LLM may generate a simple CSV or ad-hoc Excel. But any command that produces a **standard deliverable** (pro forma, waterfall, debt sizing, CAM reconciliation) must use the template path.

This means `skills/*/assets/` contains both content templates (markdown) and **auditable Excel templates** (.xlsx) for standard deliverables. The non-goals section permits this: the repo ships pre-built templates, not code that must be compiled.

### 5.5 Cross-command state: the deal context directory

The cross-plugin workflows in Section 11 (e.g., the 11-step acquisition lifecycle) only work if one command's output is discoverable by the next command's input. Without a defined mechanism, users must re-provide inputs at every step, or the LLM guesses filenames -- both break the workflow value proposition.

#### The deal context directory

Every multi-command workflow operates within a **deal context directory** -- a working directory for a specific property, fund, or project. Commands read from and write to this directory using standardized naming conventions.

```
deals/
└── 123-main-st-dallas/                    # Deal context directory
    ├── _manifest.json                      # Tracks all artifacts produced
    ├── inputs/                             # User-provided source documents
    │   ├── rent-roll-2026-q1.xlsx
    │   ├── t12-trailing-mar-2026.xlsx
    │   └── offering-memo.pdf
    ├── underwriting/                       # /underwrite-asset outputs
    │   ├── proforma.xlsx
    │   ├── assumptions.json
    │   └── summary.md
    ├── comps/                              # /acq-comps outputs
    │   └── sale-comps.csv
    ├── market/                             # /market-snapshot outputs
    │   └── submarket-snapshot.md
    ├── pricing/                            # /bid-envelope outputs
    │   ├── bid-range.xlsx
    │   └── sensitivity.csv
    ├── stress/                             # /downside-case outputs
    │   └── downside-scenarios.xlsx
    ├── debt/                               # /debt-size outputs
    │   └── debt-sizing.xlsx
    ├── memo/                               # /ic-memo outputs
    │   └── ic-memo.md
    ├── diligence/                          # /diligence-punchlist outputs
    │   └── punchlist.md
    └── closing/                            # /close-readiness outputs
        └── close-readiness.md
```

#### The manifest file

`_manifest.json` is the key coordination mechanism. Every command appends to it when it produces output, and reads from it when it needs prior outputs. Structure:

```json
{
  "deal_name": "123 Main St, Dallas",
  "property_type": "industrial",
  "created": "2026-04-01T10:00:00Z",
  "artifacts": [
    {
      "command": "/underwrite-asset",
      "produced_at": "2026-04-01T10:15:00Z",
      "outputs": {
        "proforma": "underwriting/proforma.xlsx",
        "assumptions": "underwriting/assumptions.json",
        "summary": "underwriting/summary.md"
      },
      "key_metrics": {
        "going_in_cap": 0.055,
        "stabilized_noi": 2850000,
        "unlevered_irr": 0.082,
        "levered_irr": 0.112
      }
    },
    {
      "command": "/bid-envelope",
      "produced_at": "2026-04-01T11:30:00Z",
      "consumes": ["underwriting/proforma.xlsx", "underwriting/assumptions.json"],
      "outputs": {
        "bid_range": "pricing/bid-range.xlsx",
        "sensitivity": "pricing/sensitivity.csv"
      },
      "key_metrics": {
        "bid_low": 48500000,
        "bid_target": 51000000,
        "bid_walk": 53500000
      }
    }
  ]
}
```

#### How commands use the manifest

1. **On start**: The command checks if `_manifest.json` exists in the working directory (or a parent). If it does, the command reads it to discover available prior outputs.

2. **Input resolution**: When a command needs data that a prior command produced (e.g., `/ic-memo` needs the pro forma), it looks in the manifest's `artifacts` array for the relevant command's outputs. If found, it reads the file. If not found, it asks the user for the input.

3. **On completion**: The command appends its entry to the manifest, including: which files it consumed (`consumes`), which files it produced (`outputs`), and a small set of `key_metrics` (scalar values that downstream commands commonly need without opening the full file).

4. **Staleness**: If a command finds prior artifacts but they are stale (e.g., the underwriting was done with different assumptions than the user now wants), the command flags this and asks whether to re-run or proceed with existing outputs. Staleness is determined by the user, not by timestamp -- the command surfaces what exists and lets the user decide.

#### Naming conventions

| Directory | Commands that write here | Standard filenames |
|-----------|------------------------|--------------------|
| `inputs/` | User-provided (not command output) | Descriptive, user-chosen |
| `underwriting/` | `/underwrite-asset` | `proforma.xlsx`, `assumptions.json`, `summary.md` |
| `comps/` | `/acq-comps` | `sale-comps.csv`, `lease-comps.csv` |
| `market/` | `/market-snapshot` | `submarket-snapshot.md` |
| `pricing/` | `/bid-envelope` | `bid-range.xlsx`, `sensitivity.csv` |
| `stress/` | `/downside-case` | `downside-scenarios.xlsx` |
| `debt/` | `/debt-size` | `debt-sizing.xlsx` |
| `memo/` | `/ic-memo`, `/investment-memo-draft` | `ic-memo.md`, `draft-memo.md` |
| `diligence/` | `/diligence-punchlist` | `punchlist.md`, `issues.csv` |
| `closing/` | `/close-readiness` | `close-readiness.md` |
| `esg/` | `/climate-risk`, `/green-lease-audit` | `climate-risk.md`, `green-lease-audit.xlsx` |
| `performance/` | `/fund-performance`, `/attribution` | `fund-returns.xlsx`, `attribution.xlsx` |
| `reporting/` | `/monthly-asset-report`, `/investor-update` | `asset-report-YYYY-MM.md`, `investor-update.md` |
| `operations/` | `/cam-recon`, `/property-budget` | `cam-recon.xlsx`, `budget-YYYY.xlsx` |
| `leasing/` | `/pipeline-review`, `/lease-abstract` | `pipeline.xlsx`, `abstract-[tenant].md` |

#### For non-deal workflows

Some commands operate at portfolio or fund level rather than deal level (e.g., `/fund-performance`, `/quarterly-portfolio-review`). These use the same pattern but with a portfolio context directory:

```
portfolios/
└── lion-properties-fund/
    ├── _manifest.json
    ├── performance/
    ├── reporting/
    └── esg/
```

The mechanism is identical -- `_manifest.json` tracks artifacts, commands discover prior outputs. The only difference is the directory name and scope.

#### What this requires from commands

Every command's SKILL.md must specify:

- **Reads from**: Which manifest artifact types it looks for (e.g., `/ic-memo` reads from `underwriting/*` and `pricing/*`)
- **Writes to**: Which directory and filenames it produces
- **Key metrics exported**: Which scalar values it writes to the manifest for downstream consumption
- **Behavior when prior artifacts are missing**: Does it ask the user, or can it proceed with direct inputs?

---

## 6. Command Design Principles

### Naming rules

Every command must map to a **recognizable real-estate business workflow**. Use names that practitioners would say out loud:

| Do | Don't |
|----|-------|
| `/screen-deal` | `/analyze-file` |
| `/cam-recon` | `/run-spreadsheet` |
| `/monthly-asset-report` | `/make-summary` |
| `/bid-envelope` | `/calculate-price` |
| `/covenant-check` | `/test-data` |
| `/gresb-prep` | `/collect-esg-data` |

### Command count constraint

**6-9 commands per plugin.** No exceptions. If a workflow doesn't justify its own command, it belongs as a skill invoked from an existing command.

### Canonical workflow ownership

Multiple commands touch overlapping analytical domains (underwriting, memo-writing, market context). To prevent duplication and inconsistency, each calculation or output type has a **single canonical owner** -- a skill that performs the logic. Commands are thin wrappers that invoke skills.

| Analytical domain | Canonical skill (owner) | Lives in | Commands that invoke it |
|-------------------|------------------------|----------|------------------------|
| Pro forma / NOI projection | `underwriting-standards` | core | `/underwrite-asset`, `/screen-deal` (quick version), `/bid-envelope`, `/hold-sell`, `/reforecast` |
| Property valuation (cap rate, DCF) | `valuation-methods` | core | `/value-asset`, `/underwrite-asset` (embedded), `/hold-sell` (forward value) |
| Rent roll normalization & analysis | `rent-roll-normalization` | core | `/rent-roll-qc`, `/underwrite-asset` (embedded), `/mark-to-market` |
| Market data assembly & comps | `market-analysis` | core | `/market-snapshot`, `/acq-comps`, `/underwrite-asset` (market context) |
| Variance analysis (actuals vs. plan) | `variance-analysis` | core | `/ops-variance`, `/property-budget` (YTD section), `/reforecast` (variance inputs) |
| Debt sizing | `debt-sizing-hierarchy` | capital-markets | `/debt-size`, `/underwrite-asset` (debt section), `/refi-compare` |
| Memo narrative structure | `memo-writing` | core | `/investment-memo-draft`, `/ic-memo`, `/dev-ic-memo`, `/investor-update`, `/debt-memo` |
| Return calculations (property-level) | `underwriting-standards` | core | `/underwrite-asset`, `/bid-envelope`, `/downside-case`, `/hold-sell` |
| Return calculations (fund-level) | `fund-return-calculations` | asset-mgmt | `/fund-performance`, `/attribution` |
| Scenario / stress testing | `scenario-stress-testing` | acquisitions | `/downside-case`, `/bid-envelope` (sensitivity), `/hold-sell` (scenarios) |
| Capex prioritization | `capex-prioritization` | asset-mgmt | `/capital-plan`, `/asset-business-plan` (capex section) |
| Lender universe matching | `lender-matching` | capital-markets | `/lender-shortlist`, `/refi-compare` (lender fit) |
| Development schedule analysis | `schedule-analysis` | development | `/schedule-risk`, `/draw-package` (timeline context) |
| Vendor / contract evaluation | `vendor-evaluation` | property-ops | `/vendor-review`, `/expense-audit` (contract anomalies) |
| GHG emissions calculation | `ghg-emissions` | esg | `/carbon-footprint`, `/gresb-prep` (emissions section) |

Commands that are **pure orchestration** (sequencing checks, assembling status from multiple sources, no reusable analytical logic):
- `/close-readiness` — aggregates diligence status, approval status, and third-party report status. No calculation logic; all value is in the checklist structure, which lives in the `acquisition-risk` skill's diligence templates.

**Rule**: When `/screen-deal` needs a quick underwrite, it invokes `underwriting-standards` with a "screening" flag that produces abbreviated output. It does **not** reimplement pro forma logic. When `/ic-memo` needs financial exhibits, it invokes `underwriting-standards` for the numbers and `memo-writing` for the narrative. The command orchestrates; the skills compute.

### Command file format

Commands use YAML frontmatter and markdown body. Two styles:

**Short (delegates to skill):**
```markdown
---
description: Quick go/no-go screen for an acquisition opportunity
argument-hint: "[property name or address]"
---

Load the `deal-screening` skill and evaluate the opportunity against fund criteria.

If a property is provided, use it. Otherwise ask the user for the target property.
```

**Long (full workflow):**
```markdown
---
description: Full underwriting package for a CRE acquisition
argument-hint: "[property name or address]"
---

# Underwrite Asset

Build an institutional-grade underwriting package...

## Workflow

### Step 1: Gather Property Information
...

### Step 2: Load Underwriting Skill
Use `skill: "underwriting-standards"` to build the analysis...

### Step 3: Create Excel Output
...

## Quality Checklist
- [ ] Rent roll tied to trailing financials
- [ ] Cap rate sources documented
- [ ] Downtime and TI/LC assumptions market-supported
...

## Escalation Notes
- If rent roll is missing or incomplete, ask the user before proceeding
- If market data is unavailable, note the gap and use manual assumptions
```

### Required command anatomy

Each command markdown file should include:

- **Purpose** — what it produces
- **When to use** — the business trigger
- **Required inputs** — what the user must provide
- **Optional inputs** — what enhances the output
- **Skills invoked** — which canonical skills this command orchestrates (prevents reimplementation)
- **MCP sources used** — which connectors power it (with fallback if unavailable)
- **Reads from manifest** — which prior artifact types this command consumes (see Section 5.5)
- **Writes to manifest** — directory, filenames, and key_metrics this command exports
- **Behavior when prior artifacts missing** — ask user, or accept direct inputs?
- **Workflow steps** — the sequenced logic
- **Output artifact** — format and file naming (see Section 5)
- **QA checklist** — what to verify before delivery
- **Escalation notes** — how to handle missing data or uncertainty
- **Standards references** — which industry standards the output assists with (not "complies with")

---

## 7. Skills Design Principles

Skills carry the domain judgment. Commands are thin wrappers; skills do the heavy lifting.

### Skill file format

Each `SKILL.md` should include:

- **Trigger conditions** — when this skill activates
- **Business context** — why this workflow exists, who uses it
- **Source hierarchy** — which MCP/data source to prefer (see Section 8.4)
- **Workflow steps** — the detailed logic
- **Materiality / QA checks** — what errors to catch
- **Output structure** — expected format and sections
- **Edge cases** — asset-type variations, missing data handling
- **Escalation / uncertainty rules** — when to stop and ask
- **Standards references** — which industry standards this skill helps address

### Shared skills (live in core plugin)

These are cross-cutting and used by multiple verticals:

| Skill | Purpose |
|-------|---------|
| `underwriting-standards` | Pro forma construction, NOI line items, capital reserves, assumption documentation |
| `valuation-methods` | Cap rate, DCF, per-unit, per-SF, replacement-cost approaches |
| `rent-roll-normalization` | Rent roll cleanup, standardization, rollover and WALT calculation |
| `real-estate-metrics` | DSCR, debt yield, LTV, breakeven occupancy, cap rate, yield-on-cost definitions |
| `market-analysis` | Submarket delineation, supply/demand framework, comp selection and adjustment, demographic/employment context |
| `variance-analysis` | Actuals vs. budget/prior-year/underwriting comparison, driver decomposition, materiality thresholds |
| `memo-writing` | IC memo, asset report, investor letter tone and structure |
| `excel-presentation-qa` | Model audit rules, formula tracing, hardcode detection, slide QA |

### Asset-type adaptation

Skills should handle property-type differences via reference files, not separate skills:

```
skills/cam-reconciliation/
├── SKILL.md
├── references/
│   ├── office-cam-conventions.md
│   ├── retail-percentage-rent.md
│   ├── industrial-nnn-structure.md
│   ├── multifamily-rubs.md
│   └── boma-expense-classification.md
└── assets/
    └── cam-recon-template.md
```

---

## 8. MCP Strategy

### 8.1 Integration status matrix

Most MCP endpoints listed in earlier spec versions were hypothetical. This matrix tracks the actual status of each target integration. **Do not declare an MCP server in `.mcp.json` unless its status is "Native MCP available" or "Wrapper built."**

| System | Category | Status | Notes |
|--------|----------|--------|-------|
| **CoStar** | Market intelligence | API available, no known MCP | CoStar has a commercial API. Wrapper needed to expose as MCP. |
| **REIS / Moody's Analytics CRE** | Market intelligence | API available, no known MCP | Moody's Analytics has data APIs. Wrapper needed. |
| **Argus (Altus Group)** | Valuation | API limited, no known MCP | Argus Enterprise is primarily desktop software. File-based integration likely (import/export). |
| **Reonomy** | Property intelligence | API available, no known MCP | REST API exists. Wrapper needed. |
| **ATTOM** | Property data | API available, no known MCP | Well-documented REST API. Wrapper straightforward. |
| **Cherre** | Data integration | API available, no known MCP | GraphQL API. Wrapper needed. |
| **CoreLogic** | Property data | API available, no known MCP | Multiple API products. Wrapper needed. |
| **Trepp** | CMBS / debt | API available, no known MCP | Data feeds and API. Wrapper needed. |
| **RealPage** | Multifamily analytics | API limited, no known MCP | Primarily SaaS; API access varies by contract. |
| **Green Street** | REIT / CRE research | API limited, no known MCP | Research platform; limited programmatic access. Manual import likely. |
| **Yardi** | Property management | API available, no known MCP | Yardi Voyager API. Wrapper needed. Complex auth. |
| **Egnyte** | Document management | Native MCP available | Egnyte ships an MCP server. Ready to use. |
| **ENERGY STAR Portfolio Manager** | Energy benchmarking | API available, no known MCP | Public REST API (EPA). Wrapper straightforward. |
| **Procore** | Construction management | API available, no known MCP | Well-documented REST API. Wrapper needed. |
| **Measurabl** | ESG data | API available, no known MCP | Platform API. Wrapper needed. |
| **Moody's ESG / Four Twenty Seven** | Climate risk | API available, no known MCP | Risk data API. Wrapper needed. |
| **VTS** | Leasing CRM | API available, no known MCP | REST API. Wrapper needed. |

> **Key takeaway**: As of this writing, only Egnyte has a known native MCP server. All other integrations require either MCP wrapper development or manual data import. The `.mcp.json` files should only contain connectors that have been built and tested. Until then, commands and skills must support **manual data input as the primary path**, with MCP as an enhancement.

### 8.2 Core plugin .mcp.json

The core plugin's `.mcp.json` starts with only verified, built connectors. As wrappers are developed, they are added here:

```json
{
  "mcpServers": {
    "egnyte": {
      "type": "http",
      "url": "https://mcp-server.egnyte.com/mcp"
    }
  }
}
```

> **Target state** (once wrappers are built): CoStar, REIS/Moody's, ATTOM, CoreLogic, Trepp, Yardi, ENERGY STAR. Each will be added to `.mcp.json` only after the wrapper is built, tested, and documented.

### 8.3 MCP categories (target state)

| Category | Target systems | Used by |
|----------|---------------|---------|
| **Property / accounting** | Yardi, MRI, RealPage, AppFolio | Property ops, leasing, asset mgmt, ESG |
| **Market intelligence** | CoStar, REIS/Moody's, Green Street, Trepp | All verticals |
| **Deal / relationship** | Salesforce, HubSpot, VTS | Acquisitions, leasing, capital markets |
| **Documents / collaboration** | Egnyte, SharePoint, Box, Google Drive | All verticals |
| **Development / construction** | Procore | Development only |
| **Location / GIS / parcel** | ArcGIS, Google Maps, county parcel feeds | Acquisitions, development, ESG |
| **ESG / sustainability** | ENERGY STAR, Measurabl, Moody's ESG / Four Twenty Seven | ESG, asset mgmt, property ops |

### 8.4 Source-of-record precedence and conflict resolution

Skills should specify which system is authoritative for each data type. This prevents conflicting data from multiple sources.

#### Precedence table

| Data type | System of record | Fallback | Manual import? |
|-----------|-----------------|----------|----------------|
| Lease terms (rent, dates, options) | Executed lease document | Yardi/MRI lease abstract | Yes -- PDF/scan |
| Billed / collected revenue | Yardi/MRI GL | Manual rent roll | Yes -- Excel |
| Operating expenses (actuals) | Yardi/MRI GL | T-12 from offering memo | Yes -- Excel |
| Market rents and vacancy | CoStar | REIS/Moody's, then broker opinion | Yes -- user states assumptions |
| Sale / lease comps | CoStar | Reonomy, then ATTOM | Yes -- user provides |
| CMBS / debt data | Trepp | Reonomy debt records | Yes -- loan docs |
| Property ownership | Reonomy | ATTOM, then county records | Yes -- user provides |
| Zoning / parcel | County GIS / ATTOM | Manual input | Yes -- always |
| Construction costs | Procore (if connected) | RSMeans benchmarks, then manual | Yes -- budget Excel |
| REIT financials | SEC filings (10-K/10-Q) | Green Street, then CoStar | Yes -- user provides |
| Energy / utility consumption | ENERGY STAR Portfolio Manager | Yardi utility module | Yes -- utility bills |
| Building certifications | USGBC (LEED), EPA (ENERGY STAR) | Manual records | Yes -- always |
| Physical climate risk | Moody's ESG / Four Twenty Seven | FEMA flood maps | Yes -- third-party reports |

#### Conflict resolution rules

When data from multiple sources disagrees, or data quality is uncertain, skills must follow these rules:

1. **Temporal alignment**: Before combining data from multiple sources, check that dates are compatible. A rent roll from March, GL actuals from April, and market comps from last quarter are **not** automatically combinable. Skills must:
   - State the as-of date for each data source used
   - Flag when source dates differ by more than one quarter
   - Never silently blend data from different periods without disclosure

2. **Freshness gates**: Do not compute outputs that depend on stale inputs without explicit user acknowledgment:
   - Market rents: stale if > 6 months old
   - Property valuations: stale if > 1 quarter old
   - Rent rolls: stale if > 3 months old
   - Operating actuals: stale if > 1 month for monthly reports, > 1 quarter for annual analysis
   - Climate risk data: stale if > 1 year old

3. **Disagreement handling**: When two sources provide conflicting values for the same data point:
   - Present both values and their sources
   - Flag the discrepancy to the user
   - Do **not** silently average, pick one, or resolve the conflict
   - Ask the user which source to rely on, or whether to show a range

4. **Missing data escalation**: When required data is unavailable from any source:
   - State what is missing and why it matters
   - Suggest where the user might obtain it
   - Offer to proceed with user-provided assumptions, clearly marked as manual inputs
   - Never fabricate data or use placeholder values without explicit labeling

5. **"Do not compute unless" gates**: Certain outputs are misleading without minimum input quality. Skills must refuse to produce these outputs (and explain why) if minimum inputs are not met:
   - Pro forma: requires at minimum a rent roll OR stated rent/occupancy assumptions
   - Valuation: requires at minimum a stabilized NOI or assumptions to derive one
   - Fund performance: requires at minimum quarterly property valuations and cash flows
   - GRESB prep: requires at minimum 12 months of utility data for the Performance component

---

## 9. Plugin Specifications

### 9.1 real-estate-analysis (CORE)

> Required foundation plugin. Install first. Owns shared MCP connectors and cross-cutting skills.

**`.claude-plugin/plugin.json`**

```json
{
  "name": "real-estate-analysis",
  "version": "0.1.0",
  "description": "Core real estate analysis with shared MCP connectors, underwriting, valuation, rent roll normalization, and reporting skills.",
  "author": {
    "name": "Anthropic"
  }
}
```

#### Commands (6)

| # | Command | Workflow | Skills invoked | Output |
|---|---------|---------|----------------|--------|
| 1 | `/underwrite-asset` | Build a base underwriting view from OM, rent roll, T-12, and market data. Pro forma, debt sizing, and return metrics. | `underwriting-standards`, `rent-roll-normalization`, `valuation-methods`, `market-analysis`, `debt-sizing-hierarchy` | Excel |
| 2 | `/value-asset` | Property valuation using cap rate, DCF, and market comp framing. Produces supportable value range with methodology. | `valuation-methods`, `market-analysis` | Excel |
| 3 | `/rent-roll-qc` | Normalize and QA a rent roll: rollover schedule, downtime, top-tenant exposure, mark-to-market, and WALT. | `rent-roll-normalization` | Excel |
| 4 | `/ops-variance` | Compare actuals vs. budget / prior year / underwriting case. Flag material variances with driver explanations. | `variance-analysis` | Excel + Word |
| 5 | `/market-snapshot` | Submarket supply/demand summary: vacancy, rents, construction pipeline, absorption, demographics, and recent transactions. | `market-analysis` | Word |
| 6 | `/investment-memo-draft` | Produce a neutral draft memo using the repo's standard real-estate memo template. | `memo-writing` | Word |

#### Skills (8)

| Skill | Purpose |
|-------|---------|
| `underwriting-standards` | Pro forma construction, NOI line items, capital reserves, assumption documentation |
| `valuation-methods` | Income approach (direct cap, DCF), sales comparison, cost approach, reconciliation |
| `rent-roll-normalization` | Rent roll cleanup, standardization, rollover/WALT calc, tenant credit flagging |
| `real-estate-metrics` | DSCR, debt yield, LTV, breakeven occupancy, cap rate, yield-on-cost definitions |
| `market-analysis` | Submarket delineation, supply/demand framework, comp selection and adjustment, demographic/employment context |
| `variance-analysis` | Actuals vs. budget/prior-year/underwriting comparison, driver decomposition, materiality thresholds |
| `memo-writing` | IC memo, asset report, investor letter structure and tone conventions |
| `excel-presentation-qa` | Model audit rules, formula tracing, hardcode detection, slide QA |

---

### 9.2 acquisitions-investments

> Deal screening through close for acquisitions teams, PE investors, REIT investment groups, and family office buyers.

**`.claude-plugin/plugin.json`**

```json
{
  "name": "acquisitions-investments",
  "version": "0.1.0",
  "description": "CRE acquisition workflows: deal screening, underwriting, bid strategy, IC memos, diligence tracking, and close readiness.",
  "author": {
    "name": "Anthropic"
  }
}
```

#### Commands (8)

| # | Command | Workflow | Skills invoked | Output |
|---|---------|---------|----------------|--------|
| 1 | `/screen-deal` | Quick go/no-go screen based on asset, market, seller ask, yield, and risk flags against fund criteria. | `deal-screening`, `underwriting-standards` (quick mode) | Word |
| 2 | `/bid-envelope` | Recommend bid range and key pricing sensitivities. Tests multiple exit cap / rent growth / capex scenarios. | `bid-strategy`, `underwriting-standards`, `scenario-stress-testing` | Excel |
| 3 | `/acq-comps` | Gather sale and lease comps relevant to the opportunity. Adjust for property differences, produce formatted comp set. | `market-analysis` | Excel |
| 4 | `/ic-memo` | Draft acquisition investment committee memo: executive summary, market, financials, risks, and recommendation. | `ic-memo-conventions`, `memo-writing`, `underwriting-standards` | Word |
| 5 | `/diligence-punchlist` | Generate sector-specific diligence checklist and open-issues tracker with responsibility assignments. | `acquisition-risk` | Word + Excel |
| 6 | `/downside-case` | Pressure-test rents, downtime, exit cap, capex, and financing terms. Produce bear-case returns vs. base. | `scenario-stress-testing`, `underwriting-standards` | Excel |
| 7 | `/deal-structure` | Compare direct acquisition vs. JV / preferred equity / programmatic structure. Model GP/LP splits and promotes. | `deal-structuring` | Excel |
| 8 | `/close-readiness` | Summarize unresolved diligence, outstanding approvals, third-party reports, and closing risks. Go/no-go for close. | Orchestration only -- aggregates status using `acquisition-risk` diligence templates. No reusable calc logic. | Word |

#### Skills (6)

| Skill | Purpose |
|-------|---------|
| `deal-screening` | Go/no-go framework, strategy-specific criteria (core/value-add/opportunistic), quick underwrite |
| `bid-strategy` | Bid range methodology, pricing sensitivity, competitive positioning |
| `ic-memo-conventions` | IC memo structure, executive summary framework, risk/mitigation format |
| `acquisition-risk` | Risk taxonomy for CRE acquisitions, due diligence scoping by property type |
| `deal-structuring` | JV, preferred equity, programmatic structures, promote mechanics |
| `scenario-stress-testing` | Downside construction, breakeven analysis, sensitivity methodology |

---

### 9.3 asset-management

> Portfolio surveillance, fund performance reporting, and investor communication for asset managers, portfolio managers, REIT operating teams, fund managers, and separate-account managers.

**`.claude-plugin/plugin.json`**

```json
{
  "name": "asset-management",
  "version": "0.1.0",
  "description": "Asset and portfolio management: monthly reporting, reforecasting, hold-sell analysis, business plans, fund performance, and investor updates.",
  "author": {
    "name": "Anthropic"
  }
}
```

#### Commands (9)

| # | Command | Workflow | Skills invoked | Output |
|---|---------|---------|----------------|--------|
| 1 | `/monthly-asset-report` | Monthly asset report: leasing activity, collections, NOI, occupancy, capex updates, and management commentary. | `same-store-noi`, `leasing-spread-analysis` | Word + Excel |
| 2 | `/quarterly-portfolio-review` | Portfolio review across assets, sectors, geographies, and watchlist items. Includes performance attribution. | `portfolio-review-writing`, `performance-attribution` | Word + PPT |
| 3 | `/reforecast` | Update full-year outlook using YTD actuals, leasing pipeline, capex timing, and market changes. | `underwriting-standards` (projection mode) | Excel |
| 4 | `/hold-sell` | Evaluate hold, refinance, recapitalize, or sell options with forward return comparison. | `hold-sell-framework`, `underwriting-standards`, `valuation-methods` | Excel + Word |
| 5 | `/asset-business-plan` | Draft or update the asset's 12-24 month operating and capital plan with measurable milestones. | `business-plan-governance` | Word |
| 6 | `/capital-plan` | Rank capex projects by urgency, NOI impact, risk, and tenant-retention value. Multi-year schedule. | `capex-prioritization` | Excel |
| 7 | `/fund-performance` | Assist with fund-level return calculations: TWRR, IRR, TVPI/DPI/RVPI, TGER. Structure data for NCREIF/ODCE submission preparation. | `fund-return-calculations` | Excel |
| 8 | `/attribution` | Performance attribution by property type, geography, vintage, and strategy vs. benchmark (NPI, ODCE). Decompose into income return and capital appreciation. | `performance-attribution` | Excel + Word |
| 9 | `/investor-update` | Draft LP / board / REIT management update for a given asset or portfolio segment. | `investor-reporting`, `memo-writing` | Word |

#### Skills (8)

| Skill | Purpose |
|-------|---------|
| `same-store-noi` | Same-store NOI analysis, occupancy bridge, revenue and expense decomposition |
| `leasing-spread-analysis` | New lease and renewal spreads, rollover waterfall, retention economics |
| `portfolio-review-writing` | Portfolio review structure, watchlist escalation standards, KPI framing |
| `hold-sell-framework` | Hold/sell/refi/recap decision framework, forward IRR comparison |
| `business-plan-governance` | Asset plan structure, milestone tracking, variance-to-plan reporting |
| `capex-prioritization` | Capex project scoring (urgency, NOI impact, risk, tenant retention), reserve adequacy, multi-year scheduling |
| `investor-reporting` | LP letter conventions, REIT-style disclosure, fund-level attribution |
| `fund-return-calculations` | TWRR and IRR methodology, TVPI/DPI/RVPI multiples, TGER calculation. Assists with NCREIF/PREA reporting preparation. |
| `performance-attribution` | Return decomposition (income vs. appreciation), benchmark comparison, property-type and geographic attribution |

---

### 9.4 capital-markets

> Borrower-side debt and structured finance workflows for capital markets teams, treasury/finance groups, and in-house financing teams. Does **not** cover lender-side debt portfolio surveillance (see Section 3).

**`.claude-plugin/plugin.json`**

```json
{
  "name": "capital-markets",
  "version": "0.1.0",
  "description": "Borrower-side debt and structured finance: loan sizing, refinance comparison, covenant surveillance, maturity watchlists, and financing memos.",
  "author": {
    "name": "Anthropic"
  }
}
```

#### Commands (7)

| # | Command | Workflow | Skills invoked | Output |
|---|---------|---------|----------------|--------|
| 1 | `/debt-size` | Size loan proceeds based on DSCR, debt yield, LTV, and lender-specific constraints across multiple structures (agency, CMBS, bank, bridge). | `debt-sizing-hierarchy` | Excel |
| 2 | `/refi-compare` | Compare refinance options across lenders and structures. Side-by-side terms, proceeds, and cost analysis. | `debt-sizing-hierarchy`, `refinance-risk` | Excel |
| 3 | `/lender-shortlist` | Recommend likely lender universe for the asset profile and business plan. Rank by fit and recent activity. | `lender-matching` | Excel |
| 4 | `/debt-memo` | Draft financing memo or lender package summary with property overview, financials, and borrower profile. | `credit-memo-language`, `memo-writing` | Word |
| 5 | `/covenant-check` | Test actual and forecast performance against loan covenants and trigger thresholds. Flag breaches and near-misses. | `covenant-surveillance` | Excel + Word |
| 6 | `/maturity-watchlist` | Flag loans with upcoming maturities and refinancing risk. Rank by severity and optionality. | `refinance-risk` | Excel |
| 7 | `/hedge-review` | Review floating-rate exposure, interest rate caps/swaps, hedging gaps, and mark-to-market on existing hedges. | `rate-hedging` | Excel |

#### Skills (5)

| Skill | Purpose |
|-------|---------|
| `debt-sizing-hierarchy` | DSCR/DY/LTV constraint waterfall, lender program parameters, sizing methodology |
| `lender-matching` | Lender universe segmentation (agency, CMBS, bank, bridge, life co), asset/strategy fit scoring, recent activity matching |
| `credit-memo-language` | Financing memo structure, borrower presentation, property summary conventions |
| `covenant-surveillance` | Covenant testing methodology, cure/waiver framing, early warning thresholds |
| `refinance-risk` | Maturity risk scoring, interest rate exposure analysis, prepayment considerations |
| `rate-hedging` | Cap/swap mechanics, mark-to-market methodology, hedge effectiveness |

---

### 9.5 development-construction

> Ground-up and value-add development workflows for developers, development managers, construction lenders, and repositioning teams.

**`.claude-plugin/plugin.json`**

```json
{
  "name": "development-construction",
  "version": "0.1.0",
  "description": "Development workflows: site feasibility, entitlements, budgets, draw packages, GMP comparison, and lease-up monitoring.",
  "author": {
    "name": "Anthropic"
  }
}
```

#### Commands (8)

| # | Command | Workflow | Skills invoked | Output |
|---|---------|---------|----------------|--------|
| 1 | `/site-feasibility` | Site constraints, access, utilities, parcel context, zoning envelope, highest-and-best-use, and preliminary financial viability. | `feasibility-analysis` | Word |
| 2 | `/zoning-check` | Zoning and entitlement issue summary: allowed uses, density/FAR, setbacks, variances needed, likely approval path and timeline. | `entitlement-workflow` | Word + Excel |
| 3 | `/dev-budget-review` | Analyze development budget: hard/soft cost breakdown, contingencies, value-engineering options, and cost overrun risks. | `dev-budget-taxonomy` | Excel |
| 4 | `/schedule-risk` | Assess schedule critical path, dependencies, delivery threats, and weather/permitting risks. | `schedule-analysis` | Word + Excel |
| 5 | `/draw-package` | Prepare lender or equity draw summary: budget-to-date, retainage, lender advance calculation, interest reserve, and support checklist. | `draw-governance` | Excel |
| 6 | `/gmp-compare` | Compare contractor or GMP proposals side by side. Normalize scope, flag exclusions, and recommend. | `gmp-evaluation` | Excel + Word |
| 7 | `/lease-up-monitor` | Track absorption, concessions, occupancy ramp, and stabilization timing vs. pro forma. | `lease-up-tracking` | Excel |
| 8 | `/dev-ic-memo` | Draft development investment memo or approval package: site, program, budget, returns, risks, and recommendation. | `memo-writing`, `feasibility-analysis` | Word |

#### Skills (6)

| Skill | Purpose |
|-------|---------|
| `feasibility-analysis` | Highest-and-best-use framework, zoning envelope, site capacity, preliminary returns |
| `entitlement-workflow` | Approval process mapping, timeline estimation, community engagement, risk factors |
| `dev-budget-taxonomy` | CSI MasterFormat structure, cost benchmarking, escalation factors, contingency methodology |
| `schedule-analysis` | Critical-path identification, dependency mapping, delivery risk scoring, weather/permitting schedule impact |
| `draw-governance` | Draw request format, retainage rules, lender advance mechanics, interest reserve calc |
| `gmp-evaluation` | Scope normalization, exclusion flagging, contractor comparison methodology |
| `lease-up-tracking` | Absorption modeling, concession burn-off, stabilization metrics, variance-to-proforma |

#### Unique MCP (declared in this plugin's .mcp.json when wrapper is built)

Target: Procore (construction management). Until available, commands accept manual budget/schedule data.

---

### 9.6 property-operations

> Property-level operations for property managers, regional operations leaders, owner-operator finance teams, and CAM/recoveries analysts.

**`.claude-plugin/plugin.json`**

```json
{
  "name": "property-operations",
  "version": "0.1.0",
  "description": "Property operations: budgeting, CAM reconciliation, expense audits, collections monitoring, vendor review, and benchmarking.",
  "author": {
    "name": "Anthropic"
  }
}
```

#### Commands (8)

| # | Command | Workflow | Skills invoked | Output |
|---|---------|---------|----------------|--------|
| 1 | `/property-budget` | Annual property budget with key assumptions, line-item projections, CPI escalation, contract parsing, and narrative commentary. | `budget-narrative`, `operations-kpi` | Excel + Word |
| 2 | `/cam-recon` | CAM/OPEX recovery reconciliation: pro-rata share allocation, gross-up, cap/stop application, over/under billings, tenant statements. | `cam-reconciliation` | Excel |
| 3 | `/expense-audit` | Identify unusual expense growth, GL coding issues, duplicate payments, and savings opportunities. | `expense-coding-hygiene` | Excel + Word |
| 4 | `/collections-watchlist` | Surface delinquency, tenant concentration risk, near-term cash exposure, and recommended escalation actions. | `collections-escalation` | Excel |
| 5 | `/vendor-review` | Compare vendor performance, pricing, contract renewals, and scope compliance. Flag renegotiation opportunities. | `vendor-evaluation` | Excel + Word |
| 6 | `/service-level-report` | Work order analysis: response times, recurring failures, tenant service patterns, and maintenance backlog. | `operations-kpi` | Word + Excel |
| 7 | `/opex-benchmark` | Compare building operating costs vs. internal portfolio and market benchmarks. Uses IREM Income/Expense IQ categories where available. | `opex-benchmarking` | Excel |
| 8 | `/property-flash` | Concise weekly or month-end building flash report: key metrics, exceptions, and management action items. | `operations-kpi` | Word |

#### Skills (6)

| Skill | Purpose |
|-------|---------|
| `cam-reconciliation` | Expense pool definitions, pro-rata share calc, gross-up, cap/stop application, tenant statement format. References BOMA expense classification. |
| `expense-coding-hygiene` | GL code validation, duplicate detection, reclassification rules |
| `budget-narrative` | Property budget commentary style, assumption documentation, variance explanation |
| `collections-escalation` | Delinquency thresholds, escalation workflow, credit risk flagging |
| `vendor-evaluation` | Vendor performance scoring, contract pricing comparison, renewal timing, scope compliance checking |
| `operations-kpi` | Occupancy, collections rate, work order metrics, energy/utility benchmarks |
| `opex-benchmarking` | Per-SF expense calculation, IREM/BOMA category mapping, quartile comparison, normalization adjustments. References IREM Income/Expense IQ methodology. |

---

### 9.7 leasing

> Leasing workflows for leasing teams, asset managers running leasing strategy, broker management teams, and lease-up teams across office, retail, industrial, and multifamily.

**`.claude-plugin/plugin.json`**

```json
{
  "name": "leasing",
  "version": "0.1.0",
  "description": "Leasing workflows: pipeline review, proposal comparison, lease abstracting, mark-to-market, renewal strategy, and broker briefs.",
  "author": {
    "name": "Anthropic"
  }
}
```

#### Commands (8)

| # | Command | Workflow | Skills invoked | Output |
|---|---------|---------|----------------|--------|
| 1 | `/pipeline-review` | Active prospect summary: stage progression, blockers, near-term wins/losses, and velocity metrics. | `pipeline-analytics` | Excel + Word |
| 2 | `/proposal-compare` | Compare LOIs or lease proposals side by side: economics, concessions, term, options, and net effective rent. | `lease-economics` | Excel |
| 3 | `/lease-abstract` | Extract key economics and rights from a signed lease or redline: dates, rent schedule, escalations, options, expense structure, green lease clauses, and critical clauses. | `lease-economics`, `green-lease-extraction` | Word |
| 4 | `/mark-to-market` | Analyze upcoming rollover against current market rents. Quantify spread opportunity or loss exposure by suite. | `rollover-waterfall`, `rent-roll-normalization` | Excel |
| 5 | `/renewal-strategy` | Recommend renewal vs. backfill approach by tenant/suite. Model retention NPV, concession cost, and downtime risk. | `renewal-decision` | Excel + Word |
| 6 | `/leasing-pack` | Prepare landlord leasing update for ownership or lenders: activity summary, pipeline, executed deals, and market context. | `pipeline-analytics`, `memo-writing` | Word + PPT |
| 7 | `/tenant-exposure` | Top-tenant concentration, rollover schedule, option exercise risk, and credit exposure analysis. | `tenant-credit`, `rollover-waterfall` | Excel |
| 8 | `/broker-brief` | Draft broker guidance note: space positioning, target tenants, concession parameters, and negotiation guardrails. | `broker-communication` | Word |

#### Skills (7)

| Skill | Purpose |
|-------|---------|
| `lease-economics` | Net effective rent calculation, concession valuation, TI amortization, free rent NPV |
| `renewal-decision` | Retention NPV framework, backfill cost modeling, walk-away threshold calculation |
| `rollover-waterfall` | Rollover schedule construction, downtime assumptions, re-leasing spread methodology |
| `pipeline-analytics` | Prospect staging, velocity metrics, conversion rates, pipeline-to-vacancy coverage |
| `tenant-credit` | Credit assessment framework, watchlist criteria, concentration risk scoring |
| `broker-communication` | Broker brief structure, market positioning language, negotiation parameter framing |
| `green-lease-extraction` | Identify and flag green lease provisions during abstraction: utility data sharing, efficiency cost recovery, submetering, sustainability fit-out. References Green Lease Leaders criteria. |

---

### 9.8 esg-sustainability

> ESG data collection, sustainability reporting, and climate risk analysis for ESG committees, asset managers, and investor relations teams preparing GRESB submissions, UNPRI reports, and TCFD/IFRS S2 disclosures.

**`.claude-plugin/plugin.json`**

```json
{
  "name": "esg-sustainability",
  "version": "0.1.0",
  "description": "ESG and sustainability workflows: GRESB submission prep, carbon footprint, utility benchmarking, climate risk, green lease audits, and certification tracking.",
  "author": {
    "name": "Anthropic"
  }
}
```

#### Commands (7)

| # | Command | Workflow | Skills invoked | Output |
|---|---------|---------|----------------|--------|
| 1 | `/gresb-prep` | Assist with GRESB Real Estate Assessment preparation: collect and organize asset-level data across indicators, identify gaps, estimate approximate score positioning, and structure data for submission. Does not produce submission-ready files directly. | `gresb-assessment`, `ghg-emissions`, `utility-analysis` | Excel + Word |
| 2 | `/carbon-footprint` | Calculate portfolio GHG emissions across Scope 1 (direct), Scope 2 (purchased energy), and Scope 3 (tenant, embodied). Produce intensity metrics (per SF, per unit) and year-over-year trend. | `ghg-emissions` | Excel |
| 3 | `/utility-benchmark` | Track and benchmark energy, water, and waste at the asset level. Like-for-like year-over-year comparison for consistent property sets. Compare against ENERGY STAR scores where available. | `utility-analysis` | Excel |
| 4 | `/climate-risk` | Physical and transition climate risk assessment per asset: flood zone, extreme heat, sea-level rise, wildfire, regulatory exposure. Produce risk summary and flag high-exposure assets. | `climate-risk-assessment` | Excel + Word |
| 5 | `/green-lease-audit` | Audit portfolio for green lease clause adoption: utility data sharing, cost recovery for efficiency improvements, submetering coverage, sustainability fit-out requirements. | `green-lease-standards` | Excel |
| 6 | `/esg-report` | Draft annual ESG report narrative sections. Helps organize disclosures aligned with GRI, TCFD/IFRS S2, and UNPRI frameworks. Pulls data from other ESG commands. | `esg-reporting-frameworks` | Word |
| 7 | `/certification-tracker` | Track building certifications (LEED, ENERGY STAR, BREEAM, Fitwel, WELL) across portfolio: current status, expiration dates, coverage percentage by area and count. | `certification-management` | Excel |

#### Skills (7)

| Skill | Purpose |
|-------|---------|
| `gresb-assessment` | GRESB indicator mapping (Management + Performance components), data collection guidance, gap identification, approximate score estimation. Does not guarantee submission-readiness or exact scoring replication. |
| `ghg-emissions` | GHG Protocol methodology guidance, Scope 1/2/3 classification for real estate, emission factor selection (EPA eGRID, IEA), intensity metric calculation |
| `utility-analysis` | Energy (kWh, therms), water (gallons/m3), waste (tons) tracking; like-for-like methodology; ENERGY STAR score interpretation |
| `climate-risk-assessment` | Physical risk categories (flood, heat, wind, wildfire, sea-level), transition risk (carbon pricing, regulation), asset-level risk flagging |
| `green-lease-standards` | Green lease clause taxonomy, cost recovery mechanisms, metering/submetering standards, compliance tracking. References Green Lease Leaders and GRESB TC indicators. |
| `esg-reporting-frameworks` | Guidance on GRI universal standards (302, 303, 305, 306), TCFD/IFRS S2 four-pillar structure, UNPRI real estate module. Helps organize disclosures but does not guarantee framework compliance. |
| `certification-management` | Certification types (LEED levels, ENERGY STAR, BREEAM ratings, Fitwel, WELL), renewal cadences, portfolio coverage calculation |

#### Unique MCP (declared when wrappers are built)

Targets: Measurabl (ESG data platform), Four Twenty Seven / Moody's ESG (climate risk data). Until available, commands accept manual utility data and third-party climate risk reports.

---

## 10. Partner Plugins

### Ownership model

CoStar and Yardi appear in two roles in this repo. To avoid ambiguity:

- **Core MCP connectors** (in `real-estate-analysis/.mcp.json`): The core plugin declares MCP connections to CoStar and Yardi APIs when wrappers are built. These provide raw data access (property lookups, GL queries, comp searches) available to all installed plugins.
- **Partner plugins** (in `partner-built/costar/` and `partner-built/yardi/`): These are **additional skills and commands** contributed by the partners themselves that layer on top of the core MCP connections. They add partner-specific workflows, proprietary analytics, and optimized data retrieval patterns that go beyond what the core connector provides.

The partner plugin does **not** own the MCP connection. The core plugin does. The partner plugin adds value through specialized skills that use the same connector more effectively.

| Responsibility | Core plugin | Partner plugin |
|---------------|------------|----------------|
| MCP connection declaration | Yes | No (uses core's) |
| Authentication setup docs | Yes | May supplement |
| Raw data access (property lookup, GL query) | Yes (via MCP tools) | Inherited |
| Specialized workflows and skills | No | Yes |
| Versioning and maintenance | Anthropic | Partner |

### partner-built/costar

```json
{
  "name": "costar",
  "version": "1.0.0",
  "description": "CoStar Group skills: advanced comp analysis, submarket deep-dives, tenant prospecting, and market forecasting powered by CoStar data.",
  "author": {
    "name": "CoStar Group",
    "email": "integrations@costar.com"
  },
  "homepage": "https://www.costar.com",
  "license": "Apache-2.0",
  "keywords": ["real-estate", "commercial", "comps", "market-data"]
}
```

### partner-built/yardi

```json
{
  "name": "yardi",
  "version": "1.0.0",
  "description": "Yardi Systems skills: Voyager-optimized lease administration, GL reporting, maintenance workflows, and portfolio data extraction.",
  "author": {
    "name": "Yardi Systems",
    "email": "integrations@yardi.com"
  },
  "homepage": "https://www.yardi.com",
  "license": "Apache-2.0",
  "keywords": ["property-management", "leasing", "accounting", "yardi-voyager"]
}
```

---

## 11. Cross-Plugin Workflow Examples

### Acquisition lifecycle

1. **`/screen-deal`** (acquisitions) — Quick go/no-go screen
2. **`/acq-comps`** (acquisitions) — Sale and lease comps
3. **`/market-snapshot`** (core) — Submarket fundamentals
4. **`/underwrite-asset`** (core) — Base underwriting
5. **`/bid-envelope`** (acquisitions) — Pricing and sensitivities
6. **`/downside-case`** (acquisitions) — Stress test
7. **`/climate-risk`** (esg) — Physical/transition risk assessment
8. **`/debt-size`** (capital-markets) — Financing options
9. **`/ic-memo`** (acquisitions) — Investment committee package
10. **`/diligence-punchlist`** (acquisitions) — DD tracker
11. **`/close-readiness`** (acquisitions) — Final go/no-go

### Asset management annual cycle

1. **`/monthly-asset-report`** (asset-mgmt) — Recurring monthly reports
2. **`/ops-variance`** (core) — Quarterly variance deep-dives
3. **`/reforecast`** (asset-mgmt) — Mid-year outlook update
4. **`/quarterly-portfolio-review`** (asset-mgmt) — Portfolio-level review
5. **`/fund-performance`** (asset-mgmt) — Quarterly return calculations
6. **`/attribution`** (asset-mgmt) — Performance attribution vs. benchmark
7. **`/hold-sell`** (asset-mgmt) — Annual hold/sell evaluation
8. **`/investor-update`** (asset-mgmt) — LP/board communication

### Leasing + operations coordination

1. **`/mark-to-market`** (leasing) — Identify rollover opportunity
2. **`/renewal-strategy`** (leasing) — Decide renew vs. backfill
3. **`/proposal-compare`** (leasing) — Evaluate incoming LOIs
4. **`/cam-recon`** (property-ops) — Year-end tenant reconciliation
5. **`/property-budget`** (property-ops) — Next-year budget with leasing assumptions
6. **`/leasing-pack`** (leasing) — Ownership update

### Development project lifecycle

1. **`/site-feasibility`** (development) — Site evaluation
2. **`/zoning-check`** (development) — Entitlement analysis
3. **`/climate-risk`** (esg) — Climate exposure before committing
4. **`/dev-ic-memo`** (development) — Approval package
5. **`/deal-structure`** (acquisitions) — JV/equity structure
6. **`/dev-budget-review`** (development) — Budget analysis
7. **`/gmp-compare`** (development) — Contractor selection
8. **`/draw-package`** (development) — Monthly draws
9. **`/lease-up-monitor`** (development) — Absorption tracking
10. **`/debt-size`** (capital-markets) — Permanent financing

### Capital markets refinancing

1. **`/maturity-watchlist`** (capital-markets) — Identify upcoming maturities
2. **`/value-asset`** (core) — Updated valuation
3. **`/debt-size`** (capital-markets) — Size new loan
4. **`/refi-compare`** (capital-markets) — Compare lender options
5. **`/lender-shortlist`** (capital-markets) — Target lenders
6. **`/debt-memo`** (capital-markets) — Lender package

### Annual ESG reporting cycle

1. **`/utility-benchmark`** (esg) — Collect and benchmark asset-level utility data
2. **`/carbon-footprint`** (esg) — Calculate portfolio emissions
3. **`/certification-tracker`** (esg) — Update certification status
4. **`/green-lease-audit`** (esg) — Audit green lease adoption
5. **`/climate-risk`** (esg) — Refresh climate risk assessments
6. **`/gresb-prep`** (esg) — Prepare GRESB submission (Apr-Jul window)
7. **`/esg-report`** (esg) — Draft annual ESG report

---

## 12. Industry Standards Alignment

> **Important caveat on all standards references**: The plugins **assist with preparation** of standards-aligned outputs. They do not guarantee compliance, submission-readiness, or audit-grade accuracy. Producing truly compliant NCREIF submissions, GRESB assessments, or IFRS S2 disclosures requires field-level validation rules, calculation audits, and version-specific formatting that are beyond what v1 delivers. The standards references in skills guide the structure and terminology, not the exact specification.

### How standards are addressed

| Standard / Organization | Plugin(s) | What the plugin does | What it does NOT do |
|------------------------|-----------|---------------------|-------------------|
| **NCREIF** (NPI, ODCE) | asset-management | `/fund-performance` assists with return calculations (TWRR, IRR, multiples). `/attribution` helps structure benchmark comparisons. Skills use NCREIF terminology and metric definitions. | Does not produce submission-ready NCREIF data files. Does not replicate exact NCREIF calculation rules or validation edits. Firms must validate against NCREIF Data Collection Manual. |
| **NCREIF/PREA Reporting Standards** | asset-management, core | `fund-return-calculations` skill references TGER methodology and IRR hierarchy. `memo-writing` uses NCREIF/PREA terminology. | Does not implement the full Global Definitions Database. Does not produce auditable Schedule of Investments (FR.04). |
| **NAREIM** | asset-management | `portfolio-review-writing` skill references NAREIM asset-level reporting best practices. | Does not replicate NAREIM member-only benchmarking surveys. |
| **PREA** | asset-management | Covered through NCREIF/PREA joint standards above. | Same limitations as NCREIF. |
| **IREM** | property-operations | `/opex-benchmark` maps expenses to IREM-style categories and supports per-SF quartile comparison. | Does not include IREM Income/Expense IQ benchmark data (requires IREM subscription). |
| **BOMA** | property-operations | `cam-reconciliation` skill references BOMA expense classification structure. | Does not enforce BOMA classification rules programmatically. |
| **GRESB** | esg-sustainability | `/gresb-prep` helps organize data across GRESB indicators, identifies coverage gaps, and estimates approximate positioning. | Does not replicate GRESB's proprietary scoring algorithm, relative scoring against peer groups, or validation multipliers. Does not produce the GRESB portal submission directly. |
| **TCFD / IFRS S2** | esg-sustainability | `/climate-risk` structures physical and transition risk assessment. `/esg-report` helps organize four-pillar disclosures. | Does not implement all 18 IFRS S2 real estate industry-based disclosures at field level. |
| **UNPRI** | esg-sustainability, acquisitions | `/esg-report` helps organize PRI module disclosures. `/screen-deal` includes ESG considerations. | Does not map to all 24 PRI real estate module indicators. |
| **GRI** | esg-sustainability | `/esg-report` references GRI universal standards (302, 303, 305, 306). | No GRI real estate sector standard exists yet. Coverage is framework-level only. |
| **ULI Greenprint** | esg-sustainability | `/utility-benchmark` supports like-for-like YoY energy/water/waste comparisons. | Does not interface with ULI Greenprint data platform. |
| **Green Lease Leaders** | esg, leasing | `/green-lease-audit` checks clause adoption. `green-lease-extraction` flags provisions in `/lease-abstract`. | Does not certify Green Lease Leader status. |
| **ENERGY STAR** | esg-sustainability | `/utility-benchmark` can incorporate ENERGY STAR scores. `certification-management` tracks certifications. | Does not submit to ENERGY STAR Portfolio Manager. |

---

## 13. Build Order and v1 Scope

### v1 MVP (ship first)

Build only these three plugins in v1. This covers the highest-value workflows for the broadest audience (acquisitions teams, asset managers, portfolio managers):

1. **`real-estate-analysis`** (core) — 6 commands, 8 skills
2. **`acquisitions-investments`** — 8 commands, 6 skills
3. **`asset-management`** — 9 commands, 9 skills

**v1 total: 3 plugins, 23 commands, 23 skills.**

v1 MCP: Egnyte only (native MCP). All other data via manual import. Begin building CoStar and Yardi MCP wrappers in parallel.

### v1.1 (execution layers)

4. `capital-markets` — 7 commands
5. `leasing` — 8 commands
6. `property-operations` — 8 commands

### v1.2 (compliance and specialization)

7. `esg-sustainability` — 7 commands
8. `development-construction` — 8 commands

### v1.3 (partner integrations)

9. `partner-built/costar`
10. `partner-built/yardi`

> **Note on ESG timing**: Firms with active GRESB submissions (Apr-Jul annual window) may pull `esg-sustainability` forward. The ESG plugin has no dependency on v1.1 plugins.

---

## 14. Non-Goals for v1

- **One plugin per asset class** (office, multifamily, industrial, retail, hotel, self-storage, seniors housing). Asset-class differences live in skill reference files.
- **One plugin per owner type** (REIT vs. PE vs. pension vs. family office). Owner-type differences are handled via personas in skills and local.md settings.
- **Lender-side debt portfolio surveillance** (monitoring originated loans for mortgage REITs or debt funds). v1 capital-markets is borrower-side only.
- **Generic AI utility commands** (`/analyze-file`, `/summarize`, `/make-chart`). Every command maps to a named business workflow.
- **Heavy code or build tooling** inside the plugin repo. Plugin definitions are markdown and JSON. The repo ships validated Python calculation functions and Excel templates (see Section 5.4), but these are standalone scripts and files -- no build system, no compilation, no package manager required.
- **Residential brokerage or mortgage origination** workflows.
- **Submission-ready compliance outputs**. v1 assists with preparation of NCREIF, GRESB, and other standards-aligned deliverables. It does not produce auditable, submission-ready files (see Section 12).
- **MCP wrapper development**. The plugins are designed to work with manual data input. MCP wrappers are a separate workstream that enhances but is not required for plugin functionality.

---

## 15. Summary

| Plugin | Vertical | Commands | Skills | Phase |
|--------|----------|----------|--------|-------|
| **real-estate-analysis** | Core analysis | 6 | 8 | v1 |
| **acquisitions-investments** | Deal screening -> close | 8 | 6 | v1 |
| **asset-management** | Portfolio + fund performance | 9 | 9 | v1 |
| **capital-markets** | Borrower-side debt | 7 | 6 | v1.1 |
| **leasing** | Pipeline -> execution | 8 | 7 | v1.1 |
| **property-operations** | Building-level ops | 8 | 7 | v1.1 |
| **esg-sustainability** | ESG & climate risk | 7 | 7 | v1.2 |
| **development-construction** | Ground-up & value-add | 8 | 7 | v1.2 |
| **costar** (partner) | CoStar skills | -- | 3+ | v1.3 |
| **yardi** (partner) | Yardi skills | -- | 3+ | v1.3 |
| **Total** | | **61** | **57+** | |

### Key architectural decisions

| Decision | Resolution |
|----------|-----------|
| Cross-plugin MCP sharing | Primary: core owns connectors, add-ons share. Fallback: single-plugin with command packs. **Conditional until R1-R6 verified** -- `docs/runtime-compatibility.md` is a hard gate before repo structure is finalized (Section 2). |
| Runtime compatibility | Not yet verified. R1-R6 tests must be run and documented before any plugin code is written. Architecture is conditional until this is done. |
| MCP endpoint availability | Only Egnyte confirmed native MCP. All others are target integrations requiring wrappers (Section 8.1). Manual input is the primary data path for v1. |
| CoStar/Yardi dual role | Core plugin owns MCP connection. Partner plugins add specialized skills on top. No ownership ambiguity (Section 10). |
| Standards compliance claims | All downgraded to "assists with preparation." No submission-ready or audit-grade claims (Section 12). |
| Command overlap | Canonical skill ownership table assigns every analytical domain to a single skill (Section 6). All commands invoke named skills -- only `/close-readiness` is pure orchestration (justified: no reusable calc logic). |
| Output artifacts | Commands produce structured markdown, CSV, or template-filled Excel. Auditable Excel templates ship in the repo (Section 5). |
| Computational trust | LLM must never reason through precision-sensitive math (IRR, waterfall, amortization). Validated Python functions with unit tests are mandatory. LLM calls the code, does not replicate it (Section 5.4). |
| Debt persona scope | v1 is borrower-side only. Mortgage REIT / lender-side surveillance excluded (Section 3). |
| Data conflicts | Temporal alignment, freshness gates, disagreement handling, and "do not compute unless" rules (Section 8.4). |
| Cross-command state | Deal context directory with `_manifest.json` tracks all artifacts. Commands discover prior outputs via manifest, not filename guessing. Standardized naming conventions per command (Section 5.5). |
