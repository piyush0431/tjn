import os
import re
import json

# Function to adjust time by a specified offset
def adjust_time(time, delay=0.1):
    minutes, seconds = map(float, time.split(':'))
    total_seconds = minutes * 60 + seconds + delay
    adjusted_minutes = int(total_seconds // 60)
    adjusted_seconds = total_seconds % 60
    return f"{adjusted_minutes:02d}:{adjusted_seconds:.2f}"

# Function to read lyrics from a file and generate the JSON structure
def generate_json_from_lyrics_file(input_file, output_file):
    # Check if the output file already exists
    if os.path.isfile(output_file):
        overwrite = input("The file already exists. Do you want to overwrite it? (y/n): ").lower()
        if overwrite != 'y':
            new_filename = input("Enter a new filename: ")
            if not new_filename:
                new_filename = "lyrics.json"
            elif not new_filename.endswith(".json"):
                new_filename += ".json"
            output_file = new_filename

    # Ask the user to enter song title and movie name
    song_title = input("Enter the song title: ")
    movie_name = input("Enter the movie name: ")

    lyrics_data = {"song_title": song_title, "movie_name": movie_name, "lyrics": []}
    previous_end_time = "0:00"
    sno = 1  # Initialize sno counter

    with open(input_file, "r") as file:
        lines = file.readlines()

    for i in range(len(lines)):
        line = lines[i].strip()
        if line:
            time_match = re.search(r'\[(\d+:\d+\.\d+)\]', line)
            if time_match:
                start_time = time_match.group(1)
                # Adjust the start_time 0.8 seconds earlier
                adjusted_start_time = adjust_time(start_time, -0.8)
                # Use the rest of the line as hinglish lyrics
                hinglish_lyrics = line[time_match.end():].strip()

                # Determine end time for the current lyric
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    next_time_match = re.search(r'\[(\d+:\d+\.\d+)\]', next_line)
                    if next_time_match:
                        next_start_time = next_time_match.group(1)
                        end_time = adjust_time(next_start_time, -0.5)
                    else:
                        # If next line doesn't have a valid time, use the start_time as end_time
                        end_time = start_time
                else:
                    # For the last line, use the start_time as end_time
                    end_time = start_time

                # Add new attributes to the lyrics object
                lyrics_data["lyrics"].append({
                    "sno": sno,
                    "start_time": adjusted_start_time,
                    "end_time": end_time,
                    "hinglish_lyrics": hinglish_lyrics,
                    "image_frame": "img_link_here",
                    "placement": "place",
                    "fg": "color"
                })

                sno += 1  # Increment sno counter

    with open(output_file, "w") as json_file:
        json.dump(lyrics_data, json_file, indent=4)

    print(f"JSON file '{output_file}' has been created.")

# Rest of the code remains unchanged

# Ask the user for the output filename
output_filename = input("Enter the output filename (default is 'lyrics.json'): ")
if not output_filename:
    output_filename = "lyrics.json"
elif not output_filename.endswith(".json"):
    output_filename += ".json"



generate_json_from_lyrics_file("tjn.txt", output_filename)