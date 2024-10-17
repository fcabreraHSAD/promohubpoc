import streamlit as st
import requests
from datetime import datetime
import uuid

# Promotion Management Hub Streamlit App

def main():
    st.set_page_config(page_title="Promotion Management Hub", layout="wide")

    # Create a menu with two pages
    menu = ["Promotion Form", "Promotions List"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Promotion Form":
        # Set page title and logo
        display_logo()
        st.title("Promotion Management Hub")
        st.write("By MarTech Solutions")

        # Form to collect promotion data
        with st.form("promotion_form", clear_on_submit=False):
            st.header("Enter Promotion Details")

            # Generate system-generated Promotion ID with prefix 'PMH'
            promotion_id = f"PMH{uuid.uuid4().int % 10000000:07d}"

            # Collect form data
            promo_name, coupon_code = st.columns(2)
            promo_name = promo_name.text_input("Promo Name*", value=st.session_state.get("promo_name", ""), help="Enter the name of the promotion")
            coupon_code = coupon_code.text_input("Coupon Code (if applicable)", value=st.session_state.get("coupon_code", ""))

            start_date, end_date = st.columns(2)
            start_date = start_date.date_input("Start Date*", value=datetime.now())
            end_date = end_date.date_input("End Date*", value=datetime.now())

            display_start_date, display_end_date = st.columns(2)
            display_start_date = display_start_date.date_input("Display Start Date*", value=datetime.now())
            display_end_date = display_end_date.date_input("Display End Date*", value=datetime.now())

            title, description = st.columns(2)
            title = title.text_input("Title*", value=st.session_state.get("title", ""), max_chars=60, help="Enter the title of the promotion (Maximum 60 characters)")
            description = description.text_area("Description", value=st.session_state.get("description", ""), max_chars=100, help="Enter the description of any free gift offered in the promotion (Maximum 100 characters). Example: Free tote bag with 100.00 USD purchase.")

            body_copy = st.text_area("Body Copy*", value=st.session_state.get("body_copy", ""), help="Enter detailed text for the promotion", key='body_copy')

            link, cta = st.columns(2)
            link = link.text_input("Link (URL)*", value=st.session_state.get("link", ""), help="URL or hyperlink associated with the CTA")
            cta = cta.text_input("CTA (Call to Action)", value=st.session_state.get("cta", ""), help="Button label for the promotion")

            assets = st.text_input("Assets*", value=st.session_state.get("assets", ""), help="Links to promotional assets like images or videos", key='assets')
            terms_conditions = st.text_input("Terms & Conditions*", value=st.session_state.get("terms_conditions", ""), key='terms_conditions')
            target_audience = st.multiselect("Target Audience*", ["All Customers", "New Customers", "Returning Customers"], help="Select the target audience for the promotion", default=st.session_state.get("target_audience", []))
            discount_rate = st.number_input("Discount Rate (if applicable)", min_value=0.0, step=0.1, value=st.session_state.get("discount_rate", 0.0))
            status = "Upcoming"  # Default status
            store_name = st.multiselect("Store Name*", ["OBS", "EOS", "PM", "ThinQ"], help="Select applicable stores for the promotion", default=st.session_state.get("store_name", []))
            applicable_products = st.multiselect("Applicable Products or Categories", ["Fetch product data from the shared Google Sheet"], help="Select applicable products or categories for the promotion", default=st.session_state.get("applicable_products", []))
            promotion_type = st.selectbox("Promotion Type*", [
                "Product package Rebate", "Product package instant discount", "Package with variable discount", "Single product rebate",
                "Single product instant discount", "Product bundle", "Value-add", "Cross-sells", "Upsell", "Add-ons", "Buy one, get one free",
                "Buy more, save more", "Promo code", "Subscriptions", "Store Credit", "Rewards points"
            ], index=[
                "Product package Rebate", "Product package instant discount", "Package with variable discount", "Single product rebate",
                "Single product instant discount", "Product bundle", "Value-add", "Cross-sells", "Upsell", "Add-ons", "Buy one, get one free",
                "Buy more, save more", "Promo code", "Subscriptions", "Store Credit", "Rewards points"
            ].index(st.session_state.get("promotion_type", "Single product rebate")))
            is_finalized = st.checkbox("Is Finalized*", value=st.session_state.get("is_finalized", False), help="Check if the promotion details are finalized")
            activation_channel = st.multiselect("Activation Channel", [
                "Email Marketing", "Social Media Platforms", "SMS/Text Message", "Affiliate Partners", "Display",
                "Onsite via CMS", "Onsite via Personalization / AB Testing Tool", "PLA", "SEM"
            ], default=st.session_state.get("activation_channel", []))
            extended_end_date = st.date_input("Extended End Date (if applicable)", value=None)

            # Button to pre-populate form data for testing
                    st.experimental_rerun()
