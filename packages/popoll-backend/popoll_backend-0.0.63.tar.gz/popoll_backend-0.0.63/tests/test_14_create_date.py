from tests import IntegrationTest

class TestCreateDate(IntegrationTest):

    def setUp(self):
        super().setUp()
        self.date1_id = self.create_date(date='2025-03-12', time='15:00:00', title='firstDate', end_time=None)['id']
        
    def test_create_date(self):
        self.assertEqual(1, len(self.get_dates()['dates']))
        self.date2_id = self.create_date(date='2025-03-10', title='secondDate', time=None, end_time=None)['id']
        _json = self.get_dates()
        self.assertEqual(2, len(_json['dates']))
        self.assertDates(_json['dates'], 0, self.date2_id, '2025-03-10', None, None, 'secondDate')
        
    def test_create_date_only_end_time(self):
        self.assertEqual(1, len(self.get_dates()['dates']))
        self.date2_id = self.create_date(date='2025-03-10', title='secondDate', time=None, end_time='18:00:00')['id']
        _json = self.get_dates()
        self.assertEqual(2, len(_json['dates']))
        self.assertDates(_json['dates'], 0, self.date2_id, '2025-03-10', None, '18:00:00', 'secondDate')
