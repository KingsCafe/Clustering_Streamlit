import streamlit as st 
while True:
    x = st.text_input('enter your color: [green,blue] ')
    try:
        
        if x == 'green':
            st.write('box1')
        elif x == 'blue':
            st.write('box2')
        break
    except:
        st.write('please enter a valid color')

