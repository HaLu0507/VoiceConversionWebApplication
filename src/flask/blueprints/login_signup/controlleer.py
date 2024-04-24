from flask import Blueprint
# from flask import Flask

login_signup = Blueprint('login_signup', __name__, url_prefix='/blueprints/login_signup')

#パスワード認証
@login_signup.route('/login', methods=['GET', 'POST'])
def modeSelect():
    # フォームから送信されたユーザー名とパスワードを取得
    try:
        entered_password = request.form['data1']
        if(not entered_password == "webapp2023"):
            return render_template('login.html')
        else:
            return render_template('modeSelect.html')

    except:
        return render_template('login.html')