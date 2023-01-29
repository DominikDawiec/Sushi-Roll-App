import streamlit as st
from PIL import Image

# List of ingredients
ingredients = ['smoked salmon', 'avocado', 'cucumber', 'crab', 'cream cheese', 'eel sauce', 'wasabi', 'soy sauce']

# Sushi rolls and their ingredients
sushi_rolls = {
    'Seattle Roll': ['smoked salmon', 'avocado', 'cucumber'],
    'Philadelphia Roll': ['cream cheese', 'smoked salmon', 'avocado'],
    'Spicy Tuna Roll': ['tuna', 'cream cheese', 'avocado'],
    'Dragon Roll': ['eel sauce', 'avocado', 'cucumber'],
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

# Divide the columns into three parts
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<center>", unsafe_allow_html=True)
    for ingredient in ingredients[:len(ingredients)//3]:
        try:
            img = Image.open(f"{ingredient}.png")
            if st.checkbox(f"{ingredient}", key=ingredient):
                selected_ingredients.append(ingredient)
            st.image(img, width=50, use_column_width=True)
        except:
            if st.checkbox(f"{ingredient}", key=ingredient):
                selected_ingredients.append(ingredient)
    st.markdown("</center>", unsafe_allow_html=True)

with col2:
    st.markdown("<center>", unsafe_allow_html=True)
    for ingredient in ingredients[len(ingredients)//3:2*len(ingredients)//3]:
        try:
            img = Image.open(f"{ingredient}.png")
            if st.checkbox(f"{ingredient}", key=ingredient):
                selected_ingredients.append(ingredient)
            st.image(img, width=50, use_column_width=True)
        except:
            if st.checkbox(f"{ingredient}", key=ingredient):
                selected_ingredients.append(ingredient)
    st.markdown("</center>", unsafe_allow_html=True)
    
with col3:
    st.markdown("<center>", unsafe_allow_html=True)
    for ingredient in ingredients[2*len(ingredients)//3:]:
        try:
            img = Image.open(f"{ingredient}.png")
            if st.checkbox(f"{ingredient}", key=ingredient):
                selected_ingredients.append(ingredient)
            st.image(img, width=50, use_column_width=True)
        except:
            if st.checkbox(f"{ingredient}", key=ingredient):
                selected_ingredients.append(ingredient)
    st.markdown("</center>", unsafe_allow_html=True)
    
if st.button("Load"):
    st.markdown("<center>", unsafe_allow_html=True)
    if len(selected_ingredients) > 0:
        st.write("You can make the following rolls:")
        rolls = get_rolls(selected_ingredients)
        if rolls:
            for roll in rolls:
                roll_img = Image.open(f"{roll}.png")
                st.image(roll_img, width=100)
                st.write("Ingredients: ", sushi_rolls[roll])
        else:
            st.write("You cannot make any sushi rolls.")
    else:
        st.write("Please select ingredients.")
