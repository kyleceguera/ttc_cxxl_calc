import streamlit as st
from datetime import datetime, timedelta

today = datetime.today().date()

st.set_page_config(page_title='TTC Cancellation Calculator', page_icon='dollar', layout="centered", initial_sidebar_state="auto", menu_items=None)
st.title("TTC CANCELLATION CALCULATOR")


def calc_refund(amount_paid, claim_amount):
    return round(amount_paid - claim_amount,2)

def dep_amount(x):
    if x ==2:
        return float(350)
    else:
        return float(200)

def calculate_segment_fees(price, days_until_segment):
    if days_until_segment >= 30 and today > final_pmt_date:
        return round(price * 0.50,2)
    elif 2 <= days_until_segment <= 29:
        return round(price * 0.8,2)
    elif today <= final_pmt_date:
        return 0
    else: 
        return round(price,2)

def calculate_total_fees(prices, days_until_segments):
    total_fees = 0
    if today < final_pmt_date:
        total_fees = deposit_amount + air_price
    else:
        for price, days_until_segment in zip(prices, days_until_segments):
            segment_fee = calculate_segment_fees(price, days_until_segment)
            total_fees += segment_fee
        return total_fees
            
amount_paid = st.number_input("Amount Paid for this particular passenger:")
cancellation_tier = st.selectbox('Trip Level', list(range(1,3)))
deposit_amount = dep_amount(cancellation_tier)
air_price = st.number_input("Air Department advised fees:", format="%.2f")
ins_price = st.number_input("If insurance was purchased, input price of insurance:", format="%.2f")
st.markdown(f"###### Deposit Amount: ${deposit_amount:.2f}")
first_departure_date = st.date_input(
    'First Date Shown on Booking', 
    format="YYYY-MM-DD",
    help="Please list the very first date shown on the booking. Date should be entered as YYYY-MM-DD", 
    min_value=today
    )
days_to_departure = (first_departure_date - today).days

if cancellation_tier == 1:
    final_pmt_date = first_departure_date - timedelta(60)
else:
    final_pmt_date = first_departure_date - timedelta(90)
    
st.markdown(f"Days to departure: {days_to_departure}")
st.write(f"Final Payment Due Date: :green[{final_pmt_date}]")
# selected_tour = st.selectbox('Choose the tour:', tour_names)

if today < final_pmt_date:
    st.markdown("#### We are outside of final payment date, so cancellation fees are just loss of deposit")
    st.write(f"Land Deposit = ${deposit_amount:.2f}")
    st.write(f"Air Cancellation fees, advised by air: ${air_price:.2f}")
    loss_deposits = round(air_price + deposit_amount,2)
    st.write(f"Total Cxxl Penalty (land+air deposit): ${loss_deposits:.2f}")
    cxxl_fees = round(ins_price + loss_deposits,2)
    st.write(f"Total Witheld (deposites + insurance): ${cxxl_fees:.2f}")
    refund = round(amount_paid - cxxl_fees,2)
    st.write(f"Refund Due: ${refund:.2f}")
    st.write(f"Amount to Claim with Insurance: ${loss_deposits:.2f}")


if today >= final_pmt_date and first_departure_date != today:
    st.markdown("#### Input relevant booking information")
    column1, column2, column3= st.columns([0.4,0.2, 0.4])
    with column1:
        arr_xfer_price = st.number_input("If booked, enter arrival transfer price:", format="%.2f")
        prenight_price = st.number_input('Enter pre-night price, if booked:', format="%.2f")
        mct_price = st.number_input("Enter LAND price:", format="%.2f")
        post_price = st.number_input('Enter post-night price, if booked:', format="%.2f")
        dep_xfer_price = st.number_input("If booked, enter departure transfer price:", format="%.2f")
        
    with column2:
        arr_xfer_date = st.date_input("Arr Xfer Date",format="YYYY-MM-DD", help="Date should be entered as YYYY-MM-DD", min_value=first_departure_date)
        prenight_date = st.date_input("Prenight Date",format="YYYY-MM-DD", help="Date should be entered as YYYY-MM-DD", min_value=arr_xfer_date)
        mct_date = st.date_input("Tour Dep Date",format="YYYY-MM-DD", help="Date should be entered as YYYY-MM-DD", min_value=prenight_date)
        post_date = st.date_input("Postnight Date",format="YYYY-MM-DD", help="Date should be entered as YYYY-MM-DD", min_value=mct_date)
        dep_xfer_date = st.date_input("Dep Xfer Date",format="YYYY-MM-DD", help="Date should be entered as YYYY-MM-DD", min_value=post_date)

    if st.button("Calculate Total"):
    # Calculate days to departure for each date
        days_to_arr_xfer_date = (arr_xfer_date - today).days if arr_xfer_price != 0 else 0
        days_to_prenight_date = (prenight_date - today).days if prenight_price != 0 else 0
        days_to_mct_date = (mct_date - today).days if mct_price != 0 else 0
        days_to_post_date = (post_date - today).days if post_price != 0 else 0
        days_to_dep_xfer_date = (dep_xfer_date - today).days if dep_xfer_price != 0 else 0

        # Calculate fees for each date
        arr_xfer_date_fees = calculate_segment_fees(arr_xfer_price, days_to_arr_xfer_date)
        prenight_date_fees = calculate_segment_fees(prenight_price, days_to_prenight_date)
        mct_date_fees =  deposit_amount if today <= final_pmt_date else calculate_segment_fees(mct_price, days_to_mct_date)
        post_date_fees = calculate_segment_fees(post_price, days_to_post_date)
        dep_xfer_date_fees = calculate_segment_fees(dep_xfer_price, days_to_dep_xfer_date)

        with column3: #Display the calculated fees
            st.write(f"Insurance Price (not claimable): ${ins_price:.2f}")
            st.write(f"Fees Advised for Air: ${air_price:.2f}")
            st.write(f"Arr Xfer Fees: ${arr_xfer_date_fees:.2f} | :red[{days_to_arr_xfer_date} days away]")
            st.write(f"Prenight Fees: ${prenight_date_fees:.2f} | :red[{days_to_prenight_date} days away]")
            st.write(f"Fees for LAND: ${mct_date_fees:.2f} | :red[{days_to_mct_date} days away]")
            st.write(f"Postnight Fees: ${post_date_fees:.2f} | :red[{days_to_post_date} days away]")
            st.write(f"Dep Xfer Fees: ${dep_xfer_date_fees:.2f} | :red[{days_to_dep_xfer_date} days away]")

            total_fees = ins_price + air_price + arr_xfer_date_fees + prenight_date_fees + mct_date_fees + post_date_fees + dep_xfer_date_fees
            claim_amount = total_fees - ins_price
        
        st.write(f"Total Amound Paid: ${amount_paid:.2f}")
        st.write(f"TOTAL Witheld: ${total_fees:.2f}")
        st.write(f"Claim Amount: ${claim_amount:.2f} :red[(total witheld MINUS cost of insurance)]")
        refund_amount = calc_refund(amount_paid, total_fees)
        st.write(f"REFUND DUE: ${refund_amount:.2f}")
        
