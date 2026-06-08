# Kubernetes Rules

## Deployment philosophy

- Start simple and Kubernetes-native.
- Use the minimum set of objects needed for the current phase.
- Keep manifests understandable by humans who need to operate them.

## Workload design

- Use `Deployment` for long-running stateless services.
- Use `Job` for on-demand evaluation execution when the work is bounded.
- Use `CronJob` only when scheduled evaluations are introduced.
- Keep worker behavior and API behavior separated when lifecycle needs differ.

## Configuration

- Put non-secret configuration in `ConfigMap`.
- Put credentials and sensitive connection details in `Secret`.
- Keep image tags explicit and deployable.

## Reliability

- Add readiness and liveness checks once services do real work.
- Set resource requests and limits deliberately.
- Design for safe restarts and idempotent job behavior.

## Networking and security

- Expose only what needs to be reachable.
- Keep service boundaries explicit.
- Avoid baking credentials or environment-specific details into images or manifests.

## Operability

- Make logs and metrics available from every service.
- Keep manifests consistent across services.
- Favor one namespace for the POC until multi-environment needs are real.
