from flask import Blueprint, render_template, request, redirect
from .models.db_func import register, auth, isSameUser

login_signup = Blueprint('login_signup', __name__, template_folder='login_signup_templates')

# login
@login_signup.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

# sign up 
@login_signup.route('/sign_up', methods=['GET', 'POST'])
def signup():
    return render_template('sign_up.html')

# login, sign up 後の動作
@login_signup.route('/modeSelect', methods=['GET', 'POST'])
def modeSelect():
    # login か sign up をURLを取得することにより判定する
    login_or_signup = request.referrer.split('/')[-1]
    print(f"送信元URL : {login_or_signup}")

    # 入力されたユーザ名とパスワードを取得
    entered_name = request.form['username']
    entered_password = request.form['password']

    if login_or_signup == "sign_up":
        print(f"新たなユーザを登録する")
        try:
            # 同一ユーザがいるかどうか確認する
            if isSameUser(entered_name):
                print("同名のユーザが存在する")
                return redirect("/sign_up")
            
            else: # 同一のユーザがいない場合、登録する
                register(entered_name, entered_password)
                return render_template("modeSelect.html")
        
        except Exception as e:
            print(e)
            return redirect('/sign_up')
    
    elif login_or_signup == "login":
        print(f"ユーザの認証を行う")

        try:
            isAuth = auth(entered_name, entered_password)
            if isAuth: # 認証が正しく行われた時
                print("認証成功")
                return render_template("modeSelect.html")
            else: # 認証が失敗した時
                print("認証失敗")
                return redirect("/login")
        
        except Exception as e:
            print(e)
            return redirect("/login")
    
    else:
        print("Error")