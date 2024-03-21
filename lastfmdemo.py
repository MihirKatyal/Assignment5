#Mihir Katyal
#mkatyal@uci.edu
#19099879

from LastFM import LastFM

def main():
    user = "MihirKatyal"
    api_key = "43effd57c3bbcfc8d88897c50b1cb0cf"

    last_fm = LastFM(user)
    last_fm.set_apikey(api_key)
    try:
        last_fm.load_data()  # Updated from load_top_tracks
        last_fm.print_top_tracks()
    except ConnectionError as e:
        print(f"Error: {str(e)}")
    except ValueError as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()
