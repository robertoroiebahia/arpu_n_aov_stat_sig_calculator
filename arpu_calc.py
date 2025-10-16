import math
import statistics
import streamlit as st
from scipy import stats
import plotly.graph_objects as go
import plotly.express as px

# Page Config
st.set_page_config(
    page_title="CRO Test Calculator | Enavi",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* Global Styles */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container background */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .block-container {
        padding-top: 3rem !important;
        padding-bottom: 3rem !important;
        max-width: 1400px !important;
    }
    
    /* Header styling */
    .main h1 {
        color: white !important;
        font-weight: 800 !important;
        font-size: 3rem !important;
        margin-bottom: 0.5rem !important;
        text-align: center;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .main h2 {
        color: white !important;
        font-weight: 700 !important;
        font-size: 1.8rem !important;
        margin-top: 2rem !important;
        margin-bottom: 1.5rem !important;
    }
    
    .main h3 {
        color: #1e293b !important;
        font-weight: 700 !important;
        font-size: 1.25rem !important;
        margin-top: 1rem !important;
        margin-bottom: 1rem !important;
    }
    
    /* Subtitle styling */
    .subtitle {
        color: rgba(255,255,255,0.95) !important;
        text-align: center;
        font-size: 1.125rem;
        font-weight: 500;
        margin-bottom: 2.5rem;
    }
    
    /* Card container for input sections */
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 800 !important;
        color: #1e293b !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.875rem !important;
        font-weight: 600 !important;
        color: #64748b !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 1rem !important;
        font-weight: 700 !important;
    }
    
    /* Input styling */
    .stNumberInput input, .stTextArea textarea {
        border-radius: 8px !important;
        border: 2px solid #e2e8f0 !important;
        font-size: 0.95rem !important;
        padding: 0.75rem !important;
        background: white !important;
    }
    
    .stNumberInput input:focus, .stTextArea textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Labels */
    .stNumberInput label, .stTextArea label {
        font-weight: 600 !important;
        color: #1e293b !important;
        font-size: 0.95rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* Alert styling */
    .stAlert {
        border-radius: 12px !important;
        border-left-width: 4px !important;
        padding: 1rem 1.25rem !important;
        font-weight: 500 !important;
        background: white !important;
    }
    
    /* Divider */
    hr {
        margin: 2.5rem 0 !important;
        border: none !important;
        height: 2px !important;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent) !important;
    }
    
    /* Column spacing */
    [data-testid="column"] {
        padding: 0 0.75rem !important;
    }
    
    /* Caption text */
    .stCaptionContainer {
        color: #64748b !important;
        font-size: 0.875rem !important;
        margin-top: 0.25rem !important;
    }
    
    /* Info box at bottom */
    .stAlert[data-baseweb="notification"] {
        background: white !important;
    }
</style>
""", unsafe_allow_html=True)

def calculate_welch_t_test(mean_A, sd_A, n_A, mean_B, sd_B, n_B):
    """Welch's t-test for unequal variances"""
    if n_A < 2 or n_B < 2:
        return None, None, None
    
    se_diff = math.sqrt((sd_A ** 2) / n_A + (sd_B ** 2) / n_B)
    if se_diff == 0:
        return None, None, None
    
    t_stat = (mean_B - mean_A) / se_diff
    df = ((sd_A ** 2 / n_A) + (sd_B ** 2 / n_B)) ** 2 / (
         ((sd_A ** 2 / n_A) ** 2) / (n_A - 1) + ((sd_B ** 2 / n_B) ** 2) / (n_B - 1)
    )
    p_value = 2 * stats.t.sf(abs(t_stat), df)
    
    return t_stat, df, p_value

def calculate_z_test_conversion(conv_A, n_A, conv_B, n_B):
    """Z-test for conversion rate comparison"""
    p_A = conv_A / 100
    p_B = conv_B / 100
    
    p_pooled = ((p_A * n_A) + (p_B * n_B)) / (n_A + n_B)
    se = math.sqrt(p_pooled * (1 - p_pooled) * (1/n_A + 1/n_B))
    
    if se == 0:
        return None, None
    
    z_stat = (p_B - p_A) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
    
    return z_stat, p_value

def create_comparison_chart(control_val, variant_val, metric_name, is_currency=False):
    """Create a beautiful comparison bar chart"""
    
    fig = go.Figure()
    
    # Format text based on metric type
    if is_currency:
        control_text = f'${control_val:.2f}'
        variant_text = f'${variant_val:.2f}'
    else:
        control_text = f'{control_val:.2f}%'
        variant_text = f'{variant_val:.2f}%'
    
    fig.add_trace(go.Bar(
        name='Control',
        x=['Control'],
        y=[control_val],
        marker_color='#94a3b8',
        text=[control_text],
        textposition='outside',
        textfont=dict(size=14, family='Inter', color='#1e293b'),
        width=0.5
    ))
    
    fig.add_trace(go.Bar(
        name='Variant',
        x=['Variant'],
        y=[variant_val],
        marker_color='#667eea',
        text=[variant_text],
        textposition='outside',
        textfont=dict(size=14, family='Inter', color='#1e293b'),
        width=0.5
    ))
    
    # Calculate max value for proper y-axis range
    max_val = max(control_val, variant_val)
    
    fig.update_layout(
        title=dict(
            text=metric_name, 
            font=dict(size=16, family='Inter', color='#1e293b'),
            x=0.5,
            xanchor='center'
        ),
        showlegend=False,
        paper_bgcolor='white',
        plot_bgcolor='white',
        height=300,
        margin=dict(l=20, r=20, t=80, b=40),  # Increased top margin
        yaxis=dict(
            showgrid=True, 
            gridcolor='#f1f5f9', 
            zeroline=False,
            title=None,
            range=[0, max_val * 1.25]  # Add 25% padding above bars for labels
        ),
        xaxis=dict(
            showgrid=False,
            title=None
        )
    )
    
    return fig
def calculate_sample_size_per_variant(baseline_rate, mde, alpha=0.05, power=0.80):
    """
    Calculate required sample size per variant for conversion rate tests
    baseline_rate: baseline conversion rate (as decimal, e.g., 0.028 for 2.8%)
    mde: minimum detectable effect (as decimal, e.g., 0.10 for 10% relative lift)
    alpha: significance level (default 0.05 for 95% confidence)
    power: statistical power (default 0.80)
    """
    # Calculate the alternative conversion rate
    p1 = baseline_rate
    p2 = baseline_rate * (1 + mde)
    
    # Z-scores for alpha and power
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)
    
    # Pooled probability
    p_avg = (p1 + p2) / 2
    
    # Sample size formula for two proportions
    n = ((z_alpha * math.sqrt(2 * p_avg * (1 - p_avg)) + 
          z_beta * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2) / ((p2 - p1) ** 2)
    
    return math.ceil(n)

def calculate_days_needed(required_visitors, current_visitors, days_elapsed):
    """Calculate additional days needed based on current traffic rate"""
    if days_elapsed <= 0:
        return None
    
    visitors_per_day = current_visitors / days_elapsed
    
    if visitors_per_day <= 0:
        return None
    
    days_needed = math.ceil(required_visitors / visitors_per_day)
    additional_days = max(0, days_needed - days_elapsed)
    
    return days_needed, additional_days

# Header
st.markdown("<h1>🎯 CRO Test Calculator</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Calculate statistical significance for conversion optimization tests</p>", unsafe_allow_html=True)

st.markdown("---")

# Input Section
st.markdown("## ⚙️ Test Configuration")

config_col1, config_col2 = st.columns(2)

with config_col1:
    days_live = st.number_input(
        "Days Live", 
        min_value=0, 
        value=7, 
        step=1, 
        help="How many days has this test been running?"
    )

with config_col2:
    mde_percent = st.number_input(
        "Minimum Detectable Effect (MDE %)", 
        min_value=1.0, 
        max_value=100.0, 
        value=10.0, 
        step=1.0,
        help="The smallest lift you want to be able to detect. Typically 5-15% for conversion tests."
    )

st.markdown("---")

col_a, col_b = st.columns(2, gap="large")

with col_a:
    st.markdown("### 🅰️ Control Group")
    n_A = st.number_input("Total Visitors (Control)", min_value=1, value=10000, step=100, key="control_visitors")
    n_purchasers_A = st.number_input("Number of Conversions (Control)", min_value=0, value=280, step=1, key="control_conversions")
    revenue_A = st.text_area(
        "Revenue per order (comma-separated)", 
        value="89.50, 120.00, 67.99, 145.50, 89.50, 95.00, 110.50, 89.50, 78.00, 125.00",
        height=120,
        key="control_revenue"
    )

with col_b:
    st.markdown("### 🅱️ Variant Group")
    n_B = st.number_input("Total Visitors (Variant)", min_value=1, value=10000, step=100, key="variant_visitors")
    n_purchasers_B = st.number_input("Number of Conversions (Variant)", min_value=0, value=312, step=1, key="variant_conversions")
    revenue_B = st.text_area(
        "Revenue per order (comma-separated)", 
        value="95.00, 128.00, 72.50, 152.00, 95.00, 98.50, 115.00, 95.00, 82.00, 130.50",
        height=120,
        key="variant_revenue"
    )

# Parse revenues
try:
    purchaser_revenues_A = [float(x.strip()) for x in revenue_A.split(',') if x.strip()][:n_purchasers_A]
    purchaser_revenues_B = [float(x.strip()) for x in revenue_B.split(',') if x.strip()][:n_purchasers_B]
except:
    st.error("⚠️ Error parsing revenue values. Please check your input.")
    st.stop()

# Extend with actual number of conversions
if len(purchaser_revenues_A) < n_purchasers_A:
    avg_rev_A = statistics.mean(purchaser_revenues_A) if purchaser_revenues_A else 0
    purchaser_revenues_A.extend([avg_rev_A] * (n_purchasers_A - len(purchaser_revenues_A)))

if len(purchaser_revenues_B) < n_purchasers_B:
    avg_rev_B = statistics.mean(purchaser_revenues_B) if purchaser_revenues_B else 0
    purchaser_revenues_B.extend([avg_rev_B] * (n_purchasers_B - len(purchaser_revenues_B)))

# Create full revenue arrays
full_revenues_A = purchaser_revenues_A + [0.0] * (n_A - n_purchasers_A)
full_revenues_B = purchaser_revenues_B + [0.0] * (n_B - n_purchasers_B)

# Calculate metrics
conv_rate_A = (n_purchasers_A / n_A) * 100 if n_A > 0 else 0
conv_rate_B = (n_purchasers_B / n_B) * 100 if n_B > 0 else 0

aov_A = statistics.mean(purchaser_revenues_A) if purchaser_revenues_A else 0
aov_B = statistics.mean(purchaser_revenues_B) if purchaser_revenues_B else 0
sd_aov_A = statistics.stdev(purchaser_revenues_A) if len(purchaser_revenues_A) > 1 else 0
sd_aov_B = statistics.stdev(purchaser_revenues_B) if len(purchaser_revenues_B) > 1 else 0

arpu_A = sum(full_revenues_A) / n_A if n_A > 0 else 0
arpu_B = sum(full_revenues_B) / n_B if n_B > 0 else 0
sd_arpu_A = statistics.stdev(full_revenues_A) if n_A > 1 else 0
sd_arpu_B = statistics.stdev(full_revenues_B) if n_B > 1 else 0

st.markdown("---")

st.markdown("---")

# Test Duration & Sample Size Analysis
st.markdown("## ⏱️ Test Duration & Sample Size")

# Calculate required sample size
baseline_conv_rate = conv_rate_A / 100  # Convert to decimal
mde_decimal = mde_percent / 100
required_sample_per_variant = calculate_sample_size_per_variant(baseline_conv_rate, mde_decimal)

# Current totals
total_current_visitors = n_A + n_B

# Duration analysis
duration_col1, duration_col2, duration_col3, duration_col4 = st.columns(4)

with duration_col1:
    st.metric("Days Live", f"{days_live} days")

with duration_col2:
    st.metric("Current Sample Size", f"{total_current_visitors:,}")

with duration_col3:
    required_total = required_sample_per_variant * 2
    st.metric("Required Sample Size", f"{required_total:,}")
    st.caption(f"Based on {mde_percent}% MDE")

with duration_col4:
    sample_progress = (total_current_visitors / required_total * 100) if required_total > 0 else 0
    st.metric("Sample Progress", f"{sample_progress:.1f}%")

# Calculate days recommendation
if days_live > 0:
    days_result = calculate_days_needed(required_total, total_current_visitors, days_live)
    
    if days_result:
        total_days_needed, additional_days = days_result
        
        st.markdown("")  # spacing
        
        # Recommendations
        if total_current_visitors >= required_total and days_live >= 14:
            st.success(f"✅ **Test is ready to conclude** — You've reached the required sample size ({required_total:,} visitors) and run for {days_live} days. You can confidently analyze results.")
        elif total_current_visitors >= required_total and days_live < 14:
            days_remaining = 14 - days_live
            st.warning(f"⚠️ **Sample size reached, but run longer** — You have enough visitors, but tests should run at least 14 days to capture weekly patterns. Recommend running {days_remaining} more days.")
        elif total_current_visitors < required_total and days_live >= 14:
            st.warning(f"⚠️ **Need more sample size** — You've run for {days_live} days, but need approximately **{additional_days} more days** to reach {required_total:,} total visitors (based on current traffic of {total_current_visitors/days_live:.0f} visitors/day).")
        else:
            # Need both more time and more sample
            days_for_sample = max(total_days_needed, 14)
            days_remaining = days_for_sample - days_live
            st.info(f"📊 **Continue testing** — Recommend running for approximately **{days_remaining} more days** to reach both minimum duration (14 days) and required sample size ({required_total:,} visitors).")
        
        # Show detailed breakdown
        with st.expander("📈 See detailed breakdown"):
            st.markdown(f"""
            **Current Status:**
            - Days running: {days_live}
            - Total visitors so far: {total_current_visitors:,}
            - Average visitors per day: {total_current_visitors/days_live:.0f}
            
            **Requirements:**
            - Minimum detectable effect (MDE): {mde_percent}% relative lift
            - Required visitors per variant: {required_sample_per_variant:,}
            - Required total visitors: {required_total:,}
            - Minimum recommended duration: 14 days
            
            **Projection:**
            - Estimated total days needed: {max(total_days_needed, 14)} days
            - Additional days recommended: {max(additional_days, 14 - days_live)} days
            """)
else:
    st.info("💡 Enter the number of days this test has been running to get duration recommendations.")

st.markdown("---")

# Summary Metrics
st.markdown("## 📊 Performance Overview")

# Create metrics row
metric_col1, metric_col2, metric_col3 = st.columns(3)

with metric_col1:
    conv_lift = ((conv_rate_B - conv_rate_A) / conv_rate_A * 100) if conv_rate_A > 0 else 0
    st.metric(
        "Conversion Rate",
        f"{conv_rate_B:.2f}%",
        delta=f"{conv_lift:+.1f}% vs control",
        delta_color="normal"
    )
    st.caption(f"Control: {conv_rate_A:.2f}%")

with metric_col2:
    aov_lift = ((aov_B - aov_A) / aov_A * 100) if aov_A > 0 else 0
    st.metric(
        "Average Order Value",
        f"${aov_B:.2f}",
        delta=f"{aov_lift:+.1f}% vs control",
        delta_color="normal"
    )
    st.caption(f"Control: ${aov_A:.2f}")

with metric_col3:
    arpu_lift = ((arpu_B - arpu_A) / arpu_A * 100) if arpu_A > 0 else 0
    st.metric(
        "Revenue Per Visitor",
        f"${arpu_B:.2f}",
        delta=f"{arpu_lift:+.1f}% vs control",
        delta_color="normal"
    )
    st.caption(f"Control: ${arpu_A:.2f}")

# Visual comparisons
st.markdown("---")
st.markdown("## 📈 Visual Comparison")

chart_col1, chart_col2, chart_col3 = st.columns(3)

with chart_col1:
    fig_conv = create_comparison_chart(conv_rate_A, conv_rate_B, "Conversion Rate", is_currency=False)
    st.plotly_chart(fig_conv, use_container_width=True)

with chart_col2:
    fig_aov = create_comparison_chart(aov_A, aov_B, "Average Order Value", is_currency=True)
    st.plotly_chart(fig_aov, use_container_width=True)

with chart_col3:
    fig_rpv = create_comparison_chart(arpu_A, arpu_B, "Revenue Per Visitor", is_currency=True)
    st.plotly_chart(fig_rpv, use_container_width=True)

st.markdown("---")

# Statistical Tests
st.markdown("## 🔬 Statistical Significance Analysis")

# Test 1: Conversion Rate
st.markdown("### 1️⃣ Conversion Rate Test")
z_stat_conv, p_value_conv = calculate_z_test_conversion(conv_rate_A, n_A, conv_rate_B, n_B)

if z_stat_conv is not None:
    confidence_level_conv = (1 - p_value_conv) * 100
    
    test_col1, test_col2, test_col3, test_col4, test_col5 = st.columns(5)
    
    with test_col1:
        st.metric("Relative Lift", f"{conv_lift:+.2f}%")
    with test_col2:
        st.metric("Z-Score", f"{z_stat_conv:.3f}")
    with test_col3:
        st.metric("P-Value", f"{p_value_conv:.4f}")
    with test_col4:
        st.metric("Confidence", f"{confidence_level_conv:.2f}%")
    with test_col5:
        if p_value_conv < 0.05:
            st.metric("Result", "✅ Significant", delta="95%+ confidence")
        else:
            st.metric("Result", "❌ Inconclusive", delta="Need more data")
    
    st.markdown("")  # spacing
    
    if p_value_conv < 0.05:
        st.success(f"✅ **Statistically Significant** — {confidence_level_conv:.2f}% confidence this isn't random chance.")
    elif p_value_conv < 0.10:
        st.warning(f"⚠️ **Marginally Significant** — {confidence_level_conv:.2f}% confidence. P-value of {p_value_conv:.4f} suggests a trend, but more data recommended.")
    else:
        st.error(f"❌ **Not Significant** — Only {confidence_level_conv:.2f}% confidence. P-value of {p_value_conv:.4f} means we can't rule out random chance. Continue testing.")

st.markdown("")  # spacing

# Test 2: RPV/ARPU
st.markdown("### 2️⃣ Revenue Per Visitor Test")
t_stat_arpu, df_arpu, p_value_arpu = calculate_welch_t_test(arpu_A, sd_arpu_A, n_A, arpu_B, sd_arpu_B, n_B)

if t_stat_arpu is not None:
    confidence_level_arpu = (1 - p_value_arpu) * 100
    
    test_col1, test_col2, test_col3, test_col4, test_col5 = st.columns(5)
    
    with test_col1:
        st.metric("Relative Lift", f"{arpu_lift:+.2f}%")
    with test_col2:
        st.metric("T-Score", f"{t_stat_arpu:.3f}")
    with test_col3:
        st.metric("P-Value", f"{p_value_arpu:.4f}")
    with test_col4:
        st.metric("Confidence", f"{confidence_level_arpu:.2f}%")
    with test_col5:
        if p_value_arpu < 0.05:
            st.metric("Result", "✅ Significant", delta="95%+ confidence")
        else:
            st.metric("Result", "❌ Inconclusive", delta="Need more data")
    
    st.markdown("")  # spacing
    
    if p_value_arpu < 0.05:
        st.success(f"✅ **Statistically Significant** — {confidence_level_arpu:.2f}% confidence this isn't random chance.")
    elif p_value_arpu < 0.10:
        st.warning(f"⚠️ **Marginally Significant** — {confidence_level_arpu:.2f}% confidence. P-value of {p_value_arpu:.4f} suggests a trend, but more data recommended.")
    else:
        st.error(f"❌ **Not Significant** — Only {confidence_level_arpu:.2f}% confidence. P-value of {p_value_arpu:.4f} means we can't rule out random chance. Continue testing.")

st.markdown("")  # spacing

# Test 3: AOV
st.markdown("### 3️⃣ Average Order Value Test")

if n_purchasers_A > 1 and n_purchasers_B > 1:
    t_stat_aov, df_aov, p_value_aov = calculate_welch_t_test(aov_A, sd_aov_A, n_purchasers_A, aov_B, sd_aov_B, n_purchasers_B)
    
    if t_stat_aov is not None:
        confidence_level_aov = (1 - p_value_aov) * 100
        
        test_col1, test_col2, test_col3, test_col4, test_col5 = st.columns(5)
        
        with test_col1:
            st.metric("Relative Lift", f"{aov_lift:+.2f}%")
        with test_col2:
            st.metric("T-Score", f"{t_stat_aov:.3f}")
        with test_col3:
            st.metric("P-Value", f"{p_value_aov:.4f}")
        with test_col4:
            st.metric("Confidence", f"{confidence_level_aov:.2f}%")
        with test_col5:
            if p_value_aov < 0.05:
                st.metric("Result", "✅ Significant", delta="95%+ confidence")
            else:
                st.metric("Result", "❌ Inconclusive", delta="Need more data")
        
        st.markdown("")  # spacing
        
        if p_value_aov < 0.05:
            st.success(f"✅ **Statistically Significant** — {confidence_level_aov:.2f}% confidence this isn't random chance.")
        elif p_value_aov < 0.10:
            st.warning(f"⚠️ **Marginally Significant** — {confidence_level_aov:.2f}% confidence. P-value of {p_value_aov:.4f} suggests a trend, but more data recommended.")
        else:
            st.error(f"❌ **Not Significant** — Only {confidence_level_aov:.2f}% confidence. P-value of {p_value_aov:.4f} means we can't rule out random chance. Continue testing.")
else:
    st.warning("⚠️ Need at least 2 conversions in each group to test AOV significance.")

st.markdown("---")

# Bottom Info
st.info("""
**📖 How to Read Results:**
- **P-value < 0.05**: Statistically significant at 95% confidence (winner!)
- **P-value 0.05-0.10**: Marginally significant (interesting trend, keep testing)
- **P-value > 0.10**: Not significant (likely random chance)
- **Relative Lift**: Percentage improvement over control
- **MDE (Minimum Detectable Effect)**: The smallest lift you want to reliably detect

**💡 Pro Tips:**
- Run tests for at least 2 weeks to account for weekly patterns
- Aim for minimum 100 conversions per variation for reliable results
- Don't stop tests early just because you see significance
- Consider business significance, not just statistical significance
- Lower MDE requires more sample size (5% MDE needs 4x more traffic than 10% MDE)
- Typical MDE targets: 5-10% for high-traffic sites, 10-20% for lower-traffic sites
""")

# Bottom Info
st.info("""
**📖 How to Read Results:**
- **P-value < 0.05**: Statistically significant at 95% confidence (winner!)
- **P-value 0.05-0.10**: Marginally significant (interesting trend, keep testing)
- **P-value > 0.10**: Not significant (likely random chance)
- **Relative Lift**: Percentage improvement over control
- **MDE (Minimum Detectable Effect)**: The smallest lift you want to reliably detect

**💡 Pro Tips:**
- Run tests for at least 2 weeks to account for weekly patterns
- Aim for minimum 100 conversions per variation for reliable results
- Don't stop tests early just because you see significance
- Consider business significance, not just statistical significance
- Lower MDE requires more sample size (5% MDE needs 4x more traffic than 10% MDE)
- Typical MDE targets: 5-10% for high-traffic sites, 10-20% for lower-traffic sites
""")

st.markdown("---")

# Statistical Methodology Section
st.markdown("## 📚 Statistical Methodology & Validity")

st.markdown("""
This calculator uses industry-standard statistical tests to determine whether your A/B test results are statistically significant. 
Here's how it works and why these methods are valid:
""")

# Create tabs for different explanations
method_tab1, method_tab2, method_tab3, method_tab4 = st.tabs([
    "Conversion Rate Test", 
    "Revenue Tests (AOV & RPV)", 
    "Sample Size Calculation",
    "Why This Matters"
])

with method_tab1:
    st.markdown("""
    ### Z-Test for Conversion Rates
    
    **What it does:**  
    Compares two conversion rates to determine if the difference between them is statistically significant or just random variation.
    
    **The Math:**
    1. **Calculate pooled conversion rate:**  
       `p_pooled = (conversions_A + conversions_B) / (visitors_A + visitors_B)`
    
    2. **Calculate standard error:**  
       `SE = √[p_pooled × (1 - p_pooled) × (1/n_A + 1/n_B)]`
    
    3. **Calculate Z-statistic:**  
       `Z = (conversion_rate_B - conversion_rate_A) / SE`
    
    4. **Calculate p-value:**  
       Using the Z-statistic, we look up the probability in the standard normal distribution
    
    **Why it's valid:**
    - The **Z-test** (also called a two-proportion z-test) is the gold standard for comparing conversion rates
    - Based on the **Central Limit Theorem**, which says that with large enough sample sizes, the sampling distribution of proportions is approximately normal
    - This is the same method used by tools like Optimizely, VWO, Google Optimize, and Convert
    - Assumes independent observations (each visitor is independent) and sufficiently large sample sizes (typically n × p > 5 and n × (1-p) > 5)
    
    **Real-world example:**
    - Control: 280 conversions out of 10,000 visitors = 2.8% conversion rate
    - Variant: 312 conversions out of 10,000 visitors = 3.12% conversion rate
    - This calculator determines if that 0.32 percentage point difference is real or just random noise
    """)

with method_tab2:
    st.markdown("""
    ### Welch's T-Test for Revenue Metrics
    
    **What it does:**  
    Compares the means of two groups (like Average Order Value or Revenue Per Visitor) when the groups may have different variances and different sample sizes.
    
    **The Math:**
    1. **Calculate standard error of the difference:**  
       `SE_diff = √[(SD_A² / n_A) + (SD_B² / n_B)]`
    
    2. **Calculate t-statistic:**  
       `t = (mean_B - mean_A) / SE_diff`
    
    3. **Calculate degrees of freedom (Welch-Satterthwaite equation):**  
       `df = [(SD_A²/n_A + SD_B²/n_B)²] / [(SD_A²/n_A)²/(n_A-1) + (SD_B²/n_B)²/(n_B-1)]`
    
    4. **Calculate p-value:**  
       Using the t-statistic and degrees of freedom, we look up the probability in the t-distribution
    
    **Why Welch's T-Test (not Student's T-Test):**
    - **Student's t-test** assumes equal variances between groups — rarely true in real-world e-commerce data
    - **Welch's t-test** doesn't assume equal variances, making it more robust and accurate for A/B tests
    - Revenue data is often highly variable (some customers spend $50, others spend $500+)
    - Welch's test is considered the default choice by statisticians when comparing means
    
    **Why it's valid:**
    - Welch's t-test is widely accepted in academic research and industry practice
    - More conservative than Student's t-test (less likely to give false positives)
    - Used by data science teams at companies like Netflix, Airbnb, and Booking.com
    - Works well even when sample sizes are unequal between variants
    
    **Two separate tests:**
    - **Average Order Value (AOV):** Only looks at customers who purchased (compares spending among converters)
    - **Revenue Per Visitor (RPV/ARPU):** Looks at all visitors, including those who didn't buy (the real business metric)
    
    **Real-world example:**
    - Control AOV: $95.00 (among 280 purchasers)
    - Variant AOV: $102.50 (among 312 purchasers)
    - This test tells you if that $7.50 difference is statistically significant, accounting for the variability in order values
    """)

with method_tab3:
    st.markdown("""
    ### Sample Size & MDE Calculation
    
    **What it does:**  
    Calculates how many visitors you need to reliably detect a specific lift (your Minimum Detectable Effect).
    
    **The Math:**
    Uses the standard formula for comparing two proportions:
    
    `n = [(Z_α × √(2p̄(1-p̄)) + Z_β × √(p₁(1-p₁) + p₂(1-p₂)))² / (p₂ - p₁)²]`
    
    Where:
    - `Z_α` = Z-score for significance level (1.96 for 95% confidence)
    - `Z_β` = Z-score for statistical power (0.84 for 80% power)
    - `p₁` = baseline conversion rate
    - `p₂` = expected conversion rate after lift
    - `p̄` = pooled probability
    
    **Key parameters:**
    - **Alpha (α = 0.05):** 5% chance of false positive (finding significance when there isn't any)
    - **Power (1 - β = 0.80):** 80% chance of detecting a real effect when it exists
    - These are industry-standard values used by professional experimenters
    
    **Why it matters:**
    - Running a test with too few visitors = wasting time on inconclusive results
    - MDE helps you plan realistic tests based on your traffic levels
    - If you need to detect a 5% lift but only have traffic for 20% MDE, you'll need to either:
        - Run the test much longer
        - Focus on bigger, bolder changes
        - Accept that you might miss smaller wins
    
    **The traffic vs. sensitivity tradeoff:**
    - Detecting a **5% lift** requires ~4× more traffic than detecting a **10% lift**
    - Detecting a **10% lift** requires ~4× more traffic than detecting a **20% lift**
    - This is why high-traffic sites can detect smaller optimizations
    
    **Real-world example:**
    - Baseline: 2.8% conversion rate
    - MDE: 10% relative lift (2.8% → 3.08%)
    - Required: ~31,000 visitors per variant = 62,000 total
    - At 2,000 visitors/day, you'd need to run the test for 31 days
    """)

with method_tab4:
    st.markdown("""
    ### Why Statistical Significance Matters
    
    **The core problem:**  
    Random chance creates variation in test results. Without statistical testing, you can't tell the difference between:
    - A real improvement that will persist when you ship the variant
    - Random noise that will disappear with more data
    
    **Real example of the problem:**
    Imagine you flip a coin 10 times and get 6 heads. Is the coin biased? Probably not — that could easily happen by chance.  
    But if you flip it 10,000 times and get 6,000 heads? Now we can be confident something's up.
    
    **What p-value actually means:**
    - **p-value = 0.03** means: "If there were truly no difference between control and variant, there's only a 3% chance we'd see results this extreme"
    - **Not** "there's a 97% chance the variant is better" (common misconception)
    - **Not** "the variant will definitely give these results in production"
    
    **Why we use p < 0.05 as the threshold:**
    - It's a convention, not a law of nature
    - Means we accept a 5% false positive rate (1 in 20 "winners" might be flukes)
    - For critical business decisions, you might want p < 0.01 (99% confidence)
    - For quick learning, some teams accept p < 0.10 (90% confidence)
    
    **Common pitfalls this calculator helps you avoid:**
    
    1. **Peeking problem:**  
       Checking results daily and stopping when you see significance inflates false positive rate. Solution: pre-calculate required sample size and commit to running until you hit it.
    
    2. **Sample size too small:**  
       With 50 conversions per variant, even a 20% lift might not reach significance. Solution: use the MDE calculator to plan appropriately.
    
    3. **Stopping too early:**  
       Tests need to run for complete business cycles (usually 1-2 weeks minimum) to account for day-of-week effects, paycheck timing, etc.
    
    4. **Multiple metrics problem:**  
       Testing 20 metrics simultaneously increases false positive risk (even random data will show 1 in 20 as "significant"). This is why we focus on your primary KPIs.
    
    **Why these specific tests?**
    - **Z-test for conversion rates** → This is the industry standard, used by every major testing platform
    - **Welch's t-test for revenue** → More robust than Student's t-test when variances differ (which they always do with revenue data)
    - These aren't proprietary methods — they're fundamental statistical techniques taught in graduate-level statistics courses and used across industries
    
    **Peer review & validation:**
    - These methods are documented in:
        - "Trustworthy Online Controlled Experiments" by Kohavi, Tang & Xu (Microsoft Research)
        - "Statistical Methods in Online A/B Testing" by Georgi Georgiev
        - Academic papers from tech companies (Google, Netflix, Microsoft, Booking.com)
    - If you want to verify the math, you can compare results against:
        - [Evan Miller's A/B Test Calculator](https://www.evanmiller.org/ab-testing/)
        - [AB Testguide Calculator](https://abtestguide.com/calc/)
        - The `scipy.stats` library functions we use are peer-reviewed open source implementations
    
    **When this calculator might not be appropriate:**
    - Very small sample sizes (< 30 conversions per variant) → consider sequential testing methods instead
    - Non-independent observations (e.g., same user counted multiple times) → need more advanced clustering techniques
    - Multiple variants or complex experiments → requires multiple comparison corrections (Bonferroni, Šidák, etc.)
    - Very skewed revenue distributions → might need bootstrapping or non-parametric tests
    
    For the vast majority of e-commerce A/B tests with clean data and standard setups, this calculator provides reliable, industry-standard statistical analysis.
    """)

st.markdown("---")

# References section
st.markdown("### 📖 References & Further Reading")

st.markdown("""
**Books:**
- Kohavi, R., Tang, D., & Xu, Y. (2020). *Trustworthy Online Controlled Experiments: A Practical Guide to A/B Testing*. Cambridge University Press.
- Georgiev, G. (2019). *Statistical Methods in Online A/B Testing*. 

**Online Resources:**
- [Evan Miller's A/B Testing Formulas](https://www.evanmiller.org/ab-testing/)
- [Netflix Tech Blog on A/B Testing](https://netflixtechblog.com/tagged/ab-testing)
- [Optimizely Stats Engine Documentation](https://www.optimizely.com/optimization-glossary/statistical-significance/)
- [SciPy Stats Documentation](https://docs.scipy.org/doc/scipy/reference/stats.html)

**Academic Papers:**
- Welch, B.L. (1947). "The generalization of 'Student's' problem when several different population variances are involved." *Biometrika* 34(1-2): 28-35.
- Kohavi, R., et al. (2009). "Controlled experiments on the web: survey and practical guide." *Data Mining and Knowledge Discovery* 18(1): 140-181.
""")
