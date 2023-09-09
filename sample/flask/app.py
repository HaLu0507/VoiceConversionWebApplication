from flask import Flask, render_template, request
from sentimentAnalyze import getSentiment
from getSimilarity import calcSimilarity

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST': # データを受け取るとき
        text = request.form.get('user_tweet')
        usr_feel, usr_feel_point = getSentiment(text)
        usr_feeling = f"{usr_feel}(score : {usr_feel_point})"

        if usr_feel == "ポジティブ":
            artist, song, score = calcSimilarity(text, True)
        else:
            artist = "Nothing"
            song = "Nothing"
            score = "None"

        return render_template('index.html', text=text, usr_feeling=usr_feeling, artist_name=artist, song_name=song, song_feeling="ポジティブ", similar_point=score)
    else: # データを渡すとき
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)