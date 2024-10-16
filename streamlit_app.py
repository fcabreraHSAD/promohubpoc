import streamlit as st
import requests
from datetime import datetime

# Promotion Management Hub Streamlit App
def main():
    st.set_page_config(page_title="Promotion Management Hub", layout="wide")
    st.markdown("""
        <div style='text-align: center;'>
            <img src='https://media.us.lg.com/m/4f3e261da34f4910/original/lg_logo.svg' width='150'>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("""
        <div style='text-align: center;'>
            <img src='https://drive.google.com/uc?export=view&id=147CmaCAFLYlfgRsGYP0XN4qm2NXOD0Kp' width='150'>
        </div>
        """, unsafe_allow_html=True)
    st.title("Promotion Management Hub")
    st.write("By MarTech Solutions")
    
    # Apply theme colors as specified by user
    st.markdown(
        """
        <style>
            .stTextInput > div > input, .stTextArea > div > textarea {
                background-color: #f0ece4;
                color: #152542;
                border-radius: 5px;
                border: 1px solid #a3afc4;
                padding: 8px;
            }
            .stForm > div {
                background-color: #fcfdfe;
                padding: 20px;
                border-radius: 10px;
            }
            .stButton > button {
                background-color: #ea1917;
                color: #ffffff;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            .stButton > button:hover {
                background-color: #a60032;
            }
            .stSelectbox > div > select, .stMultiselect > div > div > select {
                background-color: #e2e7f0;
                color: #3e547c;
                border-radius: 5px;
                border: 1px solid #a3afc4;
                padding: 8px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Form to collect promotion data
    with st.form("promotion_form", clear_on_submit=True):
        st.header("Enter Promotion Details")
        import random

        # Generate system-generated Promotion ID with prefix 'PMH'
        promotion_id = f"PMH{random.randint(1000, 9999)}"
        col1, col2 = st.columns(2)
        with col1:
            promo_name = st.text_input("Promo Name*", value="", help="Enter the name of the promotion")
        with col2:
            coupon_code = st.text_input("Coupon Code (if applicable)", value="")
        col3, col4 = st.columns(2)
        with col3:
            start_date = st.date_input("Start Date*", value=datetime.now())
        with col4:
            end_date = st.date_input("End Date*", value=datetime.now())
        col5, col6 = st.columns(2)
        with col5:
            display_start_date = st.date_input("Display Start Date*", value=datetime.now())
        with col6:
            display_end_date = st.date_input("Display End Date*", value=datetime.now())
        col7, col8 = st.columns(2)
        with col7:
            title = st.text_input("Title*", value="", max_chars=60, help="Enter the title of the promotion (Maximum 60 characters)")
        with col8:
            description = st.text_area("Description", value="", max_chars=100, help="Enter the description of any free gift offered in the promotion (Maximum 100 characters). Example: Free tote bag with 100.00 USD purchase.")
        body_copy = st.text_area("Body Copy*", value="", help="Enter detailed text for the promotion", key='body_copy')
        col9, col10 = st.columns(2)
        with col9:
            cta = st.text_input("CTA (Call to Action)", value="", help="Button label for the promotion")
        with col10:
            link = st.text_input("Link (URL)*", value="", help="URL or hyperlink associated with the CTA") if cta else ""
        assets = st.text_input("Assets*", value="", help="Links to promotional assets like images or videos", key='assets')
        terms_conditions = st.text_input("Terms & Conditions*", value="", key='terms_conditions')
        target_audience = st.multiselect("Target Audience*", ["All Customers", "New Customers", "Returning Customers"], help="Select the target audience for the promotion")
        discount_rate = st.text_input("Discount Rate (if applicable)", value="")
        status = "Upcoming"  # Default status
        store_name = st.multiselect("Store Name*", ["OBS", "EOS", "PM", "ThinQ"], help="Select applicable stores for the promotion")
        applicable_products = st.multiselect("Applicable Products or Categories", ["Fetch product data from the shared Google Sheet"], help="Select applicable products or categories for the promotion")
        promotion_type = st.selectbox("Promotion Type*", [
            "Product package Rebate", "Product package instant discount", "Package with variable discount", "Single product rebate",
            "Single product instant discount", "Product bundle", "Value-add", "Cross-sells", "Upsell", "Add-ons", "Buy one, get one free",
            "Buy more, save more", "Promo code", "Subscriptions", "Store Credit", "Rewards points"
        ])
        is_finalized = st.checkbox("Is Finalized*", value=False, help="Check if the promotion details are finalized")
        activation_channel = st.multiselect("Activation Channel", [
            "Email Marketing", "Social Media Platforms", "SMS/Text Message", "Affiliate Partners", "Display",
            "Onsite via CMS", "Onsite via Personalization / AB Testing Tool", "PLA", "SEM"
        ])
        extended_end_date = st.date_input("Extended End Date (if applicable)", value=None)
        
        # Form submission button
        submitted = st.form_submit_button("Submit Promotion")
        
        # Ensure all required fields are filled out before submission
        if submitted:
            missing_fields = []
            if extended_end_date and extended_end_date < end_date:
                st.error("Extended End Date cannot be earlier than End Date.")
                missing_fields.append('Extended End Date (if applicable)')
            if not promo_name: missing_fields.append('Promo Name*')
            if not start_date: missing_fields.append('Start Date*')
            if not end_date: missing_fields.append('End Date*')
            if not display_start_date: missing_fields.append('Display Start Date*')
            if not display_end_date: missing_fields.append('Display End Date*')
            if not title: missing_fields.append('Title*')
            if not body_copy: missing_fields.append('Body Copy*')
            if not assets: missing_fields.append('Assets*')
            if not terms_conditions: missing_fields.append('Terms & Conditions*')
            if not target_audience: missing_fields.append('Target Audience*')
            if not store_name: missing_fields.append('Store Name*')
            if not promotion_type: missing_fields.append('Promotion Type*')
            if missing_fields:
                for field in missing_fields:
                    st.warning(f"Please fill out the field: {field}")
                st.error("Please fill out all required fields before submitting the form.")
                st.error("Please fill out all required fields before submitting the form.")
            else:
                # Prepare the data for webhook submission
                promotion_data = {
                    "PromotionID": promotion_id,
                    "PromoName": promo_name,
                    "CouponCode": coupon_code,
                    "StartDate": start_date.strftime("%m/%d/%Y"),
                    "EndDate": end_date.strftime("%m/%d/%Y"),
                    "DisplayStartDate": display_start_date.strftime("%m/%d/%Y"),
                    "DisplayEndDate": display_end_date.strftime("%m/%d/%Y"),
                    "Description": description,
                    "Title": title,
                    "BodyCopy": body_copy,
                    "CTA": cta,
                    "Link": link,
                    "Assets": assets,
                    "TermsConditions": terms_conditions,
                    "TargetAudience": target_audience,
                    "DiscountRate": discount_rate,
                    "Status": status,
                    "StoreName": store_name,
                    "ApplicableProducts": applicable_products,
                    "PromotionType": promotion_type,
                    "IsFinalized": is_finalized,
                    "ActivationChannel": activation_channel,
                    "ExtendedEndDate": extended_end_date.strftime("%m/%d/%Y") if extended_end_date else ""
                }
                
                # Send data to Zapier webhook
                webhook_url = "https://hooks.zapier.com/hooks/catch/9480052/2197ir5/"
                response = requests.post(webhook_url, json=promotion_data)
                
                # Handle the response
                if response.status_code == 200:
                    st.success("Promotion details successfully submitted!")
                else:
                    st.error(f"Failed to submit promotion details. Status code: {response.status_code}")

if __name__ == "__main__":
    main()
