
from flask import Flask, request, render_template_string, jsonify
from instagrapi import Client

app = Flask(__name__)

LOGIN_FORM = """{{ login_html }}"""

@app.route("/", methods=["GET"])
def index():
    return render_template_string(LOGIN_FORM, login_html=LOGIN_FORM)

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
        return jsonify({
            "status": "success",
            "not_following_back": not_following_back[:10]
        })
    except Exception as e:
        return jsonify({ "status": "fail", "message": str(e) })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
