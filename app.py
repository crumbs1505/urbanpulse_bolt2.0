from flask import Flask, request, render_template
import requests

app = Flask(__name__)

def aqi(city,city_dict):
    api_key = "5e471b4b35198fd08b744e5cd5a6306dba8f4e6d"
    url = f'https://api.waqi.info/feed/{city}/?token={api_key}'
    response = requests.get(url)
    json_data = response.json()
    geo = json_data['data']['city']['geo']
    lat = geo[0]
    long = geo[1]
    aqi = json_data['data']['aqi']

    city_dict['name'] = city
    city_dict['lat'] = lat
    city_dict['long'] = long
    city_dict['aqi'] = aqi
    return aqi


def aqirankfinder(aqi):
    #aqiranklogic
    if(aqi<50):
        aqirank=10
    elif(aqi>50 and aqi<100):
        aqirank=8
    elif(aqi>100 and aqi<150):
        aqirank=6
    elif(aqi>150 and aqi<200):
        aqirank=4
    elif(aqi>200 and aqi<300):
        aqirank=2
    else:
        aqirank=0
    return aqirank

def uv(city,city_dict):
    api_key = "openuv-13xm4grlsx39x07-io"
    header = {'x-access-token': "openuv-13xm4grlsx39x07-io"}
    url = f"https://api.openuv.io/api/v1/uv?lat={city_dict['lat']}&lng={city_dict['long']}&alt=100&dt=2024-02-20T13:30:00.000Z"
    response = requests.get(url,headers=header)
    json_data = response.json()
    uv = json_data['result']['uv_max']
    city_dict['uv'] = uv
    return uv

def uvrankfinder(uv):
    #uvranklogic
    if(uv<2):
        uvrank=10
    elif(uv>2 and uv<5):
        uvrank=7
    elif(uv>5 and uv<8):
        uvrank=4
    elif(uv>8):
        uvrank=0
    return uvrank


@app.route('/')
def index():
    return render_template('up.html')
@app.route('/index.html')
def second():
    return render_template('index.html')

@app.route('/compare_cities', methods=['POST'])
def compare_cities():
    city_a = request.form.get('A')
    city_a_dict={}
    city_b = request.form.get('B')
    city_b_dict={}

    aqi_a = aqi(city_a,city_a_dict)
    aqi_b= aqi(city_b,city_b_dict)

    uv_a = uv(city_a,city_a_dict)
    uv_b = uv(city_b,city_b_dict)

    aqirank_a=aqirankfinder(aqi_a)
    aqirank_b=aqirankfinder(aqi_b)
    uvrank_a=uvrankfinder(uv_a)
    uvrank_b=uvrankfinder(uv_b)

    score_a=aqirank_a+uvrank_a
    score_b=aqirank_b+uvrank_b

    comparison_result = {
        'city_a': {
            'name': city_a,
            'aqi': aqi_a,
            'uv': uv_a,
            'score': score_a
        },
        'city_b': {
            'name': city_b,
            'aqi': aqi_b,
            'uv': uv_b,
            'score': score_b
        }
        
    }

    return render_template('results.html', comparison_result=comparison_result)

if __name__ == '__main__':
    app.run(debug=True)