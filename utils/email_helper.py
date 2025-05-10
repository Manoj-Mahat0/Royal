import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "codeinlastbench@gmail.com"
SMTP_PASS = "jbgw uual jybh qgnn"

def send_birthday_email(to_email: str, to_name: str, custom_message: str = ""):
    subject = "🎉 Happy Birthday from Cake Shop!"

    html_template = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #fff7f9; padding: 20px;">
        <div style="max-width: 600px; margin: auto; background-color: #ffffff; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
            <div style="text-align: center; background-color: #ff6f91; padding: 20px 0; color: white; border-top-left-radius: 8px; border-top-right-radius: 8px;">
                <h1>🎂 Happy Birthday, {to_name}!</h1>
            </div>
            <div style="padding: 20px; text-align: center;">
                <p style="font-size: 16px;">{custom_message or f"We hope your day is filled with love, cake, and lots of sweet memories!"}</p>
                <img src="https://cdn-icons-png.flaticon.com/512/477/477742.png" alt="Cake" width="100"/>
                <p style="margin-top: 30px;">- From all of us at <strong>Cake Shop</strong></p>
            </div>
        </div>
    </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = to_email

    msg.attach(MIMEText(html_template, "html"))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        return True
    except Exception as e:
        print("Email send failed:", e)
        return False
