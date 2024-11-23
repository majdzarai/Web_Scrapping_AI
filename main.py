import streamlit as st
from scrape import (
    scrape_website,
    split_don_content,
    clean_body_content,
    extract_body_content,
    extract_images  # Import the new function
)
from parse import parse_with_ollama

# Set page configuration
st.set_page_config(
    page_title="Scraper AI",
    page_icon="🌐",
    layout="wide"
)

# Header with title and description
st.markdown(
    """
    <style>
    .header {
        text-align: center;
        padding: 10px;
        font-family: 'Arial', sans-serif;
        background-color: #f5f5f5;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
    }
    </style>
    <div class="header">
        <h1>Scraper AI</h1>
        <p>Une application alimentée par l'IA pour extraire et analyser le contenu des sites Web.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Input URL section
st.markdown("### 📍 Entrez une URL de site Web :")
url = st.text_input("Saisissez l'URL ici")

if st.button("Scraper le site"):
    st.write("📂 Extraction des données du site Web...")
    result = scrape_website(url)
    body_content = extract_body_content(result)
    cleaned_content = clean_body_content(body_content)
    st.session_state.dom_content = cleaned_content
    st.session_state.html_content = result  # Store the raw HTML content for image extraction

    with st.expander("🔍 Contenu extrait"):
        st.text_area("Contenu DOM", cleaned_content, height=300)

# Parsing section
if "dom_content" in st.session_state:
    st.markdown("### ✂️ Décrire ce que vous voulez analyser :")
    parse_description = st.text_area("Décrivez ici")

    if st.button("Analyser le contenu"):
        st.write("📊 Analyse du contenu en cours...")
        dom_chunks = split_don_content(st.session_state.dom_content)
        result = parse_with_ollama(dom_chunks, parse_description)
        st.success("Analyse terminée !")
        st.markdown("### Résultats de l'analyse :")
        st.write(result)

# New button to extract and visualize all images
if "html_content" in st.session_state:
    if st.button("Extraire et afficher toutes les images"):
        st.write("📷 Extraction des images en cours...")
        image_urls = extract_images(st.session_state.html_content, url)
        if image_urls:
            st.markdown("### 🖼️ Images extraites :")
            for img_url in image_urls:
                # Adjust the size of the displayed images
                st.image(img_url, caption="Image", width=300)  # Set width to 300px or adjust as needed
        else:
            st.warning("Aucune image trouvée dans le contenu HTML.")


# Footer
st.markdown(
    """
    <hr style="border: 1px solid #ddd;">
    <p style="text-align: center; color: #888; font-size: 14px;">
        🚀 Développé par <span style="color: red;">❤</span> Majd Zarai.
    </p>
    """,
    unsafe_allow_html=True
)
