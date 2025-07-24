from models.health_model import fetch_healthfinder_stress_tips

def get_stress_tips():
    try:
        sections = fetch_healthfinder_stress_tips()
        return [(sec["Title"], sec["Content"]) for sec in sections]
    except:
        return []
