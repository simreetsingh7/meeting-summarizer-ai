import streamlit as st
from openai import OpenAI

# --- 1. SEO & PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Meeting Summarizer | Instant Bullet Points & Action Items",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- 2. SIDEBAR: MONETIZATION & AUTH ---
st.sidebar.header("🚀 Pro Access")
st.sidebar.write("Get **unlimited summaries** and priority support.")
st.sidebar.write("**Price: CA$9.99 / month**")

# --- YOUR REAL STRIPE PAYMENT LINK ---
stripe_payment_link = "https://buy.stripe.com/7sYcN73uOgVkeA75Ob3sI00"

# Simple Session State for Free Trial Logic
if 'count' not in st.session_state:
    st.session_state.count = 0

is_pro = st.session_state.get('is_pro', False)

if not is_pro:
    st.sidebar.info("You have **1 free summary** remaining.")
    if st.session_state.count >= 1:
        st.sidebar.warning("⚠️ Free trial used! Upgrade to continue.")
        st.sidebar.markdown(f"[**👉 Subscribe Now — CA$9.99/mo**]({stripe_payment_link})")
        pro_code = st.sidebar.text_input("Enter Pro Access Code (from email)")
        if pro_code == "BETA2026":
            st.session_state['is_pro'] = True
            st.rerun()
    else:
        st.sidebar.success("✅ Ready to start!")
else:
    st.sidebar.success("🌟 Pro Member: Unlimited Access")
    if st.sidebar.button("Manage Subscription"):
        st.sidebar.markdown(f"[Click here]({stripe_payment_link})")

st.sidebar.markdown("---")
st.sidebar.caption("Powered by NVIDIA Nemotron-3-Super | Free Beta")

# --- 3. MAIN APP UI ---
st.title("📝 Instant Meeting Summarizer")
st.text("Transform long meeting transcripts into clear bullet points and action items in seconds using advanced AI.")
st.markdown("---")

# --- 4. API CLIENT SETUP ---
try:
    api_key = st.secrets["NVIDIA_API_KEY"]
except:
    api_key = "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"

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key
)

# --- 5. USER INPUT ---
user_text = st.text_area(
    "Paste your meeting transcript below:", 
    height=200,
    placeholder="Example: 'Hey everyone, thanks for joining. Let's start with the Q3 review...'"
)

# --- 6. GENERATE BUTTON & LOGIC ---
if st.button("✨ Summarize Now", type="primary"):
    if user_text:
        # Check Trial Limit
        if not is_pro and st.session_state.count >= 1:
            st.error("🔒 You have used your free trial. Please upgrade in the sidebar to continue.")
            st.stop()

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
                
                # Increment Free Trial Counter
                if not is_pro:
                    st.session_state.count += 1
                    if st.session_state.count >= 1:
                        st.rerun()
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("⚠️ Please paste a transcript first.")

# --- 7. FOOTER ---
st.markdown("---")
st.caption("© 2026 Simreet Singh | Built with NVIDIA NIM")