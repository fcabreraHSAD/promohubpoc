import streamlit as st
import requests
from datetime import datetime

# Promotion Management Hub Streamlit App
def main():
    st.set_page_config(page_title="Promotion Management Hub", layout="wide")
    st.title("Promotion Management Hub")
    st.write("By MarTech Solutions")
    
    # Add support for dark and light mode themes
    st.markdown(
        """
        <style>
            @media (prefers-color-scheme: dark) {
                .stTextInput > div > input, .stTextArea > div > textarea {
                    background-color: #333;
                    color: #f0ece4;
                    border-radius: 5px;
                    border: 1px solid #a3afc4;
                    padding: 8px;
                }
                .stForm > div {
                    background-color: #2c2c2c;
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
            }
            @media (prefers-color-scheme: light) {
                .stTextInput > div > input, .stTextArea > div > textarea {
                    border-radius: 5px;
                    border: 1px solid #a3afc4;
                    padding: 8px;
                }
                .stForm > div {
                    background-color: #f0ece4;
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
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Form to collect promotion data
    with st.form("promotion_form"):
        st.header("Enter Promotion Details")
        promotion_id = st.text_input("Promotion ID (Primary Key)*", value="", help="Enter a unique identifier for the promotion")
        promo_name = st.text_input("Promo Name*", value="", help="Enter the name of the promotion")
        coupon_code = st.text_input("Coupon Code (if applicable)", value="")
        start_date = st.date_input("Start Date*", value=datetime.now())
        end_date = st.date_input("End Date*", value=datetime.now())
        display_start_date = st.date_input("Display Start Date*", value=datetime.now())
        display_end_date = st.date_input("Display End Date*", value=datetime.now())
        description = st.text_area("Description", value="", help="Enter a brief overview of what the promotion entails")
        title = st.text_input("Title*", value="", help="Enter the title of the promotion")
        body_copy = st.text_area("Body Copy*", value="", help="Enter detailed text for the promotion")
        cta = st.text_input("CTA (Call to Action)", value="", help="Button label for the promotion")
        link = st.text_input("Link (URL)*", value="", help="URL or hyperlink associated with the CTA") if cta else ""
        assets = st.text_input("Assets*", value="", help="Links to promotional assets like images or videos")
        terms_conditions = st.text_input("Terms & Conditions*", value="")
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
            if not (promotion_id and promo_name and start_date and end_date and display_start_date and display_end_date and title and body_copy and assets and terms_conditions and target_audience and store_name and promotion_type):
                st.error("Please fill out all required fields before submitting the form.")
            else:
                # Prepare the data for webhook submission
                promotion_data = {
                    "PromotionID": promotion_id,
                    "PromoName": promo_name,
                    "CouponCode": coupon_code,
                    "StartDate": start_date.strftime("%Y-%m-%d"),
                    "EndDate": end_date.strftime("%Y-%m-%d"),
                    "DisplayStartDate": display_start_date.strftime("%Y-%m-%d"),
                    "DisplayEndDate": display_end_date.strftime("%Y-%m-%d"),
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
                    "ExtendedEndDate": extended_end_date.strftime("%Y-%m-%d") if extended_end_date else ""
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
