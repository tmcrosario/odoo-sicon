# Migration Notes — odoo-sicon (14.0 → 19.0)

Module: `sicon` (Sistema de Concesiones Generales). Branch `19.0` created fresh from
`14.0` (no prior 18.0/19.0 branch; working tree was clean, no stash needed).

## Summary of changes by category

### Models / wizards

- No ORM API deprecations found (no `name_get`, `fields_view_get`, `xmlid_to_res_id`,
  `view_type`, `_translate`, `read_group`, `_cr/_uid/_context`, single-record `create`,
  `@api.one/multi`).
- `_sql_constraints` in `zone.py`, `grantor.py`, `administrator.py`, `event_type.py`
  left as-is (still valid in 19.0; style-only conversion intentionally skipped).
- **Removed dangling `_inherit = ["tmc.report"]`** from `models/concession.py` and
  `wizards/concession_report.py`. `tmc.report` was a py3o report mixin provided by
  `tmc_data_py3o`, which was deleted from this codebase — a dangling `_inherit` to a
  missing model is a hard install failure. See "Items left for human review".

### Views

- `<tree>` → `<list>` in 8 view/report files; `view_mode` `tree`/`tree,form` →
  `list`/`list,form` (9 occurrences). Existing `*_view_tree` record xmlids were kept (no
  cosmetic renames).
- Converted all 28 `attrs="{...}"` to direct `invisible`/`readonly`/`required`
  expressions across `concession_views.xml` (21), `wizards/add_event_views.xml` (5),
  `partner_views.xml` (1), `event_views.xml` (1). All `attrs` were in form views, so
  `invisible` (not `column_invisible`) is correct.

### Reports (py3o — STUBBED, per migration decision)

- `report/concession.xml` and `report/concessions_list.xml` defined `ir.actions.report`
  with `report_type="py3o"` referencing `tmc_data_py3o.local_server`. Since
  `tmc_data_py3o` was removed and the py3o engine has no confirmed 19.0 release, **both
  report records are commented out** (the module installs cleanly). A
  `TODO(19.0 migration)` explains how to reinstate (QWeb or restored py3o). The `.odt`
  templates (`report/concession_details.odt`, `report/concessions_list.odt`) are kept on
  disk.

### Security

- `security/groups.xml`: migrated from the removed-in-19.0 `category_id`-on-`res.groups`
  pattern to the **19.0 `res.groups.privilege` pattern** (matching the already-migrated
  `tmc`/`me` modules): added a `res.groups.privilege` record
  (`res_groups_privilege_sicon`, `category_id` → the `ir.module.category`), and the
  three `res.groups` now reference it via `privilege_id`. `implied_ids` and `users`
  retained.

### Tests

- `tests/test_zone.py` is a plain `TransactionCase` with no removed
  `at_install`/`post_install` decorators — left unchanged.

### Manifest

- `version` `14.0.1.0.0` → `19.0.1.0.0`; removed dead `"qweb": []`; license `AGPL-3`
  (unchanged).
- **Removed `tmc_data_py3o` from `depends`** (with a `TODO(19.0 migration)` comment).
  Remaining deps: `tmc`, `tmc_data`, `document_pdf`, `partner_tmc`, `partner_fiscal`.
  Data load order unchanged (the stubbed report XML still load as empty files).

## 18.0 branch

- None existed. Branch `19.0` created from `14.0`.

## Removed dependencies

- **`tmc_data_py3o`** — deleted from this codebase during the tmc-data 19.0 migration;
  the py3o report engine has no confirmed 19.0 release.
  `# TODO(19.0 migration): restore (or reimplement reports as QWeb) when available.`

## Dependencies to verify before push

- `partner_firstname`, `base_address_extended` (pulled transitively via `partner_tmc`) —
  verify 19.0 availability (see odoo-partner notes).
- `tmc`, `tmc_data`, `document_pdf`, `partner_tmc`, `partner_fiscal` — internal; confirm
  installable at 19.0.

## attrs conversions to review (compound domains)

- `add_event_views.xml`:
  `[('modify_concession','=',False),('concessionaire_id','!=',False)]` →
  `invisible="not modify_concession and concessionaire_id"` (implicit AND of two
  tuples).
- `add_event_views.xml`: `[('state','not in',['awarded','on_term'])]` →
  `invisible="state not in ['awarded', 'on_term']"`.
- `concession_views.xml` (term/extension blocks), the OR-chains:
  - `['|','|',('term_certain_expiration','=',False),('term_expiration','=','uncertain'),('term_certain_expiration','=','date')]`
    →
    `invisible="not term_certain_expiration or term_expiration == 'uncertain' or term_certain_expiration == 'date'"`
    (x2 — fields + label).
  - `['|','|',(...,'=',False),('term_expiration','=','uncertain'),('term_certain_expiration','in',(False,'duration'))]`
    →
    `invisible="not term_certain_expiration or term_expiration == 'uncertain' or term_certain_expiration in [False, 'duration']"`.
  - The analogous three `extension_*` OR-chains → same pattern with `extension_*`
    fields.
  - `('term_expiration','in',(False,'uncertain'))` →
    `term_expiration in [False, 'uncertain']`;
    `('extension_expiration','in',(False,'uncertain'))` →
    `extension_expiration in [False, 'uncertain']`. Please spot-check these OR/`in`
    conversions visually.

## Autosave / onchange → constrains conversions

- None required (no `@api.onchange` raising `UserError`/`ValidationError`).

## Items left for human review

1. **`tmc.report` mixin removed** — `concession.py` and `concession_report.py` no longer
   inherit it. `concession.py` had no other reference to it, so the model is unaffected
   at install. BUT the wizard button `check_and_generate_report` (in
   `concession_report_views.xml`) calls `self.generate_report()`, which came from that
   mixin and is now **undefined** → the button will raise at runtime until report
   generation is reimplemented. Both the py3o reports it fed are stubbed. Also verify no
   sicon **view/field** depended on fields the `tmc.report` mixin may have provided.
2. **py3o reports** (`report/concession.xml`, `report/concessions_list.xml`) — stubbed;
   reinstate as QWeb or restored py3o at validation.
3. `res.groups` `users` field on `group_*` records was kept as-is (the 19.0 rename
   affected `groups_id`→`group_ids` on the user side, not the `users` field on
   `res.groups`); confirm at boot.

## Lint findings

- Captured in the `[ADD]` tooling commit. Non-blocking reporters only.

## Translations

- Translation regeneration deferred to a later stage.
