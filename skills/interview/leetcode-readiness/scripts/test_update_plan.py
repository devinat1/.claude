import unittest

from update_plan import END_MARKER, START_MARKER, merge_generated_section


class MergeGeneratedSectionTest(unittest.TestCase):
    def test_creates_titled_note_when_empty(self):
        self.assertEqual(
            merge_generated_section("", "## Current plan"),
            f"# LeetCode Weekly Plan\n\n{START_MARKER}\n## Current plan\n{END_MARKER}\n",
        )

    def test_replaces_only_generated_section(self):
        existing = (
            "# LeetCode Weekly Plan\n\n"
            "Manual note before.\n\n"
            f"{START_MARKER}\nold plan\n{END_MARKER}\n\n"
            "Manual note after.\n"
        )

        updated = merge_generated_section(existing, "## Current plan\nnew plan")

        self.assertEqual(
            updated,
            "# LeetCode Weekly Plan\n\n"
            "Manual note before.\n\n"
            f"{START_MARKER}\n## Current plan\nnew plan\n{END_MARKER}\n\n"
            "Manual note after.\n",
        )

    def test_appends_section_when_markers_are_absent(self):
        self.assertEqual(
            merge_generated_section("Manual note.\n", "## Current plan"),
            f"Manual note.\n\n{START_MARKER}\n## Current plan\n{END_MARKER}\n",
        )

    def test_rejects_malformed_or_duplicate_markers(self):
        invalid_notes = (
            f"{START_MARKER}\nmissing end\n",
            f"{START_MARKER}\none\n{END_MARKER}\n{START_MARKER}\ntwo\n{END_MARKER}\n",
        )

        for note in invalid_notes:
            with self.subTest(note=note):
                with self.assertRaises(ValueError):
                    merge_generated_section(note, "new plan")


if __name__ == "__main__":
    unittest.main()
