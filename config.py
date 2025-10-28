"""
配置文件（USB模式）
"""

# 标签默认配置（打印区域）
DEFAULT_WIDTH = "100"   # 标签宽度(mm) - 10cm
DEFAULT_HEIGHT = "80"   # 标签高度(mm) - 8cm

# 打印机DPI设置（用于坐标转换）
# TTE-344 是 300 DPI 打印机: 11.81 dots/mm
# 常见TSC打印机DPI:
#   - TTP-244/247 (203 DPI): 8.0 dots/mm
#   - TTE-344/345 (300 DPI): 11.81 dots/mm
#   - TTP-644 (600 DPI): 23.62 dots/mm
DPI_RATIO = 11.81  # dots per mm (TTE-344 = 300 DPI)


# 注意：已改为USB连接模式，无需配置IP地址

