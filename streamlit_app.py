# Import python packages
import streamlit as st
import os
import requests  

#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

#DEBUG: show the snowflakes secrects file, has this been picked up ok ?:
st.write(st.secrets)


#from snowflake.snowpark.context import get_active_session
#Connection required for streamlit app
cnx = st.connection("snowflake")
session = cnx.session()

# Write directly to the app
st.title(':cup_with_straw: Customize Your Smoothie! :cup_with_straw:')
st.write(
  """Choose the fruits you want in your custom smoothie
  
  **And if you're new to Streamlit,** check
  out our easy-to-follow guides at
  [docs.streamlit.io](https://docs.streamlit.io).
  """
)

name_on_order = st.text_input("Enter Name youd like on your Smoothie")
st.write("The name on your Smoothie will be ", name_on_order)


my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col("SEARCH_ON"))
st.dataframe(my_dataframe, use_container_width=True)
st.stop()


ingredients_list = st.multiselect(
    "Choose up to 5 ingredients: ",
    my_dataframe,
    max_selections=5
)

if ingredients_list:

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen +' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen) 
        st.write(smoothiefroot_response.json())
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width= True)
        

    #st.write(ingredients_string)

    #my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
    #                values ('""" + ingredients_string + """')"""

    #st.write(my_insert_stmt)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order) values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    st.write(my_insert_stmt)
    #st.stop()
    
    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
