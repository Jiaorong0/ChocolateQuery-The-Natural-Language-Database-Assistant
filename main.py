import streamlit as st
from langchain_helper import get_answer

# Set page configuration
st.set_page_config(page_title="Chocolate Shop: Database Q&A", layout="wide")

# Custom CSS to inject for styling
st.markdown("""
<style>
            
div.stApp {
    background-color: #A0522D;
}
            
.big-font {
    font-size:30px !important;
    font-weight: bold;
}
.image-grid {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-around;
}
.image-grid-item {
    flex: 1;
    margin: 10px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)



# Main banner
st.image('./images/image5.jpeg', use_column_width=True)

# Title and subtitle with custom styling
st.markdown('<h1 class="big-font">Welcome to Chocolate World</h1>', unsafe_allow_html=True)
st.markdown("### Explore our exquisite collection and ask any questions you have!")

# Chocolate brands section
st.markdown('## Our Chocolate Brands')

# Create a grid of images for chocolate brands
brand_data = [
    ("./images/image1.jpeg", "Lindt Brand", "Some description about Lindt Brand."),
    ("./images/image2.jpeg", "Godiva Brand", "Some description about Godiva Brand."),
    ("./images/image3.jpeg", "Hershey Brand", "Some description about Hershey Brand."),
    ("./images/image4.jpeg", "Cadbury Brand", "Some description about Cadbury Brand.")
]

# Generate the brand display dynamically
for image_path, title, desc in brand_data:
    with st.container():
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(image_path, width=150)
        with col2:
            st.markdown(f'### {title}')
            st.write(desc)

# Q&A Section
st.markdown('## Ask a Question')
question = st.text_input("Enter your question here:")

if question:
    answer = get_answer(question)
    st.markdown('### Answer')
    st.write(answer)

# Footer
st.markdown("---")
st.markdown("Thank you for visiting our Chocolate Shop Q&A! We hope to see you again soon.")
