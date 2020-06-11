from flask import Flask, render_template, request
import pysolr
import json

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    user_input = ""
    options = "Tất cả"
    if request.method == 'POST':
        solr = pysolr.Solr(
            'http://localhost:8983/solr/tktdtt', always_commit=True)

        if 'user_input' in request.form:
            if 'options' in request.form:

                user_input = request.form['user_input']
                options = request.form['options']
                def search1(ip, op):

                    key = 'lyric : "' + ip +'"'
            
                    results = solr.search(key,**{
                        'rows': 100000,
                        'fq': {'tag :' + op }
                    })

                    return results

                results = search1(user_input, options)

            else:
                user_input = request.form['user_input']
                def search2(ip):

                    key = 'lyric : "' + ip +'"'
        
                    results = solr.search(key,**{
                        'rows': 100000 
                    })

                    return results

                results = search2(user_input)

        c = len(results)
        return render_template('result.html',input=user_input, option= options,
            name=[results.docs[i]['name'][0] for i in range(0, c)],
            link=[results.docs[i]['link'][0] for i in range(0, c)],
            lyric=[results.docs[i]['lyric'][0]  for i in range(0, c)],
            tag=[results.docs[i]['tag'][0] for i in range(0, c)],c =c)

    elif request.method == 'GET':
        print("No Post Back Call")
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)