import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

from matplotlib import colors
from matplotlib.ticker import LinearLocator
import math


def f(x, alpha, beta):
    return (1 - (beta ** -4)) * (1 / math.tan(alpha / (1 + beta))) * ((1 + 1 / beta) ** beta) * math.tan(alpha * x) * (
            (1 - x) ** beta)


def io_test(x, x_sen, alpha, beta, Iter):
    fig = plt.figure()  # 生成画布
    plt.ion()  # 打开交互模式

    # 初始化
    X = alpha
    Y = beta
    Z = np.empty((len(X), len(Y)))
    for i in range(len(X)):
        for j in range(len(Y)):
            Z[i, j] = x
    Z_sen = np.empty((len(X), len(Y)))
    for i in range(len(X)):
        for j in range(len(Y)):
            Z_sen[i, j] = x_sen

    # 开始迭代
    for idx in range(Iter):
        fig.clf()  # 清空当前Figure对象
        fig.suptitle(f"Iter{idx + 1}")
        X = alpha
        Y = beta
        X_, Y_ = np.meshgrid(Y, X)

        # Sensitive
        Z_sen_ = np.empty((len(X), len(Y)))
        ax1 = fig.add_subplot(132, projection="3d")

        for i in range(len(X)):
            for j in range(len(Y)):
                Z_sen_[i, j] = f(Z_sen[i, j], X[i], Y[j])

        surf1 = ax1.plot_surface(X_, Y_, Z_sen_, cmap=cm.hot, antialiased=True)

        ax1.set_zlim(0, 1)
        ax1.zaxis.set_major_locator(LinearLocator(11))
        ax1.view_init(elev=idx * 0.25, azim=-30 + idx * 0.2)
        ax1.set_ylabel('alpha')
        ax1.set_xlabel('beta')
        ax1.set_zlabel(f'x\'_{idx+1}')
        ax1.set_title(f"Sensitive: x\'0={x_sen}")

        Z_sen = Z_sen_

        # Original
        Z_ = np.empty((len(X), len(Y)))
        ax2 = fig.add_subplot(131, projection="3d")

        for i in range(len(X)):
            for j in range(len(Y)):
                Z_[i, j] = f(Z[i, j], X[i], Y[j])

        surf2 = ax2.plot_surface(X_, Y_, Z_, cmap=cm.hot, antialiased=True)

        ax2.set_zlim(0, 1)
        ax2.zaxis.set_major_locator(LinearLocator(11))
        ax2.view_init(elev=idx * 0.25, azim=-30 + idx * 0.2)
        ax2.set_ylabel('alpha')
        ax2.set_xlabel('beta')
        ax2.set_zlabel(f'x_{idx+1}')
        ax2.set_title(f"Original: x0={x}")

        Z = Z_

        # Difference
        Z_diff = abs(Z - Z_sen)
        ax3 = fig.add_subplot(133, projection="3d")
        norm = colors.Normalize(vmin=0, vmax=1)
        surf3 = ax3.plot_surface(X_, Y_, Z_diff, cmap=cm.hot, antialiased=True, norm=norm)

        ax3.set_zlim(0, 1)
        ax3.zaxis.set_major_locator(LinearLocator(11))
        ax3.view_init(elev=idx * 0.25, azim=-30 + idx * 0.2)
        ax3.set_title("Difference")
        ax3.set_ylabel('alpha')
        ax3.set_xlabel('beta')
        ax3.set_zlabel(f'diff_{idx+1}')
        # colorbar
        fig.colorbar(surf3, shrink=0.5, aspect=5)
        if not idx:
            plt.pause(2)
        plt.pause(0.1)

    # 关闭交互模式
    plt.ioff()
    plt.show()


if __name__ == '__main__':
    alpha1 = np.arange(0.1, 1.4, 0.05).astype(np.float32)
    beta1 = np.arange(5, 43, 2).astype(np.float32)
    alpha2 = np.arange(1.4, 1.5, 0.0025).astype(np.float32)
    beta2 = np.arange(9, 38, 1).astype(np.float32)
    alpha3 = np.arange(1.5, 1.57, 0.002).astype(np.float32)
    beta3 = np.arange(3, 15, 0.25).astype(np.float32)
    x = 0.666
    x_sen = 0.667
    Iter = 1000
    io_test(x, x_sen, alpha2, beta2, Iter)
