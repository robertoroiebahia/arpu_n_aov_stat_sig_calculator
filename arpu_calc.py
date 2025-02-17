import math
import statistics
import streamlit as st
from scipy import stats

def calculate_welch_t_test(mean_A, sd_A, n_A, mean_B, sd_B, n_B):
    """
    Calculates Welch's t-test statistic, degrees of freedom, and p-value 
    comparing two groups.
    """
    se_diff = math.sqrt((sd_A ** 2) / n_A + (sd_B ** 2) / n_B)
    t_stat = (mean_A - mean_B) / se_diff
    df = ((sd_A ** 2 / n_A) + (sd_B ** 2 / n_B)) ** 2 / (
         ((sd_A ** 2 / n_A) ** 2) / (n_A - 1) + ((sd_B ** 2 / n_B) ** 2) / (n_B - 1)
    )
    p_value = 2 * stats.t.sf(abs(t_stat), df)
    return t_stat, df, p_value

def input_revenues(group_name):
    """
    Prompts the user to input the total number of users and comma-separated
    revenue values for users who made a purchase.
    
    Returns:
      full_revenues: Revenue for all users (with 0 for non-purchasers)
      purchaser_revenues: Revenue for purchasers only
      total_users: Total number of users exposed to the test
    """
    total_users = st.number_input(f"Enter total number of users for {group_name}:", min_value=1, value=100, step=1)
    revenue_input = st.text_area(f"Enter revenue values for {group_name} (comma-separated for users who purchased):", value="100, 200, 300")
    try:
        purchaser_revenues = [float(x.strip()) for x in revenue_input.split(',') if x.strip()]
    except Exception as e:
        st.error(f"Error parsing revenue values: {e}")
        purchaser_revenues = []
    non_purchasers = total_users - len(purchaser_revenues)
    full_revenues = purchaser_revenues + [0.0] * non_purchasers
    return full_revenues, purchaser_revenues, total_users

st.title("ARPU & AOV Lift & Confidence Calculator")

st.header("Group A (Control)")
full_revenues_A, purchaser_revenues_A, n_A = input_revenues("Group A (Control)")
total_revenue_A = sum(full_revenues_A)
arpu_A = total_revenue_A / n_A
sd_arpu_A = statistics.stdev(full_revenues_A) if n_A > 1 else 0.0

if purchaser_revenues_A:
    aov_A = statistics.mean(purchaser_revenues_A)
    sd_aov_A = statistics.stdev(purchaser_revenues_A) if len(purchaser_revenues_A) > 1 else 0.0
    n_orders_A = len(purchaser_revenues_A)
else:
    aov_A, sd_aov_A, n_orders_A = 0, 0, 0

st.header("Group B (Variant)")
full_revenues_B, purchaser_revenues_B, n_B = input_revenues("Group B (Variant)")
total_revenue_B = sum(full_revenues_B)
arpu_B = total_revenue_B / n_B
sd_arpu_B = statistics.stdev(full_revenues_B) if n_B > 1 else 0.0

if purchaser_revenues_B:
    aov_B = statistics.mean(purchaser_revenues_B)
    sd_aov_B = statistics.stdev(purchaser_revenues_B) if len(purchaser_revenues_B) > 1 else 0.0
    n_orders_B = len(purchaser_revenues_B)
else:
    aov_B, sd_aov_B, n_orders_B = 0, 0, 0

st.subheader("Calculated Metrics")
st.write(f"**Group A (Control)**: Total Revenue = {total_revenue_A:.2f}, ARPU = {arpu_A:.2f}, ARPU SD = {sd_arpu_A:.2f}")
st.write(f"**Group B (Variant)**: Total Revenue = {total_revenue_B:.2f}, ARPU = {arpu_B:.2f}, ARPU SD = {sd_arpu_B:.2f}")

if n_orders_A > 0 and n_orders_B > 0:
    st.write(f"**Group A AOV**: {aov_A:.2f} (SD = {sd_aov_A:.2f}, n = {n_orders_A})")
    st.write(f"**Group B AOV**: {aov_B:.2f} (SD = {sd_aov_B:.2f}, n = {n_orders_B})")
else:
    st.write("Not enough purchaser data for AOV comparison.")

# ARPU Comparison: Welch's t-test
t_stat_arpu, df_arpu, p_value_arpu = calculate_welch_t_test(arpu_A, sd_arpu_A, n_A, arpu_B, sd_arpu_B, n_B)
confidence_level_arpu = (1 - p_value_arpu) * 100
arpu_lift = ((arpu_B - arpu_A) / arpu_A) * 100 if arpu_A != 0 else float('nan')

st.subheader("ARPU Comparison")
st.write(f"t-statistic: {t_stat_arpu:.3f}")
st.write(f"Degrees of freedom: {df_arpu:.1f}")
st.write(f"p-value: {p_value_arpu:.3f}")
st.write(f"Confidence Level: {confidence_level_arpu:.1f}%")
st.write(f"ARPU Lift (Variant vs. Control): {arpu_lift:.2f}%")

# AOV Comparison: Welch's t-test (only if sufficient data)
if n_orders_A > 1 and n_orders_B > 1:
    t_stat_aov, df_aov, p_value_aov = calculate_welch_t_test(aov_A, sd_aov_A, n_orders_A, aov_B, sd_aov_B, n_orders_B)
    confidence_level_aov = (1 - p_value_aov) * 100
    aov_lift = ((aov_B - aov_A) / aov_A) * 100 if aov_A != 0 else float('nan')
    
    st.subheader("AOV Comparison")
    st.write(f"t-statistic: {t_stat_aov:.3f}")
    st.write(f"Degrees of freedom: {df_aov:.1f}")
    st.write(f"p-value: {p_value_aov:.3f}")
    st.write(f"Confidence Level: {confidence_level_aov:.1f}%")
    st.write(f"AOV Lift (Variant vs. Control): {aov_lift:.2f}%")
else:
    st.write("Not enough data to perform AOV comparison for one or both groups.")
