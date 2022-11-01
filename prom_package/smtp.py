import smtplib
from email.message import EmailMessage

from prom_package.config import PATH_PROM, SMTP_CONFIG


def send_email(messeg):
    msg = EmailMessage()
    msg.set_content(f'PATH_PROM = {PATH_PROM}\r\n\n{messeg}')
    msg['Subject'] = 'WARNING Prom data update has falled'
    msg['From'] = f'<{SMTP_CONFIG.from_addr}> Prom data update'
    msg['To'] = SMTP_CONFIG.to_addr

    # print(f'msg = {msg}')
    with smtplib.SMTP(SMTP_CONFIG.host) as s:
        s.login(*SMTP_CONFIG.user_password)
        # s.set_debuglevel(1)
        s.send_message(msg)


if __name__ == '__main__':
    send_email('TEST  \r\ntest test')
