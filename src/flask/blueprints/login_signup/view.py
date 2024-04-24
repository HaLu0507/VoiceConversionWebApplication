from flask import Blueprint

login_signup = Blueprint('login_signup', __name__, url_prefix='/blueprints/login_signup')

#サインアップ
@login_signup.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')

#サインアップ
@login_signup.route('/modeSelect2', methods=['GET', 'POST'])
def modeSelect2():
    return render_template('modeSelect.html')