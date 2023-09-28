import requests
from bs4 import BeautifulSoup
import os

BASE_URL = "http://gamemaster.stanford.edu/library/"

def get_game_directories(file_path):
    with open(file_path, "r") as f:
        return [line.strip() for line in f.readlines()]

def fetch_and_parse_html(url):
    response = requests.get(url)
    response.raise_for_status()  # Ensure we got a successful response
    return BeautifulSoup(response.content, 'html.parser')

def download_file(url, save_dir):
    response = requests.get(url)
    response.raise_for_status()
    
    # Extract the filename from the URL and save to the specified directory
    filename = os.path.join(save_dir, url.split("/")[-1])
    with open(filename, 'wb') as f:
        f.write(response.content)

def main():
    game_directories = get_game_directories("game-directory-list.txt")

    # Ensure the directories exist
    if not os.path.exists("downloaded_games"):
        os.mkdir("downloaded_games")

    # Loop through the game directories and download the files
    for game_directory in game_directories:
        print(f"Processing {game_directory}...")
        save_dir = os.path.join("downloaded_games", game_directory)
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        
        # Fetch and parse the game directory index page
        soup = fetch_and_parse_html(BASE_URL + game_directory)
        
        # Extract and download the file links
        for link in soup.find_all("a"):
            file_url: str= link.get("href")
            if file_url and not file_url.endswith("/") and file_url.find('?') == -1:  # Check if it's a file link and not a directory
                download_file(BASE_URL + game_directory + file_url, save_dir)

if __name__ == "__main__":
    main()
