from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import requests

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Apna secure key rakhna

# ------------------------
# Home page
# ------------------------
@app.route("/")
def home():
    return render_template("Book.html", is_admin=("admin" in session))

# ------------------------
# Admin Login
# ------------------------
@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "admin" and password == "password":  # Apna cred change kar lena
            session["admin"] = True
            flash("✅ Login successful!")
            return redirect(url_for("home"))
        else:
            flash("❌ Invalid credentials")
    return render_template("admin_login.html")

# ------------------------
# Logout
# ------------------------
@app.route("/logout")
def logout():
    session.pop("admin", None)
    flash("✅ Logged out successfully")
    return redirect(url_for("home"))

# ------------------------
# Upload route → GoFile
# ------------------------
@app.route("/upload", methods=["POST"])
def upload():
    try:
        file = request.files["file"]
        if not file:
            return jsonify({"status": "error", "message": "No file uploaded"}), 400

        # File ko disk pe save nahi karna, direct stream GoFile ko forward
        files = {"file": (file.filename, file.stream, file.mimetype)}

        resp = requests.post(
            "https://upload.gofile.io/uploadFile",
            files=files
        )

        # Response GoFile se direct forward
        return resp.text, resp.status_code, {"Content-Type": "application/json"}

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ------------------------
# Run locally
# ------------------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
