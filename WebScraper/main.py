import instaloader
import json
import csv
import os
import sys
import shutil


ig=instaloader.Instaloader()
usrname=input("Enter username:")
profile=instaloader.Profile.from_username(ig.context, usrname)

with open(r"./given_test.txt", 'w') as f:
   sys.stdout = f
   instaloader.Instaloader().download_profile(usrname, profile_pic_only=True)


   sys.stdout = sys.__stdout__

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
    "usernameDigitCount": digit_count,
    "usernameLength": len(profile.username),
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
print(data)


