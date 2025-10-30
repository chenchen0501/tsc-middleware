# 🖨️ TSC-Print-Middleware

> **Zero-Driver TSC Printer USB Middleware** - Template-Based Printing | RESTful API | Ready to Use

English | [简体中文](README.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.120-green.svg)](https://fastapi.tiangolo.com/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

---

TSC-Print-Middleware is a **zero-driver USB printing middleware** for **TSC thermal label printers**. Built with **Python** and **FastAPI**, it provides a **RESTful API** for **template-based label printing** including **text**, **barcodes**, and **QR codes**. No driver installation required - direct **USB communication**. Perfect for **warehouse management**, **inventory systems**, **logistics automation**, and **asset labeling** on **Windows** platforms.

**Tech Stack**: Python 3.10+ | FastAPI 0.120 | USB Communication | TSPL Protocol | Template Engine

---

## ✨ Features

- 🚀 **Zero-Driver** - No driver installation required, direct USB communication
- 🎨 **Template System** - 5 preset templates + fully customizable layouts
- 🌐 **RESTful API** - Standard HTTP interface powered by FastAPI
- 🇨🇳 **Perfect Chinese Support** - Windows SimSun font library
- 📦 **Ready to Use** - One-command pip install
- 🔧 **Highly Flexible** - From simple to complex, meets all needs

---

## 🎯 Use Cases

- ✅ Warehouse material label printing
- ✅ Product barcode/QR code printing
- ✅ Shipping label printing
- ✅ Asset management labels
- ✅ Inventory count labels

---

## 🚀 Quick Start

### Requirements

- **OS**: Windows 10/11
- **Python**: 3.10 or higher
- **Printer**: TSC series printer (USB connection)
- **Dependencies**: VC2015-2022 x86 Runtime

### Installation

#### 1. Clone Repository

```bash
git clone https://github.com/your-username/TSC-Print-Middleware.git
cd TSC-Print-Middleware
```

#### 2. Create Virtual Environment

```cmd
python -m venv venv
venv\Scripts\activate
```

#### 3. Install Dependencies

```cmd
pip install -r requirements.txt
```

#### 4. Start Service

```cmd
python main.py
```

Service will start at `http://localhost:8000`

Visit http://localhost:8000/docs for interactive API documentation 📖

---

## 📚 Template System

TSC-Print-Middleware provides **5 printing templates** from simple to complex.

### 1️⃣ single-text - Single Line Text

Single line text centered horizontally and vertically

```python
import requests

requests.post("http://localhost:8000/print", json={
    "template": "single-text",
    "print_list": [
        {"text": "Material No: A12345"}
    ]
})
```

### 2️⃣ double-text - Double Line Text

Two lines of text per sheet (top and bottom layout)

```python
requests.post("http://localhost:8000/print", json={
    "template": "double-text",
    "print_list": [
        {"text1": "First line text"},
        {"text2": "Second line text"}
    ]
})
```

### 3️⃣ qrcode-with-text - QR Code + Text

QR code on top, text below, center aligned

```python
requests.post("http://localhost:8000/print", json={
    "template": "qrcode-with-text",
    "print_list": [
        {
            "qrcode": "https://example.com/product/12345",
            "text": "Product No: 12345"
        }
    ]
})
```

### 4️⃣ barcode-with-text - Barcode + Text

Barcode on top, text below, center aligned

```python
requests.post("http://localhost:8000/print", json={
    "template": "barcode-with-text",
    "print_list": [
        {
            "barcode": "1234567890",
            "text": "Order No: 1234567890"
        }
    ]
})
```

### 5️⃣ custom - Fully Customizable

Advanced users can fully control element positions and styles

```python
requests.post("http://localhost:8000/print", json={
    "template": "custom",
    "layout": {
        "width": 100,
        "height": 80,
        "elements": [
            {
                "type": "text",
                "x": 100,
                "y": 100,
                "text": "Custom Title",
                "font_size": 56
            },
            {
                "type": "qrcode",
                "x": 300,
                "y": 300,
                "content": "https://example.com",
                "size": 10
            }
        ]
    },
    "qty": 1
})
```

---

## 🔧 API Endpoints

### Basic Endpoints

#### GET `/` - Service Info

```bash
curl http://localhost:8000/
```

#### GET `/health` - Health Check

```bash
curl http://localhost:8000/health
```

#### POST `/test` - Test USB Connection

```bash
curl -X POST http://localhost:8000/test
```

### Print Endpoint

#### POST `/print` - Unified Print Interface

See [API.md](API.md) for detailed documentation

---

## 🏗️ Architecture

```
┌─────────────────┐      HTTP/JSON       ┌──────────────────────┐
│   Frontend App  │ ─────────────────>  │  FastAPI Service     │
│  (Any Language) │                      │   TSC-Print-MW       │
└─────────────────┘                      └──────────────────────┘
                                                   │
                                                   │ pythonnet
                                                   │ + tsclib
                                                   ▼
                                         ┌──────────────────────┐
                                         │   TSC Printer        │
                                         │   (USB Connection)   │
                                         └──────────────────────┘
```

**Tech Stack**:

- FastAPI - Web framework
- pythonnet - Python .NET interop
- tsclib - TSC printer control library

---

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Quick Steps

1. Fork the project
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## ❓ FAQ

### 1. Printer Not Found

**Issue**: "USB printer connection failed"

**Solution**:

- Check USB connection
- Ensure printer is powered on
- Verify printer in Windows Device Manager

### 2. Chinese Characters Garbled

**Issue**: Chinese text displays as squares or gibberish

**Solution**:

- Confirm Windows has SimSun font installed
- Check Python environment encoding is UTF-8
- Try other Chinese fonts in config.py

### 3. Print Position Offset

**Issue**: Print content position is inaccurate

**Solution**:

- Verify DPI_RATIO matches your printer model
- Run paper calibration: `python -c "from printer import calibrate_paper; calibrate_paper()"`
- Adjust PRINT_MARGIN in config.py

---

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [pythonnet](https://github.com/pythonnet/pythonnet) - Python .NET interop
- [TSC](https://www.tscprinters.com/) - TSC Printers

---

## 📮 Contact

- Bug Reports: [GitHub Issues](https://github.com/your-username/TSC-Print-Middleware/issues)
- Feature Requests: [GitHub Discussions](https://github.com/your-username/TSC-Print-Middleware/discussions)

---

**⭐ If this project helps you, please give it a Star!**
