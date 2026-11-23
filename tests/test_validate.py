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
