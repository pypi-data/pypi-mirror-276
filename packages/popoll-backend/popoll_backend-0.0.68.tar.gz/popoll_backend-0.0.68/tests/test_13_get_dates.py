from tests import IntegrationTest

class TestGetDates(IntegrationTest):

    def setUp(self):
        super().setUp()
        self.date1_id = self.create_date(date='2025-03-10', time='15:00:00', title='firstDate', end_time=None)['id']
        self.date2_id = self.create_date(date='2025-03-12', title='secondDate', time=None, end_time=None)['id']
        self.date3_id = self.create_date(date='2025-03-11', time='15:00:00', title='thirdDate', end_time='18:00:00')['id']
        self.date4_id = self.create_date(date='2025-03-11', title='fourthDate', end_time='18:00:00', time=None)['id']
        
    def test_get_dates(self):
        _json = self.get_dates()
        self.assertEqual(4, len(_json['dates']))
        self.assertDates(_json['dates'], 0, self.date1_id, '2025-03-10', '15:00:00', None, 'firstDate')
        self.assertDates(_json['dates'], 1, self.date4_id, '2025-03-11', None, '18:00:00', 'fourthDate')
        self.assertDates(_json['dates'], 2, self.date3_id, '2025-03-11', '15:00:00', '18:00:00', 'thirdDate')
        self.assertDates(_json['dates'], 3, self.date2_id, '2025-03-12', None, None, 'secondDate')
