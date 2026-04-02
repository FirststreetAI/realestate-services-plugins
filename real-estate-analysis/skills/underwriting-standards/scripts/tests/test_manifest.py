"""
Unit tests for the deal context manifest system (manifest.py).
"""

import json
import os
import sys
import tempfile

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from manifest import (
    DEAL_SUBDIRECTORIES,
    MANIFEST_FILENAME,
    append_artifact,
    create_manifest,
    ensure_deal_directory,
    find_artifact,
    find_manifest,
    get_key_metric,
    read_manifest,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def deal_dir(tmp_path):
    """Create a minimal deal directory with a manifest."""
    d = tmp_path / "deals" / "test-deal"
    d.mkdir(parents=True)
    return str(d)


@pytest.fixture
def manifest_path(deal_dir):
    """Return the path to a freshly-created manifest."""
    return create_manifest(deal_dir, "Test Deal", "industrial")


# ---------------------------------------------------------------------------
# create_manifest / read_manifest
# ---------------------------------------------------------------------------

class TestCreateAndRead:
    def test_create_manifest_creates_file(self, deal_dir):
        path = create_manifest(deal_dir, "123 Main St, Dallas", "industrial")
        assert os.path.isfile(path)
        assert path.endswith(MANIFEST_FILENAME)

    def test_manifest_has_required_fields(self, deal_dir):
        path = create_manifest(deal_dir, "123 Main St, Dallas", "industrial")
        data = read_manifest(path)
        assert data["deal_name"] == "123 Main St, Dallas"
        assert data["property_type"] == "industrial"
        assert "created" in data
        assert data["artifacts"] == []

    def test_read_manifest_roundtrip(self, manifest_path):
        data = read_manifest(manifest_path)
        assert data["deal_name"] == "Test Deal"
        assert isinstance(data["artifacts"], list)

    def test_read_manifest_file_not_found(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            read_manifest(str(tmp_path / "nonexistent.json"))

    def test_read_manifest_invalid_json(self, tmp_path):
        bad = tmp_path / MANIFEST_FILENAME
        bad.write_text("not json {{{")
        with pytest.raises(json.JSONDecodeError):
            read_manifest(str(bad))


# ---------------------------------------------------------------------------
# append_artifact
# ---------------------------------------------------------------------------

class TestAppendArtifact:
    def test_append_single_artifact(self, manifest_path):
        artifact = append_artifact(
            manifest_path,
            command="/underwrite-asset",
            outputs={"proforma": "underwriting/proforma.xlsx"},
            key_metrics={"stabilized_noi": 2_850_000},
            consumes=["inputs/rent-roll.xlsx"],
        )
        assert artifact["command"] == "/underwrite-asset"
        assert "produced_at" in artifact
        assert artifact["outputs"]["proforma"] == "underwriting/proforma.xlsx"
        assert artifact["key_metrics"]["stabilized_noi"] == 2_850_000
        assert artifact["consumes"] == ["inputs/rent-roll.xlsx"]

        data = read_manifest(manifest_path)
        assert len(data["artifacts"]) == 1

    def test_append_multiple_artifacts(self, manifest_path):
        append_artifact(
            manifest_path,
            command="/underwrite-asset",
            outputs={"proforma": "underwriting/proforma.xlsx"},
            key_metrics={"stabilized_noi": 2_000_000},
        )
        append_artifact(
            manifest_path,
            command="/price-deal",
            outputs={"pricing": "pricing/pricing-summary.xlsx"},
            key_metrics={"target_price": 40_000_000},
        )
        data = read_manifest(manifest_path)
        assert len(data["artifacts"]) == 2
        assert data["artifacts"][0]["command"] == "/underwrite-asset"
        assert data["artifacts"][1]["command"] == "/price-deal"

    def test_append_defaults_consumes_to_empty(self, manifest_path):
        artifact = append_artifact(
            manifest_path,
            command="/comp-analysis",
            outputs={"comps": "comps/set.xlsx"},
            key_metrics={"avg_cap_rate": 0.055},
        )
        assert artifact["consumes"] == []


# ---------------------------------------------------------------------------
# find_artifact
# ---------------------------------------------------------------------------

class TestFindArtifact:
    def test_find_existing_artifact(self, manifest_path):
        append_artifact(
            manifest_path,
            command="/underwrite-asset",
            outputs={"proforma": "underwriting/proforma.xlsx"},
            key_metrics={"stabilized_noi": 2_850_000},
        )
        manifest = read_manifest(manifest_path)
        result = find_artifact(manifest, "/underwrite-asset")
        assert result is not None
        assert result["command"] == "/underwrite-asset"

    def test_find_nonexistent_artifact(self, manifest_path):
        manifest = read_manifest(manifest_path)
        assert find_artifact(manifest, "/does-not-exist") is None

    def test_find_returns_most_recent(self, manifest_path):
        append_artifact(
            manifest_path,
            command="/underwrite-asset",
            outputs={"proforma": "underwriting/proforma-v1.xlsx"},
            key_metrics={"stabilized_noi": 2_000_000},
        )
        append_artifact(
            manifest_path,
            command="/underwrite-asset",
            outputs={"proforma": "underwriting/proforma-v2.xlsx"},
            key_metrics={"stabilized_noi": 2_850_000},
        )
        manifest = read_manifest(manifest_path)
        result = find_artifact(manifest, "/underwrite-asset")
        assert result["outputs"]["proforma"] == "underwriting/proforma-v2.xlsx"
        assert result["key_metrics"]["stabilized_noi"] == 2_850_000

    def test_find_artifact_empty_manifest(self):
        manifest = {"deal_name": "x", "property_type": "office", "artifacts": []}
        assert find_artifact(manifest, "/underwrite-asset") is None


# ---------------------------------------------------------------------------
# get_key_metric
# ---------------------------------------------------------------------------

class TestGetKeyMetric:
    def test_get_existing_metric(self, manifest_path):
        append_artifact(
            manifest_path,
            command="/underwrite-asset",
            outputs={"proforma": "underwriting/proforma.xlsx"},
            key_metrics={"stabilized_noi": 2_850_000, "cap_rate": 0.055},
        )
        manifest = read_manifest(manifest_path)
        assert get_key_metric(manifest, "/underwrite-asset", "stabilized_noi") == 2_850_000
        assert get_key_metric(manifest, "/underwrite-asset", "cap_rate") == 0.055

    def test_get_metric_missing_command(self, manifest_path):
        manifest = read_manifest(manifest_path)
        assert get_key_metric(manifest, "/no-such-command", "foo") is None

    def test_get_metric_missing_key(self, manifest_path):
        append_artifact(
            manifest_path,
            command="/underwrite-asset",
            outputs={},
            key_metrics={"stabilized_noi": 2_850_000},
        )
        manifest = read_manifest(manifest_path)
        assert get_key_metric(manifest, "/underwrite-asset", "nonexistent") is None

    def test_get_metric_from_most_recent(self, manifest_path):
        """When a command has been run twice, metric comes from the latest."""
        append_artifact(
            manifest_path,
            command="/underwrite-asset",
            outputs={},
            key_metrics={"stabilized_noi": 1_000_000},
        )
        append_artifact(
            manifest_path,
            command="/underwrite-asset",
            outputs={},
            key_metrics={"stabilized_noi": 2_850_000},
        )
        manifest = read_manifest(manifest_path)
        assert get_key_metric(manifest, "/underwrite-asset", "stabilized_noi") == 2_850_000


# ---------------------------------------------------------------------------
# find_manifest (directory walk)
# ---------------------------------------------------------------------------

class TestFindManifest:
    def test_find_in_current_directory(self, manifest_path):
        deal_dir = os.path.dirname(manifest_path)
        assert find_manifest(deal_dir) == manifest_path

    def test_find_from_subdirectory(self, manifest_path):
        deal_dir = os.path.dirname(manifest_path)
        subdir = os.path.join(deal_dir, "underwriting")
        os.makedirs(subdir, exist_ok=True)
        assert find_manifest(subdir) == manifest_path

    def test_find_from_deeply_nested_subdirectory(self, manifest_path):
        deal_dir = os.path.dirname(manifest_path)
        deep = os.path.join(deal_dir, "underwriting", "drafts", "v2")
        os.makedirs(deep, exist_ok=True)
        assert find_manifest(deep) == manifest_path

    def test_find_from_file_path(self, manifest_path):
        deal_dir = os.path.dirname(manifest_path)
        subdir = os.path.join(deal_dir, "inputs")
        os.makedirs(subdir, exist_ok=True)
        dummy_file = os.path.join(subdir, "rent-roll.xlsx")
        with open(dummy_file, "w") as f:
            f.write("")
        assert find_manifest(dummy_file) == manifest_path

    def test_find_returns_none_when_missing(self, tmp_path):
        empty_dir = tmp_path / "no-manifest-here"
        empty_dir.mkdir()
        assert find_manifest(str(empty_dir)) is None


# ---------------------------------------------------------------------------
# ensure_deal_directory
# ---------------------------------------------------------------------------

class TestEnsureDealDirectory:
    def test_creates_directory_with_subdirs(self, tmp_path):
        deal_dir = ensure_deal_directory(str(tmp_path), "123 Main St, Dallas")
        assert os.path.isdir(deal_dir)
        for subdir in DEAL_SUBDIRECTORIES:
            assert os.path.isdir(os.path.join(deal_dir, subdir))

    def test_slug_format(self, tmp_path):
        deal_dir = ensure_deal_directory(str(tmp_path), "123 Main St, Dallas")
        slug = os.path.basename(deal_dir)
        assert slug == "123-main-st-dallas"

    def test_idempotent(self, tmp_path):
        """Calling twice with same name should not raise."""
        d1 = ensure_deal_directory(str(tmp_path), "Test Deal")
        d2 = ensure_deal_directory(str(tmp_path), "Test Deal")
        assert d1 == d2

    def test_special_characters(self, tmp_path):
        deal_dir = ensure_deal_directory(str(tmp_path), "Unit #5 @ 100 Broadway!")
        slug = os.path.basename(deal_dir)
        # No special chars remain, only lowercase alphanumerics and hyphens
        assert all(c.isalnum() or c == "-" for c in slug)
        assert "--" not in slug
        assert not slug.startswith("-")
        assert not slug.endswith("-")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
