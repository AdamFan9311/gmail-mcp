#!/usr/bin/env python3
"""
Gmail Secure MCP Server - 安全密鑰生成工具
用於生成生產環境所需的所有安全密鑰
"""

import secrets
import bcrypt
from cryptography.fernet import Fernet
import getpass

def generate_jwt_key():
    """生成 JWT 安全密鑰"""
    return secrets.token_urlsafe(32)

def generate_encryption_key():
    """生成 Fernet 加密密鑰"""
    return Fernet.generate_key().decode()

def generate_password_hash(password=None):
    """生成 bcrypt 密碼哈希"""
    if not password:
        password = getpass.getpass("請輸入管理員密碼: ")
        confirm = getpass.getpass("請確認管理員密碼: ")
        
        if password != confirm:
            print("❌ 密碼不匹配！")
            return None
    
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def main():
    print("🔐 Gmail Secure MCP Server - 安全密鑰生成工具")
    print("=" * 50)
    
    # 生成所有密鑰
    jwt_key = generate_jwt_key()
    encryption_key = generate_encryption_key()
    password_hash = generate_password_hash()
    
    if not password_hash:
        return
    
    print("\n✅ 安全密鑰生成完成！")
    print("請將以下內容複製到你的 .env 文件中：")
    print("=" * 50)
    
    env_content = f"""# Gmail Secure MCP Server 環境配置
# 生產環境專用 - 請妥善保管這些密鑰

# JWT 安全密鑰
JWT_SECRET_KEY={jwt_key}

# 加密密鑰
ENCRYPTION_KEY={encryption_key}

# 管理員密碼哈希
ADMIN_PASSWORD_HASH={password_hash}

# 安全設置
REQUIRE_HTTPS=true
RATE_LIMIT_PER_HOUR=10
"""
    
    print(env_content)
    
    # 可選：直接寫入文件
    save_to_file = input("\n是否直接保存到 .env 文件？(y/N): ").lower().strip()
    if save_to_file == 'y':
        try:
            with open('.env', 'w') as f:
                f.write(env_content)
            print("✅ 已保存到 .env 文件")
        except Exception as e:
            print(f"❌ 保存失敗：{e}")
    
    print("\n⚠️  安全提醒：")
    print("1. 請妥善保管這些密鑰，不要洩露給他人")
    print("2. 不要將 .env 文件提交到版本控制系統")
    print("3. 定期更換密鑰以確保安全")
    print("4. 生產環境必須使用 HTTPS")

if __name__ == "__main__":
    main()