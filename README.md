# Git PR Playground — Python Task Tracker

A small working Python CLI project built for practicing **forks, branches, commits, signed commits, pull requests, code reviews, and merges** using two GitHub accounts.

No external Python packages are required. Python 3.10+ recommended.

## Run it

```bash
python taskboard.py add "Practice GitHub PRs"
python taskboard.py add "Learn signed commits"
python taskboard.py list
python taskboard.py done 1
python taskboard.py list
```

Your tasks are saved to `tasks.json`, which is ignored by Git so your private tasks do not get committed.

## Run tests

```bash
python -m unittest discover -s tests -v
```

GitHub Actions runs the same tests on pushes and pull requests.

## Contributor assignments

Start with **PR #1** and leave `main` unchanged until the owner reviews and merges it.

### PR #1: Add task deletion (recommended first PR)

1. Create branch `feature/delete-task` in the fork owned by Account 2.
2. In `taskboard.py`, implement `delete_task(task_id, data_file=DEFAULT_DATA_FILE)`.
3. Make it remove only the matching task. Keep `next_id` intact so IDs are not reused.
4. Raise `ValueError(f"Task #{task_id} not found")` when there is no match.
5. Add a `delete` subcommand to `main()` with one integer ID argument.
6. Add tests verifying successful deletion and the missing-ID error.
7. Commit, push, open PR against Account 1's `main` branch, and request review.

**Expected result after your PR:**

```bash
python taskboard.py add "Temporary"
python taskboard.py delete 1
python taskboard.py list
# No tasks yet ... or an empty list
```

### PR #2: Search tasks

On a new branch, add a `search` command that finds tasks whose title contains a query (case insensitive) and write tests for it.

### PR #3: Practice review feedback

Account 1 requests a change on PR #2. Account 2 pushes another signed commit to the **same** branch; the PR updates automatically. Account 1 approves and merges it.

## Workflow overview

- **Account 1:** Original public repository (`upstream`), reviews and merges.
- **Account 2:** Forks Account 1's repository, creates branches, makes commits and PRs.
- **GitHub Desktop:** Clone fork, create branch, view diff, commit, push.
- **GitHub website:** Open PR, review, approve, merge.
- **Git terminal:** Optional alternative for clone/branch/commit/push.

See `CONTRIBUTING.md` and the included pull request template for the checklist.
