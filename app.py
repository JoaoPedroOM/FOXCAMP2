from cs50 import SQL
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, flash, session, url_for

app = Flask(__name__)
app.secret_key = "Felipe Wai"

app.config["TEMPLATES_AUTO_RELOAD"] = True

db = SQL("sqlite:///database.db")

@app.route("/")
def homepage():
    if "user_id" in session:
        user = session["user_id"]
        get_nome = db.execute("SELECT * FROM users WHERE id = ?", user)
        return render_template("homepageloged.html", username=get_nome)
    return render_template("homepage.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email").upper()
        password = request.form.get("password")
        if not email:
            flash("Email faltando!", category='info')
            return redirect("/login")
        elif not password:
            flash("Senha faltando!", category='info')
            return redirect("/login")
        
        rows = db.execute("SELECT * FROM users WHERE email = ?", email)

        if len(rows) != 1 or not check_password_hash(rows[0]['senha'], password):
            flash("Email ou senha inválido!", category='info')
            return redirect("/login")

        session["user_id"] = rows[0]["id"]

        username = db.execute("SELECT * FROM users WHERE id = ?", rows[0]['id'])
        for rows in username:
            usr = rows['nome']
        
        return redirect(url_for("usr", usr=usr))

        
        

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        genero = "masculino"
        nome = request.form.get("nome").upper()
        sobrenome = request.form.get("sobrenome").upper()
        email = request.form.get("email").upper()
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        if not email:
            flash("Email faltando!", category="info")
            return redirect("/register")
        if not nome:
            flash("Nome faltando!", category="info")
            return redirect("/register")
        if not sobrenome:
            flash("Sobrenome faltando!", category="info")
            return redirect("/register")
        if not password:
            flash("Senha faltando!", category="info")
            return redirect("/register")
        if not confirm_password:
            flash("Confirme sua senha!", category="info")
            return redirect("/register")
        if password != confirm_password:
            flash("Senhas não coincidem!", category="info")
            return redirect("/register")
        password_hash = generate_password_hash(password)
        db = db.execute("INSERT INTO users (nome, sobrenome, email, genero, senha) VALUES (?, ?, ?, ?, ?)", nome, sobrenome, email, genero, password_hash)
        return redirect("/")

@app.route("/users/<usr>")
def userpage(usr):
    return render_template("usrpage.html", user=usr)

if __name__ == "__main__":
    app.run(debug=True)

