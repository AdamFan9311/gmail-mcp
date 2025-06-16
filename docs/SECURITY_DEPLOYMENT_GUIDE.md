# 🔒 Gmail MCP 伺服器 - 網路安全部署指南

## ⚠️ **重要安全警告**

將 Gmail MCP 伺服器部署到網際網路存在重大安全風險！請務必閱讀並實施所有安全措施。

## 🚨 **主要安全風險**

### 1. 憑證洩露風險
- **HTTP 明文傳輸** → Gmail 憑證可被攔截
- **內存轉儲攻擊** → 憑證可能從內存中洩露
- **日誌洩露** → 錯誤日誌可能包含敏感信息

### 2. 濫用風險
- **垃圾郵件發送** → 你的 Gmail 帳號被用於發送垃圾郵件
- **配額耗盡** → Google 每日發送限制被快速用完
- **帳號封鎖** → Gmail 帳號可能被 Google 暫停

### 3. 法律風險
- **隱私法規** → GDPR、CCPA 等隱私法規合規問題
- **垃圾郵件法律** → 可能違反反垃圾郵件法律
- **責任問題** → 用戶濫用服務的法律責任

## 🛡️ **安全部署方案**

### 方案 1：僅限內網使用 ⭐ **推薦**

```bash
# 僅綁定內網 IP
python gmail_universal_mcp.py --host 192.168.1.100 --port 8000
```

**優點：**
- ✅ 完全避免網際網路暴露
- ✅ 適合團隊內部使用
- ✅ 零額外安全配置

### 方案 2：VPN + 私有部署

```bash
# 使用 WireGuard 或 OpenVPN
# 只有 VPN 用戶可訪問
python gmail_universal_mcp.py --host 10.0.0.1 --port 8000
```

### 方案 3：企業級安全部署 🔒

使用 `gmail_secure_mcp.py` 並實施以下措施：

#### 3.1 HTTPS 強制

```bash
# 生成 SSL 憑證
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365

# 設置環境變量
export SSL_KEYFILE=/path/to/key.pem
export SSL_CERTFILE=/path/to/cert.pem
export REQUIRE_HTTPS=true
```

#### 3.2 身份驗證設置

```bash
# 生成管理員密碼 hash
python3 -c "import bcrypt; print(bcrypt.hashpw(b'your_secure_password', bcrypt.gensalt()).decode())"

# 設置環境變量
export ADMIN_PASSWORD_HASH="$2b$12$..."
export JWT_SECRET_KEY="your-super-secret-jwt-key"
export ENCRYPTION_KEY="generated-fernet-key"
```

#### 3.3 反向代理配置

使用 Nginx 添加額外安全層：

```nginx
server {
    listen 443 ssl;
    server_name yourdomain.com;
    
    ssl_certificate /etc/ssl/certs/yourdomain.crt;
    ssl_certificate_key /etc/ssl/private/yourdomain.key;
    
    # 安全標頭
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;
    add_header X-XSS-Protection "1; mode=block";
    
    # 速率限制
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/m;
    
    location /sse {
        limit_req zone=api burst=5;
        
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # SSE 特定配置
        proxy_buffering off;
        proxy_cache off;
        proxy_set_header Connection '';
        proxy_http_version 1.1;
        chunked_transfer_encoding off;
    }
}
```

## 🔐 **安全檢查清單**

### 部署前檢查

- [ ] **HTTPS 憑證**：有效的 SSL/TLS 憑證
- [ ] **防火牆**：只開放必要端口
- [ ] **身份驗證**：強密碼和 JWT 配置
- [ ] **速率限制**：每小時/每天發送限制
- [ ] **監控系統**：異常訪問檢測
- [ ] **日誌管理**：敏感信息脫敏
- [ ] **備份策略**：配置和密鑰備份

### 運行時監控

- [ ] **訪問日誌**：記錄所有 API 調用
- [ ] **錯誤監控**：實時錯誤告警
- [ ] **性能監控**：資源使用情況
- [ ] **安全掃描**：定期漏洞掃描
- [ ] **配額監控**：Gmail 發送配額追蹤

### 定期維護

- [ ] **憑證更新**：SSL 憑證定期更新
- [ ] **密鑰輪換**：JWT 密鑰定期更換
- [ ] **依賴更新**：Python 包安全更新
- [ ] **日誌清理**：定期清理舊日誌
- [ ] **安全審計**：定期安全評估

## 🌐 **雲端部署建議**

### AWS 部署

```yaml
# ECS Task Definition 範例
version: '3'
services:
  gmail-mcp:
    image: your-account/gmail-mcp:latest
    environment:
      - REQUIRE_HTTPS=true
      - JWT_SECRET_KEY=${JWT_SECRET}
      - ENCRYPTION_KEY=${ENCRYPTION_KEY}
    secrets:
      - admin_password_hash
    deploy:
      replicas: 1
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
```

### Google Cloud Run

```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: gmail-mcp-secure
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/maxScale: "10"
        run.googleapis.com/vpc-access-connector: your-connector
    spec:
      containers:
      - image: gcr.io/your-project/gmail-mcp:latest
        env:
        - name: REQUIRE_HTTPS
          value: "true"
        - name: JWT_SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: jwt-secret
              key: key
```

## ⚡ **效能與擴展**

### 負載平衡

```nginx
upstream gmail_mcp {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}
```

### Redis Session 存儲

```python
import redis

# 使用 Redis 存儲 sessions
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def store_session(user_id: str, token: str):
    redis_client.setex(f"session:{user_id}", 86400, token)
```

## 🚫 **不推薦的部署方式**

### ❌ 絕對避免

- **HTTP 無加密部署**
- **無身份驗證的公開服務**
- **共享服務器部署**
- **使用預設密碼**
- **關閉所有安全檢查**

### ⚠️ 高風險

- **個人 VPS 部署**（除非你是安全專家）
- **免費雲端服務**（通常缺乏企業級安全）
- **開發環境直接暴露**

## 📊 **合規建議**

### GDPR 合規

- 明確的隱私政策
- 用戶同意機制
- 數據刪除權利
- 數據處理記錄

### 企業使用

- 資訊安全政策審核
- 數據分類和保護
- 員工安全培訓
- 第三方安全評估

## 🎯 **最佳實踐總結**

1. **🏠 優先考慮內網部署**
2. **🔒 必須使用 HTTPS**
3. **🔑 強制身份驗證**
4. **📊 監控和日誌**
5. **🔄 定期安全更新**

## ⚠️ **免責聲明**

本指南僅提供技術建議，不承擔任何法律責任。在生產環境部署前，請：

- 諮詢專業的資訊安全團隊
- 進行全面的安全評估
- 確保符合當地法律法規
- 購買適當的網路保險

---

**記住：安全不是一次性的設置，而是持續的過程！** 🔐 