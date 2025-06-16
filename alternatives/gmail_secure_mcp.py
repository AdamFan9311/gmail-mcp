#!/usr/bin/env python3
"""
Gmail 安全 MCP 伺服器 - 生產環境專用
支持 HTTPS、身份驗證、加密存儲
"""

import os
import ssl
import smtplib
import hashlib
import secrets
import base64
from cryptography.fernet import Fernet
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from datetime import datetime, timedelta
import bcrypt
import jwt

from fastmcp import FastMCP, Context

# 載入環境變量
load_dotenv()

# 創建 MCP 服務器
mcp = FastMCP("Gmail 安全 MCP 伺服器 🔒")

# 安全配置
SECRET_KEY = os.getenv("JWT_SECRET_KEY", secrets.token_urlsafe(32))
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", Fernet.generate_key())
ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH")  # bcrypt hash
REQUIRE_HTTPS = os.getenv("REQUIRE_HTTPS", "true").lower() == "true"
RATE_LIMIT_PER_HOUR = int(os.getenv("RATE_LIMIT_PER_HOUR", "10"))

# Gmail SMTP 設定
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# 加密工具
cipher_suite = Fernet(ENCRYPTION_KEY)

# 安全存儲（加密的用戶憑證）
encrypted_credentials: Dict[str, Dict[str, Any]] = {}
user_sessions: Dict[str, Dict[str, Any]] = {}
rate_limits: Dict[str, list] = {}

def encrypt_data(data: str) -> str:
    """加密敏感數據"""
    return cipher_suite.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data: str) -> str:
    """解密敏感數據"""
    return cipher_suite.decrypt(encrypted_data.encode()).decode()

def generate_session_token(user_id: str) -> str:
    """生成安全的session token"""
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=24),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_session_token(token: str) -> Optional[str]:
    """驗證session token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def check_rate_limit(user_id: str) -> bool:
    """檢查速率限制"""
    now = datetime.utcnow()
    hour_ago = now - timedelta(hours=1)
    
    if user_id not in rate_limits:
        rate_limits[user_id] = []
    
    # 清理過期記錄
    rate_limits[user_id] = [
        timestamp for timestamp in rate_limits[user_id] 
        if timestamp > hour_ago
    ]
    
    # 檢查是否超過限制
    if len(rate_limits[user_id]) >= RATE_LIMIT_PER_HOUR:
        return False
    
    # 記錄此次請求
    rate_limits[user_id].append(now)
    return True

@mcp.tool()
def authenticate_user(
    ctx: Context,
    username: str,
    password: str
) -> str:
    """
    用戶身份驗證
    
    Args:
        username: 用戶名
        password: 密碼
    """
    
    # 檢查HTTPS要求
    if REQUIRE_HTTPS and not getattr(ctx, 'is_secure', False):
        return "❌ 安全錯誤：此服務要求 HTTPS 連接"
    
    try:
        # 簡單的用戶驗證（實際應用中應使用數據庫）
        if username == "admin" and ADMIN_PASSWORD_HASH:
            if bcrypt.checkpw(password.encode(), ADMIN_PASSWORD_HASH.encode()):
                token = generate_session_token(username)
                user_sessions[username] = {
                    "token": token,
                    "created_at": datetime.utcnow()
                }
                return f"""🎉 驗證成功！

🔐 Session Token: {token}
⏰ 有效期：24小時
🛡️ 安全級別：高

請保存此 token，後續操作需要使用。"""
        
        return "❌ 認證失敗：用戶名或密碼錯誤"
        
    except Exception as e:
        return f"❌ 認證錯誤：{str(e)}"

@mcp.tool()
def setup_secure_gmail_credentials(
    ctx: Context,
    session_token: str,
    gmail_address: str,
    app_password: str,
    user_name: Optional[str] = None
) -> str:
    """
    安全設置 Gmail 憑證（需要有效的session token）
    
    Args:
        session_token: 身份驗證token
        gmail_address: Gmail 地址
        app_password: Google 應用密碼
        user_name: 可選的用戶標識
    """
    
    # 驗證session
    authenticated_user = verify_session_token(session_token)
    if not authenticated_user:
        return "❌ 認證失敗：無效或過期的 session token"
    
    # 檢查速率限制
    if not check_rate_limit(authenticated_user):
        return f"❌ 速率限制：每小時最多 {RATE_LIMIT_PER_HOUR} 次操作"
    
    user_id = user_name or authenticated_user
    
    try:
        # 清理應用密碼格式
        app_password_clean = app_password.replace(" ", "")
        
        # 測試Gmail連接
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(gmail_address, app_password_clean)
        server.quit()
        
        # 加密存儲憑證
        encrypted_credentials[user_id] = {
            "email": encrypt_data(gmail_address),
            "app_password": encrypt_data(app_password_clean),
            "created_at": datetime.utcnow().isoformat(),
            "last_used": None
        }
        
        return f"""🔒 Gmail 憑證安全設置成功！

👤 用戶：{user_id}
✅ 帳號：{gmail_address}
🔐 存儲：加密保護
⏰ 設置時間：{datetime.utcnow().isoformat()}

憑證已使用軍用級加密算法保護。"""
        
    except smtplib.SMTPAuthenticationError:
        return """❌ Gmail 認證失敗！

📋 安全檢查清單：
1. Gmail 地址格式正確？
2. 應用密碼正確？（16位）
3. 已啟用兩步驗證？
4. 應用密碼未過期？

🔗 設置指南：https://myaccount.google.com/apppasswords"""
        
    except Exception as e:
        return f"❌ 設置失敗：{str(e)}"

@mcp.tool()
def send_secure_email(
    ctx: Context,
    session_token: str,
    to_email: str,
    subject: str,
    message: str,
    from_name: Optional[str] = None,
    user_name: Optional[str] = None
) -> str:
    """
    安全發送郵件（需要有效的session token）
    
    Args:
        session_token: 身份驗證token
        to_email: 收件人郵箱
        subject: 郵件主題
        message: 郵件內容
        from_name: 發件人顯示名稱
        user_name: 用戶標識
    """
    
    # 驗證session
    authenticated_user = verify_session_token(session_token)
    if not authenticated_user:
        return "❌ 認證失敗：無效或過期的 session token"
    
    # 檢查速率限制
    if not check_rate_limit(authenticated_user):
        return f"❌ 速率限制：每小時最多 {RATE_LIMIT_PER_HOUR} 次操作"
    
    user_id = user_name or authenticated_user
    
    if user_id not in encrypted_credentials:
        return "❌ 未找到憑證：請先使用 setup_secure_gmail_credentials 設置"
    
    try:
        # 解密憑證
        creds = encrypted_credentials[user_id]
        gmail_address = decrypt_data(creds["email"])
        app_password = decrypt_data(creds["app_password"])
        
        # 創建郵件
        msg = MIMEMultipart()
        
        if from_name:
            msg['From'] = f"{from_name} <{gmail_address}>"
        else:
            msg['From'] = gmail_address
            
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain', 'utf-8'))
        
        # 發送郵件
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(gmail_address, app_password)
        
        text = msg.as_string()
        server.sendmail(gmail_address, to_email, text)
        server.quit()
        
        # 更新最後使用時間
        encrypted_credentials[user_id]["last_used"] = datetime.utcnow().isoformat()
        
        return f"""📧 郵件安全發送成功！

👤 發件人：{gmail_address}
✅ 發送至：{to_email}
📝 主題：{subject}
🔐 安全級別：高
⏰ 發送時間：{datetime.utcnow().isoformat()}"""
        
    except Exception as e:
        return f"❌ 發送失敗：{str(e)}"

@mcp.tool()
def get_security_status(
    ctx: Context,
    session_token: str
) -> str:
    """檢查安全狀態和配置"""
    
    authenticated_user = verify_session_token(session_token)
    if not authenticated_user:
        return "❌ 認證失敗：無效或過期的 session token"
    
    # 統計信息
    total_users = len(encrypted_credentials)
    current_sessions = len(user_sessions)
    
    # 安全配置檢查
    security_checks = {
        "HTTPS 要求": "✅ 已啟用" if REQUIRE_HTTPS else "⚠️ 未啟用",
        "加密存儲": "✅ 已啟用",
        "JWT 驗證": "✅ 已啟用",
        "速率限制": f"✅ {RATE_LIMIT_PER_HOUR}/小時",
        "Session 管理": "✅ 已啟用"
    }
    
    status_report = f"""
🔒 Gmail 安全 MCP 伺服器狀態報告

👤 當前用戶：{authenticated_user}
📊 總用戶數：{total_users}
🔌 活躍 Sessions：{current_sessions}

🛡️ 安全配置：
"""
    
    for check, status in security_checks.items():
        status_report += f"  {check}: {status}\n"
    
    status_report += f"""
⚡ 伺服器狀態：正常運行
🕐 報告時間：{datetime.utcnow().isoformat()}

🔐 安全提醒：
- 定期更換 JWT 密鑰
- 監控異常訪問模式
- 保持 HTTPS 連接
- 定期清理過期 sessions
    """
    
    return status_report

if __name__ == "__main__":
    print("🔒 Gmail 安全 MCP 伺服器啟動中...")
    print("🛡️ 企業級安全特性已啟用")
    print("📡 建議使用 HTTPS 傳輸協議")
    
    if not ADMIN_PASSWORD_HASH:
        print("⚠️  警告：未設置管理員密碼，請設置 ADMIN_PASSWORD_HASH 環境變量")
    
    # 使用 SSE 傳輸協議，建議配置 HTTPS
    mcp.run(
        transport="sse", 
        host="0.0.0.0", 
        port=8000,
        ssl_keyfile=os.getenv("SSL_KEYFILE"),
        ssl_certfile=os.getenv("SSL_CERTFILE")
    ) 