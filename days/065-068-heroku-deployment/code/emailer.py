import smtplib

smtp_server = smtplib.SMTP('smtp.gmail.com', 587)

smtp_server.ehlo()

smtp_server.starttls()

smtp_server.login('stevegleds@gmail.com', 'tgdm mcpa jqkm hpiq')

smtp_server.sendmail('<stevegleds@gmail.com', '<steve@pcresolver.es>', 'Subject: Hello from Heroku!\nTest email from my Heroku test app. Cheers! \nSteve')

smtp_server.quit()
