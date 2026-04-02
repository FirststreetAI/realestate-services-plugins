"""
Deal context manifest system (spec Section 5.5).

Every multi-command workflow operates within a deal context directory that
contains a ``_manifest.json`` file.  Commands append to the manifest when they
produce output and read from it when they need prior outputs.

Standard deal directory subdirectories:
    inputs/  underwriting/  comps/  market/  pricing/  stress/  debt/  memo/
    diligence/  closing/  esg/  performance/  reporting/  operations/  leasing/
"""

import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

MANIFEST_FILENAME = "_manifest.json"

DEAL_SUBDIRECTORIES = [
    "inputs",
    "underwriting",
    "comps",
    "market",
    "pricing",
    "stress",
    "debt",
    "memo",
    "diligence",
    "closing",
    "esg",
    "performance",
    "reporting",
    "operations",
    "leasing",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _now_iso() -> str:
    """Return the current UTC time as an ISO-8601 string."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def find_manifest(start_path: str) -> Optional[str]:
    """Walk up directories from *start_path* looking for ``_manifest.json``.

    Parameters
    ----------
    start_path : str
        A file or directory path.  If it is a file the search begins in its
        parent directory.

    Returns
    -------
    str or None
        Absolute path to the manifest file, or ``None`` if not found before
        reaching the filesystem root.
    """
    current = os.path.abspath(start_path)
    if os.path.isfile(current):
        current = os.path.dirname(current)

    while True:
        candidate = os.path.join(current, MANIFEST_FILENAME)
        if os.path.isfile(candidate):
            return candidate
        parent = os.path.dirname(current)
        if parent == current:
            # Reached filesystem root
            return None
        current = parent


def create_manifest(
    deal_dir: str,
    deal_name: str,
    property_type: str,
) -> str:
    """Initialise a new ``_manifest.json`` inside *deal_dir*.

    Parameters
    ----------
    deal_dir : str
        Path to the deal context directory (must already exist).
    deal_name : str
        Human-readable deal name, e.g. ``"123 Main St, Dallas"``.
    property_type : str
        Property type slug, e.g. ``"industrial"``, ``"multifamily"``.

    Returns
    -------
    str
        Absolute path to the newly created manifest file.
    """
    manifest = {
        "deal_name": deal_name,
        "property_type": property_type,
        "created": _now_iso(),
        "artifacts": [],
    }
    path = os.path.join(os.path.abspath(deal_dir), MANIFEST_FILENAME)
    with open(path, "w") as fh:
        json.dump(manifest, fh, indent=2)
    return path


def read_manifest(manifest_path: str) -> Dict[str, Any]:
    """Read and parse a manifest file.

    Parameters
    ----------
    manifest_path : str
        Absolute or relative path to the manifest JSON file.

    Returns
    -------
    dict
        Parsed manifest dictionary.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    json.JSONDecodeError
        If the file is not valid JSON.
    """
    with open(manifest_path, "r") as fh:
        return json.load(fh)


def append_artifact(
    manifest_path: str,
    command: str,
    outputs: Dict[str, str],
    key_metrics: Dict[str, Any],
    consumes: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Append an artifact entry to an existing manifest.

    Parameters
    ----------
    manifest_path : str
        Path to ``_manifest.json``.
    command : str
        Slash-command name, e.g. ``"/underwrite-asset"``.
    outputs : dict
        Mapping of output label to relative file path.
    key_metrics : dict
        Scalar values that downstream commands commonly need.
    consumes : list of str, optional
        Relative paths to files this command consumed.

    Returns
    -------
    dict
        The artifact entry that was appended.
    """
    manifest = read_manifest(manifest_path)
    artifact = {
        "command": command,
        "produced_at": _now_iso(),
        "consumes": consumes or [],
        "outputs": outputs,
        "key_metrics": key_metrics,
    }
    manifest["artifacts"].append(artifact)
    with open(manifest_path, "w") as fh:
        json.dump(manifest, fh, indent=2)
    return artifact


def find_artifact(
    manifest: Dict[str, Any],
    command: str,
) -> Optional[Dict[str, Any]]:
    """Return the most recent artifact produced by *command*.

    Parameters
    ----------
    manifest : dict
        A parsed manifest (as returned by :func:`read_manifest`).
    command : str
        The slash-command name to search for.

    Returns
    -------
    dict or None
        The most recent matching artifact, or ``None``.
    """
    matches = [a for a in manifest.get("artifacts", []) if a["command"] == command]
    if not matches:
        return None
    # Last entry is most recent (append-only log)
    return matches[-1]


def get_key_metric(
    manifest: Dict[str, Any],
    command: str,
    metric_name: str,
) -> Optional[Any]:
    """Retrieve a single key metric from the most recent artifact of *command*.

    Parameters
    ----------
    manifest : dict
        A parsed manifest.
    command : str
        The slash-command name whose metrics to inspect.
    metric_name : str
        The key inside ``key_metrics`` to return.

    Returns
    -------
    Any or None
        The metric value, or ``None`` if the command or metric is not found.
    """
    artifact = find_artifact(manifest, command)
    if artifact is None:
        return None
    return artifact.get("key_metrics", {}).get(metric_name)


def ensure_deal_directory(base_path: str, deal_name: str) -> str:
    """Create the standardised deal directory structure.

    Converts *deal_name* to a filesystem-safe slug (lowercase, hyphens) and
    creates the directory along with all standard subdirectories.

    Parameters
    ----------
    base_path : str
        Parent directory under which the deal folder is created.
    deal_name : str
        Human-readable deal name.

    Returns
    -------
    str
        Absolute path to the deal directory.
    """
    slug = deal_name.lower().strip()
    # Replace commas, spaces, and other non-alphanumeric chars with hyphens
    slug = "".join(c if c.isalnum() else "-" for c in slug)
    # Collapse multiple hyphens and strip leading/trailing ones
    while "--" in slug:
        slug = slug.replace("--", "-")
    slug = slug.strip("-")

    deal_dir = os.path.join(os.path.abspath(base_path), slug)
    os.makedirs(deal_dir, exist_ok=True)
    for subdir in DEAL_SUBDIRECTORIES:
        os.makedirs(os.path.join(deal_dir, subdir), exist_ok=True)
    return deal_dir
