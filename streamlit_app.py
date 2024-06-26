# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("""Choose the fruits you want in your custom Smoothie!
    """)


name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your smoothie will be", name_on_order)

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe=session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list=st.multiselect(
    'choose upto 5 ingrdeients:',
    my_dataframe,
    max_selections=5
)

if ingredients_list and name_on_order:
    ingredients_string = ', '.join(ingredients_list)
    
    ingredients_string = ''
    for x in ingredients_list:
        ingredients_string += x + ' '
        
    #st.write(ingredients_string)
    
    my_insert_stmt = f"""
    INSERT INTO smoothies.public.orders (ingredients, name_on_order)
    VALUES ('{ingredients_string}', '{name_on_order}')
    """
    #st.write(my_insert_stmt) #st.stop()
    
    time_to_insert=st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
