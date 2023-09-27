import pickle
import streamlit as st
import numpy as np
import time
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from scipy.stats import randint

pickle_in = open("classifier.pkl","rb")
model = pickle.load(pickle_in)

def make_a_dict(FollowerCount, FollowingCount, BioLength, Posts, HasProfilePic, IsPrivate, digitCount):
    
    data = {
        "FollowerCount": FollowerCount,
        "FollowingCount": FollowingCount,
        "BioLength": BioLength,
        "Posts":  Posts,
        "HasProfilePic": HasProfilePic,
        "IsPrivate": IsPrivate,
        "usernameDigitCount": digitCount
    }

    return data
       

def prediction(ans):
     prediction = model.predict(ans)
     return prediction
     

def main():
        st.title("Fake Instagram Detector")
    
        username = st.text_input("Enter the username")
        userlength = len(username)
        FollowerCount = st.number_input("Enter the Followers Count", min_value=1, value=None, step=1)
        FollowingCount = st.number_input("Enter the Following Count", min_value=1, value=None, step=1)
        BioLength = len(st.text_input("User Bio"))
        Posts = st.slider("Number of Posts", 0, 2000)
        HasProfilePic = st.number_input("Type 1 for profile pic else type 0", min_value=0, value=None, step=1)
        IsPrivate = st.number_input("Type 1 for private acc else type 0", min_value=0, value=None, step=1)
        digit_count = sum(1 for char in username if char.isdigit())

        if userlength > 0:
            usernameDigitCount = digit_count / userlength

        if st.button("Detect"):
                data = make_a_dict(FollowerCount, FollowingCount, BioLength, Posts, HasProfilePic, IsPrivate, usernameDigitCount)

                ans = []
                for keys in data:
                    ans.append(data[keys])

                ans = np.array(ans)
                ans = ans.reshape(1, -1)
                fake = prediction(ans)
                time.sleep(1)
                
                st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">', unsafe_allow_html=True)

                if fake == 0:     
            
                    htmlstr = """
                    <style>
                    .green-tick {
                        color: #2ecc71; 
                        font-size: 24px; 
                        margin-right: 8px; 
                        border-radius: 7xp;
                        padding-left: 12px;
                        padding-bottom: 13px;
                        padding-top:13px;
                    }
                    </style>
                    """
                    st.markdown(htmlstr, unsafe_allow_html=True)
                    st.markdown('<i class="green-tick fas fa-check-circle"></i> Bhai tera genuine hai', unsafe_allow_html=True)
                else:
                    htmlstr = """
                    <style>
                    .icon {
                        color: #ff0000; 
                        font-size: 24px; 
                        margin-right: 8px; 
                        border-radius: 7xp;
                        padding-left: 12px;
                        padding-bottom: 13px;
                        padding-top:13px;
                    }
                    </style>
                    """
                    st.markdown(htmlstr, unsafe_allow_html=True)
                    st.markdown('<i class="icon fas fa-times"></i> Tu to gyo', unsafe_allow_html=True)
        
        
if __name__=='__main__':
    main()
        
