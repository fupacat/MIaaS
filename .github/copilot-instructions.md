# MIaaS Agent & Copilot Workflow Instructions

## Agent Execution Policy
- By default, agents (including Copilot) should immediately execute any user task or request if it is possible, unless the user explicitly asks for planning, review, or discussion only.
- If a task cannot be executed, the agent should explain why and suggest next steps.

## Board Columns & Issue States
- **Backlog**: Deferred work, ideas, or stories needing more context/enrichment.
- **Ready**: Issues/stories with all requirements and context, ready for execution.
- **In progress**: Actively being worked on.
- **In review**: Awaiting code/design review.
- **Done**: Completed and merged.

## Issue & Story Handling
- Only pick up issues/stories in **Ready** with "fully fleshed out" checked in the template.
- For items in **Backlog** with "needs more context," enrich by clarifying requirements, asking questions, or gathering missing details.
- After enrichment, update the issue/story, check "fully fleshed out," and move to **Ready**.
- When starting work, move the item to **In progress** and add progress comments.
- Upon completion, move to **In review** and request review.
- After approval, move to **Done** and close the issue/story.

## Labels & Automation
- Use labels like `needs-enrichment`, `ready-for-agent`, `priority:high/medium/low` to help agents prioritize and filter work.
- Agents should not execute on items in **Backlog** unless specifically tasked with enrichment.

## Branching Strategy
- Create a new branch for each issue/story (e.g., `feature/42-node-registration`, `bug/17-fix-heartbeat`).
- Branch names should reference the issue number for traceability.
- Branches are short-lived; merge to `main` after review and CI pass.
- No `develop` branch unless multiple contributors require it.
- Use `release/` and `hotfix/` branches for major milestones or urgent fixes.

## Pull Requests
- Open a PR from your feature branch to `main`.
- Reference related issues/stories in PR descriptions (`Closes #42`).
- Use the PR template checklist for review.
- CI/CD runs automatically; address any failed checks.
- Only merge after all reviews and checks are complete.
- Automatically close related issues via PR merge.

## Code Review & Merge
- Review code for correctness, completeness, and adherence to acceptance criteria.
- Discuss changes and request improvements as needed.
- Merge PRs only after approval and passing CI.

## Documentation
- Update `README.md`, Wiki, and GitHub Pages (`docs/`) as features are added or changed.
- Document major decisions and architecture in Discussions.

## Releases
- Tag releases for major milestones (`v1.0.0`, `v1.1.0`).
- Use the Releases tab to publish notes and attach artifacts.

## Dependency & Security
- Dependabot runs weekly for dependency updates and security alerts.
- Address alerts promptly.

## Acceptance Criteria & Verification
- Each story/feature includes clear, testable acceptance criteria.
- Criteria are used by reviewers and agents to verify PRs.
- Automated tests should map to acceptance criteria where possible.

## Complex Stories & Sub-Tasks
- For complex stories, break work into smaller issues/tasks.
- Link sub-tasks to the parent story using GitHub issue linking.
- Only mark the parent story as Done when all sub-tasks are completed and merged.

---

**Agents and Copilot should always follow this workflow for consistent collaboration and automation.**