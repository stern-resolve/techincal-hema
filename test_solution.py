# Technical Task - testing
import unittest
import solution

TEST_DATA_1_HDR = ["mon","tue","some_column1","wed","thu","fri","description"]
TEST_DATA_1_DROW = [1,5,"data",2,3,3,"first_desc"]

TEST_DATA_2_HDR = ["mon-thu","fri","description","another_column2"]
TEST_DATA_2_DROW = [2,3,"second_desc","some_data"]

TEST_RESULTS_1 = [
    {'day': 'mon', 'description': 'first_desc 1', 'square': 1, 'value': 1},
    {'day': 'tue', 'description': 'first_desc 25', 'square': 25, 'value': 5},
    {'day': 'wed', 'description': 'first_desc 4', 'square': 4, 'value': 2},
    {'day': 'thu', 'description': 'first_desc 6', 'double': 6, 'value': 3},
    {'day': 'fri', 'description': 'first_desc 6', 'double': 6, 'value': 3}
 ]


TEST_RESULTS_2 = [
    {'day': 'mon', 'description': 'second_desc 4', 'square': 4, 'value': 2},
    {'day': 'tue', 'description': 'second_desc 4', 'square': 4, 'value': 2},
    {'day': 'wed', 'description': 'second_desc 4', 'square': 4, 'value': 2},
    {'day': 'thu', 'description': 'second_desc 4', 'double': 4, 'value': 2},
    {'day': 'fri', 'description': 'second_desc 6', 'double': 6, 'value': 3}
]
class TestDailyData(unittest.TestCase):

	def test_get_daily_data(self):

		self.check_daily_data(TEST_DATA_1_HDR,TEST_DATA_1_DROW,TEST_RESULTS_1)

		self.check_daily_data(TEST_DATA_2_HDR,TEST_DATA_2_DROW,TEST_RESULTS_2)



	def check_daily_data(self,test_data_header,test_data_data_row,test_results):
		day_results = solution.get_daily_data(test_data_header, test_data_data_row)
		self.assertEqual(len(day_results),5)
		
		# did we get five days data?
		
		# 0=mon,...,4=fri
		for dow in range(5):
			# test results
			day_test_d = test_results[dow]

			test_day_name=day_test_d['day']
			test_day_desc = day_test_d['description']
			test_day_opname = 'square' if dow<3 else 'double'
			test_day_value = day_test_d['value']
			test_day_op_value = day_test_d[test_day_opname]
			
			# result from our function
			day = day_results[dow]
			
			# assertions
			# day name
			self.assertEqual(day.name,test_day_name)

			# description
			self.assertEqual(day.description, test_day_desc)

			# value
			self.assertEqual(day.value, test_day_value)
			
			# op name & value
			self.assertEqual(day.op_name, test_day_opname)
			self.assertEqual(day.op_value, test_day_op_value)





if __name__ == "__main__":
    unittest.main()