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
st.title("LIVE-7 AI News Anchor")
st.markdown('<style>h1{color: orange; text-align: center;}</style>', unsafe_allow_html=True)
st.subheader('AI NEWS ANCHOR - MULTILINGUAL SCRIPT READER')
st.markdown('<style>h3{color: pink; text-align: center;}</style>', unsafe_allow_html=True)

# Avatar options - Multiple Fatha URLs as fallback
avatar_options = {
    "Custom News Anchor": {
        "type": "url",
        "value": "https://i.ibb.co/hYcxXTW/anchor.png",
        "preview": "https://i.ibb.co/hYcxXTW/anchor.png",
        "fallback": None
    },
    "Fatha (Professional)": {
        "type": "url",
        "value": "https://d-id-public-bucket.s3.amazonaws.com/alice.jpg",  # Using a known working D-ID image as fallback
        "preview": "https://create-images-results.d-id.com/DefaultPresenters/Fatha_f/image.jpeg",
        "fallback": [
            "https://create-images-results.d-id.com/DefaultPresenters/Fatha_f/image.jpeg",
            "https://d-id-public-bucket.s3.amazonaws.com/alice.jpg",  # D-ID's test image
            "https://i.ibb.co/hYcxXTW/anchor.png"  # Ultimate fallback to custom anchor
        ]
    }
}

# Create two columns for layout
col1, col2 = st.columns([1, 2])

with col1:
    st.info("Your AI News Anchor")
    
    # Avatar selection
    st.markdown("### 👤 Select Avatar")
    selected_avatar_name = st.selectbox(
        "Choose your news anchor:",
        list(avatar_options.keys()),
        help="Select between custom anchor or Fatha presenter"
    )
    
    avatar_config = avatar_options[selected_avatar_name]
    
    # Display selected avatar preview (use preview image for display)
    st.image(avatar_config["preview"], caption=f"Selected: {selected_avatar_name}", use_container_width=True)
    
    # Show API status
    if st.button("🔧 Test D-ID Connection", help="Check if D-ID API is working"):
        with st.spinner("Testing API..."):
            import requests
            test_url = "https://api.d-id.com/credits"
            auth = f"Basic {video_api_key}" if ':' in video_api_key else f"Bearer {video_api_key}"
            try:
                resp = requests.get(test_url, headers={"authorization": auth})
                if resp.status_code == 200:
                    st.success("✅ API Connected!")
                    credits = resp.json()
                    st.info(f"Credits remaining: {credits.get('remaining', 'N/A')}")
                else:
                    st.error(f"❌ API Error: {resp.status_code}")
            except Exception as e:
                st.error(f"❌ Connection failed: {str(e)}")
    
    # Voice selection with better categorization
    st.markdown("### 🎤 Select Voice & Language")
    
    # Language selection first
    language_options = {
        "English": {
            "Sophie (Default)": "en-US-JennyNeural",
            "James": "en-US-GuyNeural", 
            "Emma": "en-US-EmmaNeural",
            "Christopher": "en-US-ChristopherNeural",
            "Neerja (India)": "en-IN-NeerjaNeural"
        },
        "हिंदी (Hindi)": {
            "Swara (स्वरा)": "hi-IN-SwaraNeural",
            "Madhur (मधुर)": "hi-IN-MadhurNeural", 
            "Aarti (आरती)": "hi-IN-AartiNeural",
            "Arjun (अर्जुन)": "hi-IN-ArjunNeural"
        }
    }
    
    selected_language = st.selectbox("Choose Language:", list(language_options.keys()))
    selected_voice_name = st.selectbox("Choose Voice:", list(language_options[selected_language].keys()))
    selected_voice_id = language_options[selected_language][selected_voice_name]
    
    # Voice styles for supported voices
    style_options = {"Default": "default"}
    if selected_voice_id in ["hi-IN-SwaraNeural", "en-IN-NeerjaNeural"]:
        style_options.update({
            "Cheerful (खुशी)": "cheerful",
            "Newscast (समाचार)": "newscast", 
            "Empathetic (सहानुभूति)": "empathetic"
        })
    
    selected_style = st.selectbox("Voice Style:", list(style_options.keys()))
    
    # Display current selection
    st.markdown("---")
    st.markdown("**Current Selection:**")
    st.write(f"👤 Avatar: {selected_avatar_name}")
    st.write(f"🌍 Language: {selected_language}")
    st.write(f"🎭 Voice: {selected_voice_name}")
    if style_options[selected_style] != "default":
        st.write(f"🎨 Style: {selected_style}")

with col2:
    st.markdown("### 📝 Enter Your News Script")
    
    # Language-specific default scripts
    if selected_language == "हिंदी (Hindi)":
        default_script = """नमस्कार दोस्तों, मैं आपकी AI समाचारवाचिका हूं।

आज की मुख्य खबर: [यहाँ अपनी मुख्य समाचार कहानी दर्ज करें]

अन्य समाचारों में: [यहाँ अतिरिक्त समाचार आइटम जोड़ें]

आज के समाचार समाप्त। अधिक अपडेट के लिए जुड़े रहें। देखने के लिए धन्यवाद!"""
    else:
        default_script = """Hello World, I'm your AI News Anchor. 

Today's top story: [Enter your main news story here]

In other news: [Add additional news items here]

That's all for today. Stay tuned for more updates. Thank you for watching!"""
    
    news_script = st.text_area(
        "Write or paste your news script below:",
        value=default_script,
        height=300,
        help="Enter the complete script. For Hindi, you can type in Devanagari script or romanized Hindi."
    )
    
    # Script options
    st.markdown("### ⚙️ Script Options")
    col2a, col2b = st.columns(2)
    
    with col2a:
        add_intro = st.checkbox("Add standard intro", value=True)
    with col2b:
        add_outro = st.checkbox("Add standard outro", value=True)
    
    # Language-specific tips
    if selected_language == "हिंदी (Hindi)":
        st.info("💡 Tip: You can mix Hindi and English words naturally. The AI will handle code-switching automatically!")
    else:
        st.info("💡 Tip: Keep sentences clear and use proper punctuation for natural pauses.")

# Generate button
if st.button("🎬 Generate News Video", type="primary", use_container_width=True):
    if news_script and news_script.strip():
        with st.spinner("🎥 Generating your multilingual AI news anchor video... This may take a few moments."):
            
            # Prepare the final script with language-appropriate intro/outro
            final_script = ""
            
            if add_intro:
                if selected_language == "हिंदी (Hindi)":
                    final_script = "नमस्कार दोस्तों, मैं आपकी AI समाचारवाचिका हूं। आज के समाचारों में आपका स्वागत है।\n\n"
                else:
                    final_script = "Hello World, I'm your AI News Anchor. Welcome to today's broadcast.\n\n"
            
            final_script += news_script
            
            if add_outro:
                if selected_language == "हिंदी (Hindi)":
                    final_script += "\n\nआज के समाचार समाप्त। अधिक जानकारी के लिए जुड़े रहें। देखने के लिए धन्यवाद!"
                else:
                    final_script += "\n\nThat's all for today's news. Thank you for watching, and stay informed!"
            
            # Generate the video with fallback support
            try:
                # Set the selected voice and generate video
                video_generator.voice_id = selected_voice_id
                
                # Handle voice styles for supported voices
                voice_for_generation = selected_voice_id
                if style_options[selected_style] != "default":
                    # For styled voices, we'll modify the script with SSML
                    style_name = style_options[selected_style]
                    styled_script = f'<mstts:express-as style="{style_name}">{final_script}</mstts:express-as>'
                    script_to_use = styled_script
                else:
                    script_to_use = final_script
                
                # Try primary URL first
                video_url = None
                avatar_url_used = avatar_config["value"]
                
                # For Fatha, try the D-ID test image that we know works
                if selected_avatar_name == "Fatha (Professional)":
                    # Use D-ID's working test image
                    avatar_url_used = "https://d-id-public-bucket.s3.amazonaws.com/alice.jpg"
                    st.info("Note: Using D-ID's test avatar due to server issues. The appearance may differ from Fatha.")
                
                video_url = video_generator.generate_video(
                    script_to_use, 
                    avatar_url_used, 
                    voice_for_generation
                )
                
                # If failed and we have fallbacks, try them
                if not video_url and avatar_config.get("fallback"):
                    st.warning("Primary avatar failed, trying fallback options...")
                    for fallback_url in avatar_config["fallback"]:
                        st.info(f"Trying fallback: {fallback_url[:50]}...")
                        video_url = video_generator.generate_video(
                            script_to_use, 
                            fallback_url, 
                            voice_for_generation
                        )
                        if video_url:
                            avatar_url_used = fallback_url
                            break
                
                if video_url:
                    st.success("✅ Video generated successfully!")
                    
                    # Display the video
                    st.markdown("### 📺 Your Multilingual AI News Broadcast")
                    st.video(video_url)
                    
                    # Provide download link
                    st.markdown(f"[📥 Download Video]({video_url})")
                    
                    # Display the script that was used
                    with st.expander("📄 View Final Script"):
                        st.text(final_script)
                        
                    # Show technical details
                    with st.expander("🔧 Technical Details"):
                        st.write(f"**Avatar:** {selected_avatar_name}")
                        st.write(f"**Image URL Used:** {avatar_url_used}")
                        st.write(f"**Voice ID:** {selected_voice_id}")
                        st.write(f"**Language:** {selected_language}")
                        st.write(f"**Style:** {selected_style}")
                        st.write(f"**Script Length:** {len(final_script)} characters")
                else:
                    st.error("❌ Failed to generate video.")
                    st.error("D-ID's servers appear to be having issues (500 Internal Server Error).")
                    st.info("**Try these solutions:**")
                    st.write("1. Wait a few minutes and try again")
                    st.write("2. Use the 'Custom News Anchor' option instead")
                    st.write("3. Contact D-ID support if the problem persists")
                    st.write("4. Check D-ID's status page: https://status.d-id.com/")
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                if "500" in str(e) or "Internal Server Error" in str(e):
                    st.error("D-ID is experiencing server issues. Please try again later.")
                    st.info("You can check D-ID's status at: https://status.d-id.com/")
                else:
                    st.write("Please check your D-ID API configuration and try again.")
    else:
        st.warning("⚠️ Please enter a news script before generating the video.")

# Sidebar with multilingual instructions
with st.sidebar:
    st.markdown("## 🚨 D-ID Server Status")
    st.warning("""
    If you're getting 500 errors:
    - D-ID's servers may be down
    - Try the Custom News Anchor
    - Check: https://status.d-id.com/
    """)
    
    st.markdown("## 📖 How to Use")
    st.markdown("""
    1. **Choose Avatar**: Select between Custom or Fatha
    2. **Choose Language**: Select English or Hindi (हिंदी)
    3. **Select Voice**: Pick your preferred anchor voice
    4. **Choose Style**: Select voice emotion/style (for supported voices)
    5. **Write Script**: Enter your news script
    6. **Generate**: Click the Generate button
    7. **Watch**: View your multilingual AI news video!
    """)
    
    st.markdown("## 👤 Available Avatars")
    st.markdown("""
    **1. Custom News Anchor**
    - Your original anchor image
    - Professional news presenter style
    - Most reliable option
    
    **2. Fatha**
    - D-ID's professional female presenter
    - May fall back to test avatar if servers have issues
    """)
    
    st.markdown("## 🔧 Troubleshooting")
    st.markdown("""
    **Getting 500 errors?**
    - D-ID servers might be down
    - Use Custom News Anchor instead
    - Wait and retry in a few minutes
    
    **Wrong avatar appearing?**
    - Server issues may cause fallback
    - Custom anchor always works
    """)
    
    st.markdown("## 🎭 Available Voices")
    
    st.markdown("**English Voices:**")
    st.markdown("- Sophie, James, Emma, Christopher (US)")
    st.markdown("- Neerja (Indian English)")
    
    st.markdown("**हिंदी आवाजें:**")
    st.markdown("- स्वरा (Swara) - Female")
    st.markdown("- मधुर (Madhur) - Male") 
    st.markdown("- आरती (Aarti) - Female")
    st.markdown("- अर्जुन (Arjun) - Male")