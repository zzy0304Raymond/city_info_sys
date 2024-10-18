from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_city_info', methods=['POST'])
def get_city_info():
    city_name = request.form['city_name']
    city_data = get_city_data(city_name)  # 从 API Ninjas 获取城市数据  OK
    wiki_data = get_wiki_info(city_name)  # 从维基百科获取城市信息  OK
    gaode_data = get_gaode_info(city_name)  # 从高德地图获取城市坐标  OK
    economic_data = get_economic_data(city_name)  # 从 NewsAPI 获取经济相关消息
    tech_news_data = get_tech_news(city_name)  # 从科技新闻API获取最新科技消息
    news_data = get_news(city_name)  # 从新闻API获取最新新闻  OK
    air_quality_data = get_air_quality(city_name)  # 从 API Ninjas 获取空气质量信息  OK
    # tourist_spots_data = get_tourist_spots(city_name)  # 从 Geoapify 获取旅游景点
    # weather_data = get_weather_info(city_name)  # 从 OpenWeatherMap 获取天气信息
    return jsonify({
        **city_data, 
        **wiki_data, 
        **gaode_data, 
        **air_quality_data, 
        **news_data,
        **economic_data,
        **tech_news_data
    })

def get_tourist_spots(city_name):
    api_url = f"https://api.geoapify.com/v1/places?text={city_name}&categories=tourism&limit=5&apiKey=f9db5b977224486ab40cfd847d043dd0"
    
    try:
        response = requests.get(api_url)
        
        if response.status_code == 200:
            spots_data = response.json()
            spots_list = []
            for spot in spots_data.get('features', []):
                spots_list.append({
                    "name": spot["properties"]["name"],
                    "address": spot["properties"].get("formatted", "地址未提供")
                })
            return {"tourist_spots": spots_list}
        
        else:
            return {"error": "未找到旅游景点"}
    
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
        return {"error": "请求失败"}

def get_city_data(city_name):
    # 使用 API Ninjas 获取城市数据
    api_ninjas_url = f'https://api.api-ninjas.com/v1/city?name={city_name}'
    response = requests.get(api_ninjas_url, headers={'X-Api-Key': 'PpwILlvK17NLbijRSv9yHA==CfDdU4ozIkv5qlCQ'})  # 替换为你的 API Ninjas 密钥
    if response.status_code == 200:
        city_info = response.json()
        if city_info:
            return {
                'name': city_info[0]['name'],
                'population': city_info[0]['population'],
                'country': city_info[0]['country']
            }
        else:
            return {'error': '未找到相关信息'}
    else:
        return {'error': '请求失败'}

def get_news(city_name):
    api_key = "e839f71bb3ab49a8bdd25c58dce51fec"  # 替换为你的新闻API密钥
    url = f"https://newsapi.org/v2/everything?q={city_name}&apiKey={api_key}"
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            news_data = response.json()
            articles = news_data.get("articles", [])
            news_list = [{"title": article["title"], "url": article["url"]} for article in articles[:5]]
            return {"news": news_list}
        
        else:
            return {"error": "未找到相关社会新闻"}
    
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
        return {"error": "请求失败"}

def get_economic_data(city_name):
    api_key = "e839f71bb3ab49a8bdd25c58dce51fec"  # 替换为你的新闻API密钥
    url = f"https://newsapi.org/v2/everything?q={city_name}+economy&apiKey={api_key}"
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            news_data = response.json()
            articles = news_data.get("articles", [])
            economic_news_list = [{"title": article["title"], "url": article["url"]} for article in articles[:5]]
            return {"economic_news": economic_news_list}
        
        else:
            return {"error": "未找到经济相关新闻"}
    
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
        return {"error": "请求失败"}

def get_tech_news(city_name):
   api_key = "e839f71bb3ab49a8bdd25c58dce51fec"  # 替换为你的科技新闻API密钥
   url = f"https://newsapi.org/v2/everything?q={city_name}+technology&apiKey={api_key}"
   
   try:
       response = requests.get(url)
       
       if response.status_code == 200:
           news_data = response.json()
           articles = news_data.get("articles", [])
           tech_news_list = [{"title": article["title"], "url": article["url"]} for article in articles[:5]]
           return {"tech_news": tech_news_list}
       
       else:
           return {"error": "未找到科技相关新闻"}
   
   except requests.exceptions.RequestException as e:
       print(f"请求错误: {e}")
       return {"error": "请求失败"}

def get_wiki_info(city_name):
    # 使用维基百科API获取城市信息
    url = f'https://zh.wikipedia.org/w/api.php?action=query&format=json&list=search&srsearch={city_name}&utf8=1'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['query']['search']:
            page_title = data['query']['search'][0]['title']
            page_url = f'https://zh.wikipedia.org/wiki/{page_title}'
            return {'wiki_title': page_title, 'wiki_url': page_url}
        else:
            return {'error': '未找到相关信息'}
    else:
        return {'error': '请求失败'}

def get_gaode_info(city_name):
    # 使用高德地图API获取城市坐标
    api_url = f'https://restapi.amap.com/v3/geocode/geo?address={city_name}&key=302fc8f01ea33caae9306e983b557fe6'  # 替换为你的高德API密钥
    response = requests.get(api_url)
    
    # 打印响应内容以进行调试
    print("高德地图API响应:", response.json())
    
    if response.status_code == 200:
        city_info = response.json()
        if 'geocodes' in city_info and city_info['geocodes']:
            location = city_info['geocodes'][0]['location'].split(',')
            return {
                'latitude': location[1],
                'longitude': location[0]
            }
        else:
            return {'error': '未找到相关信息'}
    else:
        return {'error': '请求失败'}

def get_geodb_info(city_name):
    api_url = f'https://geodb-free-service.wirefreethought.com/v1/geo/cities?namePrefix={city_name}&limit=1'
    
    try:
        response = requests.get(api_url)
        
        if response.status_code == 200:
            city_info = response.json()
            print("GeoDB API响应:", city_info)  # 打印响应内容
            
            if city_info['data']:
                return {
                    'region': city_info['data'][0]['region'],
                    'population': city_info['data'][0]['population'],
                    'timezone': city_info['data'][0].get('timezone', '未提供')  # 使用 .get() 方法避免 KeyError
                }
            else:
                return {'error': '未找到相关信息'}
        else:
            return {'error': '请求失败'}
    
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
        return {'error': '请求失败'}


def get_country_info(city_name):
    api_url = f'https://restcountries.com/v3.1/name/{city_name}'
    
    try:
        response = requests.get(api_url)
        
        if response.status_code == 200:
            country_info = response.json()
            if country_info:
                return {
                    'region': country_info[0]['region'],
                    'population': country_info[0]['population'],
                    'capital': country_info[0]['capital'][0] if 'capital' in country_info[0] else "未提供"
                }
            else:
                return {'error': '未找到相关城市信息'}
        else:
            return {'error': '请求失败'}
    
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
        return {'error': '请求失败'}

def get_air_quality(city_name):
    api_url = f'https://api.api-ninjas.com/v1/airquality?city={city_name}'
    
    try:
        response = requests.get(api_url, headers={'X-Api-Key': 'PpwILlvK17NLbijRSv9yHA==CfDdU4ozIkv5qlCQ'})
        
        if response.status_code == 200:
            air_quality_data = response.json()
            if air_quality_data and "overall_aqi" in air_quality_data:
                return {
                    "air_quality_index": air_quality_data["overall_aqi"],
                    "pollutants": air_quality_data
                }
            else:
                return {"error": "未找到空气质量信息"}
        else:
            return {"error": "请求失败"}
    
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
        return {"error": "请求失败"}

def get_weather_info(city_name):
    api_key = "4174d0fdbb515a1bb35dedcd67ea8310"  # 替换为你的天气API密钥
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if data.get("main"):
            return {
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "weather": data["weather"][0]["description"]
            }
        else:
            return {"error": "未找到天气信息"}
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
        return {"error": "请求失败"}
    


if __name__ == '__main__':
    app.run(debug=True)