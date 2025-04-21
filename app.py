
from flask import Flask, request, render_template_string, redirect, session
from instagrapi import Client
import os
import requests

app = Flask(__name__)
app.secret_key = 'supersecretkey'

LOGIN_FORM = '''
    <form method="POST">
        <input name="username" placeholder="Kullanıcı Adı" required><br>
        <input name="password" type="password" placeholder="Şifre" required><br>
        <button type="submit">Giriş Yap</button>
    </form>
'''

VERIFY_FORM = '''
    <form method="POST">
        <input name="code" placeholder="Gelen Kodu Gir" required><br>
        <button type="submit">Kodu Doğrula</button>
    </form>
'''

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        cl = Client()

        def challenge_code_handler(choice):
            session["challenge"] = cl.challenge
            return redirect("/verify")

        cl.challenge_code_handler = challenge_code_handler

        try:
            cl.login(username, password)
            followers = cl.user_followers(cl.user_id)
            followings = cl.user_following(cl.user_id)
            not_following_back = [uid for uid in followings if uid not in followers]
            first_10 = not_following_back[:10]
            message = "Seni takip etmeyen ilk 10 kişi:
" + "\n".join([str(uid) for uid in first_10]) if first_10 else "Herkes seni geri takip ediyor!"
            requests.post(f"https://api.telegram.org/bot{os.environ['TOKEN']}/sendMessage", data={
                "chat_id": os.environ['CHAT_ID'],
                "text": message
            })
            return "Giriş başarılı, mesaj Telegram'a gönderildi."
        except Exception as e:
            if "challenge" in str(e).lower():
                session["cl"] = cl.get_settings()
                return redirect("/verify")
            return f"Giriş hatası: {str(e)}"

    return render_template_string(LOGIN_FORM)

@app.route("/verify", methods=["GET", "POST"])
def verify():
    if "cl" not in session:
        return redirect("/")
    cl = Client()
    cl.set_settings(session["cl"])
    cl.challenge = session["challenge"]

    if request.method == "POST":
        code = request.form["code"]
        try:
            cl.challenge_resolve(code)
            followers = cl.user_followers(cl.user_id)
            followings = cl.user_following(cl.user_id)
            not_following_back = [uid for uid in followings if uid not in followers]
            first_10 = not_following_back[:10]
            message = "Seni takip etmeyen ilk 10 kişi:
" + "\n".join([str(uid) for uid in first_10]) if first_10 else "Herkes seni geri takip ediyor!"
            requests.post(f"https://api.telegram.org/bot{os.environ['TOKEN']}/sendMessage", data={
                "chat_id": os.environ['CHAT_ID'],
                "text": message
            })
            return "Doğrulama başarılı, Telegram'a mesaj gönderildi."
        except Exception as e:
            return f"Doğrulama hatası: {str(e)}"

    return render_template_string(VERIFY_FORM)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
