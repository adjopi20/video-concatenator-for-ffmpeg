import typer
import os
import subprocess 

app = typer.Typer(help="Welcome to the Video Segment Concatenator. Use --help for a list of commands.")

@app.command(help="Concatenate video segments from a given url pattern and directly download it using ffmpeg as new larger file")
def new_txt_concatenated_segment(base_url: str, first_segment: int, extension: str, last_segment: int, output_video: str):    
    """
    Concatenate video segments from a given URL pattern.

    Args:
        base_url (str): Base URL for the segments.
        first_segment (int): First segment number.
        extension (str): File extension for the segments.
        last_segment (int): Last segment number.
        output_video (str): Output video file name including format.
    """

    segment_dir="folder output"

    #first concatenation segment, lanjut subproses wget
    with open("segment.txt", "w") as f:
        for i in range(first_segment, last_segment, i+1):
            url = f"{base_url}{i}{extension}"
            f.write(f"{url}\n")
    print("concatenated segmentation has been written in segment.txt")

    subprocess.run(["wget", "-i", "segment.txt", "-P", segment_dir])

    #change dir to downloaded
    os.chdir(segment_dir)

    #second  concatenation the input, lanjut subproses dari ffmpeg
    with open("input.txt", "w") as f:
        for segment in sorted(os.listdir(".")):
            if segment.endswith(".ts"):
                f.write(f"file '{segment}'\n")

    subprocess.run(["ffmpeg", "-f", "concat", "-safe", "0", "-i", "input.txt", "-c", "copy", output_video])

    print("Segments have been concatenated into {output_video}")


if __name__ == '__main__':
    app()