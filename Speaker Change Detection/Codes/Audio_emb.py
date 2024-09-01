from resemblyzer import preprocess_wav, VoiceEncoder
from demo_utils import *
from pathlib import Path
from pydub import AudioSegment
import csv


# DEMO 02: we'll show how this similarity measure can be used to perform speaker diarization
# (telling who is speaking when in a recording).


## Get reference audios
# Load the interview audio from disk
# Source for the interview: https://www.youtube.com/watch?v=X2zqiX6yL3I

def cut_audio(input_file, output_file, start_time, end_time):
    """
    Cut an audio file to the desired time range.
    
    Args:
        input_file (str): Path to the input audio file.
        output_file (str): Path to the output audio file.
        start_time (int): Start time in milliseconds.
        end_time (int): End time in milliseconds.
    """
    # Load the audio file
    audio = AudioSegment.from_mp3(input_file)
    
    # Cut the audio to the desired time range
    audio_cut = audio[start_time:end_time]
    
    # Export the cut audio to a new file
    audio_cut.export(output_file, format="mp3")

# Example usage
input_file = "input_audio.mp3"
output_file = "output_cut.mp3"
start_time = 0  # Start time in milliseconds (e.g., 5 seconds)
end_time = 180000   # End time in milliseconds (e.g., 15 seconds)

cut_audio(input_file, output_file, start_time, end_time)


wav_fpath = "output_cut.mp3"
wav = preprocess_wav(wav_fpath)

# Cut some segments from single speakers as reference audio
segments = [[0,10],[39,44],[59,104]]
speaker_names = ["reporter-male","interviewer-female","topG-male"]
speaker_wavs = [wav[int(s[0] * sampling_rate):int(s[1] * sampling_rate)] for s in segments]
  
    
## Compare speaker embeds to the continuous embedding of the interview
# Derive a continuous embedding of the interview. We put a rate of 16, meaning that an 
# embedding is generated every 0.0625 seconds. It is good to have a higher rate for speaker 
# diarization, but it is not so useful for when you only need a summary embedding of the 
# entire utterance. A rate of 2 would have been enough, but 16 is nice for the sake of the 
# demonstration. 
# We'll exceptionally force to run this on CPU, because it uses a lot of RAM and most GPUs 
# won't have enough. There's a speed drawback, but it remains reasonable.
encoder = VoiceEncoder("cuda")
print("Running the continuous embedding on cpu, this might take a while...")
_, cont_embeds, wav_splits = encoder.embed_utterance(wav, return_partials=True, rate=16)


# Get the continuous similarity for every speaker. It amounts to a dot product between the 
# embedding of the speaker and the continuous embedding of the interview
speaker_embeds = [encoder.embed_utterance(speaker_wav) for speaker_wav in speaker_wavs]
similarity_dict = {name: cont_embeds @ speaker_embed for name, speaker_embed in 
                   zip(speaker_names, speaker_embeds)}


## Run the interactive demo
#interactive_diarization(similarity_dict, wav, wav_splits)

# Create a list to store segment names and their similarity scores
segment_similarity_data = []

# Iterate through similarity_dict to gather segment names and similarity scores
for segment_name, similarity_scores in similarity_dict.items():
    # Create a dictionary to store segment name and similarity score
    segment_data = {'Segment': segment_name}
    
    # Add similarity scores to the dictionary
    for i, score in enumerate(similarity_scores):
        segment_data[f'Similarity_{i+1}'] = score.item()
    
    # Append the dictionary to the list
    segment_similarity_data.append(segment_data)

# Define the output CSV file path
output_csv_file = 'segment_similarity_scores.csv'

# Write the data to a CSV file
with open(output_csv_file, 'w', newline='') as csvfile:
    fieldnames = ['Segment'] + [f'Similarity_{i+1}' for i in range(len(similarity_scores))]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    # Write the header
    writer.writeheader()
    
    # Write the segment data
    for segment_data in segment_similarity_data:
        writer.writerow(segment_data)

print(f"Segment similarity scores saved to {output_csv_file}")
