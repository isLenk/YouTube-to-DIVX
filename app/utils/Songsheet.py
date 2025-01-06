import pandas as pd

class Songsheet:
    def __init__(self, start_index, songs):
        self.songs = songs
        
        # Songs contain only song name
        # Data frame - NUMBER | Song Name
        self.data = pd.DataFrame(columns=["NUMBER", "Song Name"])
        self.start_index = start_index

        # Add songs to the data frame
        for i, song in enumerate(songs):
            self.data.loc[i] = [start_index + i, song]

    def generate_excel(self):
        self.data.to_excel("songsheet.xlsx", index=False)

    def __str__(self):
        print(self.data)