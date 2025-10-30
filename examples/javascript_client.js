/**
 * TSC-Print-Middleware JavaScript 客户端示例
 * 
 * 展示如何使用 JavaScript/Node.js 调用打印中间件的各种功能
 * 
 * 安装依赖: npm install axios
 * 运行示例: node javascript_client.js
 */

const axios = require('axios');

// 服务地址配置
const BASE_URL = 'http://localhost:8000';

/**
 * TSC 打印客户端类
 */
class TSCPrintClient {
  constructor(baseUrl = BASE_URL) {
    this.baseUrl = baseUrl;
    this.client = axios.create({
      baseURL: baseUrl,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json'
      }
    });
  }

  /**
   * 健康检查
   */
  async healthCheck() {
    const response = await this.client.get('/health');
    return response.data;
  }

  /**
   * 测试打印机连接
   */
  async testConnection() {
    const response = await this.client.post('/test');
    return response.data;
  }

  /**
   * 单行文本打印
   * @param {string[]} textList - 文本列表
   */
  async printSingleText(textList) {
    const response = await this.client.post('/print', {
      template: 'single-text',
      print_list: textList.map(text => ({ text }))
    });
    return response.data;
  }

  /**
   * 双行文本打印
   * @param {Array<{text1: string, text2?: string}>} textPairs - 文本对列表
   */
  async printDoubleText(textPairs) {
    const response = await this.client.post('/print', {
      template: 'double-text',
      print_list: textPairs
    });
    return response.data;
  }

  /**
   * 二维码+文本打印
   * @param {Array<{qrcode: string, text: string}>} items - 二维码列表
   */
  async printQRCode(items) {
    const response = await this.client.post('/print', {
      template: 'qrcode-with-text',
      print_list: items
    });
    return response.data;
  }

  /**
   * 条形码+文本打印
   * @param {Array<{barcode: string, text: string}>} items - 条形码列表
   */
  async printBarcode(items) {
    const response = await this.client.post('/print', {
      template: 'barcode-with-text',
      print_list: items
    });
    return response.data;
  }

  /**
   * 自定义布局打印
   * @param {Array} elements - 元素列表
   * @param {number} qty - 打印数量
   * @param {number} width - 标签宽度(mm)
   * @param {number} height - 标签高度(mm)
   */
  async printCustom(elements, qty = 1, width = null, height = null) {
    const layout = { elements };
    if (width) layout.width = width;
    if (height) layout.height = height;

    const response = await this.client.post('/print', {
      template: 'custom',
      layout,
      qty
    });
    return response.data;
  }
}

/**
 * 示例1: 单行文本打印
 */
async function example1SingleText() {
  console.log('\n=== 示例1: 单行文本打印 ===');

  const client = new TSCPrintClient();

  // 打印3个单行文本标签
  const result = await client.printSingleText([
    '物料编号: A12345',
    '产品名称: 测试产品',
    '库存位置: A-01-01'
  ]);

  console.log(`✅ ${result.message}`);
}

/**
 * 示例2: 双行文本打印
 */
async function example2DoubleText() {
  console.log('\n=== 示例2: 双行文本打印 ===');

  const client = new TSCPrintClient();

  // 每张纸打印两行文本
  const result = await client.printDoubleText([
    { text1: '物料A-盖子-批次001' },
    { text2: '物料B-底座-批次002' },
    { text1: '物料C-配件-批次003' }
  ]);

  console.log(`✅ ${result.message}`);
}

/**
 * 示例3: 二维码打印
 */
async function example3QRCode() {
  console.log('\n=== 示例3: 二维码+文本打印 ===');

  const client = new TSCPrintClient();

  // 打印产品二维码
  const result = await client.printQRCode([
    {
      qrcode: 'https://example.com/product/12345',
      text: '产品编号: 12345'
    },
    {
      qrcode: 'https://example.com/product/67890',
      text: '产品编号: 67890'
    }
  ]);

  console.log(`✅ ${result.message}`);
}

/**
 * 示例4: 条形码打印
 */
async function example4Barcode() {
  console.log('\n=== 示例4: 条形码+文本打印 ===');

  const client = new TSCPrintClient();

  // 打印订单条形码
  const result = await client.printBarcode([
    {
      barcode: '1234567890',
      text: '订单号: 1234567890'
    },
    {
      barcode: '9876543210',
      text: '订单号: 9876543210'
    }
  ]);

  console.log(`✅ ${result.message}`);
}

/**
 * 示例5: 自定义布局 - 简单版
 */
async function example5CustomSimple() {
  console.log('\n=== 示例5: 自定义布局（简单）===');

  const client = new TSCPrintClient();

  // 自定义标题 + 二维码 + 文本
  const elements = [
    {
      type: 'text',
      x: 100,
      y: 100,
      text: '库存盘点标签',
      font_size: 56,
      font_name: '宋体'
    },
    {
      type: 'qrcode',
      x: 300,
      y: 300,
      content: 'https://example.com/inventory/A12345',
      size: 10
    },
    {
      type: 'text',
      x: 200,
      y: 650,
      text: '编号: A12345',
      font_size: 40
    }
  ];

  const result = await client.printCustom(elements, 1);
  console.log(`✅ ${result.message}`);
}

/**
 * 示例6: 自定义布局 - 复杂版
 */
async function example6CustomComplex() {
  console.log('\n=== 示例6: 自定义布局（复杂）===');

  const client = new TSCPrintClient();

  // 组合：标题 + 二维码 + 条形码 + 多行文本
  const elements = [
    // 标题
    {
      type: 'text',
      x: 300,
      y: 50,
      text: '产品标签',
      font_size: 48,
      font_name: '宋体'
    },
    // 二维码（左侧）
    {
      type: 'qrcode',
      x: 100,
      y: 200,
      content: 'https://example.com/product/ABC123',
      size: 8
    },
    // 产品信息（右侧）
    {
      type: 'text',
      x: 450,
      y: 200,
      text: '产品名称: 智能设备',
      font_size: 32
    },
    {
      type: 'text',
      x: 450,
      y: 260,
      text: '型号: ABC-123',
      font_size: 32
    },
    {
      type: 'text',
      x: 450,
      y: 320,
      text: '生产日期: 2024-10-30',
      font_size: 28
    },
    // 条形码（底部）
    {
      type: 'barcode',
      x: 200,
      y: 600,
      content: 'ABC123456',
      height: 80,
      barcode_type: '128'
    }
  ];

  const result = await client.printCustom(elements, 1);
  console.log(`✅ ${result.message}`);
}

/**
 * 示例7: 批量打印
 */
async function example7BatchPrinting() {
  console.log('\n=== 示例7: 批量打印 ===');

  const client = new TSCPrintClient();

  // 批量打印10个二维码标签
  const items = Array.from({ length: 10 }, (_, i) => ({
    qrcode: `https://example.com/product/${String(i + 1).padStart(5, '0')}`,
    text: `产品编号: ${String(i + 1).padStart(5, '0')}`
  }));

  const result = await client.printQRCode(items);
  console.log(`✅ ${result.message}`);
}

/**
 * 示例8: 错误处理
 */
async function example8ErrorHandling() {
  console.log('\n=== 示例8: 错误处理 ===');

  const client = new TSCPrintClient();

  try {
    // 测试打印机连接
    const result = await client.testConnection();
    console.log(`✅ 打印机连接正常: ${result.message}`);
  } catch (error) {
    if (error.response) {
      if (error.response.status === 503) {
        console.log('❌ 打印机连接失败，请检查：');
        console.log('   1. 打印机是否通过USB连接');
        console.log('   2. 打印机电源是否开启');
        console.log('   3. Windows设备管理器是否识别打印机');
      } else {
        console.log(`❌ 错误: ${error.response.data.detail}`);
      }
    } else if (error.code === 'ECONNREFUSED') {
      console.log('❌ 无法连接到打印服务，请确认服务是否启动');
    } else {
      console.log(`❌ 未知错误: ${error.message}`);
    }
  }
}

/**
 * 主函数 - 运行所有示例
 */
async function main() {
  console.log('='.repeat(60));
  console.log('TSC-Print-Middleware JavaScript 客户端示例');
  console.log('='.repeat(60));

  // 健康检查
  try {
    const client = new TSCPrintClient();
    const health = await client.healthCheck();
    console.log(`\n✅ 服务状态: ${health.status}`);
  } catch (error) {
    console.log(`\n❌ 服务未启动或连接失败: ${error.message}`);
    console.log('\n请先启动服务: python main.py');
    return;
  }

  // 运行所有示例
  const examples = [
    example1SingleText,
    example2DoubleText,
    example3QRCode,
    example4Barcode,
    example5CustomSimple,
    example6CustomComplex,
    example7BatchPrinting,
    example8ErrorHandling
  ];

  for (const example of examples) {
    try {
      await example();
    } catch (error) {
      console.log(`❌ 执行失败: ${error.message}`);
    }
  }

  console.log('\n' + '='.repeat(60));
  console.log('所有示例执行完成！');
  console.log('='.repeat(60));
}

// 运行主函数
if (require.main === module) {
  main().catch(error => {
    console.error('程序执行出错:', error);
    process.exit(1);
  });
}

// 导出供其他模块使用
module.exports = { TSCPrintClient };

