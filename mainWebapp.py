import streamlit as st
import pandas as pd
import re
import sqlite3 
import hashlib
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()
def check_hashes(password,hashed_text):
    if make_hashes(password)==hashed_text:
        return hashed_text
    return False
    
conn = sqlite3.connect('data1.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(FirstName TEXT,LastName TEXT,Mobile TEXT,Email TEXT,password TEXT,Cpassword TEXT,City TEXT)')
def add_userdata(FirstName,LastName,Mobile,Email,password,Cpassword,City):
    c.execute('INSERT INTO userstable(FirstName,LastName,Mobile,Email,password,Cpassword,City) VALUES (?,?,?,?,?,?,?)',(FirstName,LastName,Mobile,Email,password,Cpassword,City))
    conn.commit()
def login_user(Email,password):
    c.execute('SELECT * FROM userstable WHERE Email =? AND password = ?',(Email,password))
    data = c.fetchall()
    return data
def viw_all_users():
    c.execute("SELECT * FROM userstable")
    data=c.fetchall()
    return data
st.title("Welcome to App")
from PIL import Image
image = Image.open('lena.jpg')
menu=["Home","Login","SignUp"]
choice=st.sidebar.selectbox("Menu2",menu)
if choice=="Home":
    st.text("Welcome to Home")
    st.image(image)  
if choice=="Login":
    st.text("Welcome to login")
    Email = st.sidebar.text_input('Email')
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    password  = st.sidebar.text_input('Password',type="password")
    b=st.sidebar.checkbox("Login")
    if b:
        if re.fullmatch(regex,Email):
            create_usertable()
            hashed_psw=make_hashes(password)
            result = login_user(Email,check_hashes(password,hashed_psw))
            if result:
                st.success("Login Sucess")
               # st.warning("Not Valid Email") 
                st.success("Logged in as {}".format(Email))
                task=st.selectbox("Task",["Data","Profiles"])
                if task=="Data":
                    st.write("Display data here")
                elif task=="Profiles" and Email=="a@a.com":    
                
                   st.write('Users data')
                   user_result=viw_all_users()
                   db=pd.DataFrame(user_result,columns=["FirstName","LastName","Mobile","Email","password","Cpassword","City"])
                   st.dataframe(db)
                                                                                          
                else:
                  st.warning("Not Admin User")
            else:
                st.warning("Wrong Email/Password")
        else:
            st.warning("Not Valid Email") 
            
if choice=="SignUp":
    st.text("Welcome to SignUp")
    FirstName = st.text_input('First Name')
    LastName = st.text_input('Last Name')
    Email = st.text_input('Email')
    City  = st.text_input('City')
    Mobile  = st.text_input('Mobile Number')
    new_password  = st.text_input('Password',type="password")
    Cpassword  = st.text_input('Confirm Password',type="password")
    b1=st.button("SignUp")
    pattern=re.compile("(0|91)?[7-9][0-9]{9}")
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if b1:
        if (pattern.match(Mobile)):
            if re.fullmatch(regex,Email):
                if new_password==Cpassword:
                    create_usertable()
                    add_userdata(FirstName,LastName,Mobile,Email,make_hashes(new_password),make_hashes(Cpassword),City)
                    st.success("SignUp Sucess")
                else:
                    st.warning("Password Not Match")
            else:
                st.warning("Not Valid Email")
        else:
            st.warning("Not Valid Mobile")
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    