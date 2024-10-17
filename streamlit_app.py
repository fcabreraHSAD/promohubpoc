import streamlit as st
import requests
from datetime import datetime
import uuid

# Promotion Management Hub Streamlit App

def main():
    st.set_page_config(page_title="Promotion Management Hub", layout="wide")

    # Initialize session state for 'menu' and 'submitted'
    if 'menu' not in st.session_state:
        st.session_state['menu'] = "Promotion Form"
    if 'submitted' not in st.session_state:
        st.session_state['submitted'] = False

    # Create a menu with two pages
    menu = ["Promotion Form", "Promotions List"]
    choice = st.sidebar.selectbox("Menu", menu, index=menu.index(st.session_state['menu']))

    # If form was successfully submitted, redirect to Promotions List
    if st.session_state['submitted']:
        st.session_state['menu'] = "Promotions List"
        st.experimental_rerun()

    # Handle the different page views
    if choice == "Promotion Form":
        display_promotion_form()
    elif choice == "Promotions List":
        display_promotions_list()

def display_promotion_form():
    # Set page title and logo
    display_logo()
    st.title("Promotion Management Hub")
    st.write("By MarTech Solutions")

    # Button to pre-fill the form for testing purposes
    if st.button("Pre-fill Form for Testing"):
        st.session_state.update({
            "promo_name": "Test Promo",
            "coupon_code": "TEST100",
            "title": "Test Title",
            "description": "Test Description",
            "body_copy": "This is a test body copy for the promotion.",
            "link": "https://www.example.com",
            "cta": "Shop Now",
            "assets": "https://www.example.com/asset.jpg",
            "terms_conditions": "Terms and conditions apply.",
            "target_audience": ["All Customers"],
            "discount_rate": 10.0,
            "store_name": ["OBS", "PM"],
            "applicable_products": ["Fetch product data from the shared Google Sheet"],
            "promotion_type": "Single product instant discount",
            "is_finalized": True,
            "activation_channel": ["Social Media Platforms"]
        })

    # Form to collect promotion data
    with st.form("promotion_form", clear_on_submit=False):
        st.header("Enter Promotion Details")

        # Generate system-generated Promotion ID with prefix 'PMH'
        promotion_id = f"PMH{uuid.uuid4().int % 10000000:07d}"

        # Collect form data (similar to what you already have)
        promo_name = st.text_input("Promo Name*", value=st.session_state.get("promo_name", ""))
        # (other form fields...)

        # Form submission button
        submitted = st.form_submit_button("Submit Promotion")

        if submitted:
            missing_fields = validate_fields(promo_name)  # Assuming validate_fields checks necessary fields
            if missing_fields:
                for field in missing_fields:
                    st.warning(f"Please fill out the field: {field}")
            else:
                handle_submission(promotion_id, promo_name)
                st.session_state['submitted'] = True  # Mark form as submitted
                st.experimental_rerun()  # Rerun to redirect to Promotions List

def display_promotions_list():
    # Show your promotions list content
    st.markdown("""
    <div style='display: flex; justify-content: center; margin-top: 20px;'>
        <iframe src="https://interfaces.zapier.com/embed/page/cm2dc1615000d148mpumlhsyw?noBackground=true&allowQueryParams=true" style='max-width: 1200px; width: 95%; height: 700px; border: none;'></iframe>
    </div>
    """, unsafe_allow_html=True)

def display_logo():
    st.markdown("""
    <div style='text-align: center;'>
        <img src='https://media.us.lg.com/m/4f3e261da34f4910/original/lg_logo.svg' width='150'>
    </div>
    """, unsafe_allow_html=True)

def validate_fields(promo_name):
    missing_fields = []
    if not promo_name:
        missing_fields.append('Promo Name')
    # (other field validations...)
    return missing_fields

def handle_submission(promotion_id, promo_name):
    # Prepare data for webhook submission
    promotion_data = {
        "PromotionID": promotion_id,
        "PromoName": promo_name,
        # (other form fields...)
    }

    # Send data to Zapier webhook
    webhook_url = "https://hooks.zapier.com/hooks/catch/9480052/2197ir5/"
    response = requests.post(webhook_url, json=promotion_data)

    if response.status_code == 200:
        st.success("Promotion details successfully submitted!")
    else:
        st.error(f"Failed to submit promotion details. Status code: {response.status_code}")

if __name__ == "__main__":
    main()
