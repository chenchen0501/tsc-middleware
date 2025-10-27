"""
TSC 打印机连接诊断脚本
用于排查 openport 错误
"""
import sys
import traceback
from tsclib import TSCPrinter


def test_usb_connection():
    """测试 USB 连接（参数为整数）"""
    print("\n" + "="*60)
    print("测试 1: USB 连接 - 传递整数参数 0")
    print("="*60)
    
    p = TSCPrinter()
    try:
        print("调用: p.open_port(0)")
        result = p.open_port(0)
        print(f"✅ 成功! 返回值: {result}")
        p.close_port()
        return True
    except Exception as e:
        print(f"❌ 失败!")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {e}")
        if hasattr(e, "ToString"):
            print(f"详细错误 (.NET): {e.ToString()}")
        print("\n完整堆栈:")
        traceback.print_exc()
        return False


def test_network_as_string():
    """测试网络连接（参数为字符串 IP:端口）"""
    print("\n" + "="*60)
    print("测试 2: 网络连接 - 传递字符串参数 '192.168.1.100:9100'")
    print("="*60)
    
    p = TSCPrinter()
    try:
        print("调用: p.open_port('192.168.1.100:9100')")
        result = p.open_port("192.168.1.100:9100")
        print(f"✅ 成功! 返回值: {result}")
        p.close_port()
        return True
    except Exception as e:
        print(f"❌ 失败!")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {e}")
        if hasattr(e, "ToString"):
            print(f"详细错误 (.NET): {e.ToString()}")
        print("\n完整堆栈:")
        traceback.print_exc()
        return False


def test_list_printers():
    """测试列出打印机"""
    print("\n" + "="*60)
    print("测试 3: 列出可用打印机")
    print("="*60)
    
    p = TSCPrinter()
    try:
        print("调用: p.list_printers()")
        printers = p.list_printers()
        
        if printers:
            print(f"✅ 找到 {len(printers)} 台打印机:")
            for i, printer in enumerate(printers):
                print(f"\n  打印机 {i}:")
                print(f"    驱动名称: {printer['friendly_name']}")
                print(f"    索引: {printer['index']}")
        else:
            print("⚠️  未找到 USB 打印机")
        
        return True
    except Exception as e:
        print(f"❌ 失败!")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {e}")
        print("\n完整堆栈:")
        traceback.print_exc()
        return False


def test_driver_name():
    """测试使用驱动名称连接"""
    print("\n" + "="*60)
    print("测试 4: 使用驱动名称连接")
    print("="*60)
    
    p = TSCPrinter()
    
    # 先获取打印机列表
    try:
        printers = p.list_printers()
        if not printers:
            print("⚠️  跳过: 未找到 USB 打印机")
            return False
        
        driver_name = printers[0]['friendly_name']
        print(f"调用: p.open_port('{driver_name}')")
        
        result = p.open_port(driver_name)
        print(f"✅ 成功! 返回值: {result}")
        p.close_port()
        return True
    except Exception as e:
        print(f"❌ 失败!")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {e}")
        if hasattr(e, "ToString"):
            print(f"详细错误 (.NET): {e.ToString()}")
        print("\n完整堆栈:")
        traceback.print_exc()
        return False


def check_environment():
    """检查运行环境"""
    print("\n" + "="*60)
    print("环境信息")
    print("="*60)
    print(f"Python 版本: {sys.version}")
    print(f"操作系统: {sys.platform}")
    
    try:
        import clr
        print(f"pythonnet 已加载: ✅")
        
        # 尝试获取 .NET 运行时信息
        try:
            from System import Environment
            print(f".NET 版本: {Environment.Version}")
        except:
            print(f".NET 版本: 无法获取")
    except ImportError:
        print(f"pythonnet 未加载: ❌")


def main():
    """主函数"""
    print("\n" + "="*60)
    print("  TSC 打印机连接诊断工具")
    print("="*60)
    
    check_environment()
    
    print("\n\n" + "🔍 开始诊断测试..." + "\n")
    
    results = []
    
    # 测试 3: 列出打印机（不需要连接，先执行）
    results.append(("列出打印机", test_list_printers()))
    
    # 测试 1: USB 整数参数
    results.append(("USB连接(整数)", test_usb_connection()))
    
    # 测试 4: 驱动名称
    results.append(("驱动名称连接", test_driver_name()))
    
    # 测试 2: 网络字符串参数
    results.append(("网络连接(字符串)", test_network_as_string()))
    
    # 输出总结
    print("\n\n" + "="*60)
    print("诊断结果总结")
    print("="*60)
    
    for test_name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{test_name:20s}: {status}")
    
    print("\n" + "="*60)
    
    # 给出建议
    print("\n💡 建议:")
    if results[0][1]:  # 如果列出打印机成功
        print("  ✓ 可以成功列出打印机，说明库加载正常")
    
    if results[1][1]:  # 如果 USB 连接成功
        print("  ✓ USB 连接正常，建议使用 USB 模式")
        print("    使用: p.open_port(0)")
    elif not results[1][1]:
        print("  ✗ USB 连接失败")
        print("    可能原因: 1) 打印机未连接 2) 驱动未安装 3) 权限不足")
    
    if results[3][1]:  # 如果网络连接成功
        print("  ✓ 网络连接正常")
        print("    使用: p.open_port('IP:9100')")
    elif not results[3][1]:
        print("  ✗ 网络连接失败")
        print("    可能原因: 1) 打印机IP不可达 2) TSCSDK.node_usb 不支持网络")
        print("    建议: 使用 USB 连接代替")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 用户中断")
    except Exception as e:
        print(f"\n❌ 诊断脚本执行出错: {e}")
        traceback.print_exc()

