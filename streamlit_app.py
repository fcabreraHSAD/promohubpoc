import streamlit as st
import requests
from datetime import datetime
import uuid

# Promotion Management Hub Streamlit App

def main():
    st.set_page_config(page_title="Promotion Management Hub", layout="wide")

    # Create a menu with two pages
    menu = ["Promotion Form", "Promotions List"]
    choice = st.sidebar.selectbox("Menu", menu, index=menu.index(st.session_state.get("menu", "Promotion Form")))
    if choice == "Promotions List" and st.session_state.get("menu") == "Promotion Form":
        st.session_state.menu = "Promotion List"

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

            # Form submission button
            submitted = st.form_submit_button("Submit Promotion")

            if submitted:
                missing_fields = validate_fields(
                    promo_name, start_date, end_date, display_start_date, display_end_date,
                    title, body_copy, assets, terms_conditions, target_audience, store_name, promotion_type, extended_end_date
                )
                if missing_fields:
                    for field in missing_fields:
                        st.warning(f"Please fill out the field: {field}")
                    st.error("Please fill out all required fields before submitting the form.")
                else:
                    handle_submission(promotion_id, promo_name, start_date, end_date, display_start_date, display_end_date,
                                     title, body_copy, assets, terms_conditions, target_audience, store_name, promotion_type,
                                     extended_end_date, coupon_code, description, cta, link, discount_rate, applicable_products,
                                     is_finalized, activation_channel, status)
                    st.success("Promotion details successfully submitted! Redirecting to Promotions List...")
                    st.session_state.menu = "Promotions List"
                    st.write("Redirecting... Please use the sidebar to navigate.")

        # Link to pre-fill the form for testing
        st.markdown(
            """
            <a href="?promo_name=Test+Promo&coupon_code=TEST100&title=Test+Title&description=Test+Description&body_copy=This+is+a+test+body+copy+for+the+promotion.&link=https%3A%2F%2Fwww.example.com&cta=Shop+Now&assets=https%3A%2F%2Fwww.example.com%2Fasset.jpg&terms_conditions=Terms+and+conditions+apply.&target_audience=All+Customers&discount_rate=10.0&store_name=OBS&store_name=PM&promotion_type=Single+product+instant+discount&is_finalized=True" target="_self">Pre-fill Form for Testing</a>
            """,
            unsafe_allow_html=True
        )

    elif choice == "Promotions List":
        # Embed Zapier Interface with optimized size and placement
        st.markdown(
            """
            <div style='display: flex; justify-content: center; margin-top: 20px;'>
                <iframe src="https://interfaces.zapier.com/embed/page/cm2dc1615000d148mpumlhsyw?noBackground=true&allowQueryParams=true" style='max-width: 1200px; width: 95%; height: 700px; border: none;'></iframe>
            </div>
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

def validate_fields(promo_name, start_date, end_date, display_start_date, display_end_date,
                    title, body_copy, assets, terms_conditions, target_audience, store_name, promotion_type, extended_end_date):
    missing_fields = []
    if not promo_name:
        missing_fields.append('Promo Name')
    if not start_date:
        missing_fields.append('Start Date')
    if not end_date:
        missing_fields.append('End Date')
    if not display_start_date:
        missing_fields.append('Display Start Date')
    if not display_end_date:
        missing_fields.append('Display End Date')
    if not title:
        missing_fields.append('Title')
    if not body_copy:
        missing_fields.append('Body Copy')
    if not assets:
        missing_fields.append('Assets')
    if not terms_conditions:
        missing_fields.append('Terms & Conditions')
    if not target_audience:
        missing_fields.append('Target Audience')
    if not store_name:
        missing_fields.append('Store Name')
    if not promotion_type:
        missing_fields.append('Promotion Type')
    if extended_end_date and extended_end_date < end_date:
        missing_fields.append('Extended End Date (cannot be earlier than End Date)')
    return missing_fields

def handle_submission(promotion_id, promo_name, start_date, end_date, display_start_date, display_end_date,
                      title, body_copy, assets, terms_conditions, target_audience, store_name, promotion_type,
                      extended_end_date, coupon_code, description, cta, link, discount_rate, applicable_products,
                      is_finalized, activation_channel, status):
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
