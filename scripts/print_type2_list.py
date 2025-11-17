"""
Type 2 批量打印脚本
接受固定列表，通过 HTTP API 调用打印服务
每次打印1个标签
"""
import requests
import time


# ============================================
# 在这里直接写死要打印的列表，后续直接替换
# ============================================
PRINT_LIST = [
 "CABINET0002-1",
"CABINET0002-2",
"CABINET0002-3",
"CABINET0001-1",
"CABINET0001-2",
"CABINET0001-3",
"CABINET0003-1",
"CABINET0003-2",
"CABINET0003-3",
"CABINET0004-1",
"CABINET0004-2",
"CABINET0004-3",
"CABINET0005-1",
"CABINET0005-2",
"CABINET0005-3",
"CABINET0006-1",
"CABINET0006-2",
"CABINET0006-3",
"CABINET0007-1",
"CABINET0007-2",
"CABINET0007-3",
"CABINET0008-1",
"CABINET0008-2",
"CABINET0008-3",
"CABINET0009-1",
"CABINET0009-2",
"CABINET0009-3",
"CABINET0010-1",
"CABINET0010-2",
"CABINET0010-3",
"CABINET0011-1",
"CABINET0011-2",
"CABINET0011-3",
"CABINET0012-1",
"CABINET0012-2",
"CABINET0012-3",
"CABINET0013-1",
"CABINET0013-2",
"CABINET0013-3",
"CABINET0014-1",
"CABINET0014-2",
"CABINET0014-3",
"CABINET0015-1",
"CABINET0015-2",
"CABINET0015-3",
"CABINET0016-1",
"CABINET0016-2",
"CABINET0016-3",
"CABINET0017-1",
"CABINET0017-2",
"CABINET0017-3",
"CABINET0018-1",
"CABINET0018-2",
"CABINET0018-3",
]


class Type2Printer:
    """Type2 批量打印器"""

    def __init__(self, base_url: str = 'http://172.16.10.28:8000'):
        """
        初始化打印器

        Args:
            base_url: FastAPI 服务地址
        """
        self.base_url = base_url
        self.print_endpoint = f"{base_url}/print"

    def print_batch(self, labels: list[str], delay: float = 0.5) -> dict:
        """
        批量打印标签（每次1个）

        Args:
            labels: 标签列表
            delay: 每次请求之间的延迟（秒）

        Returns:
            打印统计信息
        """
        total = len(labels)

        # 冷却机制配置
        COOLING_INTERVAL = 50
        COOLING_TIME = 60

        expected_cooling = total // COOLING_INTERVAL

        print(f"{'='*60}")
        print(f"📋 批量打印任务 (Type 2)")
        print(f"{'='*60}")
        print(f"标签总数: {total} 个")
        print(f"打印张数: {total} 张")
        print(f"服务地址: {self.base_url}")
        if expected_cooling > 0:
            print(f"预计冷却: {expected_cooling} 次")
        print(f"{'='*60}\n")

        success_count = 0
        failed_count = 0
        failed_labels = []
        cooling_count = 0

        for i, label in enumerate(labels, 1):
            print(f"[{i}/{total}] 打印: {label} ...")

            try:
                request_data = {
                    "type": 2,
                    "print_list": [{"text": label, "qr_content": label}]
                }

                response = requests.post(
                    self.print_endpoint,
                    json=request_data,
                    timeout=30
                )

                if response.status_code == 200:
                    result = response.json()
                    print(f"  ✅ 成功: {result.get('message', '打印成功')}")
                    success_count += 1
                else:
                    error_detail = response.json().get('detail', '未知错误')
                    print(f"  ❌ 失败: HTTP {response.status_code} - {error_detail}")
                    failed_count += 1
                    failed_labels.append({
                        "index": i,
                        "label": label,
                        "error": error_detail
                    })

                # 冷却机制
                if i % COOLING_INTERVAL == 0 and i < total:
                    cooling_count += 1
                    print(f"\n🌡️  冷却中... 暂停 {COOLING_TIME} 秒")
                    for remaining in range(COOLING_TIME, 0, -5):
                        print(f"   ⏳ 剩余 {remaining} 秒...", end='\r')
                        time.sleep(5)
                    print(f"   ✅ 冷却完成{' '*20}")
                elif i < total:
                    time.sleep(delay)

            except requests.exceptions.RequestException as e:
                print(f"  ❌ 网络错误: {e}")
                failed_count += 1
                failed_labels.append({
                    "index": i,
                    "label": label,
                    "error": str(e)
                })
            except Exception as e:
                print(f"  ❌ 未知错误: {e}")
                failed_count += 1
                failed_labels.append({
                    "index": i,
                    "label": label,
                    "error": str(e)
                })

        print(f"\n{'='*60}")
        print(f"📊 打印统计")
        print(f"{'='*60}")
        print(f"成功: {success_count}/{total} 个")
        print(f"失败: {failed_count}/{total} 个")
        print(f"{'='*60}")

        if failed_labels:
            print(f"\n⚠️  失败的标签:")
            for item in failed_labels:
                print(f"  [{item['index']}] {item['label']}: {item['error']}")

        return {
            "total": total,
            "success": success_count,
            "failed": failed_count,
            "failed_labels": failed_labels
        }

    def check_service(self) -> bool:
        """检查打印服务是否可用"""
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
    BASE_URL = 'http://172.16.10.28:8000'
    DELAY = 0.5

    printer = Type2Printer(base_url=BASE_URL)

    print(f"\n🔍 检查打印服务...")
    if not printer.check_service():
        print("\n❌ 打印服务不可用")
        return

    labels = PRINT_LIST
    print(f"\n📝 待打印标签: {len(labels)} 个")
    if labels:
        print(f"   第一个: {labels[0]}")
        print(f"   最后一个: {labels[-1]}")

    print(f"\n⚠️  即将打印 {len(labels)} 个标签，共 {len(labels)} 张纸")
    confirm = input("是否继续? (y/n): ")
    if confirm.lower() != 'y':
        print("❌ 已取消打印")
        return

    print(f"\n🖨️  开始打印...\n")
    start_time = time.time()

    result = printer.print_batch(labels, delay=DELAY)

    elapsed_time = time.time() - start_time

    print(f"\n✅ 完成，耗时: {elapsed_time:.2f} 秒")
    if result['total'] > 0:
        print(f"成功率: {result['success']/result['total']*100:.1f}%")


if __name__ == "__main__":
    main()
