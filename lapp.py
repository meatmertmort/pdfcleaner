import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io

st.set_page_config(layout="wide", page_title="PDF Slide Reviewer")

st.title("📑 PDF Slide Eliminator")

# Initialize session state
if 'hidden_pages' not in st.session_state:
    st.session_state.hidden_pages = set()

uploaded_file = st.file_uploader("Upload your PDF", type="pdf")

if uploaded_file:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    
    # Filter out hidden pages first so we know how many to display
    visible_indices = [i for i in range(len(doc)) if i not in st.session_state.hidden_pages]
    
    # Create the grid: 4 slides per row
    num_cols = 4
    for i in range(0, len(visible_indices), num_cols):
        # Create a new row of 4 columns
        cols = st.columns(num_cols)
        
        # Fill the 4 columns in this specific row
        for j in range(num_cols):
            index_in_visible = i + j
            if index_in_visible < len(visible_indices):
                page_idx = visible_indices[index_in_visible]
                
                # Render page
                page = doc.load_page(page_idx)
                # Zoom 2.0 for high quality
                pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
                img_data = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_data))
                
                with cols[j]:
                    st.image(img, caption=f"Slide {page_idx + 1}", use_container_width=True)
                    if st.button(f"Mark Done: {page_idx + 1}", key=f"btn_{page_idx}"):
                        st.session_state.hidden_pages.add(page_idx)
                        st.rerun()

    st.sidebar.write(f"Remaining: {len(visible_indices)} slides")
    if st.sidebar.button("Reset All Slides"):
        st.session_state.hidden_pages = set()
        st.rerun()
