import flask
from flask import request, jsonify
import json
import requests
from flask_cors import CORS 

app = flask.Flask(__name__)
app.config["Debug"] = True
CORS(app)


@app.route('/api/Movies', methods=['GET']) #get Movies Endpoint
def getMovies():

    if 'source' in request.args:
        txt = str(request.args['source'])
        

        if txt == 'BM':
            file = open('boxoffice.json','r')
            file = file.read()
            content = json.loads(file)
            

            return jsonify(content)

        elif txt == 'RT':
            file = open('movies.json','r')
            file = file.read()
            content = json.loads(file)

    
            

            return jsonify(content)
    else:
        return 'Error: no source provided. Please try again...'
    
   


@app.route('/api/Weather',methods=['GET']) #get Weather Endpoint Leveraging OpenWeather APIs
def getWeather():
    if 'zip' in request.args:
        zip_code = str(request.args['zip'])
        country_code = str(request.args['ctry'])
        key = ''
        path = f'http://api.openweathermap.org/data/2.5/weather?zip={zip_code},{country_code}&appid={key}'

        print(path)

        response = requests.get(path)
        response = response.json()
        #print(response.keys())

        #kel to fahr 9/5(kel - 273.15) + 32

        def KelToFahr(temp):
            
            fahr = int((9/5) * (temp - 273.15) + 32)
            return fahr

        local = response.get('name')
        #print(local)
        actual_temp = KelToFahr(response.get('main')['temp'])
        feels_like = KelToFahr(response.get('main')['feels_like'])
        high = KelToFahr(response.get('main')['temp_max'])
        low = KelToFahr(response.get('main')['temp_min'])
        #print(f'Today:\nHigh:{high} Low:{low}')
        #print(f'Right Now:\nActual:{actual_temp} Feels Like: {feels_like}')

        desc = response.get('weather')[0]['description']
        print(desc)

        '''    
        resp = flask.make_response()
        resp.headers['Access-Control-Allow-Origin'] = "*"
        '''
        response = {
                    'location': local,
                    'description': desc,
                    'current': {'High': high, 'Low': low,
                                'Actual': actual_temp, 'Feels': feels_like}
                   }
        '''
        response["headers"] = {

                          'Content-Type': 'application/json',
                          "Access-Control-Allow-Origin" : "*",
                          "Access-Control-Allow-Credentials" : True

                            }

        '''
        return jsonify(response)

    else:
        return 'Error: missing parameter. Please try again.'

@app.route('/api/Stocks', methods=['GET']) #get Stocks Via NASDAQ.com
def getStocks():
    if 'source' in request.args:
        txt = str(request.args['source'])
        

        if txt == 'NAS':
            file = open('stocks.json','r')
            file = file.read()
            content = json.loads(file)
            

            return jsonify(content)
    else:
        return 'Error: no source provided. Please try again...'

@app.route('/api/News', methods=['GET']) #get News via NY Times
def getNews():
    if 'source' in request.args:
        txt = str(request.args['source'])
        print(txt)

        if txt == 'NYTimes':
            file = open('NYnews.json','r')
            file = file.read()
            content = json.loads(file)
            

            return jsonify(content)
        elif txt == 'CNN':
            file = open('CNNnews.json','r')
            file = file.read()
            content = json.loads(file)

            return jsonify(content)

        elif txt == 'NPR':
            file = open('NPRnews.json','r')
            file = file.read()
            content = json.loads(file)

            return jsonify(content)
    else:
        return 'Error: no source provided. Please try again...'

@app.route('/api/RedditFeed', methods=['GET'])
def getReddit():
    file = open('RedditPosts.json','r')
    file = file.read()
    content = json.loads(file)

    return jsonify(content)

@app.route('/api/SportsFeed', methods=['GET'])
def getSport():
    if 'sport' in request.args:
        txt = str(request.args['sport'])
        print(txt)

        name = txt

        raw_file = open('Sports.json','r')

        file = json.load(raw_file)
        

        content = {'collection': file.get(name)}

        return jsonify(content)
    


#app.run('0.0.0.0')

app.run(debug="True")
