from tests import IntegrationTest

class TestGetDate(IntegrationTest):

    def setUp(self):
        super().setUp()
        self.user1_id = self.create_user('user1', self.instru2_id, [self.instru1_id])['user']['id']
        self.user2_id = self.create_user('user2', self.instru1_id, [self.instru2_id])['user']['id']
        self.date1_id = self.create_date(date='2025-03-10', time='15:00:00', title='firstDate', end_time='18:00:00')['id']
        self.answer1_id = self.create_answer(user_id=self.user1_id, date_id=self.date1_id)['id']
        self.answer2_id = self.create_answer(user_id=self.user2_id, date_id=self.date1_id)['id']
        self.update_answer(self.answer2_id, False)
        
    def test_get_date(self):
        _json = self.get_date(self.date1_id, False)
        self.assertDate(_json, self.date1_id, '2025-03-10', '15:00:00', '18:00:00', 'firstDate')
        self.assertEqual(None, _json.get('answers', None))

    def test_get_date_details(self):
        _json = self.get_date(self.date1_id, True)
        self.assertDate(_json['date'], self.date1_id, '2025-03-10', '15:00:00', '18:00:00', 'firstDate')
        
        self.assertEqual(4, len(_json['answers']))
        
        answer0 = _json['answers'][0]
        self.assertAnswer(answer0['answer'], self.answer1_id, self.user1_id, self.date1_id, True)
        self.assertUser(answer0['user'], self.user1_id, 'user1')
        self.assertInstrument(answer0['instrument'], self.instru2_id, self.INSTRU2, self.INSTRU2_RANK)
        self.assertTrue(answer0['is_main_instrument'])
        
        answer1 = _json['answers'][1]
        self.assertAnswer(answer1['answer'], self.answer1_id, self.user1_id, self.date1_id, True)
        self.assertUser(answer1['user'], self.user1_id, 'user1')
        self.assertInstrument(answer1['instrument'], self.instru1_id, self.INSTRU1, self.INSTRU1_RANK)
        self.assertFalse(answer1['is_main_instrument'])
        
        answer2 = _json['answers'][2]
        self.assertAnswer(answer2['answer'], self.answer2_id, self.user2_id, self.date1_id, False)
        self.assertUser(answer2['user'], self.user2_id, 'user2')
        self.assertInstrument(answer2['instrument'], self.instru1_id, self.INSTRU1, self.INSTRU1_RANK)
        self.assertTrue(answer2['is_main_instrument'])
        
        answer3 = _json['answers'][3]
        self.assertAnswer(answer3['answer'], self.answer2_id, self.user2_id, self.date1_id, False)
        self.assertUser(answer3['user'], self.user2_id, 'user2')
        self.assertInstrument(answer3['instrument'], self.instru2_id, self.INSTRU2, self.INSTRU2_RANK)
        self.assertFalse(answer3['is_main_instrument'])
        