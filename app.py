import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io

st.set_page_config(layout="wide", page_title="PDF Slide Reviewer")

st.title("📑 PDF Slide Eliminator")

if 'hidden_pages' not in st.session_state:
    st.session_state.hidden_pages = set()

uploaded_file = st.file_uploader("Upload your PDF", type="pdf")

if uploaded_file:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    cols = st.columns(4) 
    
    for i in range(len(doc)):
        if i not in st.session_state.hidden_pages:
            page = doc.load_page(i)
            pix = page.get_pixmap(matrix=fitz.Matrix(0.5, 0.5))
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data))
            
            with cols[i % 4]:
                st.image(img, caption=f"Page {i+1}", use_container_width=True)
                if st.button(f"Done with {i+1}", key=f"btn_{i}"):
                    st.session_state.hidden_pages.add(i)
                    st.rerun()

    if st.button("Reset All Slides"):
        st.session_state.hidden_pages = set()
        st.rerun()
