"""Run: python3 -m unittest discover tests"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "skills", "build", "scripts"))
from textstats import clean, count_contractions, measure  # noqa: E402


class TextStats(unittest.TestCase):
    def test_possessive_is_not_a_contraction(self):
        self.assertEqual(count_contractions("The paper's method. Anna's call."), 0)

    def test_real_contractions_count(self):
        self.assertEqual(count_contractions("It's fine, don't worry, we're close and I'm sure."), 4)

    def test_initials_and_abbreviations_do_not_split(self):
        _, c = measure("See e.g. the work of J. Smith on this. It is good. Dr. Who agrees.")
        self.assertEqual(c["sentences"], 3)

    def test_markup_and_sources_are_stripped(self):
        md = ("# Title\n\nOne real sentence here. Another one follows.\n\n| a | b |\n|---|---|\n\n"
              + "Filler prose sentence. " * 10 + "\n\n**Sources**\n\n- Smith, J. A paper. 2020.\n")
        text = clean(md)
        self.assertNotIn("Title", text)
        self.assertNotIn("Smith", text)
        self.assertNotIn("|", text)

    def test_fragment_bullets_dropped_sentence_bullets_kept(self):
        text = clean("- just a fragment\n- This one is a full sentence.\n")
        self.assertNotIn("fragment", text)
        self.assertIn("full sentence", text)


if __name__ == "__main__":
    unittest.main()
