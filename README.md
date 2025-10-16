CRO Test Calculator

A statistical significance calculator built for conversion rate optimization (CRO) professionals running A/B tests on e-commerce sites. Calculate significance for conversion rates, average order value (AOV), and revenue per visitor (RPV) with proper statistical methods.

**[🚀 Live Demo](https://arpunaovstatsigcalculator-ymymjbxhwbsjrfd7ugxwnb.streamlit.app/)**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://arpunaovstatsigcalculator-ymymjbxhwbsjrfd7ugxwnb.streamlit.app/)

---

## Features

- **Multiple Statistical Tests**
  - Z-test for conversion rates
  - Welch's t-test for AOV and RPV (more robust than standard t-test)
  - Confidence level calculations for all metrics

- **Sample Size Planning**
  - Calculate required sample size based on Minimum Detectable Effect (MDE)
  - Estimate additional days needed to reach statistical significance
  - Traffic projection based on current volume

- **Visual Analysis**
  - Side-by-side comparison charts
  - Performance metrics with lift percentages
  - Clear significance indicators

- **Test Duration Recommendations**
  - Accounts for both sample size and minimum test duration (14 days)
  - Provides actionable next steps based on current progress

---

## Why This Calculator?

Most A/B testing tools either oversimplify the statistics or don't account for revenue metrics properly. This calculator:

1. **Uses industry-standard methods** — Same statistical approaches used by Netflix, Booking.com, and Microsoft Research
2. **Handles revenue correctly** — Welch's t-test for unequal variances (common in e-commerce data)
3. **Prevents premature calls** — MDE and sample size calculations help you avoid false positives
4. **Shows confidence levels** — Not just "significant/not significant" but actual confidence percentages

---

## Quick Start

### Local Installation
```bash
# Clone the repository
git clone https://github.com/robertoroiebahia/arpu_n_aov_stat_sig_calculator.git
cd arpu_n_aov_stat_sig_calculator

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run arpu_calc.py
```

### Requirements
```
streamlit>=1.18
scipy>=1.7.0
plotly
google-auth-oauthlib>=0.4.6
google-api-python-client>=2.70.0
```

---

## How to Use

### 1. Configure Your Test

- **Days Live**: How long your test has been running
- **MDE (Minimum Detectable Effect)**: The smallest lift you want to detect (typically 5-15%)

### 2. Input Your Data

**Control Group:**
- Total visitors
- Number of conversions
- Revenue per order (comma-separated list)

**Variant Group:**
- Total visitors
- Number of conversions
- Revenue per order (comma-separated list)

### 3. Review Results

The calculator provides:

- **Performance Overview**: Conversion rate, AOV, and RPV with lift percentages
- **Visual Comparisons**: Side-by-side bar charts
- **Statistical Significance**: Three separate tests with confidence levels
  - Conversion Rate Test (Z-test)
  - Revenue Per Visitor Test (Welch's t-test)
  - Average Order Value Test (Welch's t-test)
- **Duration Recommendations**: How many more days to run the test

---

## Understanding the Results

### P-value Thresholds

- **p < 0.05**: Statistically significant (95%+ confidence)
- **p 0.05-0.10**: Marginally significant (90-95% confidence)
- **p > 0.10**: Not significant (continue testing)

### Confidence Level

Shows as a percentage (e.g., 98.3% confidence) — the probability that your result isn't random chance.

### Relative Lift

The percentage improvement of variant over control. A positive number means the variant performed better.

---

## Statistical Methodology

### Conversion Rate Test (Z-Test)

Uses a two-proportion z-test to compare conversion rates:
```
Z = (p_B - p_A) / SE
where SE = √[p_pooled × (1 - p_pooled) × (1/n_A + 1/n_B)]
```

**Why Z-test?**  
Industry standard for comparing conversion rates. Based on the Central Limit Theorem, which applies with sufficiently large sample sizes.

---

### Revenue Tests (Welch's T-Test)

Uses Welch's t-test for comparing means with unequal variances:
```
t = (mean_B - mean_A) / SE_diff
where SE_diff = √[(SD_A² / n_A) + (SD_B² / n_B)]
```

**Why Welch's instead of Student's t-test?**  
E-commerce revenue data almost always has unequal variances (some customers spend $50, others $500+). Welch's t-test doesn't assume equal variances, making it more robust and accurate for real-world A/B tests.

---

### Sample Size Calculation

Uses the standard formula for comparing two proportions:
```
n = [(Z_α × √(2p̄(1-p̄)) + Z_β × √(p₁(1-p₁) + p₂(1-p₂)))² / (p₂ - p₁)²]
```

**Parameters:**
- α = 0.05 (5% false positive rate, 95% confidence)
- Power = 0.80 (80% chance of detecting real effect)
- These are industry-standard values

---

## Best Practices

1. **Run tests for at least 2 weeks** — Accounts for weekly patterns and paycheck cycles
2. **Aim for 100+ conversions per variant** — More reliable results for AOV/RPV tests
3. **Don't peek and stop early** — Increases false positive rate
4. **Consider business significance** — A statistically significant 2% lift might not be worth implementing
5. **Set realistic MDEs** — Detecting a 5% lift requires 4x more traffic than a 10% lift

---

## Common Questions

**Q: Why are conversion rate and RPV showing different significance levels?**  
A: They're measuring different things. Conversion rate only cares about yes/no (did they buy?), while RPV accounts for how much they spent. High variance in order values can make RPV harder to prove significant even when conversion rates are clearly different.

**Q: My test shows significance after 3 days. Can I call it?**  
A: No. Statistical significance isn't the only requirement. You need:
- Sufficient sample size (check the MDE calculator)
- Minimum 14 days runtime (to account for weekly patterns)
- Business impact worth the implementation cost

**Q: What MDE should I use?**  
A: Depends on your traffic:
- High-traffic sites (>100K visitors/month): 5-10% MDE
- Medium-traffic sites (10K-100K/month): 10-15% MDE
- Lower-traffic sites (<10K/month): 15-25% MDE

**Q: Can I use this for multi-variant tests?**  
A: Not directly. This calculator is for simple A/B tests (control vs. one variant). Multi-variant tests require multiple comparison corrections (Bonferroni, Šidák, etc.).

---

## References

**Books:**
- Kohavi, R., Tang, D., & Xu, Y. (2020). *Trustworthy Online Controlled Experiments: A Practical Guide to A/B Testing*. Cambridge University Press.
- Georgiev, G. (2019). *Statistical Methods in Online A/B Testing*.

**Academic Papers:**
- Welch, B.L. (1947). "The generalization of 'Student's' problem when several different population variances are involved." *Biometrika* 34(1-2): 28-35.
- Kohavi, R., et al. (2009). "Controlled experiments on the web: survey and practical guide." *Data Mining and Knowledge Discovery* 18(1): 140-181.

**Online Resources:**
- [Evan Miller's A/B Testing Formulas](https://www.evanmiller.org/ab-testing/)
- [Optimizely Stats Engine](https://www.optimizely.com/optimization-glossary/statistical-significance/)
- [SciPy Stats Documentation](https://docs.scipy.org/doc/scipy/reference/stats.html)

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

**Areas for contribution:**
- Additional statistical tests (sequential testing, Bayesian methods)
- Multi-variant support
- Export functionality (PDF reports, CSV)
- Additional visualizations
- Mobile optimization

---

## License

MIT License - feel free to use this for your own testing needs.

---

## About

Built by [Roberto Bahia](https://www.linkedin.com/in/roberto-bahia/) — CRO strategist specializing in conversion optimization and A/B testing for DTC e-commerce brands.

Questions or feedback? [Open an issue](https://github.com/robertoroiebahia/arpu_n_aov_stat_sig_calculator/issues) or connect on [LinkedIn](https://www.linkedin.com/in/roberto-bahia/).

---

## Acknowledgments

- Statistical methodology based on Microsoft Research's "Trustworthy Online Controlled Experiments"
- Built with [Streamlit](https://streamlit.io/), [SciPy](https://scipy.org/), and [Plotly](https://plotly.com/)
- Inspired by tools from ConversionXL, Evan Miller, and the experimentation community
