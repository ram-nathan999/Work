from transformers import BertTokenizer, BertModel
import torch
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load pre-trained BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# Function to encode text using BERT and obtain embeddings
def encode_text(text):
    # Tokenize input text
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
    # Get BERT embeddings
    with torch.no_grad():
        outputs = model(**inputs)
        embeddings = outputs.last_hidden_state[:, 0, :]  # Extract the [CLS] token embedding
    return embeddings.numpy()

# Function to detect speaker changes based on cosine similarity of BERT embeddings
def detect_speaker_changes(transcript):
    # Encode each text segment in the transcript using BERT
    embeddings = [encode_text(segment['text']) for segment in transcript]
    
    # Calculate cosine similarity between consecutive segments
    speaker_changes = []
    for i in range(1, len(embeddings)):
        # Compute cosine similarity between embeddings of consecutive segments
        similarity = cosine_similarity(embeddings[i-1], embeddings[i])[0][0]
        
        # Consider contextual information from previous and next segments
        if i > 1:
            prev_similarity = cosine_similarity(embeddings[i-2], embeddings[i-1])[0][0]
        else:
            prev_similarity = 0.0  # No previous segment
        if i < len(embeddings) - 1:
            next_similarity = cosine_similarity(embeddings[i], embeddings[i+1])[0][0]
        else:
            next_similarity = 0.0  # No next segment
        
        # If cosine similarity is below a threshold and is lower than both previous and next similarities,
        # consider it a speaker change
        if similarity < 0.9 and similarity < prev_similarity and similarity < next_similarity:
            speaker_changes.append(transcript[i]['timestamp'])
    return speaker_changes

# Sample transcript data
transcript = [ {"timestamp": "0:00", "text": "now the PPC has questioned the controversial social media influencer Andrew Tate at his home in the Romanian capital Bucharest"},
    {"timestamp": "0:04", "text": "Tate is under house arrest and being investigated by Romanian prosecutors for accusations including rape, human trafficking, and exploiting women which he denies"},
    {"timestamp": "0:08", "text": "the BBC challenged him on whether his views about women broadcast to his millions of online followers harmed young people as many teachers and police officers claim"},
    {"timestamp": "0:17", "text": "well the interview which had no set conditions was Tate's first since being released into house arrest from police custody last month"},
    {"timestamp": "0:33", "text": "Lucy Williamson reports now from Bucharest"},
    {"timestamp": "0:38", "text": "we are doing an interview with you"},
    {"timestamp": "0:42", "text": "because you're facing some very serious"},
    {"timestamp": "0:44", "text": "allegations correct rape human"},
    {"timestamp": "0:47", "text": "trafficking yep and also because there's"},
    {"timestamp": "0:50", "text": "a great deal of concern about the things"},
    {"timestamp": "0:52", "text": "you say and the impact that they have on"},
    {"timestamp": "0:57", "text": "young people on women I don't think the"},
    {"timestamp": "1:00", "text": "concerns about the things I say I think"},
    {"timestamp": "1:01", "text": "the concern is for the level of"},
    {"timestamp": "1:03", "text": "influence I have and the reach I have"},
    {"timestamp": "1:04", "text": "let's start with the allegations have"},
    {"timestamp": "1:06", "text": "you raped anybody absolutely not"},
    {"timestamp": "1:09", "text": "have you trafficked anybody absolutely"},
    {"timestamp": "1:11", "text": "not exploited any women for money not"},
    {"timestamp": "1:14", "text": "but you have admitted using emotional"},
    {"timestamp": "1:17", "text": "manipulation to get women to work in the"},
    {"timestamp": "1:19", "text": "webcam industry for you no we have an"},
    {"timestamp": "1:21", "text": "open criminal investigation I am"},
    {"timestamp": "1:23", "text": "absolutely not really sure I'll be found"},
    {"timestamp": "1:24", "text": "innocent I know the case better than you"},
    {"timestamp": "1:26", "text": "I know it intimately and you don't I"},
    {"timestamp": "1:28", "text": "have seen all the criminal files and the"},
    {"timestamp": "1:30", "text": "evidence against me and you haven't I"},
    {"timestamp": "1:32", "text": "know the truth of what happened and you"},
    {"timestamp": "1:33", "text": "don't and I'm telling you absolutely not"},
    {"timestamp": "1:35", "text": "really I've never hurt anybody that the"},
    {"timestamp": "1:37", "text": "case that's been put against me is"},
    {"timestamp": "1:38", "text": "completely not only fabricated and I'm"},
    {"timestamp": "1:40", "text": "never going to be found guilty of"},
    {"timestamp": "1:41", "text": "anything and it's very difficult for me"},
    {"timestamp": "1:42", "text": "to answer your in-depth questions"},
    {"timestamp": "1:43", "text": "because we're sitting here inside of the"},
    {"timestamp": "1:45", "text": "territory of Romania I'm beholden to the"},
    {"timestamp": "1:46", "text": "Romanian legal system and I'm not going"},
    {"timestamp": "1:48", "text": "to incriminate myself let me read you"},
    {"timestamp": "1:50", "text": "then what you have said about what you"},
    {"timestamp": "1:52", "text": "have done sure you have said my job was"},
    {"timestamp": "1:56", "text": "to meet a girl go on a few dates sleep"},
    {"timestamp": "1:58", "text": "with her get her to fall in love with me"},
    {"timestamp": "2:00", "text": "to the point where she'd do anything I"},
    {"timestamp": "2:02", "text": "say and then get her on webcam so we"},
    {"timestamp": "2:04", "text": "could become rich together I don't think"},
    {"timestamp": "2:06", "text": "that's what I personally said I think"},
    {"timestamp": "2:07", "text": "that's exactly what you said on your"},
    {"timestamp": "2:08", "text": "website that's no I've never said that"},
    {"timestamp": "2:10", "text": "that's something that you found on the"},
    {"timestamp": "2:12", "text": "internet doesn't mean I've said it and"},
    {"timestamp": "2:14", "text": "again once again if any female on the"},
    {"timestamp": "2:17", "text": "planet has a problem with me I strongly"},
    {"timestamp": "2:19", "text": "recommend her to go to the police and"},
    {"timestamp": "2:21", "text": "try and pursue me for criminal charges"},
    {"timestamp": "2:23", "text": "I'm actually such a nice person the BBC"},
    {"timestamp": "2:25", "text": "has spoken to somebody since your arrest"},
    {"timestamp": "2:27", "text": "who says exactly those things that with"},
    {"timestamp": "2:29", "text": "you it's all manipulation there's an"},
    {"timestamp": "2:31", "text": "ulterior oh it's Sophie the the fake name"},
    {"timestamp": "2:37", "text": "no face sorry about wanting to please him"},
    {"timestamp": "2:39", "text": "and wanting him to be happy that I was just"},
    {"timestamp": "2:42", "text": "kind of yeah okay do whatever you want"},
    {"timestamp": "2:44", "text": "and what does she accused me of a crime"},
    {"timestamp": "2:46", "text": "this imaginary Sophie she's making the"},
    {"timestamp": "2:48", "text": "point that there is actually accused me"},
    {"timestamp": "2:49", "text": "of a crime emotional or psychological"},
    {"timestamp": "2:51", "text": "manipulation and I've allowed you into"},
    {"timestamp": "2:53", "text": "my house I'm asking you a question"},
    {"timestamp": "2:55", "text": "correct but you're not the boss here"},
    {"timestamp": "2:56", "text": "because I've allowed you into my house"},
    {"timestamp": "2:57", "text": "I'm asking you the question correctly"},
    {"timestamp": "2:59", "text": "and I'm telling you you get to decide"},
    {"timestamp": "3:00", "text": "the answers no we're equal here"}
]

# Detect speaker changes using text-based BERT embeddings with contextual analysis
speaker_changes = detect_speaker_changes(transcript)
print("Speaker changes detected at timestamps:", speaker_changes)
