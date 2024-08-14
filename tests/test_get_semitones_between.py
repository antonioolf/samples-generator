import unittest

from generate_notes import get_tones_between


class TestGetSemitonesBetween(unittest.TestCase):
    def test_semitones_between_ascending(self):
        self.assertEqual(
            get_tones_between("a_sharp_1", "f_2", ascending=True),
            ['b_1', 'c_2', 'c_sharp_2', 'd_2', 'd_sharp_2', 'e_2']
        )

    def test_semitones_between_descending(self):
        self.assertEqual(
            get_tones_between("a_sharp_1", "f_2", ascending=False),
            ['e_2', 'd_sharp_2', 'd_2', 'c_sharp_2', 'c_2', 'b_1']
        )

    def test_start_note_only(self):
        self.assertEqual(
            get_tones_between(start_note="a_sharp_3"),
            ['b_3', 'c_4', 'c_sharp_4', 'd_4', 'd_sharp_4', 'e_4', 'f_4', 'f_sharp_4', 'g_4', 'g_sharp_4', 'a_4',
             'a_sharp_4', 'b_4', 'c_5', 'c_sharp_5', 'd_5', 'd_sharp_5', 'e_5', 'f_5', 'f_sharp_5', 'g_5', 'g_sharp_5',
             'a_5', 'a_sharp_5', 'b_5', 'c_6', 'c_sharp_6', 'd_6', 'd_sharp_6', 'e_6', 'f_6', 'f_sharp_6', 'g_6',
             'g_sharp_6', 'a_6', 'a_sharp_6', 'b_6', 'c_7', 'c_sharp_7', 'd_7', 'd_sharp_7', 'e_7', 'f_7', 'f_sharp_7',
             'g_7', 'g_sharp_7', 'a_7', 'a_sharp_7', 'b_7', 'c_8', 'c_sharp_8', 'd_8', 'd_sharp_8', 'e_8', 'f_8',
             'f_sharp_8', 'g_8', 'g_sharp_8', 'a_8', 'a_sharp_8', 'b_8']
        )

    def test_end_note_only_descending(self):
        self.assertEqual(
            get_tones_between(end_note="c_2", ascending=False),
            ['b_1', 'a_sharp_1', 'a_1', 'g_sharp_1', 'g_1', 'f_sharp_1', 'f_1', 'e_1', 'd_sharp_1', 'd_1', 'c_sharp_1',
             'c_1']
        )

    def test_notes_not_exist(self):
        self.assertEqual(
            get_tones_between("a_sharp_10", "f_2"),
            "Uma ou ambas as notas fornecidas não existem no array all_tones."
        )
        self.assertEqual(
            get_tones_between("a_sharp_1", "f_20"),
            "Uma ou ambas as notas fornecidas não existem no array all_tones."
        )
