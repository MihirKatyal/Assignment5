#Mihir Katyal
#mkatyal@uci.edu
#19099879

import ds_client
import Profile
from OpenWeather import OpenWeather
from LastFM import LastFM

OPENWEATHER_API_KEY = '6aff17baf0c23f582c0d2028522c3d03'
LASTFM_API_KEY = '43effd57c3bbcfc8d88897c50b1cb0cf'
OPENWEATHER_ZIP = '92617'
OPENWEATHER_COUNTRY = 'US'
LASTFM_USER = 'MihirKatyal'

# Initialize your API objects
weather_api = OpenWeather(OPENWEATHER_ZIP, OPENWEATHER_COUNTRY)
weather_api.set_apikey(OPENWEATHER_API_KEY)
lastfm_api = LastFM(LASTFM_USER)
lastfm_api.set_apikey(LASTFM_API_KEY)

def user_interface():
    profile = None  # meant to hold the user's profile information
    while True:
        print("Welcome! Please choose an option:")
        print("c - Create a new DSU file")
        print("l - Load an existing DSU file")
        print("p - Post a journal entry online")
        print("u - Update bio online")
        print("v - View current profile info")
        print("admin - Enter Admin mode for advanced commands")
        print("q - Quit")
        choice = input("Your choice (c/l/p/u/v/q): ").strip().lower()

        if choice == 'c':
            profile = create_profile()
        elif choice == 'l':
            profile = load_profile()
        elif choice == 'p' and profile:
            publish_post(profile)
        elif choice == 'u' and profile:
            update_bio(profile)
        elif choice == 'v' and profile:
            view_profile_info(profile)
        elif choice == 'admin':
            admin_mode()
        elif choice == 'q':
            break
        else:
            print("Invalid option or no profile loaded. Please choose 'c' to create or 'l' to load a profile.")

def create_profile():
    dsuserver = input("Enter DS server IP: ").strip()
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    new_profile = Profile.Profile(dsuserver, username, password)
    return new_profile

def load_profile():
    path = input("Enter the path to your DSU file: ").strip()
    loaded_profile = Profile.Profile()
    try:
        loaded_profile.load_profile(path)
        print("Profile loaded successfully.")
    except Profile.DsuFileError:
        print("Failed to load profile.")
    return loaded_profile

def publish_post(profile):
    print("Your journal entries:")
    for i, post in enumerate(profile.get_posts()):
        print(f"{i}: {post.entry}")
    post_index = int(input("Select the index of the post you want to publish: "))
    try:
        post = profile.get_posts()[post_index]
        # Process the post entry for @weather and @lastfm keywords
        # Process the entry through the weather API
        entry_with_weather = weather_api.transclude(post.entry)
        # Then process the entry through the LastFM API
        final_entry = lastfm_api.transclude(entry_with_weather)

        # Now send the final_entry instead of the original post.entry
        if ds_client.send(profile.dsuserver, 3021, profile.username, profile.password, message=final_entry):
            print("Post published successfully.")
        else:
            print("Failed to publish post.")
    except IndexError:
        print("Invalid post index.")


def update_bio(profile):
    new_bio = input("Enter your new bio: ").strip()
    if ds_client.send(profile.dsuserver, 3021, profile.username, profile.password, bio=new_bio):
        print("Bio updated successfully.")
        profile.bio = new_bio  # Update local profile bio
    else:
        print("Failed to update bio.")

def view_profile_info(profile):
    print("Current profile information:")
    print(f"Server: {profile.dsuserver}")
    print(f"Username: {profile.username}")
    print(f"Bio: {profile.bio}")
    print("Posts:")
    for post in profile.get_posts():
        print(f"- {post.entry}")

def admin_mode(profile):
    while True:
        print("\nWelcome to Admin mode! Please choose an option:")
        print("1 - View all local posts")
        print("2 - Change DS server IP")
        print("3 - View current DS server settings")
        print("4 - Test server connection")
        print("0 - Exit Admin mode")
        choice = input("Your choice: ").strip()

        if choice == '1':
            view_all_posts(profile)
        elif choice == '2':
            change_ds_server_ip(profile)
        elif choice == '3':
            view_current_server_settings(profile)
        elif choice == '4':
            test_server_connection(profile)
        elif choice == '0':
            break
        else:
            print("Invalid option. Please try again.")

def view_all_posts(profile):
    if profile and profile.get_posts():
        print("\nAll Local Posts:")
        for i, post in enumerate(profile.get_posts()):
            print(f"{i}: {post.entry} - Timestamp: {post.timestamp}")
    else:
        print("No posts available or no profile loaded.")

def change_ds_server_ip(profile):
    if profile:
        new_ip = input("Enter new DS server IP: ").strip()
        profile.dsuserver = new_ip
        print(f"DS server IP changed to {new_ip}.")
    else:
        print("No profile loaded.")

def view_current_server_settings(profile):
    if profile:
        print(f"\nCurrent DS server IP: {profile.dsuserver}")
    else:
        print("No profile loaded.")

def test_server_connection(profile):
    if profile:
        print("Testing connection to the server...")
        try:
            response = ds_client.send(profile.dsuserver, 3021, profile.username, profile.password, message="Test connection")
            if response:
                print("Connection to the server was successful.")
            else:
                print("Failed to connect to the server.")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("No profile loaded.")

if __name__ == "__main__":
    user_interface()
