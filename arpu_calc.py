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

# Header
st.markdown("<h1>🎯 CRO Test Calculator</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Calculate statistical significance for conversion optimization tests</p>", unsafe_allow_html=True)

st.markdown("---")

# Input Section
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

**💡 Pro Tips:**
- Run tests for at least 2 weeks to account for weekly patterns
- Aim for minimum 100 conversions per variation for reliable results
- Don't stop tests early just because you see significance
- Consider business significance, not just statistical significance
""")
