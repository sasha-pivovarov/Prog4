import unittest
from homework_4.task_1 import search_rabin_multi

class test_search_rabin_multi(unittest.TestCase):

    def test_simple_pattern_search(self):
        res = search_rabin_multi("kdovtechplamenech", ["ovte"])
        self.assertTrue(res == [[2]])

    def test_multiple_hits(self):
        res = search_rabin_multi("ktovtehplamenehtotmistrjan", ["to"])
        self.assertTrue(res == [[1, 15]])

    def test_no_hits(self):
        res = search_rabin_multi("hranicevzpala", ["kalich"])
        self.assertTrue(res == [[]])

    def test_disjoint_alphabets(self):
        res = search_rabin_multi("avtechtojasnychpravdyplamenech", ["чаша"])
        self.assertTrue(res == [[]])

    def test_multi_pattern(self):
        res = search_rabin_multi("brante vlast a cechu slavu", ["bran", "chu"])
        self.assertTrue(res == [[0], [17]])

    def test_complex_case(self):
        res = search_rabin_multi("svoboda je svoboda", ["svo", "svoboda je svoboda", "da ", "табор"])
        self.assertTrue(res == [[0, 11], [0], [5], []])

if __name__ == "__main__":
    unittest.main()