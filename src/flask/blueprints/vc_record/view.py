from flask import Blueprint, render_template

vc_record = Blueprint('vc_record', __name__, template_folder='vc_record_templates')

#最初の画面の表示
@vc_record.route('/', methods=['GET', 'POST'])
def convert_record_audio():
    return render_template('vc_record.html')