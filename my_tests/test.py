#!/usr/bin/python
# -*- encoding: utf-8 -*-
#python -m unittest test
import unittest
import subprocess
from os.path import join, exists
from os import mkdir, makedirs
from alirem.remove import RemoveHandler
import alirem.logger as log

class TestRemove(unittest.TestCase):
    testbead_path = "testbead"
    empty_dir_path = join(testbead_path, "empty_dir")
    file_path = join(testbead_path, "file")
    dir_path = join(testbead_path, "dir")
    logger = log.Logger(None, 'info', 'test', False)

    def setUp(self):
        mkdir(self.testbead_path)
        mkdir(self.empty_dir_path)
        open(self.file_path, 'w')
        makedirs(self.dir_path+"/dir2"+"/dir3")

    def test_run_remove_empty_dir(self):
        handler_empty_dir = RemoveHandler(True, False, False, False, False, self.logger)
        handler_empty_dir.run_remove(self.empty_dir_path)
        self.assertEqual(exists(self.empty_dir_path), False)
    def test_run_remove_dir(self):
        handler_dir = RemoveHandler(False, True, False, False, False, self.logger)
        handler_dir.run_remove(self.dir_path)
        self.assertEqual(exists(self.dir_path), False)
    def test_run_remove_file(self):
        handler_file = RemoveHandler(False, False, False, False, False, self.logger)
        handler_file.run_remove(self.file_path)
        self.assertEqual(exists(self.file_path), False)
    # def test_run_remove_not_empty_dir_with_msg(self):
    #     handler_file = RemoveHandler(True, False, False, 'basket', self.logger)
    #     handler_file.run_remove(self.dir_path)
    #     self.assertEqual(exists(self.dir_path), True)

    def tearDown(self):
        subprocess.call(["rm", "-rf", self.testbead_path])


if __name__ == '__main__':
    unittest.main()
