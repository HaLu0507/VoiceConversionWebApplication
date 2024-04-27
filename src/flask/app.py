# coding: UTF-8
from flask import Flask

# blueprint の import 
from blueprints.top_page.view import top_page
from blueprints.login_signup.view import login_signup
from blueprints.modeSelect.view import modeSelect
from blueprints.mos.view import mos
from blueprints.vc_file.view import vc_file
from blueprints.vc_record.view import vc_record

app = Flask(__name__)
# セッション情報を暗号化するために使用する
# この設定はflashを使用するために必要
app.secret_key = 'secret_key'

# blueprint の登録
app.register_blueprint(top_page)
app.register_blueprint(login_signup)
app.register_blueprint(modeSelect)
app.register_blueprint(mos)
app.register_blueprint(vc_file)
app.register_blueprint(vc_record)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=5009)
