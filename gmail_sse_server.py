#!/usr/bin/env python3
"""
Gmail SSE MCP 服務器 - 可部署到遠端
支持 Server-Sent Events 傳輸協議
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from dotenv import load_dotenv

from fastmcp import FastMCP, Context

# 載入環境變量
load_dotenv()

# 創建 MCP 服務器
mcp = FastMCP("Gmail SSE Server 📧")

# Gmail SMTP 設定
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# 從環境變量獲取憑證
GMAIL_ADDRESS = os.getenv('GMAIL_ADDRESS')
APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD')

@mcp.tool()
def send_email_sse(
    ctx: Context,
    to_email: str,
    subject: str,
    message: str,
    from_name: Optional[str] = None
) -> str:
    """
    發送郵件 - SSE 版本
    
    Args:
        to_email: 收件人郵箱
        subject: 郵件主題
        message: 郵件內容
        from_name: 發件人顯示名稱（可選）
    """
    
    # 檢查憑證
    if not GMAIL_ADDRESS or not APP_PASSWORD:
        return "❌ 請設置環境變量 GMAIL_ADDRESS 和 GMAIL_APP_PASSWORD"
    
    try:
        # 創建郵件
        msg = MIMEMultipart()
        
        # 設置發件人
        if from_name:
            msg['From'] = f"{from_name} <{GMAIL_ADDRESS}>"
        else:
            msg['From'] = GMAIL_ADDRESS
            
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # 添加郵件內容
        msg.attach(MIMEText(message, 'plain', 'utf-8'))
        
        # 發送郵件
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(GMAIL_ADDRESS, APP_PASSWORD)
        
        text = msg.as_string()
        server.sendmail(GMAIL_ADDRESS, to_email, text)
        server.quit()
        
        return f"📧 郵件發送成功！\n✅ 發送至：{to_email}\n✅ 主題：{subject}"
        
    except Exception as e:
        return f"❌ 發送失敗：{str(e)}"

@mcp.tool()
def check_server_status(ctx: Context) -> str:
    """檢查伺服器狀態"""
    
    status = f"""
🔥 Gmail SSE 伺服器狀態

📡 傳輸協議：Server-Sent Events (SSE)
📧 Gmail 憑證：{'✅ 已設置' if GMAIL_ADDRESS else '❌ 未設置'}
🌐 部署模式：遠端可訪問
⚡ 狀態：正常運行
    """
    
    return status

@mcp.tool()
def get_connection_info(ctx: Context) -> str:
    """獲取連接信息"""
    
    return """
🔗 連接信息

本伺服器使用 SSE 傳輸協議，可通過以下方式連接：

📱 在 Cursor MCP 配置中使用：
{
  "gmail-sse": {
    "url": "http://localhost:8000/sse"
  }
}

🌐 部署後使用：
{
  "gmail-sse": {
    "url": "https://your-domain.com/sse"
  }
}
    """

if __name__ == "__main__":
    print("🚀 Gmail SSE MCP 伺服器啟動中...")
    print("📡 使用 Server-Sent Events 傳輸協議")
    print("🌐 可以部署到任何支持 Python 的平台")
    
    # 使用 SSE 傳輸協議
    mcp.run(transport="sse", host="0.0.0.0", port=8000) 