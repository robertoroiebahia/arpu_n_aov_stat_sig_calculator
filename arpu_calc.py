import math
import statistics
import streamlit as st
from scipy import stats

def calculate_welch_t_test(mean_A, sd_A, n_A, mean_B, sd_B, n_B):
    se_diff = math.sqrt((sd_A ** 2) / n_A + (sd_B ** 2) / n_B)
    t_stat = (mean_A - mean_B) / se_diff
    df = ((sd_A ** 2 / n_A) + (sd_B ** 2 / n_B)) ** 2 / (
         ((sd_A ** 2 / n_A) ** 2) / (n_A - 1) + ((sd_B ** 2 / n_B) ** 2) / (n_B - 1)
    )
    p_value = 2 * stats.t.sf(abs(t_stat), df)
    return t_stat, df, p_value

st.title("ARPU & AOV Lift & Confidence Calculator")

st.header("Group A (Control)")
n_A = st.number_input("Total number of users for Group A:", min_value=1, value=100)
purchaser_revenues_A_str = st.text_area("Enter comma-separated revenue values for Group A (for users who purchased):", value="100, 200, 300")
# Parse revenue values for Group A
try:
    purchaser_revenues_A = [float(x.strip()) for x in purchaser_revenues_A_str.split(',') if x.strip()]
except:
    purchaser_revenues_A = []
non_purchasers_A = n_A - len(purchaser_revenues_A)
full_revenues_A = purchaser_revenues_A + [0.0] * non_purchasers_A

st.header("Group B (Variant)")
n_B = st.number_input("Total number of users for Group B:", min_value=1, value=100)
purchaser_revenues_B_str = st.text_area("Enter comma-separated revenue values for Group B (for users who purchased):", value="150, 250, 350")
try:
    purchaser_revenues_B = [float(x.strip()) for x in purchaser_revenues_B_str.split(',') if x.strip()]
except:
    purchaser_revenues_B = []
non_purchasers_B = n_B - len(purchaser_revenues_B)
full_revenues_B = purchaser_revenues_B + [0.0] * non_purchasers_B

# Calculate metrics for ARPU
total_revenue_A = sum(full_revenues_A)
arpu_A = total_revenue_A / n_A
sd_arpu_A = statistics.stdev(full_revenues_A) if n_A > 1 else 0.0

total_revenue_B = sum(full_revenues_B)
arpu_B = total_revenue_B / n_B
sd_arpu_B = statistics.stdev(full_revenues_B) if n_B > 1 else 0.0

# Calculate metrics for AOV (only for purchasers)
if purchaser_revenues_A:
    aov_A = statistics.mean(purchaser_revenues_A)
    sd_aov_A = statistics.stdev(purchaser_revenues_A) if len(purchaser_revenues_A) > 1 else 0.0
    n_orders_A = len(purchaser_revenues_A)
else:
    aov_A, sd_aov_A, n_orders_A = 0, 0, 0

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
    st.write("N
