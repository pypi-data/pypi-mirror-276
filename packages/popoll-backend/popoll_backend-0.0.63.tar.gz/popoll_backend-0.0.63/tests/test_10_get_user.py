from tests import IntegrationTest

class TestGetUser(IntegrationTest):

    def setUp(self):
        super().setUp()
        self.user1_id = self.create_user('user1', self.instru2_id, [self.instru3_id, self.instru1_id])['user']['id']
        
    def test_get_user(self):
        _json = self.get_user(self.user1_id, False)
        self.assertUserWithInstruments(_json, self.user1_id, 'user1', self.instru2_id, [self.instru1_id, self.instru3_id])

    def test_get_user_details(self):
        self.date1_id = self.create_date(date='2028-03-10', time='15:00:00', title='firstDate', end_time='18:00:00')['id']
        self.date2_id = self.create_date(date='2022-03-10', time='15:00:00', title='oldDate', end_time='18:00:00')['id']
        self.answer1_id = self.create_answer(user_id=self.user1_id, date_id=self.date1_id)['id']
        _json = self.get_user(self.user1_id, True)
        self.assertUser(_json['user'], self.user1_id, 'user1')
        self.assertEqual(2, len(_json['dates']))
        self.assertDate(_json['dates'][0]['date'], self.date2_id, '2022-03-10', '15:00:00', '18:00:00', 'oldDate', False, True)
        self.assertDate(_json['dates'][1]['date'], self.date1_id, '2028-03-10', '15:00:00', '18:00:00', 'firstDate', False, False)
        self.assertAnswer(_json['dates'][1]['answer'], self.answer1_id, self.user1_id, self.date1_id, True)
        
    def test_get_user_details_with_old_dates(self):
        self.date1_id = self.create_date(date='2028-03-10', time='15:00:00', title='firstDate', end_time='18:00:00')['id']
        self.date2_id = self.create_date(date='2022-03-10', time='15:00:00', title='oldDate', end_time='18:00:00')['id']
        self.answer1_id = self.create_answer(user_id=self.user1_id, date_id=self.date1_id)['id']
        _json = self.get_user(self.user1_id, True)
        self.assertEqual(2, len(_json['dates']))