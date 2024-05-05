import taipy.gui.builder as tgb

from frontend.pages.survey_page import survey, generated_itinerary, travel_buddies

with tgb.Page() as ItineraryPage:
    tgb.text(value="## Your Travel Itinerary is Ready!", mode="md")
    tgb.text(value="##### {survey.arrival_city} Trip", mode="md")
    tgb.text(value="##### {survey.trip_kind} | {survey.trip_purpose}", mode="md")
    tgb.text(value="{generated_itinerary}", mode="md")
    tgb.text(value="{travel_buddies}", mode="md")
