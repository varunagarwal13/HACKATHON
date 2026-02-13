import streamlit as st
from engine import get_analysis
import os

st.set_page_config(page_title="DeepVerify", layout="wide")

st.title("🛡️ DeepFake Credential Verifier")
st.write("Two-man Hackathon Project: AI + Cybersecurity")

uploaded_file = st.file_uploader("Upload ID Card or Portrait", type=['jpg', 'png', 'jpeg'])

if uploaded_file:
    # Save file temporarily
    with open("temp_upload.jpg", "wb") as f:
        f.write(uploaded_file.getbuffer())

    col1, col2 = st.columns(2)

    with col1:
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

    with col2:
        st.subheader("Scanning Results...")
        with st.spinner("Running Neural Networks..."):
            data = get_analysis("temp_upload.jpg")
            
            # Display Results
            if data['ai_verdict'] == "Fake":
                st.error(f"VERDICT: {data['ai_verdict']} ({data['ai_confidence']:.2%} match)")
            else:
                st.success(f"VERDICT: {data['ai_verdict']} ({data['ai_confidence']:.2%} match)")

            st.write(f"**Software Trace:** {data['software']}")
            st.write(f"**Noise Artifacts:** {data['noise_score']:.2f}")
            
            # Risk Progress Bar
            risk = 80 if data['ai_verdict'] == "Fake" else 10
            if data['is_edited']: risk += 15
            st.write("Overall Risk Score:")
            st.progress(min(risk, 100))
            
