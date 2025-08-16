from flask import Flask, render_template, request, redirect, flash, session
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your_default_secret')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')

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

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
