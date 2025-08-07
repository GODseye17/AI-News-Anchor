import streamlit as st
from news_video import VideoGenerator
from dotenv import load_dotenv
import os

load_dotenv()

# Load video API key from environment
video_api_key = os.getenv("BEARER_TOKEN")
video_generator = VideoGenerator(video_api_key)

# Page configuration
st.set_page_config(page_title="AI News Anchor", layout="wide")

# Title and styling
st.title("NEWSIEE")
st.markdown('<style>h1{color: orange; text-align: center;}</style>', unsafe_allow_html=True)
st.subheader('AI NEWS ANCHOR - CUSTOM SCRIPT READER')
st.markdown('<style>h3{color: pink; text-align: center;}</style>', unsafe_allow_html=True)

# Anchor image URL
image_url = "https://i.ibb.co/hYcxXTW/anchor.png"

# Create two columns for layout
col1, col2 = st.columns([1, 2])

with col1:
    st.info("Your AI News Anchor: Sophie")
    st.image(image_url, caption="Sophie - AI News Anchor", use_column_width=True)

with col2:
    st.markdown("### 📝 Enter Your News Script")
    
    # Text area for manual script input
    default_script = """Hello World, I'm Sophie, your AI News Anchor. 

Today's top story: [Enter your main news story here]

In other news: [Add additional news items here]

That's all for today. Stay tuned for more updates. Thank you for watching!"""
    
    news_script = st.text_area(
        "Write or paste your news script below:",
        value=default_script,
        height=300,
        help="Enter the complete script that Sophie will read. You can format it however you like!"
    )
    
    # Option to add intro and outro automatically
    st.markdown("### ⚙️ Script Options")
    add_intro = st.checkbox("Add standard intro", value=True)
    add_outro = st.checkbox("Add standard outro", value=True)
    
    # Voice selection (optional feature)
    voice_options = {
        "Sophie (Default)": "en-US-JennyNeural",
        "James": "en-US-GuyNeural",
        "Emma": "en-US-EmmaNeural",
        "Christopher": "en-US-ChristopherNeural"
    }
    selected_voice = st.selectbox("Select Anchor Voice:", list(voice_options.keys()))

# Generate button
if st.button("🎬 Generate News Video", type="primary", use_container_width=True):
    if news_script and news_script.strip():
        with st.spinner("🎥 Generating your AI news anchor video... This may take a few moments."):
            
            # Prepare the final script
            final_script = ""
            
            if add_intro:
                final_script = "Hello World, I'm Sophie, your AI News Anchor. Welcome to today's broadcast.\n\n"
            
            final_script += news_script
            
            if add_outro:
                final_script += "\n\nThat's all for today's news. Thank you for watching, and stay informed!"
            
            # Generate the video
            try:
                # Pass the selected voice to the video generator
                video_generator.voice_id = voice_options[selected_voice]
                video_url = video_generator.generate_video(final_script, image_url)
                
                if video_url:
                    st.success("✅ Video generated successfully!")
                    
                    # Display the video
                    st.markdown("### 📺 Your AI News Broadcast")
                    st.video(video_url)
                    
                    # Provide download link
                    st.markdown(f"[📥 Download Video]({video_url})")
                    
                    # Display the script that was used
                    with st.expander("📄 View Final Script"):
                        st.text(final_script)
                else:
                    st.error("❌ Failed to generate video. Please check your API key and try again.")
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
    else:
        st.warning("⚠️ Please enter a news script before generating the video.")

# Sidebar with instructions
with st.sidebar:
    st.markdown("## 📖 How to Use")
    st.markdown("""
    1. **Write Your Script**: Enter your news script in the text area
    2. **Customize Options**: Choose whether to add intro/outro
    3. **Select Voice**: Pick your preferred anchor voice
    4. **Generate**: Click the Generate button
    5. **Watch**: View your AI news anchor video!
    """)
    
    st.markdown("## 💡 Script Tips")
    st.markdown("""
    - Keep sentences clear and concise
    - Use proper punctuation for natural pauses
    - Add emphasis with exclamation marks
    - Break long segments into paragraphs
    """)
    
    st.markdown("## 🔧 Requirements")
    st.markdown("""
    - D-ID API Bearer Token
    - Set in `.env` file as `BEARER_TOKEN`
    """)