import regex
import typer
import os
import subprocess
from pathlib import Path

app = typer.Typer(help="Welcome to the Video Segment Concatenator. Use --help for a list of commands.")

@app.command(help="say hello")
def say_hello():
    print("Hello")

@app.command(help="Download using wget, concat using ffmpeg")
def scrape_and_concat(base_url: str, first_segment: int, extension: str, last_segment: int):    
    """
    Concatenate video segments from a given URL pattern.

    Args:
        base_url (str): Base URL for the segments.
        first_segment (int): First segment number.
        extension (str): File extension for the segments.
        last_segment (int): Last segment number.
    """

    # Create output directory
    output_dir_path = Path("/home/enigma/Downloads/video-concat-output2")
    output_dir_path.mkdir(parents=True, exist_ok=True)

    # Find the next available directory name
    i = 0
    vid_dir = output_dir_path / f"vid-dir-{i}"
    while vid_dir.exists():
        i += 1
        vid_dir = output_dir_path / f"vid-dir-{i}"
    vid_dir.mkdir(parents=True, exist_ok=True)

    # Write segment URLs to segment.txt
    segment_txt_path = vid_dir / "segment.txt"
    with segment_txt_path.open("w") as f:
        for i in range(first_segment, last_segment + 1):
            url = f"{base_url}{i}{extension}"
            f.write(f"{url}\n")
    print("Segment URLs have been written to segment.txt")

    # Download segments using wget
    try:
        subprocess.run(["wget",  "-i", str(segment_txt_path), "-P", str(vid_dir)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error downloading segments: {e}")
        return

     # Define a function to extract the numeric part from the file name
    def extract_segment_number(filename):
        match = regex.search(r'seg-(\d+)-v1-a1\.ts', filename)
        return int(match.group(1)) if match else -1

    # Write downloaded segment files to input.txt for ffmpeg
    input_txt_path = vid_dir / "input.txt"
    with input_txt_path.open("w") as f:
        # Get the sorted list of segment files
        segments = sorted(
            [file for file in vid_dir.iterdir() if file.suffix == ".ts"],
            key=lambda filename: extract_segment_number(filename.name)
        )
        # Write segment files to input.txt
        for segment in segments:
            f.write(f"file '{segment.name}'\n")
            print(f"Added to input.txt: {segment.name}")  # Debugging: Print added segments

    # Write downloaded segment files to input.txt for ffmpeg
    # input_txt_path = vid_dir / "input.txt"
    # with input_txt_path.open("w") as f:
    #     for i in range(first_segment, last_segment + 1):
    #         f.write(f"file 'seg-{i}-v1-a1.ts'\n")
    #         print(f"Added to input.txt: seg-{i}-v1-a1.ts")  # Debugging: Print added segments

    output_vid = vid_dir / "output.mp4"

    # Concatenate segments using ffmpeg
    try:
        subprocess.run(["ffmpeg", "-f", "concat", "-safe", "0", "-i", str(input_txt_path), "-c", "copy", str(output_vid)], check=True)
        print(f"Segments have been concatenated into {output_vid}")
    except subprocess.CalledProcessError as e:
        print(f"Error concatenating segments: {e}")


# @app.command(help="Download using wget, concat using ffmpeg")
# def scrape_and_concat_2(base_url: str, first_segment: int, extension: str, last_segment: int):    
#     """
#     Concatenate video segments from a given URL pattern.

#     Args:
#         base_url (str): Base URL for the segments.
#         first_segment (int): First segment number.
#         extension (str): File extension for the segments.
#         last_segment (int): Last segment number.
#     """

#      # Create output directory
#     output_dir_path = Path("/home/enigma/Downloads/video-concat-output")
#     output_dir_path.mkdir(parents=True, exist_ok=True)

#     # Find the next available directory name
#     i = 0
#     vid_dir = output_dir_path / f"vid-dir-{i}"
#     while True:
#         if not vid_dir.exists():
#             vid_dir.mkdir(parents=True, exist_ok=True)
#             break
#         i += 1

#     # Write segment URLs to segment.txt
#     segment_txt_path = vid_dir / "segment.txt"
#     with segment_txt_path.open("w") as f:
#         for i in range(first_segment, last_segment + 1):
#             url = f"{base_url}{i}{extension}"
#             f.write(f"{url}\n")
#     print("Concatenated segmentation has been written in segment.txt")

#     # Download segments using wget
#     print("Starting wget to download segments...")
#     result = subprocess.run(["wget", "-i", str(segment_txt_path), "-P", str(vid_dir)]
#                             # , capture_output=True, text=True, timeout=300
#                             )
#     print(f"wget stdout:\n{result.stdout}")
#     print(f"wget stderr:\n{result.stderr}")
#     if result.returncode != 0:
#         print("wget failed. Exiting.")
#         return
#     print("wget download completed.")

#     # Change directory to downloaded segments directory
#     os.chdir(vid_dir)

#     # Write initial input.txt
#     input_txt_path = vid_dir / "input.txt"
#     with input_txt_path.open("w") as f:
#         for segment in sorted(vid_dir.glob("*.ts")):
#             f.write(f"file '{segment.name}'\n")
#     print(f"Initial input.txt written with unsorted segments:\n{input_txt_path.read_text()}")

#     # Read and sort the lines in input.txt
#     with input_txt_path.open() as f:
#         def extract_int_from_line(line):
#             match = regex.search(r'file \'seg-(\d+)-v1-a1\.ts\'', line)
#             return int(match.group(1)) if match else -1

#         lines = f.read().split('\n')
#         lines = sorted(lines, key=extract_int_from_line)
#         sorted_txt = '\n'.join(lines)

#     # Write sorted lines into new_input.txt
#     new_input = vid_dir / "new_input.txt"
#     with new_input.open("w") as f:
#         f.write(sorted_txt)
#     print(f"Sorted new_input.txt written with sorted segments:\n{new_input.read_text()}")

#     output_vid = vid_dir / "output.mp4"

#     # Concatenate segments using ffmpeg
#     print("Starting ffmpeg to concatenate segments...")
#     result = subprocess.run(["ffmpeg", "-f", "concat", "-safe", "0", "-i", str(new_input), "-c", "copy", str(output_vid)], capture_output=True, text=True, timeout=300)
#     print(f"ffmpeg stdout:\n{result.stdout}")
#     print(f"ffmpeg stderr:\n{result.stderr}")
#     if result.returncode != 0:
#         print("ffmpeg failed. Exiting.")
#         return
#     print(f"Segments have been concatenated into {output_vid}")


# @app.command(help='Download and concatenate using FFmpeg directly')
# def scrape_concat(base_url: str, first_segment: int, extension: str, last_segment: int):
#     """
#     Auto download and concatenate using ffmpeg.

#     Args:
#         base_url (str): Base URL for the segments.
#         first_segment (int): First segment number.
#         extension (str): File extension for the segments.
#         last_segment (int): Last segment number.
#     """

#     # Create output directory
#     output_dir_path = Path("/home/enigma/Downloads/video-concat-output")
#     output_dir_path.mkdir(parents=True, exist_ok=True)

#     output_vid = output_dir_path / "output.mp4"

#     # Find the next available directory name
#     i = 0
#     vid_dir = output_dir_path / f"vid-dir-{i}"
#     while vid_dir.exists():
#         i += 1
#         vid_dir = output_dir_path / f"vid-dir-{i}"
#     vid_dir.mkdir(parents=True, exist_ok=True)

#     # Write segment URLs to segment.txt
#     segment_txt_path = vid_dir / "segment.txt"
#     with segment_txt_path.open("w") as f:
#         for i in range(first_segment, last_segment + 1):
#             url = f"{base_url}{i}{extension}"
#             f.write(f"file '{url}'\n")
#     print(f"Concatenated segmentation has been written in {segment_txt_path}")

#     # Run FFmpeg to concatenate the video segments directly from URLs
#     print("Starting FFmpeg to concatenate segments...")
#     result = subprocess.run([
#         "ffmpeg", "-f", "concat", "-safe", "0",
#         "-protocol_whitelist", "file,http,https,tcp,tls",
#         "-i", str(segment_txt_path),
#         "-c", "copy", str(output_vid)
#     ], capture_output=True, text=True)

#     # Debugging information
#     print(f"FFmpeg stdout:\n{result.stdout}")
#     print(f"FFmpeg stderr:\n{result.stderr}")

#     # Check if FFmpeg succeeded
#     if result.returncode != 0:
#         print("FFmpeg failed. Exiting.")
#         return

#     # Clean up the temporary file
#     segment_txt_path.unlink()
#     print(f"Segments have been concatenated into {output_vid}")

@app.command(help="Concatenate video segments from a given URL pattern and directly download it using ffmpeg as a new larger file")
def new_txt_concatenated_segment(base_url: str, first_segment: int, extension: str, last_segment: int):
    """
    Concatenate video segments from a given URL pattern.

    Args:
        base_url (str): Base URL for the segments.
        first_segment (int): First segment number.
        extension (str): File extension for the segments.
        last_segment (int): Last segment number.
    """
    output_dir_path = Path("/home/enigma/Downloads/video-concat-output")
    output_dir_path.mkdir(parents=True, exist_ok=True)


    # Find the next available directory name
    i = 0
    while True:
        vid_dir = output_dir_path / f"vid-dir-{i}"
        if not vid_dir.exists():
            vid_dir.mkdir()
            break
        i += 1

    # Create the segment.txt file with all segment URLs
    segment_txt_path = vid_dir / "segment.txt"
    with segment_txt_path.open("w") as f:
        for i in range(first_segment, last_segment + 1):
            url = f"{base_url}{i}{extension}"
            f.write(f"{url}\n")
    print(f"Concatenated segmentation has been written in {segment_txt_path}")

    # Download all segments using wget
    subprocess.run(["wget", "-i", str(segment_txt_path), "-P", str(vid_dir)], check=True)

    # Change to the directory with downloaded segments
    os.chdir(vid_dir)

    # Create input.txt for ffmpeg concatenation
    input_txt_path = vid_dir / "input.txt"
    with input_txt_path.open("w") as f:
        for segment in sorted(vid_dir.glob("*.ts")):
            f.write(f"file '{segment.name}'\n")
    
    
    output_vid = vid_dir / "output.mp4"


    # Run ffmpeg to concatenate segments into the final output video
    subprocess.run(["ffmpeg", "-f", "concat", "-safe", "0", "-i", str(input_txt_path), "-c", "copy", output_vid], check=True)

    print(f"Segments have been concatenated into {output_vid}")

@app.command(help='create segment.txt')
def txt_generator(base_url: str, first_segment: int, extension: str, last_segment: int):
    """
    Auto download and concatenate using ffmpeg.

    Args:
        base_url (str): Base URL for the segments.
        first_segment (int): First segment number.
        extension (str): File extension for the segments.
        last_segment (int): Last segment number.
    """

    # Create output directory
    output_dir_path = Path("/home/enigma/Downloads/video-concat-output")
    output_dir_path.mkdir(parents=True, exist_ok=True)

    # Find the next available directory name
    i = 0
    segment_file = output_dir_path / f"segment-{i}.txt"
    while segment_file.exists():
        i += 1
        segment_file = output_dir_path / f"segment-{i}.txt"

        # Write segment URLs to segment.txt
    with segment_file.open("w") as f:
        for i in range(first_segment, last_segment + 1):
            url = f"{base_url}{i}{extension}"
            f.write(f"file '{url}'\n")
    print(f"Concatenated segmentation has been written in {segment_file}")




if __name__ == '__main__':
    app()