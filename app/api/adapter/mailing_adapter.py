def mailing_message(email):
    "https://api.mailgun.net/v3/sandboxa9ce70879809408aa3386c574ebdf5e6.mailgun.org/messages",
    auth = ("api", "d470b0501ac7d51991d94c5c43b52951-059e099e-c9fa3bca"),
    data = {
        "from": "Decisions 1.0<mailgun@sandboxa9ce70879809408aa3386c574ebdf5e6.mailgun.org>",
        "to": [email],
        "subject": "Contact Response",
        "text": "Thank for your expressed interest. We will definitely take your opinions on board when improving "
                f"Decisions 1.0. In order to register your query please email {email} with your issue and will "
                "take it from there. Once again, thank you for your expressed interest and have a lovely day."}