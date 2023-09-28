import pickle
import streamlit as st
import instaloader
import json
import csv
#import os
import sys
import shutil
import numpy as np
import time
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from scipy.stats import randint


pickle_in = open("classifier.pkl","rb")
model = pickle.load(pickle_in)

classes = ["",0,1]

def scrap(user):
    usrname = user
    ig=instaloader.Instaloader()
    
    profile=instaloader.Profile.from_username(ig.context, usrname)

    with open(r"./given_test.txt", 'w') as f:
        sys.stdout = f
        instaloader.Instaloader().download_profile(usrname, profile_pic_only=True)

    sys.stdout = sys.stdout

    input_file_name = r"./given_test.txt"
    str_check= ""
    with open(input_file_name, "r") as input_file:
        line = input_file.readline()
        str_check = input_file.read()

    y = len(usrname) + 1
    jh = "2018-11-21_19-35-46_UTC_profile_pic.jpg " + "\n"
    check = str_check[y:]
    profile_pic = 0

    if check == jh:
        profile_pic = 0
    else:
        profile_pic = 1

    input_file.close()
    shutil.rmtree(usrname)

    x = 0
    if profile.is_private:
        x = 1
    else:
        x = 0

    digit_count = sum(1 for char in profile.username if char.isdigit())

    data = [{
        "FollowerCount": int(profile.followers),
        "FollowingCount": int(profile.followees),
        "BioLength": len(profile.biography),
        "Posts":  profile.mediacount,
        "HasProfilePic": profile_pic,
        "IsPrivate": x,
        "usernameDigitCount": digit_count/len(profile.username)
    }]

    file_path = r"./given_user_json.json"
    with open(file_path, 'w') as json_file:

        json.dump(data, json_file)

    with open(r"./given_user_json.json") as json_file:
        jsondata = json.load(json_file)

    data_file = open(r"./given_user_csv.csv", 'w', newline='')
    csv_writer = csv.writer(data_file)

    count = 0
    for data in jsondata:
        if count == 0:
            header = data.keys()
            csv_writer.writerow(header)
            count += 1
        csv_writer.writerow(data.values())
    
    return data
       

def prediction(ans):
     prediction = model.predict(ans)
     return prediction
     

def main():
        st.title("Fake Instagram Detector")
    
        user = st.text_input("Enter the username")
        button = st.button("Detect")
        if button:
            with st.spinner("Loading..."):
                data = scrap(user)

                ans = []
                for keys in data:
                    ans.append(data[keys])

                ans = np.array(ans)
                ans = ans.reshape(1, -1)
                fake = prediction(ans)
                # with st.spinner("Loading..."):
                time.sleep(0.5)
                
                st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">', unsafe_allow_html=True)

                if fake == 0:     
                    # st.success('bhai tera to genuine hai')
                    # st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">', unsafe_allow_html=True)
                    htmlstr = """
                    <style>
                    .green-tick {
                    color: #2ecc71; 
                    font-size: 30px; 
                    margin-right: 8px; 
                    border-radius: 40px;
                    border-color: #00ff00;
                    padding-left: 12px;
                    padding-bottom: 13px;
                    padding-top:13px;
                    }
                    #root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi4 > div:nth-child(1) > div > div:nth-child(7) > div > div > p{
                    color: #155724;
                    font-size: 30px;
                    border: 1px solid #2ecc71;
                    background-color: #d4edda;
                    padding: 15px;
                    margin: 10px 0;
                    border-radius: 40px;
                    }
                    </style>
                    """
                    st.markdown(htmlstr, unsafe_allow_html=True)
                    st.markdown('<i class="green-tick fas fa-check-circle"></i>Bhai tera genuine hai', unsafe_allow_html=True)
                else:
                    htmlstr = """
                    <style>
                    .icon {
                    color: #E53935; 
                    font-size: 30px; 
                    margin-right: 8px; 
                    border-radius: 40px;
                    padding-left: 12px;
                    padding-bottom: 13px;
                    padding-top:13px;
                    }
                    #root > div > div.withScreencast > div > div > div > section >  div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi4 > div.element-container:nth-child(7) > div:nth-child(1) > div:nth-child(1) > p{
                    color: #5e2523;
                    font-size: 30px;
                    border: 1px solid #D32F2F;
                    background-color: #ef9a9a;
                    padding: 15px;
                    margin: 10px 0;
                    border-radius: 40px;
                    }
                    </style>
                    """
                    st.markdown(htmlstr, unsafe_allow_html=True)
                    st.markdown('<i class="icon fas fa-times"></i> Tu to gyo', unsafe_allow_html=True)        
        
if __name__=='__main__':
    main()
    
   
