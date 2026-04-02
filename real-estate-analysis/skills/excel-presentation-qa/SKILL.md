---
description: Model audit rules, formula tracing, hardcode detection, and slide QA for real estate deliverables
---

# Excel and Presentation QA

Quality assurance skill for auditing financial models and presentation decks. Invoked after model generation or when a user asks to review an existing model.

## Trigger Conditions

Activated when:
- A command has generated an Excel model and needs QA before delivery
- User asks to audit or debug an existing model
- User asks to review a presentation for consistency

## Business Context

Financial models in real estate are high-stakes deliverables. A formula error in an IC memo model or a number mismatch between a slide deck and the underlying model can destroy credibility and lead to bad investment decisions.

## Model Audit Checklist

### Structure
- [ ] Assumptions are separated from calculations (dedicated assumptions tab/section)
- [ ] No hardcoded numbers in formula cells (except true constants like 12 months/year)
- [ ] Consistent time periods across all tabs (same column = same year)
- [ ] Clear flow: Assumptions → Revenue → Expenses → NOI → Cash Flow → Returns

### Formulas
- [ ] No circular references
- [ ] All formulas reference assumptions cells, not hardcoded values
- [ ] Growth rates applied consistently (not manually typed per year)
- [ ] IRR/NPV calculated by validated code, not Excel formulas (for institutional models)
- [ ] Sum checks: totals match sum of components

### Data Integrity
- [ ] Rent roll total ties to revenue projection year 1 (within 2%)
- [ ] T-12 total ties to expense projection year 1 (within 2%)
- [ ] Debt service ties to stated loan terms
- [ ] Exit value ties to stated exit cap rate and terminal NOI

### Sources & Assumptions
- [ ] Sources & Assumptions tab exists and is populated
- [ ] Every assumption has a source or is labeled "management estimate"
- [ ] As-of dates documented for all data inputs

### Presentation Consistency (if reviewing slides)
- [ ] Numbers on slides match the underlying model
- [ ] Cap rates, IRRs, and multiples are consistently rounded
- [ ] Property name, address, and size are consistent throughout
- [ ] Charts/tables reference the same data period

## Common Errors to Flag

1. **Vacancy applied twice** (at rent roll level and again at revenue level)
2. **Expense growth but not revenue growth** (or vice versa, without explanation)
3. **Exit cap rate < going-in cap rate** without stated appreciation thesis
4. **Missing capital reserves** (common in seller pro formas)
5. **Debt service during IO period uses amortizing payment** (or vice versa)
6. **Year 1 NOI used for exit valuation** instead of forward/terminal NOI
7. **Lease commission on existing leases** that aren't rolling

## Output

- List of issues found, categorized by severity (Error / Warning / Note)
- For each issue: location (tab/cell reference or section), description, suggested fix
- Overall assessment: Clean / Minor issues / Material errors found
