import unittest
import os
import re

if __name__ == '__main__':
	test_modules = []
	dir_name, cur_file_name = os.path.split(os.path.realpath(__file__))
	for file_name in os.listdir(dir_name):
		if re.search('.py$', file_name) and re.search(cur_file_name, file_name) is None:
			test_modules.append(file_name[0:-3])
	if len(test_modules) > 0:
		suit = unittest.TestLoader().loadTestsFromNames(test_modules)
		unittest.TextTestRunner(verbosity=2).run(suit)