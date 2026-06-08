# Docker Rules

## Development posture

- Treat Docker as a first-class local development environment, not just a deployment artifact.
- Keep local container workflows close to production shape without making them heavy.
- Favor one obvious way to run the app locally in containers.

## Image design

- Build small, focused images with explicit runtime dependencies.
- Use multi-stage builds when they materially reduce image size or separate build tooling from runtime.
- Keep images reproducible and deterministic.

## Security and configuration

- Do not bake secrets into images.
- Pass environment-specific configuration through environment variables or mounted config.
- Run processes as non-root where practical.

## Developer experience

- Optimize Dockerfiles for iterative development where it matters.
- Keep dependency install layers stable to improve rebuild speed.
- Make logs easy to read from container output.

## Runtime behavior

- One container should have one clear responsibility.
- Keep startup commands explicit and easy to override.
- Add healthcheck support when services become substantial enough to need it.

## Delivery alignment

- Keep image naming and tagging compatible with CI and Kubernetes deployment flows.
- Ensure local images behave similarly enough to deployed images that debugging translates.
