import streamlit as st
from PIL import Image
import pyparsing
from gsheetsdb import connect
import time


# Create a connection object.
conn = connect()

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=600, allow_output_mutation=True)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows

sheet_url = st.secrets["public_gsheets_url"]
df = run_query(f'SELECT * FROM "{sheet_url}"')


    
sushi_rolls = {}

for row in df:
    if row[0] not in sushi_rolls:
        sushi_rolls[row[0]] = [row[1]]
    else:
        sushi_rolls[row[0]].append(row[1])
    
sushi_rolls = {}
ingredients = set()
for row in df:
    if row[0] not in sushi_rolls:
        sushi_rolls[row[0]] = [ingredient.strip().strip('"').strip() for ingredient in row[1].split(',')]
    else:
        sushi_rolls[row[0]].extend([ingredient.strip().strip('"').strip() for ingredient in row[1].split(',')])
    ingredients.update([ingredient.strip().strip('"').strip() for ingredient in row[1].split(',')])
ingredients = list(ingredients)

# Function to get the list of rolls that can be made
def get_rolls(ingredients):
    available_rolls = []
    for roll, ingr in sushi_rolls.items():
        if set(ingr).issubset(ingredients):
            available_rolls.append(roll)
    return available_rolls

# Streamlit app
st.title("🍣 Sushi Roll Maker")

# Project description
st.markdown(
    """
    Welcome to the Sushi Roll Maker! This app is live connected to a Google Drive sheet with sushi roll recipes. 
    
    Link to the Google Drive sheet: [Google Drive Sheet with Recipes](https://docs.google.com/spreadsheets/d/1LIaTr9CqhJjCCv_V5sdJa490VBqKXhAE_HjL1o-rxcI/edit?usp=sharing).
    
    """
)

st.write("Please select ingredients that you have got in hand:")
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
            img = Image.open("nopic.png")
            st.image(img, width=50, use_column_width=True)
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
            img = Image.open("nopic.png")
            st.image(img, width=50, use_column_width=True)
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
            img = Image.open("nopic.png")
            st.image(img, width=50, use_column_width=True)
    st.markdown("</center>", unsafe_allow_html=True)

st.markdown("<center>", unsafe_allow_html=True)
if st.button("Make sushi 🔪"):
    st.markdown("<center>", unsafe_allow_html=True)

    if len(selected_ingredients) > 0:
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
        status_text.text("🍣 Preparing the rice with secret family recipe...")
        time.sleep(2)
        
        bar.progress(90)
        status_text.text("🍣 Perfectly rolling the sushi with years of practice...")
        time.sleep(2)
        
        if len(selected_ingredients) == len(ingredients):
            st.write("Wow! You have selected all possible ingredients, looks like you are really hungry or extremely interested in sushi making!")
        
        st.write("You can make the following rolls:")
        rolls = get_rolls(selected_ingredients)
        if rolls:
            for roll in rolls:
                try:
                    roll_img = Image.open(f"{roll}.png")
                    st.image(roll_img, width=100)
                except:
                    roll_img = Image.open("nopic.png")
                    st.image(roll_img, width=100)
                st.write(f"{roll}")
                st.write("Ingredients: ", ", ".join(sushi_rolls[roll]))

            bar.progress(100)
            status_text.text("🍣 Presenting the stunning sushi creations!")
        else:
            st.write("You cannot make any sushi rolls, please select more ingredients")
            roll_img = Image.open("nopic.png")
            st.image(roll_img, width=100)
    else:
        st.write("Please select ingredients.")
