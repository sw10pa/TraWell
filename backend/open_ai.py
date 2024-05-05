from openai import OpenAI

from backend.models.survey import Survey

def generate_itinerary(survey: Survey) -> str:
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "This is the application which allows user to input the data regarding their travel preferencies and depending on this data our application generates detailed daily itinerary for them. Your job is to analyze the data provided by the user and generate itinerary for them. I want to display your response in different paragraphs, whole text should be divided into as many paragraphs as there is a day in itinerary. Don't tal, generate plan and try to be more precise regarding places and times. To make parsing easier for me, return data in the following format: DAY 1: ... DAY 2: ... DAY 3: ... and so on. Generate for all the days!!! Not just for 3 days!!!"},
            {"role": "user", "content": f"{survey.to_dict()}"},
        ]
    )

    itinerary = ""
    content = completion.choices[0].message.content
    days_itinerary = content.split("DAY")[1:]
    for index, day_itinerary in enumerate(days_itinerary):
        itinerary += f"##### Day {index + 1} \n"
        itinerary += f"{day_itinerary[first_alpha_index(day_itinerary):]}\n\n"
    print(itinerary)
    return itinerary

def first_alpha_index(s: str) -> int:
    for i, char in enumerate(s):
        if char.isalpha():
            return i
    return -1
