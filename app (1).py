from flask import Flask, request, jsonify
import requests
from instagrapi import Client
import os

app = Flask(__name__)

@app.route("/")
def index():
    return "InstaTrim Login Bot Çalışıyor!"

@app.route("/login")
def login_page():
    chat_id = request.args.get("chat_id")
    return f'''
    <h2>Instagram Giriş</h2>
    <form method="POST" action="/do-login?chat_id={chat_id}">
        <input type="text" name="username" placeholder="Kullanıcı Adı"><br>
        <input type="password" name="password" placeholder="Şifre"><br>
        <input type="submit" value="Giriş Yap">
    </form>
    '''

@app.route("/do-login", methods=["POST"])
def do_login():
    chat_id = request.args.get("chat_id")
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
            f"https://api.telegram.org/bot{os.getenv("TOKEN")}/sendMessage",
            data={"chat_id": chat_id, "text": message}
        )

        return "Giriş başarılı. Takip etmeyenler Telegram’a gönderildi."

    except Exception as e:
        return f"Giriş hatası: {str(e)}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)