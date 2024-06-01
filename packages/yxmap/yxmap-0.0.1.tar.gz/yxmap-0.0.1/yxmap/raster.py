import rasterio
# from osgeo import gdal

# def get_tif_score_gdal(latitude, longitude, tif_file):
#     # 打开tif文件
#     ds = gdal.Open(tif_file)

#     # 获取地理转换参数
#     gt = ds.GetGeoTransform()

#     # 计算像素位置
#     pixel_x = int((longitude - gt[0]) / gt[1])
#     pixel_y = int((latitude - gt[3]) / gt[5])

#     # 获取raster band
#     band = ds.GetRasterBand(1)

#     # 读取像素值
#     score = band.ReadAsArray(pixel_x, pixel_y, 1, 1)[0, 0]

#     # 检查是否为nodata
#     if score == band.GetNoDataValue():
#         score = None

#     return score

def get_raster_score(latitude, longitude, tif_file):
    with rasterio.open(tif_file) as src:
        try:
            # 转换坐标为像素位置
            row, col = src.index(longitude, latitude)
            # 获取像素值
            score = src.read(1)[row, col]
        except:
            score = None

        if score == src.nodata:
            score = None

    return score


def get_raster_score_many(coord_dict, tif_file, print_log=True):
    """
    coord_dict: {id: (latitude, longitude)}
    """
    num = 0
    with rasterio.open(tif_file) as src:
        # 一次性读取整个图像到内存中
        image = src.read(1)
        score_dict = {}
        for c_id in coord_dict:
            lat, lon = coord_dict[c_id]
            try:
                # 转换坐标为像素位置
                row, col = src.index(lon, lat)
                # 从内存中获取像素值
                score = image[row, col]
            except:
                score = None

            if score == src.nodata:
                score = None

            score_dict[c_id] = score
            num += 1
            if num % 100 == 0:
                if print_log:
                    print(f"Processed {num} / {len(coord_dict)}")

    return score_dict



def get_tif_metadata(tif_file):
    metadata_dict = {}

    with rasterio.open(tif_file) as src:
        # 读取数据
        data = src.read(1)
        metadata_dict["nodata"] = src.nodata
        transform = src.transform
        crs = src.crs

        metadata_dict["ncols"] = src.width
        metadata_dict["nrows"] = src.height
        metadata_dict["xcellsize"] = transform[0]
        metadata_dict["ycellsize"] = transform[4]

        # 计算最大有效数字位数
        digit = 0
        for i in transform:
            if i < 1:
                digit = max(digit, len(str(i).split(".")[1]))

        xcellsize = transform[0]
        ycellsize = transform[4]
        xllcorner = transform[2]
        xulcorner = xllcorner
        yulcorner = transform[5]
        yllcorner = round(
            yulcorner + (metadata_dict["nrows"] - 1) * ycellsize, digit)
        xlrcorner = round(
            xllcorner + (metadata_dict["ncols"] - 1) * xcellsize, digit)
        xurcorner = xlrcorner
        ylrcorner = yllcorner
        yurcorner = yulcorner

        metadata_dict["llcorner"] = (xllcorner, yllcorner)
        metadata_dict["ulcorner"] = (xulcorner, yulcorner)
        metadata_dict["urcorner"] = (xurcorner, yurcorner)
        metadata_dict["lrcorner"] = (xlrcorner, ylrcorner)

        metadata_dict["digit"] = digit

        metadata_dict["data_shape"] = data.shape

    return metadata_dict
