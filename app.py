import streamlit as st
import google.generativeai as genai
from PIL import Image
import urllib.parse
import re


try:
    if "GEMINI_API_KEY" in st.secrets:
        API_KEY = st.secrets["GEMINI_API_KEY"]
    
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash')
except Exception as e:
    st.error("⚠️ API Key Error. If you are on the cloud, check your Secrets.")

# --- 2. UI CONFIGURATION ---
st.set_page_config(
    page_title="VibeVeda AI",
    page_icon="🧘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 3. HELPER FUNCTIONS ---

def extract_hex_codes(text):
    """Finds colors like #FF0000 and ensures they are valid"""
    hex_codes = re.findall(r'#[0-9a-fA-F]{6}', text)
    return list(set(hex_codes))[:5] # Unique colors, max 5

def create_spotify_search_link(search_query):
    """Creates a real Spotify Search Link"""
    clean_query = urllib.parse.quote(search_query)
    return f"https://open.spotify.com/search/{clean_query}"

def create_shopping_search_link(search_query):
    """Creates a Google Shopping Link"""
    clean_query = urllib.parse.quote(search_query)
    return f"https://www.google.com/search?tbm=shop&q={clean_query}"

def create_whatsapp_link(text):
    """Creates a WhatsApp Share Link"""
    clean_text = urllib.parse.quote(text)
    return f"https://wa.me/?text={clean_text}"

# --- 4. CUSTOM CSS (Visual Polish) ---
st.markdown("""
<style>
    /* Dark Theme & Typography */
    .stApp { background-color: #0E1117; color: #E0E0E0; font-family: 'Inter', sans-serif; }
    
    /* Color Swatch Styling (The Box) */
    .color-box {
        width: 100%;
        height: 100px;
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: white;
        text-shadow: 0px 0px 4px rgba(0,0,0,0.8);
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        margin-bottom: 10px;
        font-size: 14px;
    }
    
    /* Remove standard button borders for cleaner look */
    .stLinkButton > a {
        background: linear-gradient(90deg, #1F2937, #111827);
        color: #4ADE80 !important; /* Matrix Green Text */
        border: 1px solid #374151;
        font-weight: bold;
    }
    
    /* Sidebar Cleanup */
    [data-testid="stSidebar"] { background-color: #111; }
</style>
""", unsafe_allow_html=True)

# --- 5. SIDEBAR ---
with st.sidebar:
    st.title("🧘 VibeVeda")
    st.caption("Contextual AI Stylist")
    st.divider()
    
    # Context Selector
    occasion = st.selectbox(
        "Where are you going?",
        ["College Fest / Campus", "Indian Wedding", "Tech Hackathon", "First Date", "Casual Outing", "Office"]
    )
    
    st.info("💡 **Tip:** Upload an image to get a full aesthetic breakdown, including playlist and shopping links.")

# --- 6. MAIN APP LOGIC ---
st.title("✨ VibeVeda: The Aesthetic Decoder")
st.markdown("### Upload inspiration. **Get the Vibe.**")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("📸 Input Source")
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, use_container_width=True, caption="Your Inspiration")
        
        # Analyze Button
        analyze = st.button("🔮 DECODE AESTHETIC", type="primary")

with col2:
    if uploaded_file and analyze:
        with st.spinner("🤖 AI Agents are negotiating your style & music..."):
            
            # --- THE PROMPT (Fixed for Content & Gender Neutrality) ---
            prompt = f"""
            Act as a Creative Director and Music Curator. Analyze this image for a user going to: {occasion}.
            
            Your Goal: Create a rich, attractive aesthetic report.
            
            Structure your response exactly like this:
            
            ## 🎨 The Vibe Narrative
            [Write a 3-sentence poetic description of the mood in this image. Use evocative language.]
            
            ## 🧬 Color Palette
            [List 4 specific Hex Codes found in the image, e.g. #FF0000]
            
            ## 🎵 Audio Match
            **Song:** [Suggest 1 Catchy Trending Indian/Hindi/Indie Song]
            **Artist:** [Artist Name]
            **Why:** [One short sentence why]
            
            ## 🛍️ Fashion Strategy
            **Search Keyword:** [Provide 1 precise search term for shopping, e.g. 'Men's oversized beige hoodie' or 'Women's Chikankari Kurtis'. Be gender-specific based on the image content.]
            **Style Tip:** [One actionable fashion tip]
            """
            
            # Get Response
            response = model.generate_content([prompt, img])
            text = response.text
            
            # --- DISPLAY RESULTS ---
            
            # 1. Text Report (Rich Content)
            st.markdown(text)
            
            # 2. VISUAL COLOR PALETTE (Fixed!)
            st.subheader("🎨 Visual Palette")
            hex_codes = extract_hex_codes(text)
            
            if hex_codes:
                cols = st.columns(len(hex_codes))
                for i, color in enumerate(hex_codes):
                    # HTML Magic to show REAL colored boxes
                    cols[i].markdown(
                        f'<div class="color-box" style="background-color: {color};">{color}</div>', 
                        unsafe_allow_html=True
                    )
            
            st.divider()
            
            # 3. INTERACTIVE BUTTONS (Fixed!)
            st.subheader("🚀 Take Action")
            
            # Smart Logic to find the song and shopping terms from the text
            # We assume the AI followed the format, but we use safe fallbacks
            try:
                # Find the song name
                song_match = re.search(r"\*\*Song:\*\* (.*)", text)
                song_query = song_match.group(1).strip() if song_match else "Trending Hindi Song"
                
                # Find the shopping keyword
                shop_match = re.search(r"\*\*Search Keyword:\*\* (.*)", text)
                shop_query = shop_match.group(1).strip() if shop_match else "Aesthetic Outfit"
                
            except:
                song_query = "Trending India"
                shop_query = "Aesthetic Fashion"
            
            b1, b2 = st.columns(2)
            
            # Fixed Spotify Link
            with b1:
                st.link_button("🎵 Play on Spotify", create_spotify_search_link(song_query))
            
            # Fixed Shopping Link (Now uses the smart keyword)
            with b2:
                st.link_button("🛍️ Shop this Look", create_shopping_search_link(shop_query))
                
            # 4. SHARING
            st.divider()
            share_text = f"Check out my VibeVeda Report! Mood: {song_query}. #VibeVeda"
            st.link_button("💬 Share on WhatsApp", create_whatsapp_link(share_text))

    elif not uploaded_file:
        st.info("👈 Upload an image to start.")
        st.markdown("### Try uploading:")
        st.markdown("- A photo of a **wedding lehenga**")
        st.markdown("- A **neon street** scene")
        st.markdown("- A **coffee shop** aesthetic")
