import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math


# 定义迭代函数
def f(x, alpha, beta):
    return (1 - (beta ** -4)) * (1 / math.tan(alpha / (1 + beta))) * ((1 + 1 / beta) ** beta) * math.tan(alpha * x) * (
                (1 - x) ** beta)


# 设置初始参数
alpha = 0.7
beta = 28
x = 0.666

# 设置图形
fig, ax = plt.subplots()
x_list = []


# 更新函数
def update(frame):
    global x
    x_ = f(x, alpha, beta)
    x = x_
    x_list.append(x)
    ax.clear()
    ax.plot(x_list, color='blue')
    ax.set_xlim(0, len(x_list))
    ax.set_ylim(min(x_list) - 0.1, max(x_list) + 0.1)
    ax.set_title('Iteration Function')
    ax.set_xlabel('Iteration')
    ax.set_ylabel(f'Value: x{len(x_list)}')
    return ax,


# 创建动画
ani = FuncAnimation(fig, update, frames=None, interval=100)

# 显示动画
plt.show()
