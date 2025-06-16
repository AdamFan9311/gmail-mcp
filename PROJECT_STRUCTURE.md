# 📁 Gmail MCP 項目結構說明

## 🎯 **核心文件（你需要關心的）**

### 🚀 **主要 MCP 伺服器**
- **`gmail_sse_server.py`** ⭐ - **當前使用的版本**
  - 使用 SSE 傳輸協議
  - 與 Cursor 完美整合
  - 支持發送郵件功能

### 📋 **配置文件**
- **`requirements.txt`** - Python 依賴包
- **`.env`** - 你的 Gmail 憑證（需要創建）
- **`env.example`** - 憑證範例文件

### 📚 **使用說明**
- **`README.md`** - 基本使用指南

## 🔄 **其他版本（可選）**

### 📦 **不同功能版本**
- `gmail_universal_mcp.py` - 多用戶版本（讓其他人也能用）
- `gmail_secure_mcp.py` - 企業安全版本（生產環境用）

### 📖 **詳細文檔**
- `SHARING_GUIDE.md` - 如何分享給其他人
- `SECURITY_DEPLOYMENT_GUIDE.md` - 安全部署指南

## 🗑️ **過時文件（可以刪除）**

- `gmail_super_simple_mcp.py` - 最初版本，已被取代
- `cursor_gmail_helper.py` - 舊版本，不再使用
- `requirements-secure.txt` - 安全版本專用依賴

## 🏗️ **建議的項目結構**

```
gmail-mcp/
├── 📧 gmail_sse_server.py          # 主要伺服器
├── 📋 requirements.txt             # 依賴
├── 📝 README.md                    # 使用說明
├── 🔧 .env                         # 你的憑證
├── 📄 env.example                  # 憑證範例
├── 🚫 .gitignore                   # Git 忽略
├── 📁 alternatives/                # 其他版本
│   ├── gmail_universal_mcp.py      # 多用戶版本
│   └── gmail_secure_mcp.py         # 安全版本
├── 📁 docs/                        # 詳細文檔
│   ├── SHARING_GUIDE.md            # 分享指南
│   └── SECURITY_DEPLOYMENT_GUIDE.md # 安全指南
└── 📁 gmail_mcp_env/               # 虛擬環境
```

## 🎯 **對於新用戶，只需要：**

1. **`gmail_sse_server.py`** - 運行這個
2. **`requirements.txt`** - 安裝依賴
3. **`.env`** - 設置你的憑證
4. **`README.md`** - 閱讀使用說明

**其他文件都是可選的！** ✨ 