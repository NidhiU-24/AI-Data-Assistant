import streamlit as st
import requests
import pandas as pd
from PIL import Image
import io

# -----------------------------
#   BACKEND URL
# -----------------------------
BACKEND = "http://127.0.0.1:5000"

st.set_page_config(page_title="AI Data Science Assistant", layout="centered")
st.title("🤖 AI Data Science Assistant")

# Sidebar
st.sidebar.title("Navigation")
task = st.sidebar.selectbox("Choose a task:", ["Text Chat", "Analyze CSV", "Analyze Image"])

# -----------------------------
#   TEXT CHAT UI
# -----------------------------
if task == "Text Chat":
    st.header("💬 Ask any Data Science / ML question")

    user_msg = st.text_area("Enter your question:")

    if st.button("Send"):
        if not user_msg.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Generating answer..."):
                try:
                    response = requests.post(f"{BACKEND}/chat", json={"message": user_msg})
                    st.success("Response received!")
                    st.write(response.json()["response"])
                except Exception as e:
                    st.error(f"Error: {e}")


# -----------------------------
#   CSV ANALYSIS UI
# -----------------------------
elif task == "Analyze CSV":
    st.header("📊 Upload CSV for Automatic Analysis")

    csv_file = st.file_uploader("Upload your CSV file", type=["csv"])

    if csv_file is not None:
        df = pd.read_csv(csv_file)
        st.write("### Preview:")
        st.dataframe(df.head())

        if st.button("Analyze CSV"):
            with st.spinner("Analyzing CSV..."):
                try:
                    files = {"file": ("uploaded.csv", csv_file.getvalue(), "text/csv")}
                    response = requests.post(f"{BACKEND}/analyze_csv", files=files)

                    st.success("Analysis complete!")
                    st.write(response.json()["analysis"])
                except Exception as e:
                    st.error(f"Error: {e}")


# -----------------------------
#   IMAGE ANALYSIS UI
# -----------------------------
elif task == "Analyze Image":
    st.header("🖼️ Upload Image for AI Interpretation")

    img_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    if img_file is not None:
        image = Image.open(img_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        if st.button("Analyze Image"):
            with st.spinner("Analyzing image..."):
                try:
                    files = {"file": (img_file.name, img_file, img_file.type)}
                    response = requests.post(f"{BACKEND}/analyze_image", files=files)

                    st.success("Image analysis complete!")
                    st.write(response.json()["description"])
                except Exception as e:
                    st.error(f"Error: {e}")
