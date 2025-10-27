"""
列出所有连接的 TSC USB 打印机信息
用于确定打印机的驱动名称
"""
from tsclib import TSCPrinter


def main():
    """列出所有可用的 TSC USB 打印机"""
    print("=" * 60)
    print("正在扫描 TSC USB 打印机...")
    print("=" * 60)
    
    try:
        p = TSCPrinter()
        printers = p.list_printers()
        
        if printers:
            print(f"\n✅ 找到 {len(printers)} 台打印机：\n")
            
            for i, printer in enumerate(printers):
                print(f"📌 打印机 {i + 1}:")
                print(f"   驱动名称 (FriendlyName): {printer['friendly_name']}")
                print(f"   描述 (Description):      {printer['description']}")
                print(f"   制造商 (Manufacturer):   {printer['manufacturer']}")
                print(f"   设备索引 (Index):        {printer['index']}")
                print(f"   VID: {printer['vid']}  |  PID: {printer['pid']}")
                print(f"   设备路径: {printer['device_path']}")
                print()
                
            print("=" * 60)
            print("💡 提示：")
            print("   - 可以使用 '驱动名称' 作为 open_port() 的参数")
            print("   - 例如: p.open_port('TSC TTP-247')")
            print("   - 或使用索引: p.open_port(0) 表示第一台打印机")
            print("=" * 60)
        else:
            print("\n❌ 未找到 USB 打印机")
            print("\n请检查：")
            print("   1. 打印机是否已通过 USB 连接到电脑")
            print("   2. 打印机电源是否已打开")
            print("   3. 打印机驱动是否已正确安装")
            
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        print("\n可能的原因：")
        print("   1. tsclib 库未正确加载")
        print("   2. 缺少必要的运行时环境（Windows 需要 .NET，macOS 需要 Mono）")
        print("   3. 打印机 USB 连接问题")


if __name__ == "__main__":
    main()

