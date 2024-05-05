import os
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient

from backend.models.survey import Survey

load_dotenv()
URI = os.getenv("MONGO_DB_URI")

def save_survey(survey: Survey) -> None:
    client = MongoClient(URI)
    database = client["TraWell"]
    collection = database["Survey"]
    collection.insert_one(survey.to_dict())
    client.close()

def get_travel_buddies(survey: Survey) -> str:
    if not survey.social_media_link:
        return ""

    client = MongoClient(URI)
    database = client["TraWell"]
    collection = database["Survey"]

    matches = []
    this_survey = survey.to_dict()
    others_surveys = collection.find({
        "social_media_link" : {"$ne": None},
        "arrival_city": {"$eq": this_survey["arrival_city"]},
    })
    for other_survey in others_surveys:
        this_departure_date = this_survey["date_range"][0]
        other_departure_date = other_survey["date_range"][0]
        this_return_date = this_survey["date_range"][1]
        other_return_date = other_survey["date_range"][1]
        if this_return_date < other_departure_date or this_departure_date > other_return_date:
            continue

        score = 0

        this_budget = this_survey["daily_budget"]
        other_budget = other_survey["daily_budget"]
        score += 1 if 2 * min(this_budget, other_budget) > max(this_budget, other_budget) else 0

        score += 1 if this_survey["other_cities"] == other_survey["other_cities"] else 0

        score += 1 if this_survey["transportation_preference"] == other_survey["transportation_preference"] else 0

        score += 1 if this_survey["trip_purpose"] == other_survey["trip_purpose"] else 0

        this_interests = set(this_survey["interests"])
        other_interests = set(other_survey["interests"])
        score += len(this_interests.intersection(other_interests))

        matches.append((score, other_survey["first_name"], other_survey["birth_date"], other_survey["social_media_link"]))

    client.close()

    if not matches:
        return ""

    result = "## Meet Your Potential Travel Buddies!\n\n##### They shared their social media link with us too. Feel free to reach out and learn more about them!\n"
    matches.sort(key=lambda match: match[0], reverse=True)
    rank = 1
    for score, first_name, birth_date, social_media_link in matches[: 3]:
        result += f"{rank}. [{first_name} - {int((datetime.now() - birth_date).days / 365.25)} years old]({social_media_link})\n"
        rank += 1
    return result
