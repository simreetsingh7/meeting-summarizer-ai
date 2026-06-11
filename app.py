import streamlit as st
from openai import OpenAI

# --- URL PARAM PERSISTENCE (Survives Refreshes) ---
def get_from_url(key, default=None):
    """Read value from URL query params"""
    return st.query_params.get(key, default)

def set_in_url(key, value):
    """Write value to URL query params (persists across refreshes)"""
    st.query_params[key] = str(value)

# Initialize from URL params
if 'trial_used' not in st.session_state:
    trial_val = get_from_url('trial')
    st.session_state.trial_used = int(trial_val) if trial_val else 0

if 'is_pro' not in st.session_state:
    pro_val = get_from_url('pro')
    st.session_state.is_pro = (pro_val == '1')

trial_used = st.session_state.trial_used
is_pro = st.session_state.is_pro

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

stripe_payment_link = "https://buy.stripe.com/7sYcN73uOgVkeA75Ob3sI00"

if is_pro:
    st.sidebar.success("🌟 Pro Member: Unlimited Access")
    if st.sidebar.button("Manage Subscription"):
        st.sidebar.markdown(f"[Click here]({stripe_payment_link})")
else:
    remaining = max(0, 1 - trial_used)
    
    if remaining > 0:
        st.sidebar.info(f"You have **{remaining} free summary** remaining.")
        st.sidebar.success("✅ Ready to start!")
    else:
        st.sidebar.warning("⚠️ Free trial used! Upgrade to continue.")
        st.sidebar.markdown(f"[**👉 Subscribe Now — CA$9.99/mo**]({stripe_payment_link})")
        pro_code = st.sidebar.text_input("Enter Pro Access Code (from email)")
        if pro_code == "BETA2026":
            st.session_state.is_pro = True
            set_in_url('pro', '1')
            st.sidebar.success("✅ Pro activated!")
            st.rerun()

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
        if not is_pro and trial_used >= 1:
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
                
                # Increment trial and save to URL
                if not is_pro:
                    st.session_state.trial_used += 1
                    set_in_url('trial', str(st.session_state.trial_used))
                    st.info("💡 You have used your free summary. Upgrade to Pro for unlimited access.")
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("⚠️ Please paste a transcript first.")

# --- 7. FOOTER ---
st.markdown("---")
st.caption("© 2026 Simreet Singh | Built with NVIDIA NIM")