import streamlit as st
import google.generativeai as genai
from PIL import Image
import urllib.parse

# --- 1. CONFIGURATION & SETUP ---
st.set_page_config(
    page_title="VibeVeda AI | Contextual Aesthetic Engine",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Hide Streamlit Default Style
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- 2. API KEY MANAGEMENT ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("⚠️ API Key not found! Please add GEMINI_API_KEY to your Streamlit Secrets.")
    st.stop()

# --- 3. THE MODEL ---
model = genai.GenerativeModel('gemini-2.0-flash')

# --- 4. SIDEBAR (CONTEXT MANAGER) ---
with st.sidebar:
    st.title("🎛️ Context Manager")
    st.write("Defining the 'Why' behind the look.")
    
    occasion = st.selectbox(
        "Where are you going?",
        [
            "Select Context...",
            "Indian Wedding (Sangeet/Reception)",
            "College Fest / Hackathon",
            "Corporate Office / Interview",
            "First Date (Casual)",
            "Clubbing / Night Out",
            "Lazy Sunday / Home"
        ]
    )
    
    st.info(f"💡 **Current Logic:** Prioritizing '{occasion}' rules over image pixels.")

# --- 5. MAIN UI ---
st.title("✨ VibeVeda AI")
st.caption("The Contextual Aesthetic Engine | Team localhost:5000")

uploaded_file = st.file_uploader("Upload your Vibe (Image)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Input Visual", use_container_width=True)

    # --- 6. THE ACTION BUTTON ---
    if st.button("🚀 Decode Aesthetic & Context"):
        
        if occasion == "Select Context...":
            st.warning("⚠️ Please select an Occasion/Context in the Sidebar first!")
        else:
            with st.spinner(f"🧠 Orchestrating Agents for '{occasion}'..."):
                
                # --- 7. THE "SHOCK & BUILD" PROMPT ---
                prompt = f"""
                You are VibeVeda, a Context-Adaptive Style Engine.
                
                INPUT DATA:
                1. Image Analysis: Extract the core visual elements (colors, objects).
                2. CONTEXT CONSTRAINT: User is going to: '{occasion}' (This is the DOMINANT variable).

                THE CHALLENGE:
                You must ignore the "standard" vibe of the image if it conflicts with the '{occasion}'.
                Twist the interpretation to fit the context perfectly. 

                STRUCTURE YOUR RESPONSE EXACTLY LIKE THIS (Use Markdown):
                
                ### 🧠 Context Logic
                **Input Context:** {occasion}
                **Adaptation Strategy:** [Explain in 1 sentence HOW you are pivoting the style for this event.]
                
                ### 🎨 The Re-Imagined Vibe
                [Describe the new vibe specifically for {occasion}. Use 3 emotional adjectives.]
                
                ### 🧬 Context-Specific Palette
                * **Primary:** [Hex Code 1] - [Color Name]
                * **Secondary:** [Hex Code 2] - [Color Name]
                * **Accent:** [Hex Code 3] - [Color Name]
                
                ### 🎵 Audio Match ({occasion} Mix)
                * **Song:** [Song Name] - [Artist]
                * **Vibe Check:** [Why this song fits a {occasion}?]
                
                ### 🛍️ Strategic Styling (Budget vs Luxury)
                **The 'Pivot' Item:** [Suggest one item that makes this look work for {occasion}.]
                **Styling Hack:** [A specific tip to adjust the fit/accessories for {occasion}.]
                **Budget Pick:** [A cheaper alternative relevant to Indian students]
                """

                try:
                    # Call Gemini
                    response = model.generate_content([prompt, image])
                    result_text = response.text
                    
                    st.success("✅ Context Decoded Successfully!")
                    st.markdown(result_text)
                    
                    # --- 9. UPDATED ACTION BUTTONS ---
                    st.divider()
                    st.subheader("⚡ Take Action")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    # 🎵 FIXED SPOTIFY LINK (Standard Web Search)
                    spotify_query = urllib.parse.quote(f"{occasion} {occasion} hindi song") 
                    # Note: Repeating occasion helps keyword relevance
                    with col1:
                        st.link_button("🎵 Open Spotify", f"https://open.spotify.com/search/{spotify_query}")

                    # 🛍️ GOOGLE SHOPPING LINK
                    shop_query = urllib.parse.quote(f"{occasion} outfit aesthetic india")
                    with col2:
                        st.link_button("🛍️ Google Shopping", f"https://www.google.com/search?tbm=shop&q={shop_query}")
                        
                    # 💬 WHATSAPP SHARE
                    share_text = urllib.parse.quote(f"Check out my {occasion} look generated by VibeVeda AI! 🚀")
                    with col3:
                        st.link_button("💬 Share Vibe", f"https://wa.me/?text={share_text}")
                        
                except Exception as e:
                    st.error(f"An error occurred: {e}")
