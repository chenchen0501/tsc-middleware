"""
TSC-Print-Middleware Python 客户端示例

展示如何使用 Python 调用打印中间件的各种功能
"""
import requests
from typing import List, Dict, Any

# 服务地址配置
BASE_URL = "http://localhost:8000"


class TSCPrintClient:
    """TSC 打印客户端封装"""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
    
    def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        response = requests.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()
    
    def test_connection(self) -> Dict[str, Any]:
        """测试打印机连接"""
        response = requests.post(f"{self.base_url}/test")
        response.raise_for_status()
        return response.json()
    
    def print_single_text(self, text_list: List[str]) -> Dict[str, Any]:
        """
        单行文本打印
        
        Args:
            text_list: 文本列表，如 ["物料1", "物料2"]
        
        Returns:
            打印结果
        """
        response = requests.post(f"{self.base_url}/print", json={
            "template": "single-text",
            "print_list": [{"text": text} for text in text_list]
        })
        response.raise_for_status()
        return response.json()
    
    def print_double_text(self, text_pairs: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        双行文本打印（每张纸两行）
        
        Args:
            text_pairs: 文本对列表，如 [{"text1": "第一行", "text2": "第二行"}]
        
        Returns:
            打印结果
        """
        response = requests.post(f"{self.base_url}/print", json={
            "template": "double-text",
            "print_list": text_pairs
        })
        response.raise_for_status()
        return response.json()
    
    def print_qrcode(self, items: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        二维码+文本打印
        
        Args:
            items: 二维码列表，如 [{"qrcode": "url", "text": "文本"}]
        
        Returns:
            打印结果
        """
        response = requests.post(f"{self.base_url}/print", json={
            "template": "qrcode-with-text",
            "print_list": items
        })
        response.raise_for_status()
        return response.json()
    
    def print_barcode(self, items: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        条形码+文本打印
        
        Args:
            items: 条形码列表，如 [{"barcode": "123456", "text": "文本"}]
        
        Returns:
            打印结果
        """
        response = requests.post(f"{self.base_url}/print", json={
            "template": "barcode-with-text",
            "print_list": items
        })
        response.raise_for_status()
        return response.json()
    
    def print_custom(self, elements: List[Dict[str, Any]], qty: int = 1, 
                     width: int = None, height: int = None) -> Dict[str, Any]:
        """
        自定义布局打印
        
        Args:
            elements: 元素列表
            qty: 打印数量
            width: 标签宽度(mm)
            height: 标签高度(mm)
        
        Returns:
            打印结果
        """
        layout = {"elements": elements}
        if width:
            layout["width"] = width
        if height:
            layout["height"] = height
        
        response = requests.post(f"{self.base_url}/print", json={
            "template": "custom",
            "layout": layout,
            "qty": qty
        })
        response.raise_for_status()
        return response.json()


def example_1_single_text():
    """示例1: 单行文本打印"""
    print("\n=== 示例1: 单行文本打印 ===")
    
    client = TSCPrintClient()
    
    # 打印3个单行文本标签
    result = client.print_single_text([
        "物料编号: A12345",
        "产品名称: 测试产品",
        "库存位置: A-01-01"
    ])
    
    print(f"✅ {result['message']}")


def example_2_double_text():
    """示例2: 双行文本打印"""
    print("\n=== 示例2: 双行文本打印 ===")
    
    client = TSCPrintClient()
    
    # 每张纸打印两行文本
    result = client.print_double_text([
        {"text1": "物料A-盖子-批次001"},
        {"text2": "物料B-底座-批次002"},
        {"text1": "物料C-配件-批次003"}
    ])
    
    print(f"✅ {result['message']}")


def example_3_qrcode():
    """示例3: 二维码打印"""
    print("\n=== 示例3: 二维码+文本打印 ===")
    
    client = TSCPrintClient()
    
    # 打印产品二维码
    result = client.print_qrcode([
        {
            "qrcode": "https://example.com/product/12345",
            "text": "产品编号: 12345"
        },
        {
            "qrcode": "https://example.com/product/67890",
            "text": "产品编号: 67890"
        }
    ])
    
    print(f"✅ {result['message']}")


def example_4_barcode():
    """示例4: 条形码打印"""
    print("\n=== 示例4: 条形码+文本打印 ===")
    
    client = TSCPrintClient()
    
    # 打印订单条形码
    result = client.print_barcode([
        {
            "barcode": "1234567890",
            "text": "订单号: 1234567890"
        },
        {
            "barcode": "9876543210",
            "text": "订单号: 9876543210"
        }
    ])
    
    print(f"✅ {result['message']}")


def example_5_custom_simple():
    """示例5: 自定义布局 - 简单版"""
    print("\n=== 示例5: 自定义布局（简单）===")
    
    client = TSCPrintClient()
    
    # 自定义标题 + 二维码 + 文本
    elements = [
        {
            "type": "text",
            "x": 100,
            "y": 100,
            "text": "库存盘点标签",
            "font_size": 56,
            "font_name": "宋体"
        },
        {
            "type": "qrcode",
            "x": 300,
            "y": 300,
            "content": "https://example.com/inventory/A12345",
            "size": 10
        },
        {
            "type": "text",
            "x": 200,
            "y": 650,
            "text": "编号: A12345",
            "font_size": 40
        }
    ]
    
    result = client.print_custom(elements, qty=1)
    print(f"✅ {result['message']}")


def example_6_custom_complex():
    """示例6: 自定义布局 - 复杂版"""
    print("\n=== 示例6: 自定义布局（复杂）===")
    
    client = TSCPrintClient()
    
    # 组合：标题 + 二维码 + 条形码 + 多行文本
    elements = [
        # 标题
        {
            "type": "text",
            "x": 300,
            "y": 50,
            "text": "产品标签",
            "font_size": 48,
            "font_name": "宋体"
        },
        # 二维码（左侧）
        {
            "type": "qrcode",
            "x": 100,
            "y": 200,
            "content": "https://example.com/product/ABC123",
            "size": 8
        },
        # 产品信息（右侧）
        {
            "type": "text",
            "x": 450,
            "y": 200,
            "text": "产品名称: 智能设备",
            "font_size": 32
        },
        {
            "type": "text",
            "x": 450,
            "y": 260,
            "text": "型号: ABC-123",
            "font_size": 32
        },
        {
            "type": "text",
            "x": 450,
            "y": 320,
            "text": "生产日期: 2024-10-30",
            "font_size": 28
        },
        # 条形码（底部）
        {
            "type": "barcode",
            "x": 200,
            "y": 600,
            "content": "ABC123456",
            "height": 80,
            "barcode_type": "128"
        }
    ]
    
    result = client.print_custom(elements, qty=1)
    print(f"✅ {result['message']}")


def example_7_batch_printing():
    """示例7: 批量打印"""
    print("\n=== 示例7: 批量打印 ===")
    
    client = TSCPrintClient()
    
    # 批量打印10个二维码标签
    items = [
        {
            "qrcode": f"https://example.com/product/{i:05d}",
            "text": f"产品编号: {i:05d}"
        }
        for i in range(1, 11)
    ]
    
    result = client.print_qrcode(items)
    print(f"✅ {result['message']}")


def example_8_error_handling():
    """示例8: 错误处理"""
    print("\n=== 示例8: 错误处理 ===")
    
    client = TSCPrintClient()
    
    try:
        # 测试打印机连接
        result = client.test_connection()
        print(f"✅ 打印机连接正常: {result['message']}")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 503:
            print("❌ 打印机连接失败，请检查：")
            print("   1. 打印机是否通过USB连接")
            print("   2. 打印机电源是否开启")
            print("   3. Windows设备管理器是否识别打印机")
        else:
            print(f"❌ 错误: {e.response.json()}")
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到打印服务，请确认服务是否启动")


def main():
    """主函数 - 运行所有示例"""
    print("=" * 60)
    print("TSC-Print-Middleware Python 客户端示例")
    print("=" * 60)
    
    # 健康检查
    try:
        client = TSCPrintClient()
        health = client.health_check()
        print(f"\n✅ 服务状态: {health['status']}")
    except Exception as e:
        print(f"\n❌ 服务未启动或连接失败: {e}")
        print("\n请先启动服务: python main.py")
        return
    
    # 运行所有示例
    examples = [
        example_1_single_text,
        example_2_double_text,
        example_3_qrcode,
        example_4_barcode,
        example_5_custom_simple,
        example_6_custom_complex,
        example_7_batch_printing,
        example_8_error_handling
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"❌ 执行失败: {e}")
    
    print("\n" + "=" * 60)
    print("所有示例执行完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()

