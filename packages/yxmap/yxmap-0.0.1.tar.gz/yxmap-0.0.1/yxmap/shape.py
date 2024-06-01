from shapely.geometry import Point
import geopandas as gpd


def get_shp_info_many(coord_dict, shp_file, print_log=True):
    """
    coord_dict: {id: (latitude, longitude)}
    """

    num = 0

    gdf = gpd.read_file(shp_file)

    info_dict = {}
    for s in coord_dict:
        # 创建一个点对象，表示你的地理坐标
        # 注意：这里的 lon 和 lat 需要替换为你的实际坐标
        lat = coord_dict[s][0]
        lon = coord_dict[s][1]
        point = Point(lon, lat)

        # 使用 GeoPandas 的 contains 方法来判断这个点在哪个区域内
        location = gdf[gdf.geometry.contains(point)]

        info_dict[s.xyx_id] = location

        num += 1
        if num % 100 == 0:
            if print_log:
                print(f"Processed {num} / {len(coord_dict)}")

    return info_dict