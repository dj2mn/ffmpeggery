import os
import subprocess
import fnmatch
import glob

def extract_frames(movie_file, frame_rate, temp_folder):
    # Create the temp folder if it doesn't exist
    os.makedirs(temp_folder, exist_ok=True)
    
    # Use ffmpeg to extract frames from the movie file
#    subprocess.run(['ffmpeg', '-r', f'{frame_rate}', '-i', movie_file, '-vf', 'scale=1280:trunc(ow/a/2)*2', f'{temp_folder}/{file_pattern}'])
    subprocess.run(['ffmpeg', '-i', movie_file, '-vf', 'scale=1280:trunc(ow/a/2)*2', f'{temp_folder}/{file_pattern}'])

def do_crossfade(fade_time):
    num_fade_frames = fade_time * frame_rate
    start_sequence = []
    end_sequence = []

    # Get the total number of frames in the sequence
    frame_count = len(fnmatch.filter(os.listdir(temp_folder), '*.bmp'))

    # Check if we have enough frames for crossfading
    if frame_count < num_fade_frames:
        print("Error: There are not enough frames to perform the crossfade.")
        return

    # Load the first frames and rename for removal later
    for i in range(1, num_fade_frames + 1):
        filename = file_pattern % i
        start_sequence.append(filename)
        os.rename(temp_folder + '/' + filename, temp_folder + '/xfade-start-' + filename)

    # Load the last frames and rename for removal later
    for i in range(frame_count - num_fade_frames + 1, frame_count + 1 ):
        filename = file_pattern % i
        end_sequence.append(filename)
        os.rename(temp_folder + '/' + filename, temp_folder + '/xfade-end-' + filename)

    # Now we're ready to make the crossfade happen
    for i in range(1, num_fade_frames):
        # Compute the crossfade percentage
        fade_percentage = i / (num_fade_frames - 1) * 100
        
        # Create a blended image of the start and end frame sequences
        # Using the original filenames of end_sequence so blended version replaces originals
        cmd = f"magick composite -blend {fade_percentage}% {temp_folder}/xfade-start-{start_sequence[i]} {temp_folder}/xfade-end-{end_sequence[i]} {temp_folder}/{end_sequence[i]}"
        subprocess.run(cmd, shell=True)

    fileList = glob.glob(f"{temp_folder}/xfade-*.bmp")
    for filePath in fileList:
        try:
            os.remove(filePath)
        except:
            print("Error while deleting file : ", filePath)

    # Re-index the filenames to match the new shorter frame count
    fileList = sorted(glob.glob(f"{temp_folder}/frame-*.bmp"))
    frame_count = len(fileList)
    for i in range(1, frame_count):
        new_name = file_pattern % i
        os.rename( fileList[i], temp_folder + '/' + new_name )


def create_movie(input_folder, frame_rate, output_name):
    # Following the advice of http://superuser.com/questions/1212023/ddg#1212038 here
    cmd = f"/usr/local/bin/ffmpeg -y -i {input_folder}/{file_pattern} -c:v libx264 -crf 10 -tune stillimage -preset veryslow {output_name}"
    subprocess.run(cmd, shell=True)


if __name__ == "__main__":

    # set some info about the movie file you want to extract frames from etc
    input_movie_file = '/Volumes/WD4TB/4blm/2019-01-05 20.39.50.mov'
    frame_rate = 30
    output_movie_file = '/Users/stewart/Movies/crystals-output.mp4'
    file_pattern = 'frame-%04d.bmp'
    temp_folder = '/Users/stewart/.frames_temp'

    # Extract frames from the movie file
    extract_frames(input_movie_file, frame_rate, temp_folder)

    # Crossfade the first and last n seconds of frames using imagemagick
    do_crossfade(5)

    # stitch the frames back together
    create_movie(temp_folder, frame_rate, output_movie_file)

