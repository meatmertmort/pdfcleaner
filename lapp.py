import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io

st.set_page_config(layout="wide", page_title="PDF Slide Reviewer")

st.title("📑 PDF Slide Eliminator")

# 1. Initialize State
if 'hidden_pages' not in st.session_state:
    st.session_state.hidden_pages = set()
if 'selected_to_remove' not in st.session_state:
    st.session_state.selected_to_remove = set()

uploaded_file = st.file_uploader("Upload your PDF", type="pdf")

if uploaded_file:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    
    # Filter out already removed pages
    visible_indices = [i for i in range(len(doc)) if i not in st.session_state.hidden_pages]

    # 2. Control Bar (Top)
    col_a, col_b, col_c = st.columns([2, 1, 1])
    with col_a:
        st.write(f"Showing **{len(visible_indices)}** slides. Select the ones you've finished.")
    with col_b:
        if st.button("🗑️ Remove Selected", type="primary", use_container_width=True):
            st.session_state.hidden_pages.update(st.session_state.selected_to_remove)
            st.session_state.selected_to_remove = set() # Clear selection after removing
            st.rerun()
    with col_c:
        if st.button("🔄 Reset All", use_container_width=True):
            st.session_state.hidden_pages = set()
            st.session_state.selected_to_remove = set()
            st.rerun()

    st.divider()

    # 3. Grid Display (4 per row)
    num_cols = 4
    for i in range(0, len(visible_indices), num_cols):
        cols = st.columns(num_cols)
        for j in range(num_cols):
            index_in_visible = i + j
            if index_in_visible < len(visible_indices):
                page_idx = visible_indices[index_in_visible]
                
                # Render page at high quality
                page = doc.load_page(page_idx)
                pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
                img = Image.open(io.BytesIO(pix.tobytes("png")))
                
                with cols[j]:
                    st.image(img, use_container_width=True)
                    # Checkbox for selection
                    is_checked = st.checkbox(f"Slide {page_idx + 1}", key=f"check_{page_idx}")
                    
                    if is_checked:
                        st.session_state.selected_to_remove.add(page_idx)
                    else:
                        st.session_state.selected_to_remove.discard(page_idx)
