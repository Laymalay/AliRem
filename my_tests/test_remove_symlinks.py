#!/usr/bin/python
# -*- encoding: utf-8 -*-


import unittest
import subprocess
from os.path import join, exists, basename
from os import mkdir, makedirs,symlink
from alirem.remove import RemoveHandler
import alirem.logger as log
from alirem.logger import DefaultLogger

class TestRemoveSymlinks(unittest.TestCase):
    testbead_path = "testbead"
    basket = join(testbead_path, "basket")
    empty_dir_path = join(testbead_path, "empty_dir")
    file_path = join(testbead_path, "file")
    dir_path = join(testbead_path, "dir")

    link_to_file = join(testbead_path, "link_to_file")
    link_to_dir = join(testbead_path, "link_to_dir")
    link_to_emptydir = join(testbead_path, "link_to_emptydir")



    logger = DefaultLogger()

    def setUp(self):

        mkdir(self.testbead_path)
        mkdir(self.empty_dir_path)
        open(self.file_path, 'w')
        makedirs(join(self.dir_path, "dir2", "dir3"))
        symlink("file", self.link_to_file)
        symlink("dir", self.link_to_dir)
        symlink("empty_dir", self.link_to_emptydir)

    def test_run_remove_link_empty_dir(self):
        handler_empty_dir = RemoveHandler(symlinks=False, is_dir=True, is_basket=True,
                                          basket_path=self.basket, logger=self.logger)
        handler_empty_dir.remove(self.link_to_emptydir)
        self.assertEqual(exists(self.link_to_emptydir), False)
        self.assertEqual(exists(self.empty_dir_path), True)
    def test_run_remove_dir_to_basket(self):
        handler_dir = RemoveHandler(is_recursive=True, symlinks=False, is_basket=True,
                                    basket_path=self.basket, logger=self.logger)
        handler_dir.remove(self.link_to_dir)
        self.assertEqual(exists(self.link_to_dir), False)
        self.assertEqual(exists(self.dir_path), True)

    def test_run_remove_file_to_basket(self):
        handler_file = RemoveHandler(logger=self.logger, is_basket=True,
                                     symlinks=False, basket_path=self.basket,)
        handler_file.remove(self.link_to_file)
        self.assertEqual(exists(self.file_path), True)
        self.assertEqual(exists(self.link_to_file), False)

    def tearDown(self):
        subprocess.call(["rm", "-rf", self.testbead_path])


if __name__ == '__main__':
    unittest.main()
