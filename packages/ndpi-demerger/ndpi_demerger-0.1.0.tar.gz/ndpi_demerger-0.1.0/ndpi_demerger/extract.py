import os
import pandas as pd
import openslide
from PIL import Image
import numpy as np
from skimage.color import rgb2hsv
from skimage import img_as_ubyte
import shutil
import logging
import time

def calculate_saturation(patch):
    """
    计算给定PIL图像的平均饱和度。
    """
    patch_array = np.array(patch)  # 将图像转换为数组
    hsv_patch = rgb2hsv(patch_array)  # 将RGB图像转换为HSV格式
    saturation_channel = hsv_patch[:, :, 1]  # 获取饱和度通道
    saturation_channel_0_255 = img_as_ubyte(saturation_channel)  # 转换饱和度范围为0到255
    return np.mean(saturation_channel_0_255)  # 返回平均饱和度

def clear_output_directory(output_path):
    """
    清空指定的输出文件夹，如果文件夹不存在则创建它。
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)  # 如果目录不存在，创建目录
    else:
        for filename in os.listdir(output_path):
            file_path = os.path.join(output_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # 删除文件或符号链接
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # 删除子目录
            except Exception as e:
                logging.error(f'删除 {file_path} 失败。原因: {str(e)}')  # 记录删除失败的错误

def extract_patches_from_ndpi(input_path, output_path, excel_path, patch_size=512, target_magnification=20, saturation_threshold=50):
    """
    从NDPI格式的病理图像中提取符合条件的图像块，并记录相关信息到Excel文件。
    """
    slide = openslide.OpenSlide(input_path)  # 打开NDPI文件
    level = select_level_by_magnification(slide, target_magnification)  # 选择合适的图像层级
    level_downsample = slide.level_downsamples[level]  # 获取该层级的下采样因子
    width, height = slide.level_dimensions[level]  # 获取图像的尺寸

    if not os.path.exists(output_path):
        os.makedirs(output_path)  # 如果输出路径不存在，创建该路径

    data = []
    num_patches = 0

    for x in range(0, width - patch_size + 1, patch_size):
        for y in range(0, height - patch_size + 1, patch_size):
            patch = slide.read_region((int(x * level_downsample), int(y * level_downsample)), level,
                                      (patch_size, patch_size)).convert('RGB')  # 读取图像块
            saturation = calculate_saturation(patch)  # 计算饱和度
            patch_name = f'patch_{x}_{y}.tiff'  # 设置图像块的文件名
            is_saved = saturation >= saturation_threshold  # 根据饱和度决定是否保存图像块

            if is_saved:
                patch.save(os.path.join(output_path, patch_name))  # 保存图像块
                num_patches += 1

            data.append([patch_name, saturation, is_saved])

    df = pd.DataFrame(data, columns=['Patch Name', 'Saturation', 'Saved'])
    df.to_excel(excel_path, index=False)  # 将数据保存到Excel文件

    slide.close()  # 关闭文件

def select_level_by_magnification(slide, target_magnification):
    """
    根据目标放大倍数选择最接近的层级。
    """
    best_level = 0
    min_diff = float('inf')
    for i, downsample in enumerate(slide.level_downsamples):
        try:
            objective_power = float(slide.properties['openslide.objective-power'])
            current_magnification = objective_power / downsample
            magnification_diff = abs(current_magnification - target_magnification)

            if magnification_diff < min_diff:
                min_diff = magnification_diff
                best_level = i
        except KeyError:
            continue  # 如果无法获取必要的属性，跳过当前层级
        except ValueError:
            continue  # 如果属性值不正确，跳过当前层级

    return best_level

def process_ndpi_files(base_path, output_base, saturation_threshold, patch_size, target_magnification):
    """
    遍历所有子目录，查找并处理每个NDPI文件，并在相应的输出子目录中生成Excel文件，同时显示处理进度和运行时间。
    """
    logging.basicConfig(filename=os.path.join(output_base, 'error_log.txt'), level=logging.ERROR)
    ndpi_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(base_path) for f in filenames if
                 f.endswith('.ndpi')]
    total_files = len(ndpi_files)  # 总文件数
    start_time = time.time()  # 开始计时

    for index, ndpi_file in enumerate(ndpi_files):
        current_file_start_time = time.time()
        folder_name = os.path.basename(os.path.dirname(ndpi_file))
        output_path = os.path.join(output_base, folder_name)
        excel_path = os.path.join(output_path, f'{folder_name}_patches_info.xlsx')
        clear_output_directory(output_path)  # 清理输出目录
        try:
            extract_patches_from_ndpi(ndpi_file, output_path, excel_path, patch_size, target_magnification,
                                     saturation_threshold)
        except Exception as e:
            logging.error(f'处理文件 {ndpi_file} 时出现错误: {str(e)}')

        # 计算当前文件的处理时间
        current_file_elapsed_time = time.time() - current_file_start_time
        total_elapsed_time = time.time() - start_time
        print(f'已处理 {index + 1}/{total_files} 文件，占总进度的 {(index + 1) / total_files * 100:.2f}%，当前文件耗时 {current_file_elapsed_time:.2f} 秒，已运行时间 {total_elapsed_time:.2f} 秒。')

    total_elapsed_time = time.time() - start_time  # 计算总耗时
    print(f'所有文件已处理完成，总耗时 {total_elapsed_time / 60:.2f} 分钟。')

# 配置基本路径和参数
base_path = r'D:\科研\免疫\image'  # NDPI文件所在的基础路径
output_base = r'D:\科研\免疫\extract'  # 输出基础路径
threshold = 50  # patches饱和度阈值
size = 512  # patches的大小
magnification = 20  # 预设放大倍数

# 调用函数以处理NDPI文件
process_ndpi_files(base_path, output_base, saturation_threshold=threshold, patch_size=size, target_magnification=magnification)