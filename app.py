from flask import Flask, render_template, request
import pysolr
from pyvi import ViTokenizer

import searchh
app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    options = "Tất cả"
    if request.method == 'POST':

        name_input = request.form.get('name_input')
        lyric_input = request.form.get('lyric_input')

        if len(name_input) > 0 :
            if 'options' in request.form:
                options = request.form['options']
                results = searchh.search2('name', name_input, options)
                
            else:
                results = searchh.search1('name', name_input)

        elif len(lyric_input) > 0:
            if 'options' in request.form:
                options = request.form['options']
                results = searchh.search2('lyric', lyric_input, options)
                
            else:
                results = searchh.search1('lyric', lyric_input)
            name_input = lyric_input

        numFound = results.raw_response['response']['numFound']
        if numFound >20:    c =20
        else:   c = numFound

        return render_template('result.html',input=name_input, option= options, numFound = numFound,c=c,
            name=[results.docs[i]['name'][0] for i in range(0, c)],
            link=[results.docs[i]['link'][0] for i in range(0, c)],
            lyric=[results.docs[i]['lyric'][0]  for i in range(0,c)],
            tag=[results.docs[i]['tag'][0] for i in range(0, c)])

    elif request.method == 'GET':
        print("No Post Back Call")
        return render_template("index.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)