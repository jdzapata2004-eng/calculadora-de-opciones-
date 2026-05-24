import streamlit as st

st.set_page_config(
    page_title="Derivatives Pricing Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Syne:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: #0a0a0f;
    color: #e8e8f0;
}

.stApp {
    background: #0a0a0f;
}

section[data-testid="stSidebar"] {
    background: #0f0f1a !important;
    border-right: 1px solid #1e1e2e;
}

/* Hero Section */
.hero-container {
    padding: 80px 40px 60px 40px;
    position: relative;
    overflow: hidden;
}

.hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.25em;
    color: #4ade80;
    text-transform: uppercase;
    margin-bottom: 20px;
}

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 72px;
    font-weight: 800;
    line-height: 1.0;
    color: #f0f0fa;
    margin-bottom: 8px;
    letter-spacing: -2px;
}

.hero-title span {
    color: #4ade80;
}

.hero-subtitle {
    font-family: 'DM Mono', monospace;
    font-size: 14px;
    color: #555570;
    margin-top: 24px;
    letter-spacing: 0.05em;
}

/* Model cards */
.model-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-top: 60px;
    padding: 0 40px;
    max-width: 860px;
}

.model-card {
    background: #0f0f1a;
    border: 1px solid #1e1e2e;
    border-radius: 12px;
    padding: 32px;
    transition: border-color 0.2s;
    position: relative;
    overflow: hidden;
}

.model-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
}

.model-card.green::before { background: linear-gradient(90deg, #4ade80, transparent); }
.model-card.blue::before  { background: linear-gradient(90deg, #60a5fa, transparent); }

.model-card:hover {
    border-color: #2e2e4e;
}

.card-icon {
    font-size: 28px;
    margin-bottom: 16px;
}

.card-title {
    font-family: 'Syne', sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: #f0f0fa;
    margin-bottom: 8px;
}

.card-desc {
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    color: #555570;
    line-height: 1.7;
}

.card-tag {
    display: inline-block;
    margin-top: 20px;
    padding: 4px 10px;
    border-radius: 4px;
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

.tag-green { background: #0d2b1a; color: #4ade80; border: 1px solid #1a4a2e; }
.tag-blue  { background: #0d1b2b; color: #60a5fa; border: 1px solid #1a2e4a; }

/* Divider */
.section-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #1e1e2e 20%, #1e1e2e 80%, transparent);
    margin: 48px 40px;
}

/* Stats row */
.stats-row {
    display: flex;
    gap: 40px;
    padding: 0 40px;
    margin-top: 48px;
}

.stat-item {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.stat-value {
    font-family: 'DM Mono', monospace;
    font-size: 24px;
    font-weight: 500;
    color: #4ade80;
}

.stat-label {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    color: #444460;
    letter-spacing: 0.15em;
    text-transform: uppercase;
}
</style>

<div class="hero-container">
    <div class="hero-eyebrow">// Financial Engineering Platform</div>
    <div class="hero-title">Derivatives<br><span>Pricing</span></div>
    <div class="hero-subtitle">Black-Scholes · Binomial Tree · Multi-Leg Strategies</div>
</div>

<div class="stats-row">
    <div class="stat-item">
        <div class="stat-value">2</div>
        <div class="stat-label">Pricing Models</div>
    </div>
    <div class="stat-item">
        <div class="stat-value">4</div>
        <div class="stat-label">Max Legs</div>
    </div>
    <div class="stat-item">
        <div class="stat-value">1000</div>
        <div class="stat-label">Max Steps</div>
    </div>
    <div class="stat-item">
        <div class="stat-value">∞</div>
        <div class="stat-label">Strategies</div>
    </div>
</div>

<div class="section-divider"></div>

<div class="model-grid">
    <div class="model-card green">
        <div class="card-icon">🌳</div>
        <div class="card-title">Binomial Tree</div>
        <div class="card-desc">Discrete-time model for European and American options. Supports stocks, currencies and dividend-paying assets.</div>
        <span class="card-tag tag-green">European · American</span>
    </div>
    <div class="model-card blue">
        <div class="card-icon">📐</div>
        <div class="card-title">Black-Scholes Strategies</div>
        <div class="card-desc">Multi-leg payoff builder with real-time B-S pricing. Visualize spreads, straddles, and custom strategies.</div>
        <span class="card-tag tag-blue">Multi-Leg · Payoff Chart</span>
    </div>
</div>
""", unsafe_allow_html=True)
