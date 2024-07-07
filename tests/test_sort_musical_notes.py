import unittest

from main import sort_musical_notes


class TestSortMusicalNotes(unittest.TestCase):

    def test_basic_order(self):
        notes = ['c_1', 'd_1', 'e_1', 'f_1', 'g_1', 'a_1', 'b_1']
        expected = ['c_1', 'd_1', 'e_1', 'f_1', 'g_1', 'a_1', 'b_1']
        self.assertEqual(sort_musical_notes(notes), expected)

    def test_mixed_order(self):
        notes = ['d_1', 'c_1', 'b_1', 'a_1', 'g_1', 'f_1', 'e_1']
        expected = ['c_1', 'd_1', 'e_1', 'f_1', 'g_1', 'a_1', 'b_1']
        self.assertEqual(sort_musical_notes(notes), expected)

    def test_different_octaves(self):
        notes = ['c_2', 'c_1', 'c_3']
        expected = ['c_1', 'c_2', 'c_3']
        self.assertEqual(sort_musical_notes(notes), expected)

    def test_sharps(self):
        notes = ['c_1', 'c_sharp_1', 'd_1', 'd_sharp_1']
        expected = ['c_1', 'c_sharp_1', 'd_1', 'd_sharp_1']
        self.assertEqual(sort_musical_notes(notes), expected)

    def test_mixed_sharps(self):
        notes = ['d_sharp_1', 'c_sharp_1', 'd_1', 'c_1']
        expected = ['c_1', 'c_sharp_1', 'd_1', 'd_sharp_1']
        self.assertEqual(sort_musical_notes(notes), expected)

    def test_complex_case(self):
        notes = ['c_1', 'd_sharp_2', 'e_1', 'f_2', 'a_3', 'c_sharp_1', 'g_sharp_2', 'b_3', 'a_sharp_2']
        expected = ['c_1', 'c_sharp_1', 'e_1', 'd_sharp_2', 'f_2', 'g_sharp_2', 'a_sharp_2', 'a_3', 'b_3']
        self.assertEqual(sort_musical_notes(notes), expected)
