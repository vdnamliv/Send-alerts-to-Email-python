# Send-alerts-to-Email-python
## Cách sử dụng module:
1. Các thông tin cần thiết
- If don't know how to create app password, go [here](https://myaccount.google.com/apppasswords?pli=1&rapt=AEjHL4OVlHBZyIzfrw29E_Q4mYB5-Ei_wmrnL7Bw5Mvr51ST_6r9yfNADQL6wxYkdzGYKzB5DULwwhRcJaOEfKjloUDyhUbRCHUonLcj99aCP6EDXzOBBFM)
2. Tạo instance của EmailAlert
Ví dụ:
```
from email_alert import EmailAlert

    email_alert = EmailAlert(
        alert_email="recipient@example.com",
        smtp_user="your_email@example.com",
        smtp_password="your_password"
    )
    email_alert.send_email_alert("Test Alert", "This is a test message.")
```
3. Sử dụng phương thức send_email_alert để gửi thông báo:
Ví dụ:
```
subject = "Security Alert"
message = """
ALERT: Suspicious activity detected on your server.

Details:
- IP Address: 192.168.1.1
- Port: 8080
- Timestamp: 2024-12-03 10:00:00

Please investigate immediately.
"""
email_alert.send_email_alert(subject, message)

```
4. Sử dụng email_config.ini (OPTIONAL)
- Thay đổi mã nguồn đoạn: ```def __init__(self, config_path="email_config.ini")```
## Demo project cần gửi ALert từ database:
```
import sqlite3
from email_alert import EmailAlert

def check_and_send_alerts(db_path="alerts.db", email_config="email_config.ini"):
    """Kiểm tra cơ sở dữ liệu và gửi email nếu phát hiện cảnh báo mới."""
    email_alert = EmailAlert(config_path=email_config)
    
    if not os.path.exists(db_path):
        logging.error(f"Không tìm thấy cơ sở dữ liệu tại {db_path}.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT message FROM alerts WHERE status = 'new'")
        alerts = cursor.fetchall()

        if alerts:
            message = "New Alerts:\n" + "\n".join([alert[0] for alert in alerts])
            email_alert.send_email_alert("Security Alerts", message)
            logging.info("Cảnh báo đã được gửi thành công.")

            # Đánh dấu cảnh báo đã gửi
            cursor.execute("UPDATE alerts SET status = 'sent' WHERE status = 'new'")
            conn.commit()
        else:
            logging.info("Không có cảnh báo mới để gửi.")
    except Exception as e:
        logging.error(f"Lỗi khi xử lý cảnh báo: {e}")
    finally:
        conn.close()
```
