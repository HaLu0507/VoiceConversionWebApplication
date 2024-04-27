from flask import Blueprint, render_template

top_page = Blueprint('top_page', __name__, template_folder='top_page_templates')

#最初の画面の表示
@top_page.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')