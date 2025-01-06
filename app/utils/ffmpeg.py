import subprocess
import os
import pathlib
import json

# >>> ffmpeg -y -i input.file -c:v mpeg4 -b:v 868k -tag:v DIVX -s 640x480 -an -pass 1 -f rawvideo /dev/null
# >>> ffmpeg -i input.file -c:v mpeg4 -b:v 868k -tag:v DIVX -s 640x480 -c:a libmp3lame -b:a 192k -ac 2 -ar 44100 -pass 2 output.avi
# Get cwd of file even if ran outside
import os
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
TARGET = './ffmpeg_commands.json'
TARGET = os.path.join(script_dir, TARGET)
from time import sleep

class FFmpeg:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        
    def convert_mp4_to_divx(self, karaokeDevice):
        data = FFmpeg._read_json(TARGET)
        
        # Convert from POSIX to string path 
        input = self.input_file
        output = self.output_file


        if karaokeDevice not in data.keys():
            return KeyError(f"Karaoke device \"{karaokeDevice}\" does not exist.")

        commandSequence = data[karaokeDevice]
        print(commandSequence)

        for command in commandSequence:
            # <<INPUT>> and <<OUTPUT>> should be substituted
            
            command = command.replace("<<INPUT>>", str(input))
            command = command.replace("<<OUTPUT>>", str(output))

            print(command)
            subprocess.run(command, shell=True)

        # Rename the file to use '.divx' instead of '.avi'
        # subprocess.run(f'mv "{output}" "{output.with_suffix(".divx")}"', shell=True)
    
    def get_devices():
        """
        Get the list of devices that ffmpeg can use.
        """
        
        devices = FFmpeg._read_json(TARGET).keys()
        return devices
        
    def _read_json(filepath):
        with open(filepath) as content:
            data = json.load(content)
            return data
        

        # 
        # "ffmpeg -y -i \"<<INPUT>>\" -c:v mpeg4 -b:v 500k -tag:v DIVX -s 320x240 -an -pass 1 -f rawvideo /dev/null",   
        # "ffmpeg -i \"<<INPUT>>\" -c:v mpeg4 -b:v 500k -tag:v DIVX -s 320x240 -c:a wmav2 -b:a 128k -ac 2 -ar 44100 -af \"volume=0.5\" -pass 2 \"<<OUTPUT>>\""