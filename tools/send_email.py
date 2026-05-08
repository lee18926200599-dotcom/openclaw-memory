#!/usr/bin/env python3
"""
邮件发送工具 - 通过 QQ 邮箱发送文件
用法: python3 send_email.py <收件人> <主题> <文件路径> [正文]
"""

import sys
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

# 配置
SMTP_HOST = "smtp.qq.com"
SMTP_PORT = 587
SMTP_USER = "27270234@qq.com"
SMTP_PASS = "nhigibmebdqmbifj"
FROM_EMAIL = "27270234@qq.com"

def send_email(to_email, subject, file_path, body=""):
    """发送带附件的邮件"""
    
    # 创建邮件
    msg = MIMEMultipart()
    msg['From'] = FROM_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    
    # 添加正文
    if not body:
        body = f"文件发送时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    # 添加附件
    if os.path.exists(file_path):
        filename = os.path.basename(file_path)
        with open(file_path, 'rb') as f:
            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload(f.read())
        
        encoders.encode_base64(attachment)
        attachment.add_header(
            'Content-Disposition',
            f'attachment; filename="{filename}"'
        )
        msg.attach(attachment)
        print(f"附件已添加: {filename}")
    else:
        print(f"警告: 文件不存在 {file_path}")
        return False
    
    # 发送邮件
    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
        server.quit()
        print(f"邮件发送成功!")
        return True
    except Exception as e:
        print(f"邮件发送失败: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("用法: python3 send_email.py <收件人> <主题> <文件路径> [正文]")
        sys.exit(1)
    
    to_email = sys.argv[1]
    subject = sys.argv[2]
    file_path = sys.argv[3]
    body = sys.argv[4] if len(sys.argv) > 4 else ""
    
    success = send_email(to_email, subject, file_path, body)
    sys.exit(0 if success else 1)
