# Docker Environment for E2E Testing

This Dockerfile creates a Linux-based environment for running and debugging Streamlit's end-to-end tests.

**Note:** Snapshot testing will yield different results on different machines. Therefore, this container is not suitable for getting consistent snapshot results. We should still rely on CI results for snapshot testing.

## Overview

The Docker build uses a `.dockerignore` file to exclude non-git tracked files such as `node_modules` directories and build artifacts.

## Dependencies

The container includes:

- Python 3.13
- Node.js (current LTS)
- Protocol Buffers compiler (`protoc`)
- All dependency setup from `make all-devel`

## Quick Start

### Building the Image

```bash
docker build -t streamlit-e2e-test -f ./e2e_playwright/Dockerfile .
```

### Running the Container

```bash
docker run -it --rm -p 8501:8501 streamlit-e2e-test
```

### Running E2E Tests

Once inside the container:

```bash
cd /e2e_playwright
pytest ./<file_name>.py
```

#### Tips:

- It is worthwhile to to run pytest with parallelism in order to get similar runtime characteristics as CI:
  ```bash
  pytest -n auto ./<file_name>.py
  ```

## Development Workflow

### Mounting Local Code

For faster development, mount your local code into the container:

```bash
docker run -it --rm -p 8501:8501 \
  -v $(pwd)/.git:/app/.git \
  -v $(pwd)/lib:/app/lib \
  -v $(pwd)/frontend/app/src:/app/frontend/app/src \
  -v $(pwd)/frontend/app/package.json:/app/frontend/app/package.json \
  -v $(pwd)/frontend/lib/src:/app/frontend/lib/src \
  -v $(pwd)/frontend/lib/package.json:/app/frontend/lib/package.json \
  -v $(pwd)/e2e_playwright:/app/e2e_playwright \
  -e GIT_DISCOVERY_ACROSS_FILESYSTEM=true \
  streamlit-e2e-test
```

> **Note:** Volume mounts bypass the `.dockerignore` file. The targeted approach above:
>
> - Mounts only necessary directories
> - Avoids dependency conflicts
> - Preserves the container's optimized environment
> - Improves performance
>
> You can customize directory mounts based on your needs.

### After Frontend Changes

If you modify frontend code, rebuild the frontend in the container before re-running your tests:

```bash
make frontend-build-with-profiler
```
