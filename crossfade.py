import os
import subprocess

def extract_frames(movie_file, output_folder):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Use ffmpeg to extract frames from the movie file
    subprocess.run(['ffmpeg', '-i', movie_file, f'{output_folder}/frame-%04d.jpg'])
    
def crossfade_frames(output_folder):
    # Get the list of extracted frames
    frames = sorted(os.listdir(output_folder))
    
    # Check if we have enough frames for crossfading
    if len(frames) < 50:
        print("Error: There are not enough frames to perform the crossfade.")
        return
    
    # Use imagemagick to perform the crossfade effect
    subprocess.run(['convert'] + [f'{output_folder}/{frame}' for frame in frames[:25]] +
                   ['-morph', '50'] +
                   [f'{output_folder}/{frame}' for frame in frames[-25:]] +
                   [f'{output_folder}/output-%04d.jpg'])

# Path to the movie file you want to extract frames from
movie_file = './inputmovie.mp4'

# Path to the output folder where extracted frames will be saved
output_folder = './output_folder'

# Extract frames from the movie file
extract_frames(movie_file, output_folder)

# Crossfade the first and last 25 frames using imagemagick
crossfade_frames(output_folder)

