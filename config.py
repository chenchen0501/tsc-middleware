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

# 打印样式参数
PRINT_MARGIN = 10  # 打印边距 (dots)，与边框测试保持一致

# Type 1 参数（批量纯文本打印）
TYPE1_FONT_HEIGHT = 56  # 字体高度 (dots)
TYPE1_FONT_NAME = "宋体"  # 字体名称

# Type 2 参数（二维码+文本打印）
TYPE2_FONT_HEIGHT = 48  # 字体高度 (dots)
TYPE2_FONT_NAME = "宋体"  # 字体名称
TYPE2_QR_SIZE = 12  # 二维码单元宽度 (1-10)，10为最大
TYPE2_QR_SPACING = 24  # 二维码与文本间距 (dots)，约2mm

# Type 3 参数（6格二维码+文本打印，每格左侧二维码+右侧文本）
TYPE3_FONT_HEIGHT = 28  # 字体高度 (dots)，适配小格子
TYPE3_FONT_NAME = "宋体"  # 字体名称
TYPE3_QR_SIZE = 5  # 二维码单元宽度 (1-10)，适配小格子
TYPE3_QR_TEXT_SPACING = 10  # 二维码与文本间距 (dots)，约1mm

# UTF-8 Fallback 配置
# 可选字体: "TSS24.BF2", "5", "KAIU.TTF", "宋体"
UTF8_FONT_NAME = "5"  # 内置支持中文的字体（5是TSC内置中文字体编号）
UTF8_FONT_BASE_HEIGHT = 24  # 字体基础高度 (dots)
UTF8_FORCE_CHARACTERS = {"【", "】"}  # 需要强制使用 UTF-8 打印的字符

# 字符替换映射（如果 UTF-8 模式不可用，使用此映射替换特殊字符）
CHAR_REPLACEMENT_MAP = {
    "【": "[",  # 全角左方括号 → 半角左方括号
    "】": "]",  # 全角右方括号 → 半角右方括号
}

# UTF-8 模式开关（如果 UTF-8 打印不工作，可设置为 False 使用字符替换模式）
USE_UTF8_MODE = False  # 设为 False 则使用字符替换而非 UTF-8 打印（推荐）

# 注意：已改为USB连接模式，无需配置IP地址

