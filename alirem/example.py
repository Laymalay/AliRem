#!/usr/bin/python
# -*- coding: UTF-8 -*-
import Alirem as Alirem



rm = Alirem.Alirem()
rm.remove('file')
rm.check_basket_for_cleaning(is_show=True)
rm.show_basket_list()
rm.restore('file')

