import requests
import math

def calculate_distance(lat1, lng1, lat2, lng2):
    """
    2点間の距離を計算する関数
    """
    earth_radius = 6371  # 地球の半径 (km)
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = (math.sin(dlat/2) * math.sin(dlat/2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlng/2) * math.sin(dlng/2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = earth_radius * c
    return distance

def get_location(api_key, address):
    """
    指定された住所から緯度と経度を取得する関数
    """
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "key": api_key,
        "address": address,
        "language": "ja"  # 日本語に設定
    }
    res = requests.get(url, params=params).json()
    location = res["results"][0]["geometry"]["location"]
    return f"{location['lat']},{location['lng']}"

def search_places(api_key, keywords, location, radius, types=''):
    if isinstance(keywords, list):
        keyword = "|".join(keywords)
    else:
        keyword = keywords
    """
    指定された場所から指定されたキーワードに基づいて、半径2km以内の場所を検索する
    結果は、施設名、住所、検索地点からの距離で返す
    """
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "key": api_key,
        "keyword": keyword,
        "location": location,
        "radius": radius,
        "types": types,
        "language": "ja"  # 日本語に設定
    }
    places = []
    res = requests.get(url, params=params).json()
    for place in res["results"]:
        name = place["name"]
        address = place["vicinity"]
        lat = place["geometry"]["location"]["lat"]
        lng = place["geometry"]["location"]["lng"]
        distance = round(calculate_distance(float(location.split(",")[0]), float(location.split(",")[1]), lat, lng), 1)
        places.append({
            "name": name,
            "address": address,
            "distance": distance
        })
    return places

#出力テスト
# api_key = ""
# address = ""
# radius = "2000"
# keywords = "サウナ"

# location = get_location(api_key, address)
# places = search_places(api_key, keywords, location, radius)
# for place in places:
#     print(place["name"], place["address"], f"{place['distance']:.2f} km")
