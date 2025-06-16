# Gmail Secure MCP Server 🔒

**企業級安全 Gmail MCP 服務器 - 生產環境專用**

## 🛡️ 企業級安全特性

- 🔐 **JWT 身份驗證**：基於 token 的安全認證
- 🛡️ **軍用級加密**：使用 Fernet 加密存儲所有憑證
- 🚦 **智能速率限制**：防止濫用和攻擊
- 🔒 **HTTPS 強制**：生產環境必須使用 HTTPS
- 📊 **完整審計日誌**：記錄所有操作和時間戳
- 🔑 **bcrypt 密碼哈希**：安全的密碼存儲

## 🚀 快速開始

### 1. 安裝依賴

```bash
pip install -r requirements-secure.txt
```

### 2. 環境配置

創建 `.env` 文件：

```env
# JWT 安全密鑰（生產環境必須更改）
JWT_SECRET_KEY=your-super-secret-jwt-key-here

# 加密密鑰（生產環境必須更改）
ENCRYPTION_KEY=your-fernet-encryption-key-here

# 管理員密碼哈希（使用 bcrypt）
ADMIN_PASSWORD_HASH=$2b$12$example.hash.here

# 安全設置
REQUIRE_HTTPS=true
RATE_LIMIT_PER_HOUR=10
```

### 3. 生成安全密鑰

```python
# 生成 JWT 密鑰
import secrets
jwt_key = secrets.token_urlsafe(32)
print(f"JWT_SECRET_KEY={jwt_key}")

# 生成加密密鑰
from cryptography.fernet import Fernet
encryption_key = Fernet.generate_key().decode()
print(f"ENCRYPTION_KEY={encryption_key}")

# 生成管理員密碼哈希
import bcrypt
password = "your-admin-password"
hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
print(f"ADMIN_PASSWORD_HASH={hash}")
```

### 4. 運行服務器

```bash
python gmail_secure_mcp.py
```

### 5. 配置 Cursor MCP

```json
{
  "gmail-secure": {
    "url": "https://your-domain.com/sse"
  }
}
```

## 🔐 安全工作流程

### 1. 管理員認證

```
工具：authenticate_user
參數：
- username: admin
- password: 你的管理員密碼
```

返回 JWT token，24小時有效。

### 2. 設置加密憑證

```
工具：setup_secure_gmail_credentials
參數：
- session_token: 步驟1獲得的JWT token
- gmail_address: Gmail 地址
- app_password: Google 應用密碼
- user_name: 可選用戶標識
```

### 3. 發送安全郵件

```
工具：send_secure_email
參數：
- session_token: JWT token
- to_email: 收件人
- subject: 主題
- message: 內容
```

## 🔧 完整工具列表

| 工具名稱 | 功能 | 認證要求 |
|---------|------|----------|
| `authenticate_user` | 管理員登入 | 無 |
| `setup_secure_gmail_credentials` | 加密設置憑證 | JWT Token |
| `send_secure_email` | 發送加密郵件 | JWT Token |
| `get_security_status` | 查看安全狀態 | JWT Token |
| `revoke_user_credentials` | 撤銷用戶憑證 | JWT Token |
| `get_audit_log` | 查看審計日誌 | JWT Token |

## 🛡️ 安全配置詳解

### JWT 配置
- **密鑰長度**：至少 32 字節
- **算法**：HS256
- **過期時間**：24 小時
- **自動刷新**：支持

### 加密配置
- **算法**：Fernet (AES 128)
- **密鑰管理**：環境變量
- **數據加密**：所有敏感信息
- **傳輸加密**：HTTPS 強制

### 速率限制
- **默認限制**：每小時 10 次操作
- **用戶隔離**：每用戶獨立計算
- **自動重置**：滑動窗口
- **可配置**：環境變量調整

## 🌐 生產部署

### Docker 部署

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements-secure.txt .
RUN pip install -r requirements-secure.txt

COPY gmail_secure_mcp.py .
COPY .env .

EXPOSE 8000
CMD ["python", "gmail_secure_mcp.py"]
```

### Nginx 配置

```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location /sse {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 📊 監控和日誌

### 審計日誌格式
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "user_id": "admin",
  "action": "send_secure_email",
  "target": "user@example.com",
  "status": "success",
  "ip_address": "192.168.1.100"
}
```

### 監控指標
- 認證成功/失敗率
- 郵件發���量
- 速率限制觸發
- 錯誤率統計

## ⚠️ 安全注意事項

### 生產環境必須
- ✅ 使用 HTTPS
- ✅ 更改默認密鑰
- ✅ 設置防火牆
- ✅ 定期更新依賴
- ✅ 監控異常活動

### 不要在生產環境
- ❌ 使用默認密碼
- ❌ 暴露調試信息
- ❌ 忽略 SSL 證書
- ❌ 使用弱密碼
- ❌ 忽略日誌監控

## 🔧 故障排除

### 常見問題

**Q: JWT token 過期怎麼辦？**
A: 重新調用 `authenticate_user` 獲取新 token。

**Q: 忘記管理員密碼？**
A: 重新生成 bcrypt 哈希並更新 `.env` 文件。

**Q: 速率限制太嚴格？**
A: 調整 `RATE_LIMIT_PER_HOUR` 環境變量。

**Q: HTTPS 證書問題？**
A: 檢查證書路徑和有效期，確保 Nginx 配置正確。

## 📝 許可證

MIT License - 適用於企業和商業用途

## 🆘 技術支持

如需企業級技術支持，請聯繫開發團隊。