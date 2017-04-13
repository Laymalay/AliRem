#!/usr/bin/python
# -*- coding: UTF-8 -*-

import alirem.alirm as Alirem



rm = Alirem.Alirem()
rm.remove('file', is_basket=True)
rm.check_basket_for_cleaning(is_show=True)
rm.restore('file')
rm.show_basket_list()


