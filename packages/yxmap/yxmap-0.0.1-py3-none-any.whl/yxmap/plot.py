from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from .config import NATURAL_EARTH_SHP_FILE
import geopandas as gpd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import rasterio
from rasterio.windows import from_bounds

defaut_cmap = 'viridis'
defaut_latitude_limit = [-37, 51]
defaut_longitude_limit = [-20, 95]

def scatter_map_ploter(data,
                       title=None,
                       value_label=None,
                       longitude_limit=defaut_longitude_limit,
                       latitude_limit=defaut_latitude_limit,
                       type_plot_order=None,
                       ax=None,
                       s=20,
                       cmap=defaut_cmap):
    """
    data为dataframe格式, 应包含longitude, latitude, type(分类数据), value(连续数据)列
    """
    data = data[data['latitude'].notnull()]
    data = data[data['longitude'].notnull()]
    data = data[data['value'].notnull()]
    data = data[data['type'].notnull()]

    if ax is None:
        fig, ax = plt.subplots(figsize=(15, 8))
    if title is None:
        title = 'Continuous scatter map'
    if value_label is None:
        value_label = 'Value'

    # 读取内置的世界地图数据
    world = gpd.read_file(NATURAL_EARTH_SHP_FILE)

    # 在 axes 对象上绘制地图
    world.boundary.plot(color='black', linewidth=0.5, ax=ax)

    # 设置地图边界
    ax.set_xlim(longitude_limit)  # 替换为你的左右边界的经度
    ax.set_ylim(latitude_limit)  # 替换为你的上下边界的纬度

    # 定义点的形状
    if type_plot_order is None:
        type_plot_order = list(data['type'].unique())

    markers = ['o', '<', 's', '*', '^', '>', 'p', 'v', 'h', 'H', 'D', 'd', 'P', 'X']
    type_markers = {t: markers[i % len(markers)] for i, t in enumerate(type_plot_order)}

    # 在 axes 对象上添加点，使用给定值设置颜色
    for t in type_plot_order:
        subdata = data[data['type'] == t]
        scatter = ax.scatter(
            subdata['longitude'],
            subdata['latitude'],
            c=subdata['value'],
            cmap=cmap,
            vmin=min(data['value']),
            vmax=max(data['value']),
            s=s,  # s参数设置点的大小
            marker=type_markers[t],
            label=t
        )

    # 创建 inset_axes 对象
    axins = inset_axes(ax,
                       width="2%",  # width = 5% of parent_bbox width
                       height="15%",  # height : 50%
                       loc='lower left',
                       bbox_to_anchor=(0.04, 0.25, 1, 1),
                       bbox_transform=ax.transAxes,
                       borderpad=0,
                       )

    # 在 inset_axes 对象上添加颜色条
    cbar = fig.colorbar(scatter, cax=axins, orientation='vertical')
    cbar.outline.set_linewidth(1.5)
    cbar.ax.tick_params(width=1.5, labelsize=12)
    # axins.set_title(value_label)

    # 创建一个新的 inset_axes 对象用于绘制分布图
    axins2 = inset_axes(ax,
                        width="30%",  # width = 30% of parent_bbox width
                        height="30%",  # height : 30%
                        loc='lower right',
                        bbox_to_anchor=(-0.025, 0.05, 1, 1),
                        bbox_transform=ax.transAxes,
                        )

    # 在新的 inset_axes 对象上绘制分布图
    # 创建一个颜色映射
    # 创建一个颜色映射
    cmap = plt.get_cmap('viridis')
    norm = plt.Normalize(data['value'].min(), data['value'].max())

    # 计算直方图
    counts, bins = np.histogram(data['value'], bins='auto')

    # 绘制直方图的每个柱子
    for b in range(len(bins)-1):
        width = bins[b+1] - bins[b]  # 计算柱子的宽度
        axins2.bar(bins[b], counts[b], width=width, color=cmap(norm(bins[b])), edgecolor='black')

    # axins2.hist(
    #     data['value'],
    #     bins='auto',
    #     color='lightblue',
    #     edgecolor='black')
    axins2.set_title('Distribution of %s' % value_label)

    ax.set_title(title)

    # 显示图例，位置在右下角
    ax.legend(loc='lower left', frameon=False, facecolor='none', handlelength=2, handletextpad=0.15)

    if ax is None:
        plt.show()

    return ax


def continuous_scatter_map_ploter(data,
                                  title=None,
                                  value_label=None,
                                  longitude_limit=defaut_longitude_limit,
                                  latitude_limit=defaut_latitude_limit,
                                  ax=None,
                                  s=20,
                                  cmap=defaut_cmap):
    """
    data为dataframe格式, 应包含longitude, latitude, value列, 其中value为连续值
    """
    data = data[data['latitude'].notnull()]
    data = data[data['longitude'].notnull()]
    data = data[data['value'].notnull()]

    if ax is None:
        fig, ax = plt.subplots(figsize=(15, 8))
    if title is None:
        title = 'Continuous scatter map'
    if value_label is None:
        value_label = 'Value'

    # 读取内置的世界地图数据
    world = gpd.read_file(NATURAL_EARTH_SHP_FILE)

    # 在 axes 对象上绘制地图
    world.boundary.plot(color='black', linewidth=0.5, ax=ax)

    # 设置地图边界
    ax.set_xlim(longitude_limit)  # 替换为你的左右边界的经度
    ax.set_ylim(latitude_limit)  # 替换为你的上下边界的纬度

    # 在 axes 对象上添加点，使用给定值设置颜色
    scatter = ax.scatter(
        data['longitude'],
        data['latitude'],
        c=data['value'],
        cmap=cmap,
        vmin=min(
            data['value']),
        vmax=max(
            data['value']),
        s=s)  # s参数设置点的大小

    # 创建 inset_axes 对象
    axins = inset_axes(ax,
                       width="5%",  # width = 5% of parent_bbox width
                       height="30%",  # height : 50%
                       loc='lower left',
                       bbox_to_anchor=(0.05, 0.05, 1, 1),
                       bbox_transform=ax.transAxes,
                       borderpad=0,
                       )

    # 在 inset_axes 对象上添加颜色条
    cbar = fig.colorbar(scatter, cax=axins, orientation='vertical')
    axins.set_title(value_label)

    # 创建一个新的 inset_axes 对象用于绘制分布图
    axins2 = inset_axes(ax,
                        width="30%",  # width = 30% of parent_bbox width
                        height="30%",  # height : 30%
                        loc='lower right',
                        bbox_to_anchor=(-0.01, 0.05, 1, 1),
                        bbox_transform=ax.transAxes,
                        )

    # 在新的 inset_axes 对象上绘制分布图
    axins2.hist(
        data['value'],
        bins='auto',
        color='lightblue',
        edgecolor='black')
    axins2.set_title('Distribution of %s' % value_label)

    ax.set_title(title)

    if ax is None:
        plt.show()

    return ax


def discrete_scatter_map_ploter(data,
                                title=None,
                                value_label=None,
                                longitude_limit=defaut_longitude_limit,
                                latitude_limit=defaut_latitude_limit,
                                value_plot_order=None,
                                ax=None,
                                s=20,
                                cmap=defaut_cmap):
    """
    data为dataframe格式, 应包含longitude, latitude, value列, 其中value为离散值或分类名
    """
    data = data[data['latitude'].notnull()]
    data = data[data['longitude'].notnull()]
    data = data[data['value'].notnull()]

    if ax is None:
        fig, ax = plt.subplots(figsize=(15, 8))
    if title is None:
        title = 'Discrete scatter map'
    if value_label is None:
        value_label = 'Value'

    # 读取内置的世界地图数据
    world = gpd.read_file(NATURAL_EARTH_SHP_FILE)
    # 在 axes 对象上绘制地图
    world.boundary.plot(color='black', linewidth=0.5, ax=ax)

    # 设置地图边界
    ax.set_xlim(longitude_limit)  # 替换为你的左右边界的经度
    ax.set_ylim(latitude_limit)  # 替换为你的上下边界的纬度

    # 创建一个颜色映射
    # base_cmap = mpl.cm.get_cmap(cmap)
    base_cmap = plt.get_cmap(cmap)
    cmap = mpl.colors.ListedColormap(
        base_cmap(
            np.linspace(
                0, 1, len(
                    data['value'].unique()))))

    # scatter
    if value_plot_order is None:
        value_plot_order = sorted(data['value'].unique(), key=lambda x: len(
            data[data['value'] == x]), reverse=True)

    value_color = 0
    for value in value_plot_order:
        subdata = data[data['value'] == value]
        data_count = len(subdata)
        ax.scatter(
            subdata['longitude'], subdata['latitude'], c=[
                cmap(value_color)], label='%s (%d)' %
            (value, data_count), s=s)
        value_color += 1

    ax.set_title(title)

    # 显示图例，位置在右下角
    ax.legend(loc='lower right')

    # ax.axis('off')  # 关闭坐标轴
    if ax is None:
        plt.show()

    return ax


def quick_raster_plot(raster_file, title="quickly plot", target_bounds=None, cmap='viridis', vmin=None, vmax=None, figsize=(10, 10), plot_country_boundary=True, line_width=0.5):

    # 设置地理范围
    if target_bounds:
        min_lon, min_lat, max_lon, max_lat = target_bounds

    # 打开 raster 文件
    with rasterio.open(raster_file) as src:
        if target_bounds:
            window = from_bounds(min_lon, min_lat, max_lon,
                                 max_lat, src.transform)
            subset = src.read(1, window=window)
        else:
            subset = src.read(1)
            # 获取地理范围
            min_lon, min_lat, max_lon, max_lat = src.bounds
        raster_nodata = src.nodata

    # 创建一个新的图像
    fig, ax = plt.subplots(figsize=figsize)

    # 设置坐标轴的范围
    extent = [min_lon, max_lon, min_lat, max_lat]

    # 显示图像
    masked_subset = np.ma.masked_where(subset == raster_nodata, subset)
    img = ax.imshow(masked_subset, cmap=cmap, vmin=vmin,
                    vmax=vmax, extent=extent)

    if plot_country_boundary:
        # 加载国家边界
        world = gpd.read_file(NATURAL_EARTH_SHP_FILE)

        # 绘制国家边界
        world.boundary.plot(ax=ax, color='black', linewidth=line_width)

    # 添加图例
    cbar = fig.colorbar(img, ax=ax, orientation='vertical', pad=0.02)
    cbar.set_label(title, rotation=270, labelpad=15)

    # 设置标题
    ax.set_title(title)
    ax.set_xlim(min_lon, max_lon)
    ax.set_ylim(min_lat, max_lat)

    # 显示图像
    plt.show()
