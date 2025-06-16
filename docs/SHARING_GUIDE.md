# 📧 Gmail 通用 MCP 伺服器 - 分享指南

## 🌟 任何人都可以使用！

這是一個通用的 Gmail MCP 伺服器，**任何人都可以連接並使用自己的 Gmail 憑證**發送郵件。

## 🚀 對於想要使用的人

### 📋 準備你的 Gmail 應用密碼

1. **啟用兩步驗證**
   - 前往 https://myaccount.google.com/security
   - 點擊「兩步驗證」並按照指示設置

2. **生成應用密碼**
   - 前往 https://myaccount.google.com/apppasswords
   - 選擇「郵件」應用和你的設備類型
   - 複製生成的 16 位應用密碼（格式：xxxx xxxx xxxx xxxx）

### 🔌 連接到伺服器

在你的 Cursor MCP 配置 (`~/.cursor/mcp.json`) 中添加：

```json
{
  "mcpServers": {
    "gmail-universal": {
      "url": "http://localhost:8000/sse"
    }
  }
}
```

### 💡 使用步驟

1. **設置你的憑證**
   ```
   使用工具: setup_gmail_credentials
   - gmail_address: 你的Gmail地址
   - app_password: 你剛才獲取的16位密碼
   ```

2. **發送郵件**
   ```
   使用工具: send_email
   - to_email: 收件人郵箱
   - subject: 郵件主題
   - message: 郵件內容
   ```

3. **檢查狀態**
   ```
   使用工具: check_my_status
   ```

## 🔒 安全特性

✅ **隱私保護**: 你的憑證只存儲在內存中，不會被保存到文件
✅ **用戶隔離**: 每個用戶的憑證完全獨立，互不影響
✅ **自動清理**: 伺服器重啟後所有憑證自動清除
✅ **無需文件**: 不需要修改任何配置文件

## 🌐 對於想要部署的人

### 本地運行

```bash
# 克隆代碼
git clone <repository>
cd gmail-mcp

# 安裝依賴
pip install -r requirements.txt

# 運行通用伺服器
python gmail_universal_mcp.py
```

### 部署到雲端

可以部署到任何支持 Python 的平台：

- **Heroku**: 添加 `Procfile`
- **Railway**: 直接部署
- **DigitalOcean**: 使用 App Platform
- **AWS/GCP/Azure**: 使用容器服務

#### Dockerfile 範例

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY gmail_universal_mcp.py .

EXPOSE 8000
CMD ["python", "gmail_universal_mcp.py"]
```

## 📊 工具列表

1. **setup_gmail_credentials** - 設置你的 Gmail 憑證
2. **send_email** - 發送郵件
3. **check_my_status** - 檢查你的狀態
4. **get_setup_guide** - 獲取詳細指南

## ❓ 常見問題

**Q: 我的憑證安全嗎？**
A: 是的！憑證只存儲在內存中，不會被寫入文件或數據庫。

**Q: 其他人能看到我的憑證嗎？**
A: 不能！每個用戶的憑證完全獨立存儲。

**Q: 伺服器重啟後需要重新設置嗎？**
A: 是的，為了安全起見，重啟後需要重新設置憑證。

**Q: 可以同時多人使用嗎？**
A: 可以！這是一個多用戶設計，支持同時多人使用。

## 🎯 使用場景

- ✅ 團隊共享 MCP 伺服器
- ✅ 開發環境中的郵件功能
- ✅ AI 助手郵件發送能力
- ✅ 自動化郵件通知

## 🔗 連接範例

部署後，任何人都可以使用這個 URL 連接：

```json
{
  "mcpServers": {
    "gmail-shared": {
      "url": "https://your-domain.com/sse"
    }
  }
}
```

---

**就是這麼簡單！** 🚀 任何人都可以連接並使用自己的 Gmail 憑證，無需複雜設置。 