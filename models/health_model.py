import requests

def fetch_healthfinder_stress_tips():
    url = "https://odphp.health.gov/myhealthfinder/api/v4/topicsearch.json?TopicId=30560"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        return data["Result"]["Resources"]["Resource"][0]["Sections"]["section"]
    except Exception as e:
        print("[HEALTH API ERROR]", e)
        return []
