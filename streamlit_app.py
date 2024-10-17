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
        with st.form("promotion_form", clear_on_submit=True):
            st.header("Enter Promotion Details")

            # Generate system-generated Promotion ID with prefix 'PMH'
            promotion_id = f"PMH{uuid.uuid4().hex[:8]}"

            # Collect form data
            promo_name, coupon_code = st.columns(2)
            promo_name = promo_name.text_input("Promo Name*", value="", help="Enter the name of the promotion")
            coupon_code = coupon_code.text_input("Coupon Code (if applicable)", value="")

            start_date, end_date = st.columns(2)
            start_date = start_date.date_input("Start Date*", value=datetime.now())
            end_date = end_date.date_input("End Date*", value=datetime.now())

            display_start_date, display_end_date = st.columns(2)
            display_start_date = display_start_date.date_input("Display Start Date*", value=datetime.now())
            display_end_date = display_end_date.date_input("Display End Date*", value=datetime.now())

            title, description = st.columns(2)
            title = title.text_input("Title*", value="", max_chars=60, help="Enter the title of the promotion (Maximum 60 characters)")
            description = description.text_area("Description", value="", max_chars=100, help="Enter the description of any free gift offered in the promotion (Maximum 100 characters). Example: Free tote bag with 100.00 USD purchase.")

            body_copy = st.text_area("Body Copy*", value="", help="Enter detailed text for the promotion", key='body_copy')

            cta, link = st.columns(2)
            cta = cta.text_input("CTA (Call to Action)", value="", help="Button label for the promotion")
            link = link.text_input("Link (URL)*", value="", help="URL or hyperlink associated with the CTA") if cta else ""

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

            if submitted:
                handle_submission(promotion_id, promo_name, start_date, end_date, display_start_date, display_end_date,
                                 title, body_copy, assets, terms_conditions, target_audience, store_name, promotion_type,
                                 extended_end_date, coupon_code, description, cta, link, discount_rate, applicable_products,
                                 is_finalized, activation_channel, status)

    elif choice == "Promotions List":
        # Embed Zapier Interface
        st.markdown(
            """
            <iframe src="https://interfaces.zapier.com/embed/page/cm2dc1615000d148mpumlhsyw?&allowQueryParams=true" style='max-width: 900px; width: 100%; height: 500px;'></iframe>
            """,
            unsafe_allow_html=True
        )

def display_logo():
    st.markdown(
        """
        <div style='text-align: center;'>
            <img src='https://media.us.lg.com/m/4f3e261da34f4910/original/lg_logo.svg' width='150'>
        </div>
        """, unsafe_allow_html=True
    )

def handle_submission(promotion_id, promo_name, start_date, end_date, display_start_date, display_end_date,
                      title, body_copy, assets, terms_conditions, target_audience, store_name, promotion_type,
                      extended_end_date, coupon_code, description, cta, link, discount_rate, applicable_products,
                      is_finalized, activation_channel, status):
    missing_fields = []
    if extended_end_date and extended_end_date < end_date:
        st.error("Extended End Date cannot be earlier than End Date.")
        missing_fields.append('Extended End Date (if applicable)')
    required_fields = [promo_name, start_date, end_date, display_start_date, display_end_date,
                      title, body_copy, assets, terms_conditions, target_audience, store_name, promotion_type]
    for idx, field in enumerate(required_fields):
        if not field:
            missing_fields.append(f'Required Field {idx + 1}')
    if missing_fields:
        for field in missing_fields:
            st.warning(f"Please fill out the field: {field}")
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
