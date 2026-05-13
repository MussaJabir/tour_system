# Tour System — Session Log

Running record of every working session. Most recent at the top.

---

## Session 001 — 2026-05-14

**Type:** Audit + Setup
**Branch:** `main` (housekeeping only, no features)

### What we did
1. **Full codebase audit** — analysed all 8 apps, models, views, serializers, templates, Docker config, and settings
2. **Removed `.cursor/` from git tracking** — `git rm --cached .cursor/worktrees.json`, added `.cursor/` to `.gitignore`, deleted the directory locally
3. **Created `CLAUDE.md`** — full project context file: stack, structure, conventions, known issues, development rules
4. **Created `todo.md`** — prioritized product roadmap across 5 phases
5. **Created `session.md`** — this file; tracks all working sessions
6. **Established branch workflow** — all future work goes on feature branches → PR into `develop` → user manually merges `develop` → `main`
7. **Created `develop` branch** on GitHub
8. **Pushed everything to GitHub**

### Key findings from audit
- Dashboard views use `@login_required` only — **security hole**, any logged-in user can access staff dashboard
- No token auth — Flutter mobile app cannot work with current DRF `SessionAuthentication` only
- `reviews` and `ai_assistant` apps are empty stubs but installed in `INSTALLED_APPS`
- Duplicate email config block in `settings.py`
- No booking/reservation system — inquiry-to-booking loop is not closed
- No login/logout views for the dashboard
- `packages/views.py` has bare `pass` exception handlers

### Decisions made
- Branch strategy: `feature/<name>` or `fix/<name>` → `develop` → `main`
- Tests must pass on the feature branch before PRing into `develop`
- User manually PRs `develop` → `main`
- All future sessions logged here with branch name and what was done

---

_Add new sessions above this line._
