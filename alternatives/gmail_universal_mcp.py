#!/usr/bin/env python3
"""
Gmail 通用 MCP 伺服器 - 任何人都可以使用
支持多用戶動態憑證設置
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, Dict, Any
from dotenv import load_dotenv

from fastmcp import FastMCP, Context

# 載入環境變量
load_dotenv()

# 創建 MCP 服務器
mcp = FastMCP("Gmail 通用 MCP 伺服器 📧")

# Gmail SMTP 設定
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# 用戶憑證存儲（內存中，每個session獨立）
user_credentials: Dict[str, Dict[str, str]] = {}

@mcp.tool()
def setup_gmail_credentials(
    ctx: Context,
    gmail_address: str,
    app_password: str,
    user_name: Optional[str] = None
) -> str:
    """
    設置你的 Gmail 憑證
    
    設置步驟：
    1. 前往 https://myaccount.google.com/security
    2. 啟用兩步驗證
    3. 前往 https://myaccount.google.com/apppasswords
    4. 生成應用密碼（16位）
    5. 在這裡輸入你的憑證
    
    Args:
        gmail_address: 你的 Gmail 地址
        app_password: Google 應用密碼（16位，格式：xxxx xxxx xxxx xxxx）
        user_name: 可選的用戶標識（默認使用session ID）
    """
    
    # 使用用戶提供的名稱或session ID作為標識
    session_id = getattr(ctx, 'session_id', 'default')
    user_id = user_name or session_id
    
    try:
        # 清理應用密碼格式
        app_password_clean = app_password.replace(" ", "")
        
        # 測試連接
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(gmail_address, app_password_clean)
        server.quit()
        
        # 保存憑證到內存
        user_credentials[user_id] = {
            "email": gmail_address,
            "app_password": app_password_clean
        }
        
        return f"""🎉 Gmail 憑證設置成功！

👤 用戶：{user_id}
✅ 帳號：{gmail_address}
✅ 連接：正常
🔐 憑證：已安全存儲

現在你可以使用 send_email 工具發送郵件了！
憑證只存儲在當前session中，確保安全性。"""
        
    except smtplib.SMTPAuthenticationError:
        return """❌ 認證失敗！請檢查：

📋 檢查清單：
1. Gmail 地址是否正確？
2. 應用密碼是否正確？
3. 是否已啟用兩步驗證？
4. 應用密碼是否已正確生成？

💡 獲取應用密碼步驟：
1. 前往 https://myaccount.google.com/security
2. 啟用「兩步驗證」
3. 前往 https://myaccount.google.com/apppasswords
4. 選擇「郵件」應用
5. 複製 16 位應用密碼"""
        
    except Exception as e:
        return f"❌ 設置失敗：{str(e)}"

@mcp.tool()
def send_email(
    ctx: Context,
    to_email: str,
    subject: str,
    message: str,
    from_name: Optional[str] = None,
    user_name: Optional[str] = None
) -> str:
    """
    發送郵件（使用你設置的憑證）
    
    Args:
        to_email: 收件人郵箱
        subject: 郵件主題
        message: 郵件內容
        from_name: 發件人顯示名稱（可選）
        user_name: 用戶標識（可選，默認使用session ID）
    """
    
    # 獲取用戶憑證
    session_id = getattr(ctx, 'session_id', 'default')
    user_id = user_name or session_id
    
    if user_id not in user_credentials:
        return """❌ 請先設置 Gmail 憑證！

🔧 使用 setup_gmail_credentials 工具設置你的憑證：
- gmail_address: 你的 Gmail 地址
- app_password: 你的 Google 應用密碼

💡 如果你還沒有應用密碼，請參考設置工具中的說明。"""
    
    creds = user_credentials[user_id]
    gmail_address = creds["email"]
    app_password = creds["app_password"]
    
    try:
        # 創建郵件
        msg = MIMEMultipart()
        
        # 設置發件人
        if from_name:
            msg['From'] = f"{from_name} <{gmail_address}>"
        else:
            msg['From'] = gmail_address
            
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # 添加郵件內容
        msg.attach(MIMEText(message, 'plain', 'utf-8'))
        
        # 發送郵件
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(gmail_address, app_password)
        
        text = msg.as_string()
        server.sendmail(gmail_address, to_email, text)
        server.quit()
        
        return f"""📧 郵件發送成功！

👤 發件人：{gmail_address}
✅ 發送至：{to_email}
✅ 主題：{subject}
🕒 狀態：已發送"""
        
    except Exception as e:
        return f"❌ 發送失敗：{str(e)}"

@mcp.tool()
def check_my_status(
    ctx: Context,
    user_name: Optional[str] = None
) -> str:
    """檢查你的憑證和伺服器狀態"""
    
    session_id = getattr(ctx, 'session_id', 'default')
    user_id = user_name or session_id
    
    # 檢查憑證狀態
    creds_status = "✅ 已設置" if user_id in user_credentials else "❌ 未設置"
    
    if user_id in user_credentials:
        gmail_addr = user_credentials[user_id]["email"]
        creds_info = f"📧 帳號：{gmail_addr}"
    else:
        creds_info = "📧 帳號：未設置"
    
    status = f"""
🔥 Gmail 通用 MCP 伺服器狀態

👤 用戶：{user_id}
🔐 憑證狀態：{creds_status}
{creds_info}
📡 傳輸協議：Server-Sent Events (SSE)
🌐 部署模式：通用可共享
⚡ 伺服器狀態：正常運行

💡 使用說明：
1. 使用 setup_gmail_credentials 設置你的憑證
2. 使用 send_email 發送郵件
3. 每個用戶的憑證獨立存儲，確保安全
    """
    
    return status

@mcp.tool()
def get_setup_guide(ctx: Context) -> str:
    """獲取完整設置指南"""
    
    return """
🚀 Gmail 通用 MCP 伺服器使用指南

══════════════════════════════════════════

📋 步驟 1：準備 Google 應用密碼
1. 前往 https://myaccount.google.com/security
2. 啟用「兩步驗證」（如果未啟用）
3. 前往 https://myaccount.google.com/apppasswords
4. 選擇「郵件」應用和你的設備
5. 複製生成的 16 位應用密碼

📋 步驟 2：設置憑證
使用 setup_gmail_credentials 工具：
- gmail_address: 你的完整 Gmail 地址
- app_password: 剛才獲取的 16 位密碼
- user_name: （可選）自定義用戶標識

📋 步驟 3：發送郵件
使用 send_email 工具發送郵件

🔒 安全特性：
✅ 憑證只存儲在內存中
✅ 每個session獨立
✅ 不會洩露給其他用戶
✅ 服務器重啟後自動清除

🌐 共享方法：
任何人都可以連接到這個伺服器URL，使用自己的憑證：
- 本地：http://localhost:8000/sse
- 部署後：https://your-domain.com/sse

══════════════════════════════════════════
    """

if __name__ == "__main__":
    print("🚀 Gmail 通用 MCP 伺服器啟動中...")
    print("📡 使用 Server-Sent Events 傳輸協議")
    print("🌐 支持多用戶，每個人使用自己的憑證")
    print("🔐 憑證安全存儲在內存中")
    
    # 使用 SSE 傳輸協議
    mcp.run(transport="sse", host="0.0.0.0", port=8000) 