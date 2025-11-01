import streamlit as st

from helper_functions.create_df import create_df
from helper_functions.generateCustomerID import generateCustomerID
from helper_functions.write_to_csv import write_to_csv
from helper_functions.predict_churn import predict_churn
#  streamlit run customer_churn_app/app.py


# i. Values are unique to each customer. Data type: Object
# # 7590-VHVEG
if "customer_id" not in st.session_state:
    st.session_state.customer_id = generateCustomerID()
    # customer_id = generateCustomerID()
    st.subheader(f"Customer ID: {st.session_state.customer_id}")
else:
    st.subheader(f"Customer ID: {st.session_state.customer_id}")

# Styling the webpage
st.title("📊 Customer Churn Prediction")
st.write("Enter customer details to predict churn risk")

# Main tabs for organisation
tab1, tab2, tab3 = st.tabs(["Demographics", "Services", "Billing"])

with tab1:
    tab1_col1, tab1_col2 = st.columns(2)
    with tab1_col1:
        # ii. Gender: Values: [‘Female’, ‘Male’]. Data type: Object
        gender = st.radio("1) What is the customers gender?", ['Female', 'Male'], index=None)

        st.text("")  # Adds a single empty line
        st.text("")  # Adds another empty line

        # iii. Senior Citizen: Indicates if a customer is 65 or older. Values: [‘Yes’, ‘No’]. Data type: Integer
        age = st.slider("2) How old is the customer?", 0, 120, 30)
        senior_citizen = 1 if age >= 65 else 0

        st.text("") # Adds a single empty line
        st.text("") # Adds another empty line

    with tab1_col2:
        # iv. Partner: Values: [‘Yes’, ‘No’]. Data type: Object
        partner = st.selectbox("3) Does this customer have a partner?", ['Yes', 'No'], index=None)

        st.text("")  # Adds a single empty line
        st.text("")  # Adds another empty line

        # v. Dependents: Values: [‘Yes’, ‘No’]. Data type: Object
        dependents = st.selectbox("4) Do they have any dependents: children, parents, grandparents, etc?",
                                  ['Yes', 'No'], index=None)

        st.text("")  # Adds a single empty line
        st.text("")  # Adds another empty line

with tab2:
    # vi. Phone Service: Values: [‘Yes’, ‘No’]. Data type: Object
    phone_service = st.radio("5) Do they subscribe to a home phone service with the company?",
                             ['Yes', 'No'], index=None)

    st.text("")  # Adds a single empty line
    st.text("")  # Adds another empty line

    # vii. Internet Service: Values: [‘DSL’, ‘Fibre Optic’, ‘No’]. Data type: Object
    internet_service = st.radio("6) Which of these internet services do they subscribe to?",
                                ['DSL', 'Fiber optic', 'No'], index=None)

    st.text("")  # Adds a single empty line
    st.text("")  # Adds another empty line

    with st.expander("Additional Services"):
        # viii. Multiple Lines: Values: [‘Yes’, ‘No’, ‘No Phone Service’]. Data type: Object
        multiple_lines = st.radio("7) Do they subscribe to multiple telephone lines with the company?",
                                  ['Yes', 'No', 'No phone service'], index=None)

        st.text("") # Adds a single empty line
        st.text("") # Adds another empty line

        # Internet-dependent services
        if internet_service is None or internet_service == 'No':
            # ix. Online Security: Values: [‘Yes’, ‘No’, ‘No Internet Service’]. Data type: Object
            online_security = st.radio("8) Is the customer suscribed to an additional online security"
                                       " service provided by the company?",
                                       ['No internet service'], disabled=True)

            st.text("") # Adds a single empty line
            st.text("") # Adds another empty line

            # x. Online Backup: Values: [‘Yes’, ‘No’, ‘No Internet Service’]. Data type: Object
            online_backup = st.radio("9) Is the customer suscribed to an additional online backup service"
                                     " provided by the company?",
                                     ['No internet service'], disabled=True)

            st.text("") # Adds a single empty line
            st.text("") # Adds another empty line

            # xi. Device Protection: Values: [‘Yes’, ‘No’, ‘No Internet Service’]. Data type: Object
            device_protection = st.radio("10) Is the customer subscribed to an additional device protection"
                                         " plan for their internet equipment provided by the company?",
                                         ['No internet service'], disabled=True)

            st.text("") # Adds a single empty line
            st.text("") # Adds another empty line

            # xii. Tech Support: Values: [‘Yes’, ‘No’, ‘No Internet Service’]. Data type: Object
            tech_support = st.radio("11) Is the customer subscribed to an additional technical support"
                                    " plan from the company?", ['No internet service'], disabled=True)

            st.text("") # Adds a single empty line
            st.text("") # Adds another empty line

            # xiii. Streaming TV:  Values: [‘Yes’, ‘No’, ‘No Internet Service’]. Data type: Object
            streaming_tv = st.radio("12) Does the customer use their internet service to stream television"
                                    " programming from a third-party provider?",
                                    ['No internet service'], disabled=True)

            st.text("") # Adds a single empty line
            st.text("") # Adds another empty line

            # xiv. Streaming Movies: Values: [‘Yes’, ‘No’, ‘No Internet Service’]. Data type: Object
            streaming_movies= st.radio("13) Does the customer use their internet service to stream movies "
                                       "from a third-party provider?", ['No internet service'], disabled=True)

            st.text("") # Adds a single empty line
            st.text("") # Adds another empty line
        else:
            # ix. Online Security: Values: [‘Yes’, ‘No’, ‘No Internet Service’]. Data type: Object
            online_security = st.radio("8) Is the customer suscribed to an additional online security"
                                       " service provided by the company?",
                                       ['Yes', 'No', 'No internet service'], index=None)

            st.text("")  # Adds a single empty line
            st.text("")  # Adds another empty line

            # x. Online Backup: Values: [‘Yes’, ‘No’, ‘No Internet Service’]. Data type: Object
            online_backup = st.radio("9) Is the customer suscribed to an additional online backup service"
                                     " provided by the company?",
                                     ['Yes', 'No', 'No internet service'], index=None)

            st.text("")  # Adds a single empty line
            st.text("")  # Adds another empty line

            # xi. Device Protection: Values: [‘Yes’, ‘No’, ‘No Internet Service’]. Data type: Object
            device_protection = st.radio("10) Is the customer subscribed to an additional device protection"
                                         " plan for their internet equipment provided by the company?",
                                         ['Yes', 'No', 'No internet service'], index=None)

            st.text("")  # Adds a single empty line
            st.text("")  # Adds another empty line

            # xii. Tech Support: Values: [‘Yes’, ‘No’, ‘No Internet Service’]. Data type: Object
            tech_support = st.radio("11) Is the customer subscribed to an additional technical support"
                                    " plan from the company?", ['Yes', 'No', 'No internet service'], index=None)

            st.text("")  # Adds a single empty line
            st.text("")  # Adds another empty line

            # xiii. Streaming TV:  Values: [‘Yes’, ‘No’, ‘No Internet Service’]. Data type: Object
            streaming_tv = st.radio("12) Does the customer use their internet service to stream television"
                                    " programming from a third-party provider?",
                                    ['Yes', 'No', 'No internet service'], index=None)

            st.text("")  # Adds a single empty line
            st.text("")  # Adds another empty line

            # xiv. Streaming Movies: Values: [‘Yes’, ‘No’, ‘No Internet Service’]. Data type: Object
            streaming_movies = st.radio("13) Does the customer use their internet service to stream movies "
                                        "from a third-party provider?",
                                        ['Yes', 'No', 'No internet service'], index=None)

            st.text("") # Adds a single empty line
            st.text("") # Adds another empty line

with (tab3):
    # xv. Tenure: How many months has the customer been with the company by the end of the third quarter?
    # Values: Values range from [0 - 72]. Data type: Integer
    tenure = st.slider("5) Please input the total number of months that a customer has been with the "
                             "company by the end of the third quarter.", 0, 72, 12)

    st.text("") # Adds a single empty line
    st.text("") # Adds another empty line

    # xvi. Contract: Values: [‘Month-to-Month’, ‘One year’, ‘Two year’]. Data type: Object
    contract = st.selectbox("15) Which contract type is the customer subscribed to?",
                        ['Month-to-month', 'One year', 'Two year'], index=None)

    st.text("") # Adds a single empty line
    st.text("") # Adds another empty line

    # xvii. Paperless Billing: Values: [‘Yes’, ‘No’]. Data type: Object
    paperless_billing = st.radio("16) Has the customer chosen paperless billing?",
                                 ['Yes', 'No'], index=None)

    st.text("") # Adds a single empty line
    st.text("") # Adds another empty line

    # xviii. Payment Method: Values: [‘Electronic check’, ‘Mailed check’, ‘Bank transfer (automatic)’,
    # ‘Credit card (automatic)’]. Data type: Object
    payment_method = st.selectbox("17) How does the customer pay their bill?",
                              ['Electronic check', 'Mailed check', 'Bank transfer (automatic)',
                               'Credit card (automatic)'], index=None)

    st.text("") # Adds a single empty line
    st.text("") # Adds another empty line

    # xix. Monthly Charge: Values range from [18.25 – 118.75]. Data type: Float
    monthly_charges = st.number_input("18) What is the customer's total monthly charge for"
                                      " all their services from the company?", min_value=18.25, max_value=120.00,
                                      value=18.25, step=0.25, format="%.2f")

    if monthly_charges == 0: # range validation for monthly_charges
        st.warning("Monthly charges cannot be zero.")

    st.text("") # Adds a single empty line
    st.text("") # Adds another empty line

    # xx. Total Charge: Values range from [18.8 – 8684.8]. Data type: Object
    if monthly_charges is not None and tenure is not None:
        total_charges = monthly_charges * tenure
        # st.info(f"The customers estimated total charge at the end of the third quarter is: ${total_charges:.2f}")
        st.number_input("The customers estimated total charge at the end of the third quarter is:",
                        value=total_charges, format="%.2f", disabled=True)

    # # xx. Total Charge: Calculated as monthly_charges × tenure
    # if monthly_charges is not None and tenure is not None:
    #     total_charges = monthly_charges * tenure
    #     st.write(f"**19) Estimated Total Charges:** ${total_charges:.2f}")
    # else:
    #     total_charges = 0.00
    #     st.write("**19) Total Charges:** Enter monthly charges and tenure to calculate")

    st.text("") # Adds a single empty line
    st.text("") # Adds another empty line

    # xxi. Churn: Values: [‘Yes’, ‘No’]. Data type: Object
    # * Display outputs such as:
    #     * Probability of churn (e.g., “There’s a 72% chance this customer will churn”)
    #     * Model’s classification (e.g., “Likely to churn” / “Loyal customer”)
    #     * Possibly an explanation (like feature importance or risk drivers).
    if st.button("Predict Churn"):
        # prediction logic will go here

        # For optional field, provide a default if None
        multiple_lines = multiple_lines if multiple_lines is not None else ('No Phone Service' if phone_service == 'No'
                                                                            else 'No')
        online_security = online_security if online_security is not None else 'No'
        online_backup = online_backup if online_backup is not None else 'No'
        device_protection = device_protection if device_protection is not None else 'No'
        tech_support = tech_support if tech_support is not None else 'No'
        streaming_tv = streaming_tv if streaming_tv is not None else 'No'
        streaming_movies = streaming_movies if streaming_movies is not None else 'No'
        tenure = tenure if tenure is not None else 0
        monthly_charges = monthly_charges if monthly_charges is not None else 0.00
        total_charges = total_charges if total_charges is not None else 0.00

        # Check if all required fields are filled
        required_fields = {
            'Gender': gender,
            'Senior Citizen': senior_citizen,
            'Partner': partner,
            'Dependents': dependents,
            'Phone Service': phone_service,
            'Internet Service': internet_service,
            'Contract': contract,
            'Paperless Billing': paperless_billing,
            'Payment Method': payment_method
        }
        # Find missing fields
        missing_fields = [field for field, value in required_fields.items() if value is None]

        if missing_fields:
            st.error(f"❌ Please fill in the following required field(s): {', '.join(missing_fields)}")
        else:
            # All required field are filled, proceed with prediction
            st.write("Running churn prediction...")

            df = create_df(st.session_state.customer_id, gender, senior_citizen, partner, dependents, tenure, phone_service,
                           multiple_lines, internet_service, online_security, online_backup, device_protection,
                           tech_support, streaming_tv, streaming_movies, contract, paperless_billing, payment_method,
                           monthly_charges, total_charges)
            write_to_csv(df)


            st.success("✅ Customer data saved successfully!")

            try:
                churn_label = predict_churn(df)

                prob = churn_label[0][0]
                pred = churn_label[1][0]

                st.metric("Churn probability", f"{prob*100:.2f}%")

                if pred == 1:
                    st.error("🚨Customer is **likely to churn**")
                else:
                    st.success(" ✅ Customer is loyal")

            except Exception as e:
                st.error(f"⚠️Prediction failed: {e}")


