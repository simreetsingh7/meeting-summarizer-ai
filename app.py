import streamlit as st
from openai import OpenAI

# --- 1. SEO & PAGE CONFIGURATION (Must be the very first Streamlit command) ---
st.set_page_config(
    page_title="AI Meeting Summarizer | Instant Bullet Points & Action Items",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. SEO-FRIENDLY HEADER & DESCRIPTION ---
# Search engines prioritize st.header and st.text for descriptions
st.title("📝 Instant Meeting Summarizer")
st.text("Transform long meeting transcripts into clear bullet points and action items in seconds using advanced AI.")
st.markdown("---")

# --- 3. API CLIENT SETUP ---
# Uses your NVIDIA API Key securely
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)

# --- 4. USER INPUT ---
user_text = st.text_area(
    "Paste your meeting transcript below:", 
    height=200,
    placeholder="Example: 'Hey everyone, thanks for joining. Let's start with the Q3 review...'"
)

# --- 5. GENERATE BUTTON & LOGIC ---
if st.button("✨ Summarize Now", type="primary"):
    if user_text:
        with st.spinner("AI is analyzing your transcript..."):
            try:
                response = client.chat.completions.create(
                    model="nvidia/nemotron-3-super-120b-a12b",
                    messages=[
                        {"role": "system", "content": "You are a professional executive assistant. Summarize the following meeting transcript into 5 key bullet points and 3 clear action items. Use bold text for emphasis."},
                        {"role": "user", "content": user_text}
                    ],
                    max_tokens=600,
                    temperature=0.3
                )
                
                st.success("✅ Summary Generated:")
                st.markdown(response.choices[0].message.content)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("⚠️ Please paste a transcript first.")

# --- 6. FOOTER (Optional Branding) ---
st.markdown("---")
st.caption("Powered by NVIDIA Nemotron-3-Super | Free Beta Version")   