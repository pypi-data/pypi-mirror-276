import glob
import os
import subprocess
import re


def ffmpeg_encode(
    dir_path="",
    framerate=30,
    codec="libx264",
    extension="mp4",
    bitrate_kbps=5000,
    bitrate_kbps_min=5000,
    bitrate_kbps_max=5000,
    bufsize=5000,
    ffmpeg_path="ffmpeg"
):
    """Compresses a sequence of images using ffmpeg and saves individual frames as PNG files

    Args:
        dir_path (str): Path to the directory containing the images to be processed
        framerate (int): Frames per second for the target video
        codec (str): Codec to use for the encoded video file. Corresponds to the options available with ffmpeg. Default: libx264
        extension (str): Optional extension for the video file. This should correspond with the appropriate codec (e.g. ".mp4" for "libx264")
        bitrate_kbps (int): Target bitrate (kb/s) for the video file
        bitrate_kbps_min (int): Minimum bitrate (kb/s) for the video file
        bitrate_kbps_max (int): Maximum bitrate (kb/s) for the video file
        bufsize (int): Buffer size of the H.264/H.265 video file
        ffmpeg_path (str): Optional path to ffmpeg executable. Only neccessary if ffmpeg is not added to PATH

    Returns:
        None
    """

    if not os.path.exists(dir_path):
        raise OSError(f"Path 'dir_path' does not exist")
    
    # Check for ffmpeg if a custom path is not provided
    if ffmpeg_path == "ffmpeg":
        path_env = os.environ.get("PATH")
        if not "ffmpeg" in path_env:
            print("ffmpeg not found. Please download and install from 'https://ffmpeg.org/download.html'\nAlternatively, you may specify a custom path to the ffmpeg executable using the 'ffmpeg_path' argument")
            return
        
    else:
        ffmpeg_path = '"' + ffmpeg_path + '"'

    # Ensure provided path always has a trailing slash
    dir_path = os.path.join(dir_path, "")
    glob_path = dir_path + "*.rgb*"
    filepaths = glob.glob(glob_path)

    duration = 1.0/framerate
    bitrate = f"{bitrate_kbps}k"
    bitrate_min = f"{bitrate_kbps_min}k"
    bitrate_max = f"{bitrate_kbps_max}k"
    bitrate_bufsize = f"{bufsize}k"

    # Group filepaths by guid to make one video file per sequence
    pattern_guid = r"([0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12})(.rgb)"
    path_map = {}
    for fp in filepaths:
        fp = fp.replace("\\", "/")
        match = re.search(pattern_guid, fp)
        if match is not None:
            guid = match.group(1)
            if guid not in path_map:
                path_map[guid] = [fp]
            else:
                path_map[guid].append(fp)

    dir_out = os.path.join(dir_path, "compressed")
    if not os.path.exists(dir_out):
        os.makedirs(dir_out, exist_ok=True)

    for guid, sequence in path_map.items():
        with open("ffmpeg_input.txt", "wb") as outfile:
            for fp in sequence:
                outfile.write(f"file '{fp}'\n".encode())
                outfile.write(f"duration {duration}\n".encode())

        # Create filepath for video sequence and remove if exists as to not prompt user input
        extension_clean = extension.replace(".", "")
        sequence_path_out = os.path.join(dir_path, f"{guid}.sequence.{extension_clean}")
        if os.path.exists(sequence_path_out):
            os.remove(sequence_path_out)

        # Format image output filepath
        img_fn_out = f"{guid}.rgb_%04d.png"
        img_fp_out = os.path.join(dir_out, img_fn_out)

        print(f"Encoding video sequence '{guid}'...")
        command_encode = f"{ffmpeg_path} -r {framerate} -f concat -safe 0 -i ffmpeg_input.txt -c:v {codec} -b:v {bitrate} -minrate {bitrate_min} -maxrate {bitrate_max} -bufsize {bitrate_bufsize} {sequence_path_out}"
        pipe = subprocess.Popen(command_encode, shell=True, stdout=subprocess.PIPE).stdout
        output = pipe.read().decode()
        pipe.close()

        print("Extracting frames...")
        command_extract = f"{ffmpeg_path} -i {sequence_path_out} -start_number 0 {img_fp_out}"
        pipe = subprocess.Popen(command_extract, shell=True, stdout=subprocess.PIPE).stdout
        output = pipe.read().decode()
        pipe.close()
        
        # Clean up temp files
        if os.path.exists("ffmpeg_input.txt"):
            os.remove("ffmpeg_input.txt")
        if os.path.exists(sequence_path_out):
            os.remove(sequence_path_out)