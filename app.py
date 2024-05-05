from taipy import Gui

from frontend.pages.home_page import HomePage
from frontend.pages.survey_page import SurveyPage
from frontend.pages.itinerary_page import ItineraryPage

pages = {
    "/": HomePage,
    "survey": SurveyPage,
    "itinerary": ItineraryPage,
}

Gui(pages=pages).run(title="TraWell", use_reloader=True, dark_mode=False)
