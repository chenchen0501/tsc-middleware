"""
批量打印1296个JJG标签脚本
使用 Type 3 (6格批量打印) 通过 HTTP API 调用

标签格式: JJG2025110600001
- JJG: 物品编号
- 20251106: 日期
- 00001: 序号（5位，从00001到01296）
"""
import requests
import time


def generate_jjg_labels() -> list[str]:
    """
    生成JJG标签列表（独立函数，便于移植到其他语言如Java）
    
    标签格式: JJG + 日期(8位) + 序号(5位)
    示例: JJG2025110600001
    
    固定参数:
        prefix: "JJG" - 物品编号前缀
        date: "20251106" - 日期（YYYYMMDD格式）
        start: 1 - 起始序号
        end: 1296 - 结束序号
        serial_length: 5 - 序号位数（不足补0）
        
    Returns:
        标签文本列表，共1296个元素
        
    Java移植说明:
        - 使用String.format("%05d", i)格式化序号
        - 或使用String类的padLeft方法补零
        - 返回类型: List<String>
    """
    # 固定配置
    PREFIX = "JJG"
    DATE = "20251106"
    START = 1
    END = 1296
    SERIAL_LENGTH = 5
    
    # 生成标签列表
    labels = []
    for i in range(START, END + 1):
        # 序号格式化：补零到指定位数
        # Java: String.format("%05d", i)
        serial = str(i).zfill(SERIAL_LENGTH)
        
        # 拼接标签：前缀 + 日期 + 序号
        # Java: String label = PREFIX + DATE + serial;
        label = PREFIX + DATE + serial
        
        labels.append(label)
    
    return labels


class JJGPrinter:
    """JJG标签批量打印器"""
    
    # 实际打印机ip
    def __init__(self, base_url: str = 'http://172.16.10.28:8000'):
        """
        初始化打印器
        
        Args:
            base_url: FastAPI 服务地址
        """
        self.base_url = base_url
        self.print_endpoint = f"{base_url}/print"
    
    def generate_labels(self) -> list[str]:
        """
        生成标签列表（调用独立函数）
        
        Returns:
            标签文本列表
        """
        return generate_jjg_labels()
    
    def print_batch(self, labels: list[str], delay: float = 0.5) -> dict:
        """
        批量打印标签（自动分组，每6个一组）
        
        Args:
            labels: 标签列表
            delay: 每次请求之间的延迟（秒），避免打印机过载
            
        Returns:
            打印统计信息
        """
        total = len(labels)
        batch_size = 6  # Type 3 每张纸6个格子
        batches = (total + batch_size - 1) // batch_size  # 向上取整
        
        # 冷却机制配置
        COOLING_INTERVAL = 50  # 每打印50张，暂停冷却
        COOLING_TIME = 60      # 冷却60秒（30-60秒之间）
        
        # 预估冷却次数和时间
        expected_cooling = batches // COOLING_INTERVAL
        expected_cooling_time = expected_cooling * COOLING_TIME
        
        print(f"{'='*60}")
        print(f"📋 批量打印任务")
        print(f"{'='*60}")
        print(f"标签总数: {total} 个")
        print(f"每张纸: {batch_size} 个格子")
        print(f"打印张数: {batches} 张")
        print(f"服务地址: {self.base_url}")
        print(f"冷却策略: 每 {COOLING_INTERVAL} 张暂停 {COOLING_TIME} 秒")
        if expected_cooling > 0:
            print(f"预计冷却: {expected_cooling} 次（约 {expected_cooling_time} 秒）")
        print(f"{'='*60}\n")
        
        success_count = 0
        failed_count = 0
        failed_batches = []
        cooling_count = 0  # 冷却次数统计
        
        # 分批打印
        for i in range(0, total, batch_size):
            batch_num = i // batch_size + 1
            batch_labels = labels[i:i + batch_size]
            
            print(f"[批次 {batch_num}/{batches}] 打印标签 {i+1}-{min(i+batch_size, total)} ...")
            
            try:
                # 构造请求数据
                request_data = {
                    "type": 3,
                    "print_list": [{"text": label} for label in batch_labels]
                }
                
                # 发送 HTTP POST 请求
                response = requests.post(
                    self.print_endpoint,
                    json=request_data,
                    timeout=30
                )
                
                # 检查响应
                if response.status_code == 200:
                    result = response.json()
                    print(f"  ✅ 成功: {result.get('message', '打印成功')}")
                    success_count += 1
                else:
                    error_detail = response.json().get('detail', '未知错误')
                    print(f"  ❌ 失败: HTTP {response.status_code} - {error_detail}")
                    failed_count += 1
                    failed_batches.append({
                        "batch": batch_num,
                        "labels": batch_labels,
                        "error": error_detail
                    })
                
                # 冷却机制：每打印50张，暂停冷却
                if batch_num % COOLING_INTERVAL == 0 and batch_num < batches:
                    cooling_count += 1
                    print(f"\n{'='*60}")
                    print(f"🌡️  已连续打印 {COOLING_INTERVAL} 张，让打印机冷却...")
                    print(f"⏸️  暂停 {COOLING_TIME} 秒（第 {cooling_count} 次冷却）")
                    print(f"{'='*60}")
                    
                    # 倒计时显示
                    for remaining in range(COOLING_TIME, 0, -5):
                        print(f"   ⏳ 剩余 {remaining} 秒...", end='\r')
                        time.sleep(5)
                    
                    print(f"   ✅ 冷却完成，继续打印...{' '*20}")
                    print(f"{'='*60}\n")
                
                # 正常延迟，避免打印机过载
                elif i + batch_size < total:  # 不是最后一批
                    time.sleep(delay)
                    
            except requests.exceptions.RequestException as e:
                print(f"  ❌ 网络错误: {e}")
                failed_count += 1
                failed_batches.append({
                    "batch": batch_num,
                    "labels": batch_labels,
                    "error": str(e)
                })
            except Exception as e:
                print(f"  ❌ 未知错误: {e}")
                failed_count += 1
                failed_batches.append({
                    "batch": batch_num,
                    "labels": batch_labels,
                    "error": str(e)
                })
        
        # 打印统计
        print(f"\n{'='*60}")
        print(f"📊 打印统计")
        print(f"{'='*60}")
        print(f"成功: {success_count}/{batches} 批次 ({success_count * batch_size} 个标签)")
        print(f"失败: {failed_count}/{batches} 批次")
        if cooling_count > 0:
            print(f"冷却: {cooling_count} 次（共 {cooling_count * COOLING_TIME} 秒）")
        print(f"{'='*60}")
        
        # 如果有失败的批次，显示详情
        if failed_batches:
            print(f"\n⚠️  失败的批次详情:")
            for item in failed_batches:
                print(f"  批次 {item['batch']}: {item['error']}")
                print(f"    标签: {', '.join(item['labels'])}")
        
        return {
            "total": total,
            "batches": batches,
            "success": success_count,
            "failed": failed_count,
            "failed_batches": failed_batches,
            "cooling_count": cooling_count,
            "cooling_time": cooling_count * COOLING_TIME
        }
    
    def check_service(self) -> bool:
        """
        检查打印服务是否可用
        
        Returns:
            服务是否正常运行
        """
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                print(f"✅ 打印服务正常: {self.base_url}")
                return True
            else:
                print(f"❌ 打印服务异常: HTTP {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ 无法连接到打印服务: {e}")
            return False


def main():
    """主函数"""
    # 配置参数
    BASE_URL = 'http://172.16.10.28:8000' # 服务地址
    DELAY = 0.5             # 每次请求间隔（秒）
    
    # 创建打印器
    printer = JJGPrinter(base_url=BASE_URL)
    
    # 检查服务
    print(f"\n🔍 检查打印服务...")
    if not printer.check_service():
        print("\n❌ 错误: 打印服务不可用，请确保 FastAPI 服务已启动")
        print(f"💡 提示: 运行命令启动服务 -> python main.py")
        return
    
    # 生成标签（使用硬编码参数）
    print(f"\n📝 生成标签列表...")
    labels = printer.generate_labels()
    print(f"✅ 已生成 {len(labels)} 个标签")
    print(f"   第一个: {labels[0]}")
    print(f"   最后一个: {labels[-1]}")
    
    # 确认打印
    print(f"\n⚠️  即将打印 {len(labels)} 个标签，共 {(len(labels) + 5) // 6} 张纸")
    confirm = input("是否继续? (y/n): ")
    if confirm.lower() != 'y':
        print("❌ 已取消打印")
        return
    
    # 开始打印
    print(f"\n🖨️  开始批量打印...\n")
    start_time = time.time()
    
    result = printer.print_batch(labels, delay=DELAY)
    
    elapsed_time = time.time() - start_time
    
    # 最终统计
    print(f"\n{'='*60}")
    print(f"✅ 打印任务完成")
    print(f"{'='*60}")
    print(f"总耗时: {elapsed_time:.2f} 秒")
    print(f"成功率: {result['success']}/{result['batches']} ({result['success']/result['batches']*100:.1f}%)")
    print(f"{'='*60}\n")


def test_generate_labels():
    """测试标签生成功能（仅查看，不打印）"""
    print(f"\n{'='*60}")
    print(f"🧪 测试标签生成功能")
    print(f"{'='*60}\n")
    
    # 创建打印器
    printer = JJGPrinter()
    
    # 生成标签（使用硬编码参数）
    print(f"📝 生成标签...")
    print(f"  前缀: JJG")
    print(f"  日期: 20251106")
    print(f"  序号范围: 1 - 1296")
    print()
    
    labels = printer.generate_labels()
    
    # 显示统计
    print(f"✅ 已生成 {len(labels)} 个标签\n")
    
    # 显示前10个
    print(f"📋 前 10 个标签:")
    for i, label in enumerate(labels[:10], 1):
        print(f"  {i:2d}. {label}")
    
    print(f"\n  ... (中间省略 {len(labels) - 20} 个) ...\n")
    
    # 显示后10个
    print(f"📋 后 10 个标签:")
    for i, label in enumerate(labels[-10:], len(labels) - 9):
        print(f"  {i:4d}. {label}")
    
    # 显示分组信息
    batch_size = 6
    batches = (len(labels) + batch_size - 1) // batch_size
    print(f"\n{'='*60}")
    print(f"📊 打印统计（如果执行打印）")
    print(f"{'='*60}")
    print(f"每张纸: {batch_size} 个格子（3行 × 2列）")
    print(f"需要打印: {batches} 张纸")
    print(f"{'='*60}\n")
    
    # 显示几个批次示例
    print(f"📦 前 3 个批次示例（每批次6个标签，打印1张纸）:\n")
    for batch_num in range(3):
        start_idx = batch_num * batch_size
        end_idx = min(start_idx + batch_size, len(labels))
        batch_labels = labels[start_idx:end_idx]
        
        print(f"  批次 {batch_num + 1}:")
        for i, label in enumerate(batch_labels):
            position = ["左上", "右上", "左中", "右中", "左下", "右下"][i]
            print(f"    格子{i+1} ({position}): {label}")
        print()


if __name__ == "__main__":
    import sys
    
    # 如果有命令行参数 --test，则只测试生成功能
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_generate_labels()
    else:
        main()

