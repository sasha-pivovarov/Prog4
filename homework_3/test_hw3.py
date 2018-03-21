import unittest
from homework_3.hw3 import TextStatistics

class test_TextStatistics(unittest.TestCase):
    def empty_articles(self):
        stats = TextStatistics([])
        self.assertListEqual(stats.get_top_words(5), [])

    def more_words_requested_than_present(self):
        stats = TextStatistics(["bluh bluh bluh bluh blah", "blah blah blah"])
        self.assertTrue(len(stats.get_top_words(50)) == 2)

    def normal_operation_wo_idf(self):
        stats = TextStatistics(["bluh bluh bluh bluh blah", "blah blah blah blah"])
        expected_res = (["blah", "bluh"], [5, 4])
        self.assertTupleEqual(stats.get_top_words(2, False), expected_res)

    def normal_operation_with_idf(self):
        stats = TextStatistics(["bluh bluh bluh bluh blah", "blah blah blah blah"])
        expected_res = (["blah", "bluh"], [2.5, 4])
        self.assertTupleEqual(stats.get_top_words(2, False), expected_res)

    def normal_operation_trigrams_wo_idf(self):
        stats = TextStatistics(["blu", "bluh"])
        expected_res = (["blu", "luh"], [2, 1])
        self.assertTupleEqual(stats.get_top_3grams(2, False), expected_res)


if __name__ == "__main__":
    unittest.main()