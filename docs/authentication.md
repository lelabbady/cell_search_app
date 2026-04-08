# Authentication

## Token source

Cell Search uses CAVE authentication for lookups and neuroglancer workflows.

In embedded mode, auth is typically supplied through Flask request context by the host app.
In standalone mode, set CAVE_TOKEN in your shell environment.

```bash
export CAVE_TOKEN=<your-token>
```

## Common checks

1. Confirm token is set in the same shell where the app starts.
2. Confirm datastack and server address are valid for your environment.
3. Confirm the host app sets flask.g.auth_token when running in embedded mode.

## Troubleshooting symptom

If lookups fail with auth errors, verify token validity and runtime context before checking app code.
