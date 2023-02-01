import streamlit as st
from PIL import Image
import pyparsing
from gsheetsdb import connect
import time

# Create a connection object.
conn = connect()

# Perform SQL query on the Google Sheet with caching
@st.cache(ttl=600, allow_output_mutation=True)
def run_query(query):
    rows = conn.execute(query, headers=1)
    return rows.fetchall()

# Get data from Google Sheet
sheet_url = st.secrets["public_gsheets_url"]
df = run_query(f'SELECT * FROM "{sheet_url}"')

# Create dictionary of sushi rolls and their ingredients
sushi_rolls = {}
ingredients = set()
for row in df:
    roll_name = row[0]
    roll_ingredients = [ingredient.strip().strip('"').strip() for ingredient in row[1].split(',')]
    if roll_name not in sushi_rolls:
        sushi_rolls[roll_name] = roll_ingredients
    else:
        sushi_rolls[roll_name].extend(roll_ingredients)
    ingredients.update(roll_ingredients)
ingredients = list(ingredients)

# Function to get list of rolls that can be made with selected ingredients
def get_rolls(ingredients):
    available_rolls = []
    for roll, roll_ingredients in sushi_rolls.items():
        if set(roll_ingredients).issubset(ingredients):
            available_rolls.append(roll)
    return available_rolls

# Streamlit app
st.title("🍣 Sushi Roll Maker")
st.markdown("Welcome to the Sushi Roll Maker! This app is connected to a Google Drive sheet with sushi roll recipes.")
st.markdown("[Sheet with Recipes](https://docs.google.com/spreadsheets/d/1LIaTr9CqhJjCCv_V5sdJa490VBqKXhAE_HjL1o-rxcI/edit?usp=sharing). Please feel free to contribute, recipes are automatically updated every 10 minutes")
st.write("Please select ingredients you have:")
selected_ingredients = []   

# Divide ingredients into three columns for display
col1, col2, col3 = st.columns(3)

# Display ingredients and add to selected_ingredients when checked
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
            img = Image.open("nopic.png")
            st.image(img, width=50, use_column_width=True)
    st.markdown("</center>", unsafe_allow_html=True)

with col2:
    st.markdown("<center>", unsafe_allow_html=True)
    for ingredient in ingredients[len(ingredients)//3:2*len(ingredients)//3]:
        try:
            img = Image.open(f"{ingredient}.png")
            selected = ingredient in selected_ingredients
            if st.checkbox(f"{ingredient}", key=ingredient, value=selected):
                if selected:
                    selected_ingredients.remove(ingredient)
                else:
                    selected_ingredients.append(ingredient)
            st.image(img, width=50, use_column_width=True)
        except:
            selected = ingredient in selected_ingredients
            if st.checkbox(f"{ingredient}", key=ingredient, value=selected):
                if selected:
                    selected_ingredients.remove(ingredient)
                else:
                    selected_ingredients.append(ingredient)
            img = Image.open("nopic.png")
            st.image(img, width=50, use_column_width=True)
    st.markdown("</center>", unsafe_allow_html=True)

with col3:
    st.markdown("<center>", unsafe_allow_html=True)
    for ingredient in ingredients[2*len(ingredients)//3:]:
        try:
            img = Image.open(f"{ingredient}.png")
            selected = ingredient in selected_ingredients
            if st.checkbox(f"{ingredient}", key=ingredient, value=selected):
                if selected:
                    selected_ingredients.remove(ingredient)
                else:
                    selected_ingredients.append(ingredient)
            st.image(img, width=50, use_column_width=True)
        except:
            selected = ingredient in selected_ingredients
            if st.checkbox(f"{ingredient}", key=ingredient, value=selected):
                if selected:
                    selected_ingredients.remove(ingredient)
                else:
                    selected_ingredients.append(ingredient)
            img = Image.open("nopic.png")
            st.image(img, width=50, use_column_width=True)
    st.markdown("</center>", unsafe_allow_html=True)

if st.button("Make sushi 🔪"):
    st.markdown("<center>", unsafe_allow_html=True)

    if selected_ingredients:
        bar = st.progress(0)
        status_text = st.empty()

        bar.progress(10)
        status_text.text("🍣 Deciding what type of sushi to make...")
        time.sleep(2)

        bar.progress(30)
        status_text.text("🍣 Looking for inspiration from Jiro Ono sensei...")
        time.sleep(2)

        bar.progress(50)
        status_text.text("🍣 Finding the freshest fish at the Tsukiji fish market...")
        time.sleep(2)

        bar.progress(70)
        status_text.text("🍣 Preparing the rice with a secret family recipe...")
        time.sleep(2)

        bar.progress(90)
        status_text.text("🍣 Perfectly rolling the sushi with years of practice...")
        time.sleep(2)

        if len(selected_ingredients) == len(ingredients):
            st.write("Wow! You have selected all possible ingredients. Looks like you're either really hungry or extremely interested in sushi making!")

        st.write("You can make the following rolls:")
        rolls = get_rolls(selected_ingredients)

        if rolls:
            for roll in rolls:
                try:
                    roll_img = Image.open(f"{roll}.png")
                    st.image(roll_img, width=100)
                except FileNotFoundError:
                    roll_img = Image.open("nopic.png")
                    st.image(roll_img, width=100)

                st.write(roll)
                st.write(f"Ingredients: {', '.join(sushi_rolls[roll])}")

            bar.progress(100)
            status_text.text("🍣 Presenting the stunning sushi creations!")
        else:
            st.write("You cannot make any sushi rolls. Please select more ingredients.")
            roll_img = Image.open("nopic.png")
            st.image(roll_img, width=100)
    else:
        st.write("Please select ingredients.")

