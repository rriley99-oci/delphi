# GitHub Actions Rules

## Workflow design

- Keep workflows focused: validate, test, build, and deploy as distinct concerns.
- Prefer reusable steps and shared setup where duplication becomes real.
- Make workflow names and job names obvious from the Actions UI.

## Reliability

- Fail fast on validation and test errors.
- Keep CI deterministic; avoid depending on ambient machine state.
- Pin important action versions intentionally.

## Security

- Use least-privilege permissions for each workflow.
- Store secrets in GitHub secrets, not in the repo or workflow text.
- Avoid printing sensitive values to logs.

## Build and test behavior

- Run the checks that matter for the changed stack: backend, frontend, infra.
- Keep feedback fast for pull requests.
- Split long-running deployment work from ordinary validation workflows.

## Delivery

- Prefer artifact or image promotion paths that are traceable back to a commit.
- Keep deploy workflows explicit about environment and target.
- Surface enough logs and summaries that failures can be diagnosed without guesswork.
