"""Startup configuration checks for ADA entry points."""

from __future__ import annotations

import os
from collections.abc import Mapping, Sequence

from dotenv import load_dotenv


class MissingEnvironmentVariables(RuntimeError):
    """Raised when an ADA mode is missing required environment variables."""


def require_environment_variables(
    names: Sequence[str],
    environ: Mapping[str, str] | None = None,
) -> dict[str, str]:
    """Return required values or raise one actionable startup error.

    Values containing only whitespace are treated as missing. Passing ``environ``
    keeps this helper deterministic and easy to test without mutating process state.
    """

    source = os.environ if environ is None else environ
    values = {name: source.get(name, "").strip() for name in names}
    missing = [name for name, value in values.items() if not value]

    if missing:
        joined = ", ".join(missing)
        raise MissingEnvironmentVariables(
            f"Missing required environment variable(s): {joined}. "
            "Add them to your environment or the repository's .env file before starting ADA."
        )

    return values


def load_and_require(names: Sequence[str]) -> dict[str, str]:
    """Load a local .env file, then validate the requested variables."""

    load_dotenv()
    return require_environment_variables(names)
