import random

import streamlit as st
from streamlit import session_state
def set_background(url):
    st.markdown(f'''
                <style>
                .stApp {{
                    background-image:url("{url}");
                    background-attachment:fixed;
                    background-position:center;
                    background-size : cover;
                        }}
                </style>
                ''',
                unsafe_allow_html=True)


if "game_init" not in session_state:
    session_state.gold = 50
    session_state.game_init = True
    session_state.location = "start_screen"
    session_state.day = 0
    session_state.log = []
    session_state.total_customers = 0
    session_state.parts = {
        " car body" : {"name":"the body","cost": 80 ,"time" : "5h","price":100,"qty":0,"set_price":100},
        "the gearbox":{"name":"the gearbox","cost": 40 ,"time" : "7h","price":55,"qty":1,"set_price":55},
        "the engine":{"name":"the engine","cost": 120,"time":"15h","price":170,"qty":0,"set_price":170},
        "dashboard":{"name":"dashboard","cost": 60 ,"time" : "5h","price":70,"qty":3,"set_price":70},
        "maintainence":{"name":"maintainence","cost": 20 ,"time" : "2h","price":30,"qty":4,"set_price":30},
        "custom parts": {"name": "custom parts", "cost": 100, "time": "2h", "price": 140, "qty": 0, "set_price": 140}

    }
    st.rerun()

if session_state.game_init :
    c1,c2 = st.columns(2)
    with c1:
        st.write(f" <span style='color:#FFD700;'>gold : {session_state.gold}</span>",unsafe_allow_html=True)
    with c2:
        st.write(f"<span style='color: #27E0F5;'> 📅day:{session_state.day}</span>",unsafe_allow_html=True)
    st.divider()


if session_state.game_init :
    set_background("https://images.unsplash.com/photo-1583126162406-643011b3f69f?q=80&w=1103&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D")
    colm1,colm2=st.columns([4,1])
    with colm1:
        if session_state.location == "start_screen":
            if st.button("go to the garage to start the day"):
                session_state.location = "garage"
                st.rerun()
            if st.button("game stats"):
                st.write(f"the day : {session_state.day}")
                st.write(f"money : {session_state.gold}")
                st.write(f"total customers : {session_state.total_customers}")


    with colm2:
        if session_state.location == "start_screen":
            if st.button("shop"):
                session_state.location = "parts shop"
                st.rerun()
    if st.button("credits"):
        st.write("hi am the maker of this game , i wanted to make a game where i could buy , sell and keep my own prices ,so this is it , with streamlit i used st.button,st.number_input,st.write,ect. you can look up the functions on streamlit documentation , my goal is the cmf buds and i already put 18 hours in the total ,so if you came from stardance chalange plz rate this game as however you think it is , by the way tx for playing this")

def customer_car_generator():
    customers = random.randint(2,6)
    session_state.total_customers += customers
    for _ in range(customers):
        in_stock = [name for name ,details in session_state.parts.items() if details["qty"] > 0]
        if not in_stock :
            session_state.log.append("many customers came to you shop but you did not have any parts")
            continue
        parts_choice = random.choice(in_stock)
        chosen_item = session_state.parts[parts_choice]
        max_buget = chosen_item["price"]+ random.randint(1,15)
        if chosen_item["set_price"]<= max_buget:
            chosen_item["qty"]-=1
            session_state.gold += chosen_item["set_price"] # Fixed to add set_price instead of base price
            session_state.log.append(f"a customer bought {chosen_item['name']} for {chosen_item['set_price']}")
        else:
            session_state.log.append(f"customers thought the {chosen_item['name']} price is too high")





if session_state.location == "parts shop":
    for name,item in session_state.parts.items():
        if st.button(f"buy {name} for {item['cost']} qty left {item['qty']}" ,key = f"buy_{name}"):
            if session_state.gold >= item["cost"]:
                item["qty"]+=1
                session_state.gold -= item["cost"]
                session_state.log.append(f"you spent {item['cost']} gold on {name} parts")
                st.rerun()
            else:
                st.warning("you do not have enough gold")
    if st.button("enter the garage"):
        session_state.location = "garage"
        st.rerun()
    if st.button("go to menu"):
        session_state.location = "start_screen"
        st.rerun()
if session_state.location == "garage":
    col_inv,col_set_price = st.columns(2)
    with col_inv:
        for name,item in session_state.parts.items():
            st.button(f" part: {item['name']} , price: {item['cost']} , qty left: {item['qty']}" ,key = f"garage_view_{name}", disabled=True)
    with col_set_price:
        for name,item in session_state.parts.items():
            item["set_price"] = st.number_input(f"set price for {name}",min_value=item["price"], value=item["set_price"], key=f"price_input_{name}")
    if st.button("start day"):
        customer_car_generator()
        session_state.day +=1
        st.rerun()
    if st.button("enter the parts shop"):
        session_state.location = "parts shop"
        st.rerun()
    if st.button("go to menu"):
        session_state.location = "start_screen"
        st.rerun()


st.divider()
st.subheader("🏎️📝the garage log")
for log in reversed(session_state.log[-6:]):
    st.write(f"...{log}")