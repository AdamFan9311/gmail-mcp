# 📧 Gmail MCP Server

一個簡單易用的 Gmail MCP (Model Context Protocol) 伺服器，讓你在 Cursor 中直接發送郵件！

## ✨ 特色功能

- 🚀 **即插即用**：幾分鐘內完成設置
- 📡 **SSE 傳輸**：穩定的 Server-Sent Events 協議
- 🔒 **安全可靠**：使用 Google 應用密碼
- 🌐 **可部署**：支持本地、內網、雲端部署
- 🎯 **Cursor 整合**：完美支持 Cursor MCP 功能

## 🚀 快速開始

### 1. 克隆項目
```bash
git clone https://github.com/your-username/gmail-mcp.git
cd gmail-mcp
```

### 2. 安裝依賴
```bash
# 創建虛擬環境
python -m venv gmail_mcp_env
source gmail_mcp_env/bin/activate  # macOS/Linux
# 或 gmail_mcp_env\Scripts\activate  # Windows

# 安裝依賴
pip install -r requirements.txt
```

### 3. 設置 Gmail 憑證
```bash
# 複製環境變量範例
cp env.example .env

# 編輯 .env 文件，填入你的 Gmail 憑證
# GMAIL_ADDRESS=your-email@gmail.com
# APP_PASSWORD=your-16-digit-app-password
```

### 4. 獲取 Google 應用密碼
1. 前往 [Google 帳戶安全設置](https://myaccount.google.com/security)
2. 啟用「兩步驗證」
3. 前往 [應用密碼設置](https://myaccount.google.com/apppasswords)
4. 選擇「郵件」應用，生成 16 位密碼
5. 將密碼填入 `.env` 文件

### 5. 啟動伺服器
```bash
python gmail_sse_server.py
```

### 6. 配置 Cursor
在 `~/.cursor/mcp.json` 中添加：
```json
{
  "mcpServers": {
    "gmail-mcp": {
      "url": "http://localhost:8000/sse"
    }
  }
}
```

## 🛠️ 使用方法

啟動伺服器後，在 Cursor 中你會看到 3 個可用工具：

1. **send_email_sse** - 發送郵件
2. **check_server_status** - 檢查伺服器狀態
3. **get_connection_info** - 獲取連接信息

### 發送郵件範例
```
使用工具: send_email_sse
- to_email: recipient@example.com
- subject: 測試郵件
- message: 這是一封來自 MCP 的測試郵件！
- from_name: 你的名字 (可選)
```

## 📁 項目結構

```
gmail-mcp/
├── 📧 gmail_sse_server.py          # 主要伺服器
├── 📋 requirements.txt             # Python 依賴
├── 📝 README.md                    # 使用說明
├── 📄 env.example                  # 憑證範例
├── 🚫 .gitignore                   # Git 忽略文件
├── 📄 PROJECT_STRUCTURE.md         # 項目結構說明
├── 📁 alternatives/                # 其他版本
│   ├── gmail_universal_mcp.py      # 多用戶版本
│   └── gmail_secure_mcp.py         # 企業安全版本
└── 📁 docs/                        # 詳細文檔
    ├── SHARING_GUIDE.md            # 分享指南
    ├── SECURITY_DEPLOYMENT_GUIDE.md # 安全部署指南
    └── requirements-secure.txt     # 安全版本依賴
```

## 🔧 進階功能

### 多用戶版本
如果你想讓團隊成員都能使用自己的 Gmail 憑證：
```bash
python alternatives/gmail_universal_mcp.py
```

### 企業安全版本
如果需要企業級安全功能（HTTPS、身份驗證、加密存儲）：
```bash
python alternatives/gmail_secure_mcp.py
```

## 🔒 安全注意事項

- ✅ 使用 Google 應用密碼，不是帳戶密碼
- ✅ `.env` 文件已加入 `.gitignore`，不會被上傳
- ✅ 建議僅在內網或 VPN 環境使用
- ⚠️ 公開部署需要額外安全措施

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

## 📄 授權

MIT License

## 🙏 致謝

- [FastMCP](https://github.com/jlowin/fastmcp) - 優秀的 MCP 框架
- [Model Context Protocol](https://modelcontextprotocol.io/) - MCP 協議規範

---

**享受在 Cursor 中發送郵件的便利！** 📧✨ 