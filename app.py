from flask import Flask, render_template, request, redirect, flash, url_for, session
import os, requests

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your_default_secret')

ALLOWED_DOC_EXTENSIONS = {'pdf', 'epub', 'txt', 'doc', 'docx'}
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')
app.config['MAX_CONTENT_LENGTH'] = 600 * 1024 * 1024  # 600MB limit

def allowed_file(filename, types):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in types

@app.route('/', methods=['GET'])
def home():
    return render_template("Book.html", is_admin=session.get('admin') == True)

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['admin'] = True
            flash('✅ Logged in as admin')
            return redirect('/')
        else:
            flash('❌ Incorrect password')
            return redirect('/admin')
    return render_template("admin_login.html")

@app.route('/logout')
def logout():
    session.pop('admin', None)
    flash("Logged out successfully")
    return redirect('/')

@app.route('/upload', methods=['POST'])
def upload_file():
    if not session.get('admin'):
        flash('Unauthorized')
        return redirect('/admin')
    
    doc = request.files.get('book')
    if doc and allowed_file(doc.filename, ALLOWED_DOC_EXTENSIONS):
        try:
            # ✅ Upload to GoFile (2025 API)
            resp = requests.post(
                "https://api.gofile.io/upload",
                files={"file": (doc.filename, doc.stream, doc.mimetype)},
                headers={"Accept": "application/json"}
            )

            print("DEBUG GoFile Response:", resp.text)  # 👈 Render logs me dikhega

            try:
                result = resp.json()
            except Exception:
                flash("⚠️ Error: GoFile ne JSON ke bajaye kuch aur return kiya. Logs check karo.")
                return redirect('/')

            if result.get("status") == "ok":
                link = result["data"]["downloadPage"]
                flash(f'✅ File uploaded successfully! <a href="{link}" target="_blank">Download Here</a>')
            else:
                flash("❌ Upload failed, please try again.")
        except Exception as e:
            flash(f"⚠️ Error: {str(e)}")
    else:
        flash('❌ Invalid file type')
    
    return redirect('/')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # ✅ Render ke liye
    app.run(host="0.0.0.0", port=port, debug=True)
