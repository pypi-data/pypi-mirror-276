import matplotlib.pyplot as plt

# 设置图像的大小
plt.rcParams['figure.figsize'] = (6, 6)

# 设置字体
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 14
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 16
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14

# 设置坐标轴的粗细
plt.rcParams['axes.linewidth'] = 2

# 设置刻度线的粗细
plt.rcParams['xtick.major.width'] = 2
plt.rcParams['ytick.major.width'] = 2

# 其他
plt.rcParams['lines.linewidth'] = 2
plt.rcParams['lines.color'] = '#000000'

from .plot import *
from .map import *
from .raster import *
from .shape import *