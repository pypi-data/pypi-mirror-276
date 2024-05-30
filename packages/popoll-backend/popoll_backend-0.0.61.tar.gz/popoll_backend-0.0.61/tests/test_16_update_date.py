from tests import IntegrationTest

class TestUpdateDate(IntegrationTest):

    def setUp(self):
        super().setUp()
        self.date1_id = self.create_date(date='2025-03-10', time='15:00:00', title='firstDate', end_time='18:00:00')['id']
        
    def test_update_date(self):
        _json = self.udpate_date(self.date1_id, date='2025-03-10', title='firstDate', time=None, end_time=None)
        self.assertDate(_json, self.date1_id, '2025-03-10', None, None, 'firstDate')
        _json = self.get_date(self.date1_id, False)
        self.assertDate(_json, self.date1_id, '2025-03-10', None, None, 'firstDate')

    def test_update_freeze_date(self):
        _json = self.udpate_date(self.date1_id, date='2025-03-10', time='15:00:00', title='firstDate', end_time='18:00:00', is_frozen=True)
        self.assertTrue(_json['is_frozen'])
        
        self.user1_id = self.create_user('user1', self.instru2_id, [self.instru1_id])['user']['id']
        _rs = self.create_answer(self.user1_id, self.date1_id, fail=True)
        self.assertEqual(403, _rs.status_code)