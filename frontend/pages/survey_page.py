import taipy.gui.builder as tgb
from taipy.gui import navigate

from backend.models.survey import Survey
from backend.mongo_db import save_survey, get_travel_buddies
from backend.open_ai import generate_itinerary

survey = Survey()
generated_itinerary = ""
travel_buddies = ""

def plan_button_pressed(state, id, payload) -> None:
    state.assign("generated_itinerary", generate_itinerary(state.survey))
    state.assign("travel_buddies", get_travel_buddies(state.survey))
    state.assign("survey", survey)
    save_survey(state.survey)
    navigate(state=state, to="itinerary", force=True)

with tgb.Page() as SurveyPage:
    tgb.text(value="## Fill out this survey to help us plan the trip of your dreams!", mode="md")
    with tgb.layout("1 1"):
        with tgb.part():
            tgb.text(value="#### Personal Details", mode="md")
            tgb.input(value="{survey.first_name}", label="First Name")
            tgb.date(date="{survey.birth_date}", label="Birth Date")
            tgb.selector(value="{survey.gender}", lov=["Male", "Female", "Prefer not to share"], dropdown=True, label="Gender")
            tgb.text(value="#### Travel Details", mode="md")
            tgb.input(value="{survey.departure_city}", label="Departure City")
            tgb.input(value="{survey.arrival_city}", label="Arrival City")
            tgb.date_range(dates="{survey.date_range}", label_start="Departure Date", label_end="Return Date")
            tgb.selector(value="{survey.trip_purpose}", dropdown=True, lov=["Leisure/Vacation", "Business/Work", "Family/Friends Visit", "Adventure/Exploration", "Education/Cultural"], label="Purpose of the Trip")
            tgb.number(value="{survey.daily_budget}", label="Daily Budget (€)", hover_text="Excluding Flight and Hotel Expenses")
        with tgb.part():
            tgb.text(value="#### Additional Information", mode="md")
            tgb.selector(value="{survey.transportation_preference}", dropdown=True, lov=["Walking", "Bicycle", "Subway/Metro", "Tram", "Bus", "Taxi", "Car Rental"], label="Transportation Preference")
            tgb.text(value="ㅤ")
            tgb.text(value="Which attractions are you the most interested in?")
            tgb.selector(value="{survey.interests}", multiple=True, dropdown=True, lov=["Museums", "Parks", "Palaces", "Beaches", "Historical Sites", "Mountains", "Wildlife Reserves", "Architectural Landmarks", "Markets", "Adventure Activities", "Festivals", "Food Tours", "Botanical Gardens", "Temples/Shrines"], label="Interests")
            tgb.text(value="ㅤ")
            tgb.text(value="Any other interests or hobbies?")
            tgb.input(value="{survey.other_interests}", label="Surfing, karaoke, yoga...")
            tgb.text(value="ㅤ")
            tgb.toggle(value="{survey.other_cities}", label="Toggle if you want to visit other cities.")
            tgb.toggle(value="{survey.other_companions}", label="Toggle if you have travel companions.")
            tgb.text(value="ㅤ")
            tgb.text(value="Drop your social media link if you're looking for a travel buddy! We'll help you!")
            tgb.input(value="{survey.social_media_link}", label="Facebook, Instagram, etc.")
            tgb.text(value="ㅤ")
            tgb.button(label="Check Your Itinerary", class_name="plain", on_action=plan_button_pressed)
