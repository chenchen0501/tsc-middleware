"""
配置文件（USB模式）
"""

# 标签默认配置（打印区域）
DEFAULT_WIDTH = "100"   # 标签宽度(mm) - 10cm
DEFAULT_HEIGHT = "80"   # 标签高度(mm) - 8cm

# 打印机DPI设置（用于坐标转换）
# TSC打印机标准: 203 DPI (8 dots/mm)
# 如果打印区域偏小，可尝试: 7.87 或 7.5
# 如果打印区域偏大，可尝试: 8.5 或 9.0
DPI_RATIO = 8.0  # dots per mm

# 注意：已改为USB连接模式，无需配置IP地址

