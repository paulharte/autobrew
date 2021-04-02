from unittest import TestCase

from storage.dynamo import delete_nulls_from_dict


class TestDelete_nulls_from_dict(TestCase):

    def test_delete_nulls_from_dict(self):
        d = {'paul': None, 'billy': 1}
        out = delete_nulls_from_dict(d)
        self.assertEqual(out, {'billy': 1})