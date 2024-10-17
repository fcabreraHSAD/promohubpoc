# promohubpoc# Promotion Management Hub Streamlit App - README

## Overview

The **Promotion Management Hub** is a web application built using Streamlit, designed to manage and streamline promotional activities. The app provides two main functionalities:

1. **Promotion Form**: A form for entering new promotion details.
2. **Promotions List**: A list of previously created promotions displayed via an embedded Zapier interface.

The app is intended to assist marketing and promotion teams in organizing promotions effectively, tracking essential details, and managing target audiences and channels.

## Installation and Setup

### Prerequisites
- Python 3.7 or higher
- Required Python libraries: `streamlit`, `requests`

You can install the required libraries with:
```sh
pip install streamlit requests
```

### Running the Application

To start the Promotion Management Hub, use the following command:
```sh
streamlit run app.py
```
Replace `app.py` with the name of your script if it differs.

## Features

### Promotion Form

The **Promotion Form** allows users to enter the details of a new promotion. It includes various fields for entering relevant information, such as:

- **Promotion ID**: System-generated with prefix "PMH".
- **Promo Name**: Name of the promotion.
- **Coupon Code**: Optional coupon code for the promotion.
- **Start Date/End Date**: Start and end dates for the promotion.
- **Display Start Date/End Date**: Dates when the promotion will be visible to customers.
- **Title and Description**: Title and a brief description of the promotion.
- **Body Copy**: Detailed description of the promotion.
- **CTA (Call to Action)**: Button label for the promotion.
- **Link**: URL for the promotion (associated with the CTA).
- **Assets**: Links to promotional assets like images or videos.
- **Terms & Conditions**: Terms and conditions for the promotion.
- **Target Audience**: Segment of the audience that the promotion is targeted at.
- **Discount Rate**: Optional discount percentage for the promotion.
- **Store Name**: Stores where the promotion will be available.
- **Applicable Products or Categories**: Products or categories applicable for the promotion.
- **Promotion Type**: Type of promotion (e.g., rebate, bundle, value-add).
- **Finalized Status**: Indicates whether the promotion is finalized.
- **Activation Channel**: Marketing channels used for promotion (e.g., email, social media).
- **Extended End Date**: Optional extended end date for the promotion.

After entering the details, users can submit the form. Upon submission, the details are validated and sent to a Zapier webhook for further processing.

### Promotions List

The **Promotions List** page embeds a Zapier interface to display a list of created promotions. The promotions list is displayed in an iframe for easy viewing and management.

## Code Walkthrough

### Main Functions

1. **main()**: The main function sets up the Streamlit page configuration and handles the logic for displaying either the Promotion Form or the Promotions List, based on user selection.

2. **display_logo()**: Displays the LG logo at the top of the page.

3. **handle_submission()**: Handles the form submission by validating required fields, preparing the data, and sending it to a Zapier webhook. The function displays success or error messages based on the response from the webhook.

### Promotion Form Submission

- **Validation**: Before submission, required fields are checked for completeness. The extended end date is also validated to ensure it is not earlier than the original end date.
- **Webhook Integration**: Promotion data is sent to a pre-configured Zapier webhook URL for further processing.

## How to Use

1. **Navigate to the Promotion Form** to enter details for a new promotion.
2. **Fill out the form** with all required details, including promo name, start and end dates, applicable stores, and promotion type.
3. **Submit the form** once all fields are completed. The details will be validated and submitted to the Zapier webhook.
4. **View the Promotions List** to see previously created promotions.

## Customization

- **Webhook URL**: Update the `webhook_url` in the `handle_submission()` function to point to your desired endpoint.
- **Logo and Branding**: The `display_logo()` function can be customized to display your organization's logo.

## Error Handling

- **Form Submission Errors**: If required fields are missing or the extended end date is invalid, an error message is displayed, and the user is prompted to correct the input.
- **Webhook Errors**: If the webhook submission fails, the app will display an error message with the response status code.

## Dependencies
- **Streamlit**: Used to create the interactive web application interface.
- **Requests**: Used to send HTTP POST requests to the Zapier webhook.
- **Datetime**: Used to manage date inputs.
- **UUID**: Used to generate unique promotion IDs.

## Contact
For further questions or assistance, please contact MarTech Solutions.

## License
This project is licensed under the MIT License.

