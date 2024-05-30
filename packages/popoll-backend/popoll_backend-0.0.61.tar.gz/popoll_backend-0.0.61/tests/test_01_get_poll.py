from tests import IntegrationTest

class TestGetPoll(IntegrationTest):

    def test_db_creation(self):
        _json = self.get_instruments(False)
        self.assertEqual(9, len(_json['instruments']))
        self.assertEqual(self.instru1_id, _json['instruments'][0]['id'])
        self.assertEqual(self.INSTRU1, _json['instruments'][0]['name'])
        self.assertEqual(self.instru2_id, _json['instruments'][1]['id'])
        self.assertEqual(self.INSTRU2, _json['instruments'][1]['name'])
        self.assertEqual(self.instru3_id, _json['instruments'][2]['id'])
        self.assertEqual(self.INSTRU3, _json['instruments'][2]['name'])

    def test_get_poll(self):
        _json = self.get_poll()
        self.assertEqual('TESTTEST', _json['name'])
        self.assertEqual('#ff8b00', _json['color'])