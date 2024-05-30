import unittest
from typing import List

from src.simple_nlp_library.preprocessing import (
    semantic_tokens,
    stop_words,
)


class TestPreprocessing(unittest.TestCase):
    stop_words: List[str]

    @classmethod
    def setUpClass(cls) -> None:
        cls.stop_words = stop_words()

    def test_stop_words(self) -> None:
        self.assertIn("by", stop_words())
        self.assertNotIn("computer", stop_words())

    def test_custom_stop_words(self) -> None:
        self.assertEqual(semantic_tokens(["computer"], "silicon-based computer"), ["silicon", "based"])

    def test_removing_hyphens(self) -> None:
        self.assertEqual(semantic_tokens(self.stop_words, "state-of-the-art model"), ["state", "art", "model"])

    def test_lower_letters(self) -> None:
        self.assertEqual(
            semantic_tokens(self.stop_words, "Quick brown fox jUMPs"),
            ["quick", "brown", "fox", "jumps"],
        )

    def test_single_spaces(self) -> None:
        self.assertEqual(
            semantic_tokens(self.stop_words, "quick \t brown \n fox jumps"),
            ["quick", "brown", "fox", "jumps"],
        )

    def test_removing_stop_words(self) -> None:
        self.assertEqual(
            semantic_tokens(self.stop_words, "the quick brown fox jumps over"),
            ["quick", "brown", "fox", "jumps"],
        )

    def test_removing_emails_and_links(self) -> None:
        self.assertEqual(
            semantic_tokens(self.stop_words, "quick brown fox jumps over @user https://domain.com"),
            ["quick", "brown", "fox", "jumps"],
        )

    def test_semantic_tokens(self) -> None:
        self.assertEqual(
            semantic_tokens(self.stop_words, "The 2 quick \t red-brown foxes jumps, over the lazy dog and @user"),
            ["2", "quick", "red", "brown", "foxes", "jumps", "lazy", "dog"],
        )

    def test_semantic_text(self) -> None:
        self.assertEqual(
            " ".join(
                semantic_tokens(
                    self.stop_words,
                    """
                    <br> <a href="https://google.com">Google It</a> to find an answer, 
                    this is state-of-the-art model,
                    email me quick_fox@gmail.com or visit my website Http://quick-fox.com https://quick-fox.com
                    Value of PI: 3.14 it is less than 4,
                    line<br>break
                    nice movie 9/10
                    """,
                )
            ),
            "google answer state art model email visit website value pi 314 4 line break nice movie 9 10",
        )
