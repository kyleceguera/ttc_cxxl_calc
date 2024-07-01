#still a WIP

import streamlit as st
import json
from datetime import datetime, timedelta

today = datetime.today().date()

# # Load the JSON file
# with open('trip_names.json', 'r') as file:
#     tours = json.load(file)

# # Extract the tour names for the dropdown options
# tour_names = sorted([tour['name'] for tour in tours])

# # Add a blank option at the beginning
# tour_names.insert(0, '')

# Streamlit app
st.set_page_config(page_title='Input Relevant Information', page_icon='dollar', layout="centered", initial_sidebar_state="auto", menu_items=None)
st.title("TTC CANCELLATION CALCULATOR")


def calc_refund(amount_paid, claim_amount):
    return round(amount_paid - claim_amount,2)

def deposit_amount(x):
    if x ==2:
        return 350
    else:
        return 200

amount_paid = st.number_input("Amount Paid for this particular passenger:")
cancellation_tier = st.selectbox('Cancellation Tier Level', list(range(1,3)))
deposit_amount = deposit_amount(cancellation_tier)
deposit_amount = st.write(f"Deposit Amount: ${deposit_amount}")
first_departure_date = st.date_input(
'First Departure Date on Booking', 
format="YYYY-MM-DD",
help="Date should be entered as YYYY-MM-DD", 
min_value=today)
days_to_departure = (first_departure_date - today).days
if cancellation_tier == 1:
    final_pmt_date = first_departure_date - timedelta(60)
else:
    final_pmt_date = first_departure_date - timedelta(90)
st.markdown(f"Days to departure: {days_to_departure}")
st.write(f"Final Payment Due Date: :green[{final_pmt_date}]")
# selected_tour = st.selectbox('Choose the tour:', tour_names)


if first_departure_date != today:
    st.markdown("#### Input relevant booking information")
    column1, column2, column3= st.columns([0.4,0.2, 0.4])
    with column1:
        ins_price = st.number_input("If insurance was purchased, enter cost here:")
        air_price = st.number_input("Air Department advised fees:")
        arr_xfer_price = st.number_input("If booked, enter arrival transfer price:")
        prenight_price = st.number_input('Enter pre-night price, if booked:')
        mct_price = st.number_input("Enter LAND price:")
        post_price = st.number_input('Enter post-night price, if booked:')
        dep_xfer_price = st.number_input("If booked, enter departure transfer price:")
        
    with column2:
        ins_date = st.date_input("Insurance Date",format="YYYY-MM-DD", help="Date should be entered as YYYY-MM-DD", min_value=today)
        st.markdown("#")
        arr_xfer_date = st.date_input("Arr Xfer Date",format="YYYY-MM-DD", help="Date should be entered as YYYY-MM-DD", min_value=ins_date)
        prenight_date = st.date_input("Prenight Date",format="YYYY-MM-DD", help="Date should be entered as YYYY-MM-DD", min_value=arr_xfer_date)
        mct_date = st.date_input("Tour Dep Date",format="YYYY-MM-DD", help="Date should be entered as YYYY-MM-DD", min_value=prenight_date)
        post_date = st.date_input("Postnight Date",format="YYYY-MM-DD", help="Date should be entered as YYYY-MM-DD", min_value=mct_date)
        dep_xfer_date = st.date_input("Dep Xfer Date",format="YYYY-MM-DD", help="Date should be entered as YYYY-MM-DD", min_value=post_date)

def calculate_segment_fees(price, days_until_segment):
    if days_until_segment >= 30 and today > final_pmt_date:
        return round(price * 0.50,2)
    elif 2 <= days_until_segment <= 29:
        return round(price * 0.8,2)
    else:
        return round(price,2)

def calculate_total_fees(prices, days_until_segments):
    total_fees = 0
    if today <= final_pmt_date:
        return deposit_amount
    else:
        for price, days_until_segment in zip(prices, days_until_segments):
            segment_fee = calculate_segment_fees(price, days_until_segment)
            total_fees += segment_fee
        return total_fees
        
# Streamlit UI
if st.button("Calculate Total"):
    # Calculate days to departure for each date
    days_to_ins_date = (ins_date - today).days if ins_price != 0 else 0
    days_to_arr_xfer_date = (arr_xfer_date - today).days if arr_xfer_price != 0 else 0
    days_to_prenight_date = (prenight_date - today).days if prenight_price != 0 else 0
    days_to_mct_date = (mct_date - today).days if mct_price != 0 else 0
    days_to_post_date = (post_date - today).days if post_price != 0 else 0
    days_to_dep_xfer_date = (dep_xfer_date - today).days if dep_xfer_price != 0 else 0

    # Calculate fees for each date
    arr_xfer_date_fees = calculate_segment_fees(arr_xfer_price, days_to_arr_xfer_date)
    prenight_date_fees = calculate_segment_fees(prenight_price, days_to_prenight_date)
    mct_date_fees = calculate_segment_fees(mct_price, days_to_mct_date)
    post_date_fees = calculate_segment_fees(post_price, days_to_post_date)
    dep_xfer_date_fees = calculate_segment_fees(dep_xfer_price, days_to_dep_xfer_date)

    with column3: #Display the calculated fees
        st.write(f"Insurance Price (not claimable): ${ins_price}")
        st.write(f"Air Department Advised fees: ${air_price}")
        st.write(f"Fees for Arr Xfer: ${arr_xfer_date_fees} | :red[{days_to_arr_xfer_date} days away]")
        st.write(f"Fees for Prenight: ${prenight_date_fees} | :red[{days_to_prenight_date} days away]")
        st.write(f"Fees for LAND: ${mct_date_fees} | :red[{days_to_mct_date} days away]")
        st.write(f"Fees for Postnight: ${post_date_fees} | :red[{days_to_post_date} days away]")
        st.write(f"Fees for Dep Xfer: ${dep_xfer_date_fees} | :red[{days_to_dep_xfer_date} days away]")

        total_fees = ins_price + air_price + arr_xfer_date_fees + prenight_date_fees + mct_date_fees + post_date_fees + dep_xfer_date_fees
        claim_amount = total_fees - ins_price
        
    st.write(f"Total Amound Paid: ${amount_paid}")
    st.write(f"TOTAL Witheld: ${total_fees}")
    st.write(f"Claim Amount: ${claim_amount} :red[(total witheld MINUS cost of insurance)]")
    refund_amount = calc_refund(amount_paid, claim_amount)
    st.write(f"REFUND DUE: ${refund_amount}")
        
