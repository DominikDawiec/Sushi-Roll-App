import streamlit as st
from PIL import Image

# List of ingredients
ingredients = ['smoked salmon', 'avocado', 'cucumber', 'crab', 'cream cheese', 'eel sauce', 'wasabi', 'soy sauce']

# Sushi rolls and their ingredients
sushi_rolls = {
    'Seattle Roll': ['smoked salmon', 'avocado', 'cucumber'],
    'Philadelphia Roll': ['cream cheese', 'smoked salmon', 'avocado'],
    'Spicy Tuna Roll': ['tuna', 'spicy mayo', 'avocado'],
    'Dragon Roll': ['eel', 'avocado', 'cucumber'],
    'California Roll': ['crab', 'avocado', 'cucumber'],
}

# Function to get the list of rolls that can be made
def get_rolls(ingredients):
    available_rolls = []
    for roll, ingr in sushi_rolls.items():
        if set(ingr).issubset(ingredients):
            available_rolls.append(roll)
    return available_rolls

# Streamlit app
st.title("Sushi Roll Maker")

selected_ingredients = []

ingredient_list = []
for ingredient in ingredients:
    try:
        img = Image.open(f"{ingredient}.jpg")
        ingredient_list.append([img, st.checkbox(f"{ingredient}")])
    except:
        ingredient_list.append([None, st.checkbox(f"{ingredient}")])
        
if st.button("Load"):
    for ingredient in ingredient_list:
        if ingredient[1]:
            selected_ingredients.append(ingredients[ingredient_list.index(ingredient)])
    if len(selected_ingredients) > 0:
        st.write("You can make the following rolls:")
        rolls = get_rolls(selected_ingredients)
        if rolls:
            st.write("Here's what you can make:")
            for i in range(0, len(rolls), 2):
                if i + 1 < len(rolls):
                    st.write("{} \t\t {}".format(rolls[i], rolls[i + 1]))
                else:
                    st.write("{}".format(rolls[i]))
        else:
            st.write("You cannot make any sushi rolls.")
    else:
        st.write("Please select ingredients.")
