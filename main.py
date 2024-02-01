# Import from standard library
import os
import sys
import numpy as np
import openai

from taipy.gui import Gui, notify



def generate_idea(state):
    """ generate idea based on user selection plus random selection of hints """
    state.idea = ""
    hints = []
    for i, one_list  in enumerate(list_of_hints):
        j = np.random.randint(len(one_list))
        hints.append(one_list[j])

    hints_str = ' '.join(hints)

    if state.app_type == "":
        notify(state, "error", "Please select an application type")
        return
    if state.target_user == "":
        notify(state, "error", "Please select an option under 'for' ")
        return
    if state.improvement == "":
        notify(state, "error", "Please select an option under 'to be more' ")
        return

    state.prompt = (
        f"Generate a web application idea using these keywords :\
        '{state.app_type} {state.target_user}  {state.improvement}  "\
        f"  {hints_str}'.  Use less than 1000 characters to describe. \n\n\n\n"
    )
    print(state.prompt)
    response = state.client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"{state.prompt}",
            }
        ],
        model="gpt-3.5-turbo",
    )
    state.idea = response.choices[0].message.content


link_words = ['Create a ', ' for ',
              ' that helps the user to be more ', ' using these hints: ']
APP_TYPE = ['Game', 'Spreadsheet', 'Editor', 'Ticketing', 'Entertainment', 'News',\
             'Movies', 'Room booking', 'Reservation', 'To-do list','Money tracking',\
             'Reminder', 'Music', 'Recipe', 'Accouting', 'Trading', 'Law', 'Inventory',\
             'Human Resources', 'Procurement']
TARGET_USER = ['Business', 'Students', 'Academic',
               'Personal', 'Team', 'Elderly', 'Youth', 'Middle-age']
IMPROVEMENT = ['Decisive', 'Efficent', 'Timely',
               'Innovative', 'Creative', 'Diversify']

MADE_OF = ['Metal', 'Wood', 'Plastic', 'Edible', 'Paper', 'Organic']
POWER_BY = ['Manual', 'Electric', 'Clockwork', 'Solar', 'Wind', 'Water']
OF_SIZE = ['Giant', 'Mini', 'Pocket', 'Portable', 'Wearable', 'Inhabitable']
RUN_ON = ['Robot', 'Vehicle', 'Computer', 'Game', 'Tool', 'Art']
# USED_BY=['Family', 'Personal', 'Office', 'Home', 'Industrial', 'Public']
BY_MEANS = ['Flying', 'Random', 'Self-Build',
            'Underwater', 'Stealth', 'Disposable']

list_of_hints = [POWER_BY, OF_SIZE, RUN_ON, BY_MEANS]
client = None

# Variables
idea = ""
prompt = ""

app_type = "Spreadsheet"
target_user = "Students"
improvement = "Timely"

page = """
<|container|
# **Create** Ideas for your side projects #

This app creates project ideas using your input, add a pinch of hints.  
The hints are randomly selected using the Invention Dice, invented by [Atomic Shrimp](https://atomicshrimp.com/post/2014/01/20/Invention-Dice). 

<br/>

<|layout|columns=1 1 1|gap=30px|class_name=card|
<app_type|
## **Create** 
<|{app_type}|selector|lov={APP_TYPE}|dropdown|>
|app_type>


<target_user|
## **for** 
<|{target_user}|selector|lov={TARGET_USER}|dropdown|>
|target_user>

<improvement|
## **to be more**   
<|{improvement}|selector|lov={IMPROVEMENT}|dropdown|> 
|improvement>

<|Generate_idea |button|on_action=generate_idea|label=Generate|>
|>

<br/>
---
<br/>

### **Here's an idea for you**{: .color-primary} 

<|{idea}|input|multiline|label=Ideas Ideas Ideas |class_name=fullwidth|>

<br/>
**Idea from:**

- [Invention Dice](https://atomicshrimp.com/post/2014/01/20/Invention-Dice)

- [WhatShouLdIBuildNext](https://github.com/Stormix/WhatShouldIBuildNext)
|>

"""

if __name__ == "__main__":
    if "OPENAI_API_KEY" in os.environ:
        api_key = os.environ["OPENAI_API_KEY"]
    elif len(sys.argv) > 1:
        api_key = sys.argv[1]
    else:
        raise ValueError(
            "Please provide the OpenAI API key as an environment variable OPENAI_API_KEY or as a command line argument."
        )

    client = openai.Client(api_key=api_key)
    Gui(page).run(title='Idea Generation')
