import streamlit as st
import requests
from PIL import Image

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AI Dog Breed Classifier",
    page_icon="🐶",
    layout="wide"
)

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

/* Main Background */
[data-testid="stAppViewContainer"]{
    background: linear-gradient(
        135deg,
        #0f172a,
        #111827,
        #1e293b
    );
    color: white;
}

/* Sidebar */
[data-testid="stSidebar"]{
    background: rgba(15,23,42,0.95);
}

/* Hide Streamlit Branding */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* Upload Box */
[data-testid="stFileUploader"]{
    background: rgba(255,255,255,0.05);
    border-radius: 20px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.08);
}

/* Buttons */
.stButton > button{
    width: 100%;
    height: 3.3em;
    border-radius: 15px;
    border: none;
    font-size: 18px;
    font-weight: bold;
    background: linear-gradient(
        90deg,
        #00C9FF,
        #92FE9D
    );
    color: black;
    transition: 0.3s;
}

.stButton > button:hover{
    transform: scale(1.02);
}

/* Result Cards */
.result-card{
    background: rgba(255,255,255,0.07);
    backdrop-filter: blur(14px);
    padding: 25px;
    border-radius: 22px;
    margin-bottom: 25px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0px 10px 35px rgba(0,0,0,0.35);
}

/* Metrics */
.metric-card{
    background: rgba(255,255,255,0.06);
    padding: 20px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0px 8px 30px rgba(0,0,0,0.25);
}

/* Hero */
.hero{
    padding: 3rem;
    border-radius: 28px;
    background: linear-gradient(
        135deg,
        #1f4037,
        #99f2c8
    );
    text-align:center;
    color:white;
    margin-bottom:30px;
    box-shadow: 0px 12px 45px rgba(0,0,0,0.4);
}

/* Images */
img{
    border-radius: 18px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# API URL
# ==========================================

API_URL = "https://dog-classifier-api-v2.onrender.com/predict_batch"

# ==========================================
# SESSION HISTORY
# ==========================================

if "history" not in st.session_state:
    st.session_state.history = []

# ==========================================
# HERO SECTION
# ==========================================

st.markdown("""
<div class="hero">

<h1 style="font-size:58px;">
🐶 AI Dog Breed Classifier
</h1>

<p style="font-size:22px;">
Deep Learning Powered Dog Recognition System
</p>

</div>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown("# 🧠 AI Dashboard")

    st.success("Model Status: Online ✅")

    st.markdown("## ⚙️ Tech Stack")

    st.write("""
    - TensorFlow
    - FastAPI
    - Docker
    - Streamlit
    - Render Cloud
    """)

    st.markdown("## 🚀 Features")

    st.write("""
    ✅ Batch Prediction  
    ✅ Dog Breed Detection  
    ✅ Confidence Meter  
    ✅ Breed Information  
    ✅ Prediction History
    """)

    st.info("""
    🐶 AI Breed Detection System

    This deep learning model supports recognition of 100+ dog breeds including:

    • Husky
    • Labrador Retriever
    • Golden Retriever
    • German Shepherd
    • Pug
    • Rottweiler
    • Doberman
    • Chihuahua
    • Border Collie
    • Saint Bernard
    • and many more...

    📸 For best results:
    • Upload clear dog images
    • Use front-facing photos
    • Avoid blurry or dark images
    """)

    st.warning(
        "⚠️ Upload maximum 5 images for smooth prediction."
    )

# ==========================================
# FILE UPLOADER
# ==========================================

uploaded_files = st.file_uploader(
    "📤 Upload Dog Images",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

# ==========================================
# IMAGE LIMIT WARNING
# ==========================================

if uploaded_files:

    if len(uploaded_files) > 5:

        st.error(
            "⚠️ Please upload maximum 5 images for smooth prediction and better performance."
        )

        st.info(
            "Large batches may slow down the AI model on cloud deployment."
        )

        st.stop()

    else:

        st.success(
            f"✅ {len(uploaded_files)} image(s) uploaded successfully."
        )

# ==========================================
# SHOW IMAGES
# ==========================================

if uploaded_files:

    st.markdown("## 🖼 Uploaded Images")

    cols = st.columns(3)

    for idx, uploaded_file in enumerate(uploaded_files):

        image = Image.open(uploaded_file)

        with cols[idx % 3]:

            st.image(
                image,
                caption=uploaded_file.name,
                use_container_width=True
            )

# ==========================================
# PREDICT BUTTON
# ==========================================

if uploaded_files:

    if st.button("🚀 Predict Breeds"):

        with st.spinner(
            "AI Model is analyzing images..."
        ):

            try:

                files = []

                for uploaded_file in uploaded_files:

                    files.append(
                        (
                            "files",
                            (
                                uploaded_file.name,
                                uploaded_file.getvalue(),
                                uploaded_file.type
                            )
                        )
                    )

                response = requests.post(
                    API_URL,
                    files=files,
                    timeout=120
                )

                # ==========================================
                # SUCCESS RESPONSE
                # ==========================================

                if response.status_code == 200:

                    result = response.json()

                    st.success(
                        "Prediction Completed Successfully ✅"
                    )

                    # Save History
                    st.session_state.history.append(
                        result["results"]
                    )

                    # ==========================================
                    # METRICS
                    # ==========================================

                    col1, col2 = st.columns(2)

                    with col1:

                        st.markdown(f"""
                        <div class="metric-card">
                        <h2>📦 Batch Size</h2>
                        <h1>{result['batch_size']}</h1>
                        </div>
                        """, unsafe_allow_html=True)

                    with col2:

                        st.markdown(f"""
                        <div class="metric-card">
                        <h2>⏱ Processing Time</h2>
                        <h1>{result['processing_time']} sec</h1>
                        </div>
                        """, unsafe_allow_html=True)

                    st.divider()

                    # ==========================================
                    # RESULTS
                    # ==========================================

                    for item in result["results"]:

                        confidence = item["confidence"]

                        dog_info = item.get("dog_info")

                        st.markdown(f"""
                        <div class="result-card">

                        <h2 style="color:#00FFD1;">
                        🐕 {item['class_name']}
                        </h2>

                        <h4>
                        📄 {item['filename']}
                        </h4>

                        <h3 style="color:#FFD166;">
                        Confidence: {confidence:.2f}
                        </h3>

                        </div>
                        """, unsafe_allow_html=True)

                        # ==========================================
                        # CONFIDENCE BAR
                        # ==========================================

                        st.markdown(
                            "### 🎯 Confidence Meter"
                        )

                        st.progress(
                            min(float(confidence), 1.0)
                        )

                        st.caption(
                            f"{round(confidence * 100, 2)}% confident this is a {item['class_name']}"
                        )

                        # ==========================================
                        # DOG INFO
                        # ==========================================

                        if dog_info:

                            st.markdown(
                                "## 📖 Breed Information"
                            )

                            info_col1, info_col2 = st.columns(2)

                            with info_col1:

                                st.info(
                                    f"🌍 Origin: {dog_info.get('origin', 'N/A')}"
                                )

                                st.info(
                                    f"⏳ Life Span: {dog_info.get('life_span', 'N/A')}"
                                )

                                st.info(
                                    f"⚖️ Weight: {dog_info.get('weight', 'N/A')}"
                                )

                                st.info(
                                    f"📜 History: {dog_info.get('history', 'N/A')}"
                                )

                            with info_col2:

                                st.info(
                                    f"📏 Height: {dog_info.get('height', 'N/A')}"
                                )

                                st.info(
                                    f"🎭 Temperament: {dog_info.get('temperament', 'N/A')}"
                                )

                            st.markdown(
                                "### 📝 Description"
                            )

                            st.write(
                                dog_info.get(
                                    "description",
                                    "No description available."
                                )
                            )

                        else:

                            st.warning(
                                "Dog information not available."
                            )

                        st.divider()

                # ==========================================
                # API ERROR
                # ==========================================

                else:

                    st.error(
                        f"API Error: {response.text}"
                    )

            # ==========================================
            # FRONTEND ERROR
            # ==========================================

            except Exception as e:

                st.error(
                    f"Frontend Error: {str(e)}"
                )

# ==========================================
# PREDICTION HISTORY
# ==========================================

if st.session_state.history:

    st.markdown("## 🕘 Prediction History")

    for batch in reversed(st.session_state.history):

        for item in batch:

            st.markdown(f"""
            <div class="result-card">

            <h3 style="color:#92FE9D;">
            🐕 {item['class_name']}
            </h3>

            <p>
            📄 {item['filename']}
            </p>

            <p>
            Confidence: {item['confidence']:.2f}
            </p>

            </div>
            """, unsafe_allow_html=True)

# ==========================================
# PROFESSIONAL FOOTER
# ==========================================

st.markdown("""
<hr style="
border: 1px solid rgba(255,255,255,0.1);
margin-top: 50px;
margin-bottom: 20px;
">

<div style="
text-align:center;
padding: 20px;
color: #9CA3AF;
font-size: 15px;
">

<h3 style="
color:white;
margin-bottom:10px;
">
🐶 AI Dog Breed Classification System
</h3>

<p>
Deep Learning Powered Computer Vision Application
</p>

<p style="
font-size:13px;
color:#6B7280;
">
TensorFlow • FastAPI • Streamlit • Docker • Render Cloud
</p>

</div>
""", unsafe_allow_html=True)