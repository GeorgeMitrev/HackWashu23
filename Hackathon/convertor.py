import os

from pydub import AudioSegment

 

# Specify the input folder containing .m4a files

input_folder = "Music Hackathon"

 

# Specify the output folder for .mp3 files

output_folder = "convertedMusic"

 

# Ensure the output folder exists

os.makedirs(output_folder, exist_ok=True)

 

# Loop through all files in the input folder

for filename in os.listdir(input_folder):

    if filename.endswith(".m4a"):

        # Construct full paths for input and output files

        input_file = os.path.join(input_folder, filename)

        output_file = os.path.join(output_folder, os.path.splitext(filename)[0] + ".mp3")

 

        # Load the .m4a file

        audio = AudioSegment.from_file(input_file, format="m4a")

 

        # Export the audio as .mp3
        # Export the audio as .mp3

        audio.export(output_file, format="mp3")

 

        print(f"Converted {filename} to {os.path.basename(output_file)}")

 

print("Conversion complete.")
