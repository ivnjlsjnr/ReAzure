# controllers/health_controller.py

from models.health_model import fetch_healthfinder_stress_tips

CATEGORY_MAPPING = {
    "Planning": [
        "Take Action: Plan and Prepare"
    ],
    "Relaxation": [
        "Take Action: Relax"
    ],
    "Lifestyle": [
        "The Basics: Benefits of Lowering Your Stress"
    ],
    "Support": [
        "The Basics: Signs and Health Effects",
        "The Basics: Causes of Stress"
    ]
}


def get_stress_tips():
    try:
        return [(section["Title"], section["Content"]) for section in fetch_healthfinder_stress_tips()]
    except Exception as e:
        print("[PARSE ERROR]", e)
        return []

def categorize_tip(title: str) -> str:
    for category, keywords in CATEGORY_MAPPING.items():
        if title.strip() in keywords:
            return category
    return "Other"
