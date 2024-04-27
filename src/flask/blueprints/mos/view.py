from flask import Blueprint, render_template, request

mos = Blueprint('mos', __name__, template_folder='mos_templates')

#Naturalness
@mos.route('/NaturalnessMOS', methods=['GET', 'POST'])
def naturalnessMOS():
    return render_template('naturalnessMOSSample.html')


#Similarity
@mos.route('/SimilarityMOS', methods=['GET', 'POST'])
def similarityMos():
    return render_template('mosSelect.html')

#Naturalnessで評価画面へ
@mos.route('/NaturalnessEvaluation', methods=['GET', 'POST'])
def NaturalnessEvaluation():
    model = request.form.get('model')
    audio = request.form.get('audio')
    if  not(model == None) or not(audio == None):
        return render_template('naturalnessMOSEvaluation.html')
    else:
        return render_template('naturalnessMOSSample.html')

#Naturalnessの評価結果
@mos.route('/NaturalnessEvaluationRes', methods=['GET', 'POST'])
def naturalnessEvaluationRes():
    mosNaturalnessRes = []
    for i in range(5):
        p = request.form.get('test' + str(i+1))
        if(p == None):
            return render_template('naturalnessMOSEvaluation.html')
        mosNaturalnessRes.append(p)
    return render_template('login.html')