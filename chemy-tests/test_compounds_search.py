import json
import unittest
from unittest.mock import patch, call

from chemy import create_app

TEST_COMPOUND = {"ions": ['ion1', 'ion2']}


class CompoundsApiTest(unittest.TestCase):
    def setUp(self):

        app = create_app()
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_invalid_json(self):
        rv = self.app.post('/compounds', data='')
        self.assertEqual(rv.status_code, 400)
        self.assertIn(b'Unable to parse input data', rv.data)

    def test_not_list(self):
        rv = self.app.post('/compounds', json={"a": "b"})
        self.assertEqual(rv.status_code, 400)
        self.assertIn(b'Give me a list', rv.data)

    @patch('chemy.compounds.get_compounds_with_ion',
           return_value=[TEST_COMPOUND])
    def test_search_by_one_ion(self, p_one):
        rv = self.app.post('/compounds', json=["ion1"])
        json_data = json.loads(rv.get_data())
        p_one.assert_called()
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(json_data, [TEST_COMPOUND])

    @patch('chemy.compounds.get_matched_compounds',
           return_value=[TEST_COMPOUND])
    def test_search_by_multiple_ions(self, p_many):
        ions_list = ["ion1", "ion2", "ion3"]
        rv = self.app.post('/compounds', json=ions_list)
        json_data = json.loads(rv.get_data())
        p_many.assert_has_calls(
            [
                call(("ion1", "ion2")),
                call(("ion2", "ion3")),
                call(("ion1", "ion3")),
                call(("ion1", "ion2", "ion3")),
            ], any_order=True,
        )
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(json_data, [TEST_COMPOUND] * 4)
