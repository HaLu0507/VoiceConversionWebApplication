from flask import Blueprint, render_template

modeSelect = Blueprint('modeSelect', __name__, template_folder='modeSelect_templates')

#音声ファイルで変換
@modeSelect.route('/modeFile', methods=['GET', 'POST'])
def modeFile():
    return render_template('vc_file.html',boolean = False)

#音声を録音して変換
@modeSelect.route('/modeRecord', methods=['GET', 'POST'])
def modeRecord():
    return render_template('vc_record.html')

#MOSモード
@modeSelect.route('/modeMOS', methods=['GET', 'POST'])
def modeMos():
    return render_template('mosSelect.html')