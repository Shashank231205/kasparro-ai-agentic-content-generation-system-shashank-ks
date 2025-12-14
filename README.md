## Configuration Management

This project intentionally separates configuration concerns:

- `.env`  
  Used for runtime configuration such as model selection, LLM parameters,
  feature flags, and execution behavior. Loaded via `python-dotenv`.

- `config.yaml`  
  Serves as a structured, human-readable reference for file paths and
  system layout. This improves clarity, auditability, and future extensibility.

At runtime, the `.env` configuration is the authoritative source.
The YAML file does not override environment variables and exists for
documentation and future configuration tooling support.
