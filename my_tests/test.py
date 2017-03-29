# -*- encoding: utf-8 -*-
#python -m unittest test
import unittest
import os
import subprocess
from core.remove import HandlerRemove

class TestRemove(unittest.TestCase):
    testbead_path = "testbead"
    empty_dir_path = os.path.join(testbead_path, "empty_dir")
    file_path = os.path.join(testbead_path, "file")
    dir_path = os.path.join(testbead_path, "dir")

    def setUp(self):
        os.mkdir(self.testbead_path)
        os.mkdir(self.empty_dir_path)
        open(self.file_path, 'w')
        os.makedirs(self.dir_path+"/dir2"+"/dir3")

    def test_run_remove_empty_dir(self):
        handler_empty_dir = HandlerRemove(True, False, False, 'basket')
        handler_empty_dir.run(self.empty_dir_path)
        self.assertEqual(os.path.exists(self.empty_dir_path), False)
    def test_run_remove_dir(self):
        handler_dir = HandlerRemove(False, True, False, 'basket')
        handler_dir.run(self.dir_path)
        self.assertEqual(os.path.exists(self.dir_path), False)
    def test_run_remove_file(self):
        handler_file = HandlerRemove(False, False, False, 'basket')
        handler_file.run(self.file_path)
        self.assertEqual(os.path.exists(self.file_path), False)
    def test_run_remove_not_empty_dir_with_msg(self):
        handler_file = HandlerRemove(True, False, False, 'basket')
        handler_file.run(self.dir_path)
        self.assertEqual(os.path.exists(self.dir_path), True)
    def tearDown(self):
        subprocess.call(["rm", "-rf", self.testbead_path])


if __name__ == '__main__':
    unittest.main()


# def touch(fname, times=None):
#     with open(fname, 'a'):
#         os.utime(fname, times)
#     # fhandle = open(fname, 'a')
#     # try:
#     #     os.utime(fname, times)
#     # finally:
#     #     fhandle.close()
  