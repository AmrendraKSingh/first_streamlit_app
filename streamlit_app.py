import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parent New Healthy Diner')

streamlit.header('Breakfast Menu') 

streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let put a picklist here so they can pick the frut they want to conclude
fruits_selected = streamlit.multiselect("Pick some fruits: ", list(my_fruit_list.index) , ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)

#Create a repeatable code block (called function)
def get_fruityvice_data(this_fruit_choice):
   fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" +this_fruit_choice)
   # Convert the Json verson of response and normalize using Pandas library
   fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
   return fruityvice_normalized
  

streamlit.header("Fruityvice Fruit Advice!")
#Add input field for fruit choice
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  
  if not fruit_choice:
    streamlit.error('Please select a fruit to get information.')
  else:
    #streamlit.write('The user entered ', fruit_choice)
    back_from_function = get_fruityvice_data(fruit_choice) 
    # Display in tabluar format using streamlit function 
    streamlit.dataframe(back_from_function)
   
except URLError as e:
  streamlit.error()
  

# To prevent running the code here
# streamlit.stop()


 # my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
# my_data_row = my_cur.fetchone()
# streamlit.text("Hello from Snowflake:")
# streamlit.text(my_data_row)
# streamlit.text(my_data_row);

streamlit.header("The fruit load list contains") ;
#snowflake related function 
def get_fruit_load_list():
   with my_cnx.cursor() as my_cur:
      my_cur.execute("select * from pc_rivery_db.public.fruit_load_list") 
      return my_cur.fetchall()

if streamlit.button('Get fruit load list'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   my_data_rows = get_fruit_load_list()
   streamlit.dataframe(my_data_rows)
   
#Allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit) : 
   with my_cnx.cursor() as my_cur:
      my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('"+new_fruit"'))
      return 'Thanks for adding '+ new_fruit
   
   
   
# To prevent running the code here
# streamlit.stop()

add_my_furit = streamlit.text_input('What fruit would you like to add?');
if streamlit.button('Add a fruit to a list'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   back_from_function = insert_row_snowflake(add_my_furit)
   streamlit.text(back_from_function)

# For testing purpose

