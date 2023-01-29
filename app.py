import streamlit as st

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

ingredient_images = {}
for ingredient in ingredients:
    ingredient_images[ingredient] = st.image(f"{ingredient}.jpg")

# Checkbox for each ingredient
for ingredient in ingredients:
    if st.checkbox(ingredient):
        selected_ingredients.append(ingredient)

if st.button("Load"):
    if len(selected_ingredients) > 0:
        st.write("You can make the following rolls:")
        rolls = get_rolls(selected_ingredients)
        if rolls:
            for roll in rolls:
                st.write(f"- {roll}")
        else:
            st.write("You cannot make any sushi rolls.")
    else:
        st.write("Please select ingredients.")