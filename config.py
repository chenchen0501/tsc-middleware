"""
配置文件
"""
import os

# 打印机配置
PRINTER_IP = os.getenv("PRINTER_IP", "192.168.1.100")  # 默认打印机IP地址

# 标签默认配置
DEFAULT_WIDTH = "100"  # 标签宽度(mm)
DEFAULT_HEIGHT = "90"  # 标签高度(mm)

