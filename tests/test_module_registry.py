"""Tests for the canonical module inventory."""
from sovereign_master.core.module_registry import module_inventory, module_states


def test_inventory_places_all_major_engine_areas():
    states = module_states()
    for name in ("core", "providers", "memory", "secrets", "security", "knowledge", "research", "media", "voice", "jobs", "admin", "api"):
        assert name in states
    assert states["secrets"] == "opt_in"
    assert states["location"] == "preview"


def test_inventory_is_serializable():
    assert all(set(item) == {"name", "state", "location", "description"} for item in module_inventory())
