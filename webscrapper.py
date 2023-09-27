import instaloader
import json
import csv


ig=instaloader.Instaloader()

usrname=input("Enter username:")

profile=instaloader.Profile.from_username(ig.context, usrname)

x = 0
if profile.is_private:
    x = 1
else:
    x = 0

digit_count = sum(1 for char in profile.username if char.isdigit())

data = [{
    "FollowerCount": str(profile.followers),
    "FollowingCount": str(profile.followees),
    "BioLength": len(profile.biography),
    "Posts":  profile.mediacount,
    "HasProfilePic": "New York",
    "IsPrivate": x,
    "usernameDigitCount": digit_count,
    "usernameLength": len(profile.username),
}]

file_path = r"C:\Users\adars\Desktop\given_user.json"
with open(file_path, 'w') as json_file:

    json.dump(data, json_file)

with open(r"C:\Users\adars\Desktop\given_user.json") as json_file:
	jsondata = json.load(json_file)

data_file = open(r"C:\Users\adars\Desktop\real_csv.csv", 'w', newline='')
csv_writer = csv.writer(data_file)
print(profile.profile_pic_url)

count = 0
for data in jsondata:
	if count == 0:
		header = data.keys()
		csv_writer.writerow(header)
		count += 1
	csv_writer.writerow(data.values())

data_file.close()
