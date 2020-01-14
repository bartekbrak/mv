import smtplib
from email.message import EmailMessage

who = (
    ('bartek@brak.dev', 'misuczki17'),
    # tu była lista emaili
)
template = """
Cześć, 

Wyłączam https://bartekbrak.slack.com/.
Przenosimy się na https://klub.brak.dev/aa.
Twoje dane do logowania to:
user: {email}
hasło: {password}

Zmień hasło po zalogowaniu się. Account Settings > Security > Password.

Problemy: pisz na bartek@brak.dev

Bartek 
"""

server = smtplib.SMTP_SSL('smtp.yandex.com:465')
server.login('bartek@brak.dev', 'misuczki17')

for email, password in who:
    print(email)
    try:
        msg = EmailMessage()
        msg['Subject'] = 'Przenosimy się na https://klub.brak.dev/aa.'
        msg['From'] = 'bartek@brak.dev'
        msg['To'] = 'bartek@brak.dev'
        msg.set_content(template.format(email=email, password=password))
        server.sendmail('bartek@brak.dev', email, msg.as_string())
    except Exception as a:
        print(a)

server.quit()