# -*- coding: utf-8 -*-
# @Time    : 2019-05-23 15:46
# @Author  : MarsDidi
# @Email   : xiatianci_i@didiglobal.com
# @File    : plot.py

import matplotlib.pyplot as plt


x3 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11]
y3=[49.58,46.48,43.82,42.55,40.95,40.40,45.65,40.15,48.74,39.70,50.86]

x4 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11]
y4=[44.90,41.10,38.65,34.50,32.93,31.06,33.34,29.71,33.51,28.51,39.06]

group_labels = ['1', '2','3','4','5','6','7','8','9','10','11']

plt.title('train_loss vs dev_loss')
plt.xlabel('epoch')
plt.ylabel('%')


plt.plot(x3, y3,'r', label='train_loss')
plt.plot(x4, y4,'b',label='dev_loss')

plt.xticks(x3, group_labels, rotation=0)

plt.legend(bbox_to_anchor=[0.3, 1])
plt.grid()
plt.show()
