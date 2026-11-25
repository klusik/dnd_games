"""Regression tests for campaign validation.

Author: Rudolf Klusal
"""

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from tools.validate import ROOT, validate


class CampaignValidationTests(unittest.TestCase):
    """Verify valid states and reject broken or cross-campaign event chains."""

    def test_current_repository(self):
        """Validate committed campaign data."""
        self.assertEqual(validate(ROOT), [])

    def test_reject_invalid_event(self):
        """An event from another campaign must fail validation."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            shutil.copytree(ROOT / "campaigns", root / "campaigns")
            path = root / "campaigns/dawnstar-rudolf/events/000000.json"
            data = json.loads(path.read_text(encoding="utf-8"))
            data["campaign_id"] = "dawnstar-agent"
            path.write_text(json.dumps(data), encoding="utf-8")
            self.assertTrue(any("invalid event chain" in e for e in validate(root)))

    def test_reject_missing_event(self):
        """A revision cannot exist without its corresponding event."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            shutil.copytree(ROOT / "campaigns", root / "campaigns")
            path = root / "campaigns/dawnstar-rudolf/events/000000.json"
            path.unlink()
            self.assertTrue(any("event count mismatch" in e for e in validate(root)))

    def test_reject_cross_campaign_module(self):
        """A referenced sheet must belong to its own campaign."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            shutil.copytree(ROOT / "campaigns", root / "campaigns")
            path = root / "campaigns/dawnstar-rudolf/characters/rudolf.json"
            data = json.loads(path.read_text(encoding="utf-8"))
            data["campaign_id"] = "dawnstar-agent"
            path.write_text(json.dumps(data), encoding="utf-8")
            self.assertTrue(any("invalid module identity" in e for e in validate(root)))

    def test_reject_missing_module(self):
        """Referenced inventory files must exist."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            shutil.copytree(ROOT / "campaigns", root / "campaigns")
            (root / "campaigns/dawnstar-rudolf/inventories/kara.json").unlink()
            self.assertTrue(any("cannot read module" in e for e in validate(root)))

    def test_reject_negative_inventory_quantity(self):
        """A quantity cannot become negative."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            shutil.copytree(ROOT / "campaigns", root / "campaigns")
            path = root / "campaigns/dawnstar-rudolf/inventories/rudolf.json"
            data = json.loads(path.read_text(encoding="utf-8"))
            data["items"][0]["quantity"] = -1
            path.write_text(json.dumps(data), encoding="utf-8")
            self.assertTrue(any("invalid inventory quantity" in e for e in validate(root)))

    def test_reject_unsafe_module_path(self):
        """Module references cannot escape their campaign."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            shutil.copytree(ROOT / "campaigns", root / "campaigns")
            path = root / "campaigns/dawnstar-rudolf/state.json"
            data = json.loads(path.read_text(encoding="utf-8"))
            data["character"]["sheet_ref"] = "../dawnstar-agent/state.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            self.assertTrue(any("unsafe module reference" in e for e in validate(root)))

