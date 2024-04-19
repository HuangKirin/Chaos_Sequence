import math
import matplotlib.pyplot as plt
from matplotlib import cm

from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np


def f(x, alpha, beta):
    return (1 - (beta ** -4)) * (1 / math.tan(alpha / (1 + beta))) * ((1 + 1 / beta) ** beta) * math.tan(alpha * x) * ((1 - x) ** beta)


alpha = 0.7
beta = 28
x = 0.666

li = range(100)
x_list = []

for i in li:
    x_ = f(x, alpha, beta)
    x = x_
    x_list.append(x)

plt.plot(li, x_list)
plt.show()
