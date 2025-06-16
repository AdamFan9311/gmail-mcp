# Gmail Universal MCP Server 👥

**多用戶 Gmail MCP 服務器 - 任何人都可以使用自己的 Gmail 憑證**

## 🌟 特點

- 👥 **多用戶支持**：每個用戶使用自己的 Gmail 憑證
- 🔄 **動態配置**：無需修改代碼，運行時設置憑證
- 🎭 **Session 隔離**：每個用戶的憑證獨立存儲
- 📚 **內建教學**：完整的 Gmail 設置指南
- 🔒 **內存存儲**：憑證只存在內存中，重啟後自動清除

## 🚀 快速開始

### 1. 安裝依賴

```bash
pip install fastmcp>=2.8.0 python-dotenv>=1.0.0
```

### 2. 運行服務器

```bash
python gmail_universal_mcp.py
```

服務器將在 `http://localhost:8000/sse` 啟動

### 3. 配置 Cursor MCP

在 Cursor 的 MCP 設置中添加：

```json
{
  "gmail-universal": {
    "url": "http://localhost:8000/sse"
  }
}
```

## 📧 Gmail 設置指南

### 步驟 1：啟用兩步驗證
1. 前往 [Google 帳戶安全設置](https://myaccount.google.com/security)
2. 點擊「兩步驗證」
3. 按照指示完成設置

### 步驟 2：生成應用密碼
1. 前往 [Google 應用密碼](https://myaccount.google.com/apppasswords)
2. 選擇「郵件」應用
3. 複製生成的 16 位密碼（格式：`xxxx xxxx xxxx xxxx`）

## 🛠️ 使用方法

### 1. 設置你的憑證

```
工具：setup_gmail_credentials
參數：
- gmail_address: 你的 Gmail 地址
- app_password: 你的 Google 應用密碼
- user_name: 可選的用戶標識
```

### 2. 發送郵件

```
工具：send_email
參數：
- to_email: 收件人郵箱
- subject: 郵件主題
- message: 郵件內容
- from_name: 可選的發件人顯示名稱
```

### 3. 檢查狀態

```
工具：check_my_status
查看你的憑證設置狀態
```

## 🔧 可用工具

| 工具名稱 | 功能 | 必需參數 |
|---------|------|----------|
| `setup_gmail_credentials` | 設置 Gmail 憑證 | `gmail_address`, `app_password` |
| `send_email` | 發送郵件 | `to_email`, `subject`, `message` |
| `check_my_status` | 檢查憑證狀態 | 無 |
| `get_setup_guide` | 獲取設置指南 | 無 |

## 🔒 安全特性

- ✅ **Session 隔離**：每個用戶的憑證獨立存儲
- ✅ **內存存儲**：憑證不寫入磁盤
- ✅ **自動清理**：服務重啟後憑證自動清除
- ✅ **連接測試**：設置憑證時自動驗證

## 🌐 部署選項

### 本地使用
```bash
python gmail_universal_mcp.py
```

### 遠端部署
```bash
# 修改 host 和 port
mcp.run(transport="sse", host="0.0.0.0", port=8000)
```

## ❓ 常見問題

**Q: 憑證會被保存嗎？**
A: 不會，憑證只存在內存中，服務重啟後需要重新設置。

**Q: 多個用戶可以同時使用嗎？**
A: 可以，每個用戶的憑證通過 session ID 隔離。

**Q: 忘記設置憑證怎麼辦？**
A: 使用任何發送工具時會提示先設置憑證。

## 📝 許可證

MIT License - 可自由使用和修改