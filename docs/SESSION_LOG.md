## 2026-06-02 14:26 UTC

**What was done**:
- Evaluated session changes and bumped version 0.3.0 → 0.3.1 (patch: CSRF fix, base_context fix)
- Ran full release pipeline: tag v0.3.1, PR dev→main, merge, tag and push
- Added auto-release GitHub Actions workflow (triggered by v* tags, mirrors pinsheet-server pattern)
- Wrote comprehensive README.md based on cartographer plugin's format
- Set up memory framework (HANDOFF.md, SESSION_LOG.md, DECISIONS.md)

**Files touched**:
- `__init__.py` — version bump 0.3.0 → 0.3.1
- `.github/workflows/release.yml` — new auto-release workflow
- `README.md` — new comprehensive readme
- `docs/HANDOFF.md` — new memory framework
- `docs/SESSION_LOG.md` — new memory framework

**Next**: See HANDOFF.md next actions
