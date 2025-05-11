import streamlit as st
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound
import os
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """Summarize this YouTube video transcript into key points within 250 words: """

def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        # Attempt to fetch English transcript first
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    except NoTranscriptFound:
        try:
            # If English not found, fetch Hindi and translate to English
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['hi'])
            transcript = [{"text": entry["text"]} for entry in transcript]  # Simplify for translation
        except NoTranscriptFound:
            # If no transcripts exist, return None
            return None
    except Exception as e:
        raise e
    
    # Join transcript text
    transcript_text = " ".join([entry["text"] for entry in transcript])
    return transcript_text


def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")  # Updated model
    response = model.generate_content(
        [prompt + transcript_text],
        generation_config={
            "temperature": 0.7,
            "max_output_tokens": 1024,
        }
    )
    return response.text

st.title("AI YouTube Summarizer")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)

if st.button("Get Detailed Notes"):
    try:
        transcript_text = extract_transcript_details(youtube_link)
        if transcript_text:
            summary = generate_gemini_content(transcript_text, prompt)
            st.markdown("## Detailed Notes:")
            st.write(summary)
        else:
            st.error("No transcripts available for this video.")
    except Exception as e:
        st.error(f"Error: {str(e)}")