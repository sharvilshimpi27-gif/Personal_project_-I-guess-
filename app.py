import streamlit as st
import pandas as pd
from datetime import datetime
import yfinance as yf

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MKTVIEW",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Theme toggle ───────────────────────────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

# ── CSS ────────────────────────────────────────────────────────────────────────
def get_css(dark: bool) -> str:
    if dark:
        bg        = "#0a0a0f"
        bg2       = "#111118"
        bg3       = "#1a1a24"
        border    = "#2a2a38"
        text      = "#e8e8f0"
        muted     = "#6b6b80"
        accent    = "#00e5a0"
        accent2   = "#ff4d6d"
        accent3   = "#4d9fff"
        card_bg   = "#13131c"
    else:
        bg        = "#f4f4f8"
        bg2       = "#ffffff"
        bg3       = "#eaeaf0"
        border    = "#d0d0e0"
        text      = "#0f0f1a"
        muted     = "#7070888"
        accent    = "#00a572"
        accent2   = "#e02040"
        accent3   = "#1a6fd4"
        card_bg   = "#ffffff"

    return f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Outfit:wght@200;300;400;600;700&display=swap');

    /* ── Reset & base ── */
    html, body, [data-testid="stAppViewContainer"] {{
        background: {bg} !important;
        color: {text} !important;
        font-family: 'Outfit', sans-serif;
    }}
    [data-testid="stSidebar"] {{
        background: {bg2} !important;
        border-right: 1px solid {border} !important;
    }}
    [data-testid="stSidebar"] * {{ color: {text} !important; }}

    /* ── Hide default streamlit chrome ── */
    #MainMenu, footer, header {{ visibility: hidden; }}
    .block-container {{ padding: 2rem 2.5rem 4rem !important; max-width: 1400px; }}

    /* ── Wordmark ── */
    .wordmark {{
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        font-size: 1.5rem;
        letter-spacing: 0.18em;
        color: {text};
        margin-bottom: 0.2rem;
    }}
    .wordmark span {{ color: {accent}; }}

    /* ── Page title ── */
    .page-title {{
        font-size: 2.6rem;
        font-weight: 700;
        letter-spacing: -0.03em;
        color: {text};
        line-height: 1.1;
    }}
    .page-subtitle {{
        font-family: 'DM Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 0.12em;
        color: {muted};
        text-transform: uppercase;
        margin-top: 0.3rem;
    }}

    /* ── Metric cards ── */
    .metric-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1px;
        background: {border};
        border: 1px solid {border};
        border-radius: 12px;
        overflow: hidden;
        margin: 1.8rem 0;
    }}
    .metric-card {{
        background: {card_bg};
        padding: 1.4rem 1.6rem;
        position: relative;
    }}
    .metric-card::after {{
        content: '';
        position: absolute;
        bottom: 0; left: 1.6rem; right: 1.6rem;
        height: 2px;
        background: transparent;
    }}
    .metric-card.up::after   {{ background: {accent};  }}
    .metric-card.down::after {{ background: {accent2}; }}
    .metric-card.neutral::after {{ background: {accent3}; }}

    .metric-label {{
        font-family: 'DM Mono', monospace;
        font-size: 0.65rem;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: {muted};
        margin-bottom: 0.6rem;
    }}
    .metric-value {{
        font-size: 1.85rem;
        font-weight: 600;
        letter-spacing: -0.03em;
        color: {text};
        line-height: 1;
    }}
    .metric-delta {{
        font-family: 'DM Mono', monospace;
        font-size: 0.72rem;
        margin-top: 0.5rem;
    }}
    .metric-delta.up   {{ color: {accent};  }}
    .metric-delta.down {{ color: {accent2}; }}

    /* ── Section headers ── */
    .section-header {{
        display: flex;
        align-items: baseline;
        gap: 1rem;
        margin: 2rem 0 1rem;
        padding-bottom: 0.6rem;
        border-bottom: 1px solid {border};
    }}
    .section-title {{
        font-size: 0.75rem;
        font-family: 'DM Mono', monospace;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: {muted};
    }}
    .section-dot {{
        width: 6px; height: 6px;
        border-radius: 50%;
        background: {accent};
        display: inline-block;
        margin-right: 0.5rem;
    }}

    /* ── Table ── */
    .styled-table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 0.88rem;
    }}
    .styled-table th {{
        font-family: 'DM Mono', monospace;
        font-size: 0.62rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: {muted};
        text-align: left;
        padding: 0.7rem 1rem;
        border-bottom: 1px solid {border};
        font-weight: 400;
    }}
    .styled-table td {{
        padding: 0.8rem 1rem;
        border-bottom: 1px solid {border}55;
        color: {text};
        font-variant-numeric: tabular-nums;
    }}
    .styled-table tr:last-child td {{ border-bottom: none; }}
    .styled-table tr:hover td {{ background: {bg3}; }}
    .tag-up   {{ color: {accent};  }}
    .tag-down {{ color: {accent2}; }}

    /* ── Ticker banner ── */
    .ticker-wrap {{
        background: {bg2};
        border: 1px solid {border};
        border-radius: 8px;
        padding: 0.7rem 1.2rem;
        font-family: 'DM Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 0.08em;
        color: {muted};
        margin-bottom: 1.5rem;
        overflow: hidden;
        white-space: nowrap;
    }}
    .ticker-item {{ display: inline-block; margin-right: 2.5rem; }}
    .ticker-item b {{ color: {text}; font-weight: 500; margin-right: 0.4rem; }}
    .ticker-item .up   {{ color: {accent};  }}
    .ticker-item .down {{ color: {accent2}; }}

    /* ── Sidebar nav ── */
    .nav-item {{
        padding: 0.55rem 0.9rem;
        border-radius: 6px;
        margin-bottom: 0.2rem;
        font-size: 0.82rem;
        font-weight: 400;
        cursor: pointer;
        color: {muted};
        letter-spacing: 0.04em;
    }}
    .nav-item.active {{
        background: {bg3};
        color: {text};
        font-weight: 600;
    }}

    /* ── Streamlit overrides ── */
    .stSelectbox label, .stMultiSelect label, .stSlider label,
    .stTextInput label, .stDateInput label {{
        font-family: 'DM Mono', monospace !important;
        font-size: 0.65rem !important;
        letter-spacing: 0.12em !important;
        text-transform: uppercase !important;
        color: {muted} !important;
    }}
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {{
        background: {bg3} !important;
        border-color: {border} !important;
        color: {text} !important;
        font-family: 'DM Mono', monospace !important;
        font-size: 0.82rem !important;
    }}
    .stButton button {{
        background: {accent} !important;
        color: #000 !important;
        border: none !important;
        border-radius: 6px !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: 0.04em !important;
        padding: 0.45rem 1.2rem !important;
    }}
    .stButton button:hover {{ opacity: 0.85 !important; }}
    div[data-testid="stMetric"] {{
        background: {card_bg};
        border: 1px solid {border};
        border-radius: 10px;
        padding: 1rem 1.2rem;
    }}
    </style>
    """

st.markdown(get_css(st.session_state.dark_mode), unsafe_allow_html=True)

# ── Real data helpers ──────────────────────────────────────────────────────────
TICKERS = ['RELIANCE.ns', 'HDFCBANK.ns', 'BHARTIARTL.ns', 'TCS.ns', 'ICICIBANK.ns', 'SBIN.ns', 'INFY.ns',
                      'BAJFINANCE.ns', 'HINDUNILVR.ns', 'LICI.ns', 'LT.ns', 'ITC.ns', 'MARUTI.ns', 'M&M.ns',
                      'HCLTECH.ns', 'KOTAKBANK.ns', 'SUNPHARMA.ns', 'AXISBANK.ns', 'ULTRACEMCO.ns', 'BAJAJFINSV.ns',
                      'TITAN.ns', 'NTPC.ns', 'HAL.ns', 'ADANIPORTS.ns', 'ONGC.ns', 'ETERNAL.ns', 'BEL.ns',
                      'ADANIENT.ns', 'DMART.ns', 'JSWSTEEL.ns', 'ADANIPOWER.ns', 'WIPRO.ns', 'POWERGRID.ns',
                      'ASIANPAINT.ns', 'BAJAJ-AUTO.ns', 'COALINDIA.ns', 'NESTLEIND.ns', 'INDIGO.ns', 'IOC.ns',
                      'TATASTEEL.ns', 'TMPV.ns', 'HINDZINC.ns', 'JIOFIN.ns', 'HYUNDAI.ns', 'GRASIM.ns', 'SBILIFE.ns',
                      'VEDL.ns', 'DLF.ns', 'EICHERMOT.ns', 'TRENT.ns', 'HINDALCO.ns', 'DIVISLAB.ns', 'HDFCLIFE.ns',
                      'LTM.ns', 'IRFC.ns', 'ADANIGREEN.ns', 'VBL.ns', 'TVSMOTOR.ns', 'PIDILITIND.ns', 'BPCL.ns',
                      'TECHM.ns', 'BAJAJHLDNG.ns', 'BRITANNIA.ns', 'AMBUJACEM.ns', 'TATACAP.ns', 'BANKBARODA.ns',
                      'CHOLAFIN.ns', 'SHRIRAMFIN.ns', 'TMCV.ns', 'PNB.ns', 'ICICIAMC.ns', 'PFC.ns', 'SOLARINDS.ns',
                      'MUTHOOTFIN.ns', 'TATAPOWER.ns', 'CIPLA.ns', 'TORNTPHARM.ns', 'GODREJCP.ns', 'LODHA.ns',
                      'HDFCAMC.ns', 'GAIL.ns', 'CANBK.ns', 'MAXHEALTH.ns', 'ENRIN.ns', 'SIEMENS.ns', 'MAZDOCK.ns',
                      'BOSCHLTD.ns', 'ABB.ns', 'MOTHERSON.ns', 'CUMMINSIND.ns', 'TATACONSUM.ns', 'LGEINDIA.ns',
                      'POLYCAB.ns', 'CGPOWER.ns', 'UNIONBANK.ns', 'ADANIENSOL.ns', 'APOLLOHOSP.ns', 'INDHOTEL.ns',
                      'HEROMOTOCO.ns']

@st.cache_data(ttl=60)
def real_price(ticker):
    try:
        data = yf.Ticker(ticker)
        hist = data.history(period="2d")
        if len(hist) < 2:
            return 0, 0, 0
        prev_close = hist["Close"].iloc[0]
        curr_close = hist["Close"].iloc[1]
        change = round(curr_close - prev_close, 2)
        change_pct = round((change / prev_close) * 100, 2)
        return round(curr_close, 2), change, change_pct
    except:
        return 0, 0, 0

@st.cache_data(ttl=60)
def fake_ohlc(ticker, days=90):
    try:
        period = f"{days}d"
        hist = yf.Ticker(ticker).history(period=period)
        hist = hist.reset_index()[["Date", "Close"]].rename(columns={"Close": "Price"})
        hist["Date"] = pd.to_datetime(hist["Date"]).dt.tz_localize(None)
        return hist
    except:
        return pd.DataFrame({"Date": [], "Price": []})

@st.cache_data(ttl=60)
def watchlist_data():
    rows = []
    for t in TICKERS:
        try:
            info = yf.Ticker(t).fast_info
            p, c, cp = real_price(t)
            vol = round(info.three_month_average_volume / 1e6, 1)
            mkt = round(info.market_cap / 1e9, 1)
        except:
            p, c, cp = real_price(t)
            vol, mkt = 0, 0
        rows.append({"Ticker": t, "Price": p, "Change": c, "Change %": cp,
                     "Volume (M)": vol, "Mkt Cap (B)": mkt})
    return pd.DataFrame(rows)

@st.cache_data(ttl=60)
def major_indices(ticker):
    data = yf.Ticker(ticker)
    hist = data.history(period="2d")
    if len(hist) < 2:
        return 0, 0, 0
    prev_close = hist["Close"].iloc[0]
    curr_close = hist["Close"].iloc[1]
    change = round(curr_close - prev_close, 2)
    change_pct = round((change / prev_close) * 100, 2)
    ret_val = [curr_close, change_pct]
    return ret_val

@st.cache_data(ttl=60)
def get_gainers_losers(tickers: list, top_n: int = 3) -> dict:

    data = yf.download(tickers, period="2d")["Close"]

    if isinstance(data, pd.Series):
        data = data.to_frame(name=tickers[0])

    pct_change = data.pct_change().iloc[1] * 100
    pct_change = pct_change.dropna().sort_values(ascending=False)

    latest_price = data.iloc[1]

    all_tuples = [
        (ticker, round(float(pct_change[ticker]), 2), round(float(latest_price[ticker]), 2))
        for ticker in pct_change.index
    ]

    return {
        "gainers": all_tuples[:top_n],
        "losers":  all_tuples[-top_n:]
    }

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="wordmark">MKT<span>VIEW</span></div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.65rem;letter-spacing:0.1em;opacity:0.4;margin-bottom:1.5rem">MARKET INTELLIGENCE</div>', unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        ["◈  Overview", "◉  Watchlist", "◎  Chart", "◌  Portfolio", "⬡  Settings"],
        label_visibility="collapsed"
    )

    st.markdown("---")

    # Night mode toggle
    mode_label = "☀  Light Mode" if st.session_state.dark_mode else "☾  Dark Mode"
    if st.button(mode_label):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

    st.markdown('<div style="font-size:0.6rem;opacity:0.3;margin-top:2rem;letter-spacing:0.08em">v0.1.0 · MKTVIEW</div>', unsafe_allow_html=True)

# ── Strip emoji prefix from page name ─────────────────────────────────────────
page_name = page.split("  ")[-1]

# ── Ticker banner ──────────────────────────────────────────────────────────────
items = ""
for t in TICKERS[:6]:
    p, c, cp = real_price(t)
    cls = "up" if c >= 0 else "down"
    sign = "+" if c >= 0 else ""
    items += f'<span class="ticker-item"><b>{t}</b> ₹{p} <span class="{cls}">{sign}{cp}%</span></span>'

st.markdown(f'<div class="ticker-wrap">{items}</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
if page_name == "Overview":
    st.markdown('<div class="page-title">Market Overview</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-subtitle">Last updated · {datetime.now().strftime("%d %b %Y, %H:%M")}</div>', unsafe_allow_html=True)

    # ── Key indices ────────────────────────────────────────────────────────────
    idx = {
        "NIFTY 50":  major_indices('^NSEI'),
        "NIFTY MIDCAP 150":   major_indices('NIFTYMIDCAP150.ns'),
        "BSE SENSEX": major_indices('^BSESN'),
        "NIFTY Bank": major_indices('^NSEBANK'),
    }
    cards = ""
    for label, (val, chg) in idx.items():
        sign = "+" if chg >= 0 else ""
        cls  = "up" if chg >= 0 else "down"
        arr  = "▲" if chg >= 0 else "▼"
        cards += f"""
        <div class="metric-card {cls}">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{val:,.2f}</div>
            <div class="metric-delta {cls}">{arr} {sign}{chg}%</div>
        </div>"""

    st.markdown(f'<div class="metric-grid">{cards}</div>', unsafe_allow_html=True)

    # ── Top movers ─────────────────────────────────────────────────────────────
    st.markdown('<div class="section-header"><span class="section-dot"></span><span class="section-title">Top Movers</span></div>', unsafe_allow_html=True)

    nifty_top_list = ['RELIANCE.ns', 'HDFCBANK.ns', 'BHARTIARTL.ns', 'TCS.ns', 'ICICIBANK.ns', 'SBIN.ns', 'INFY.ns',
                      'BAJFINANCE.ns', 'HINDUNILVR.ns', 'LICI.ns', 'LT.ns', 'ITC.ns', 'MARUTI.ns', 'M&M.ns',
                      'HCLTECH.ns', 'KOTAKBANK.ns', 'SUNPHARMA.ns', 'AXISBANK.ns', 'ULTRACEMCO.ns', 'BAJAJFINSV.ns',
                      'TITAN.ns', 'NTPC.ns', 'HAL.ns', 'ADANIPORTS.ns', 'ONGC.ns', 'ETERNAL.ns', 'BEL.ns',
                      'ADANIENT.ns', 'DMART.ns', 'JSWSTEEL.ns', 'ADANIPOWER.ns', 'WIPRO.ns', 'POWERGRID.ns',
                      'ASIANPAINT.ns', 'BAJAJ-AUTO.ns', 'COALINDIA.ns', 'NESTLEIND.ns', 'INDIGO.ns', 'IOC.ns',
                      'TATASTEEL.ns', 'TMPV.ns', 'HINDZINC.ns', 'JIOFIN.ns', 'HYUNDAI.ns', 'GRASIM.ns', 'SBILIFE.ns',
                      'VEDL.ns', 'DLF.ns', 'EICHERMOT.ns', 'TRENT.ns', 'HINDALCO.ns', 'DIVISLAB.ns', 'HDFCLIFE.ns',
                      'LTM.ns', 'IRFC.ns', 'ADANIGREEN.ns', 'VBL.ns', 'TVSMOTOR.ns', 'PIDILITIND.ns', 'BPCL.ns',
                      'TECHM.ns', 'BAJAJHLDNG.ns', 'BRITANNIA.ns', 'AMBUJACEM.ns', 'TATACAP.ns', 'BANKBARODA.ns',
                      'CHOLAFIN.ns', 'SHRIRAMFIN.ns', 'TMCV.ns', 'PNB.ns', 'ICICIAMC.ns', 'PFC.ns', 'SOLARINDS.ns',
                      'MUTHOOTFIN.ns', 'TATAPOWER.ns', 'CIPLA.ns', 'TORNTPHARM.ns', 'GODREJCP.ns', 'LODHA.ns',
                      'HDFCAMC.ns', 'GAIL.ns', 'CANBK.ns', 'MAXHEALTH.ns', 'ENRIN.ns', 'SIEMENS.ns', 'MAZDOCK.ns',
                      'BOSCHLTD.ns', 'ABB.ns', 'MOTHERSON.ns', 'CUMMINSIND.ns', 'TATACONSUM.ns', 'LGEINDIA.ns',
                      'POLYCAB.ns', 'CGPOWER.ns', 'UNIONBANK.ns', 'ADANIENSOL.ns', 'APOLLOHOSP.ns', 'INDHOTEL.ns',
                      'HEROMOTOCO.ns']
    result = get_gainers_losers(nifty_top_list, top_n=3)
    gainers = result["gainers"]
    losers = result["losers"]

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Gainers**", help="Top gaining stocks today")
        rows = "".join([
            f"<tr><td>{t}</td><td>₹{p:.2f}</td><td class='tag-up'>+{c}%</td></tr>"
            for t, c, p in gainers
        ])
        st.markdown(f"""
        <table class="styled-table">
            <thead><tr><th>Ticker</th><th>Price</th><th>Change</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>""", unsafe_allow_html=True)

    with col2:
        st.markdown("**Losers**", help="Top losing stocks today")
        rows = "".join([
            f"<tr><td>{t}</td><td>₹{p:.2f}</td><td class='tag-down'>{c}%</td></tr>"
            for t, c, p in losers
        ])
        st.markdown(f"""
        <table class="styled-table">
            <thead><tr><th>Ticker</th><th>Price</th><th>Change</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>""", unsafe_allow_html=True)

    # ── Sector heat ───────────────────────────────────────────────────────────
    st.markdown('<div class="section-header"><span class="section-dot"></span><span class="section-title">Sector Performance</span></div>', unsafe_allow_html=True)

    sectors = {
        "Technology": +1.82, "Healthcare": +0.45, "Financials": -0.22,
        "Energy": -1.14, "Consumer": +0.67, "Industrials": +0.33,
        "Materials": -0.88, "Utilities": +0.11,
    }
    df_sec = pd.DataFrame(list(sectors.items()), columns=["Sector", "Return %"])
    st.bar_chart(df_sec.set_index("Sector"), height=220)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: WATCHLIST
# ══════════════════════════════════════════════════════════════════════════════
elif page_name == "Watchlist":
    st.markdown('<div class="page-title">Watchlist</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Track your selected securities</div>', unsafe_allow_html=True)

    df = watchlist_data()

    # Filters
    col1, col2 = st.columns([2, 1])
    with col1:
        selected = st.multiselect("Filter Tickers", TICKERS, default=TICKERS[:6])
    with col2:
        sort_col = st.selectbox("Sort By", ["Ticker", "Price", "Change %", "Volume (M)", "Mkt Cap (B)"])

    df_filtered = df[df["Ticker"].isin(selected)].sort_values(sort_col, ascending=False)

    rows = ""
    for _, r in df_filtered.iterrows():
        cls  = "tag-up" if r["Change"] >= 0 else "tag-down"
        sign = "+" if r["Change"] >= 0 else ""
        arr  = "▲" if r["Change"] >= 0 else "▼"
        rows += f"""<tr>
            <td><b>{r['Ticker']}</b></td>
            <td>₹{r['Price']:,.2f}</td>
            <td class='{cls}'>{arr} {sign}{r['Change']}</td>
            <td class='{cls}'>{sign}{r['Change %']}%</td>
            <td>{r['Volume (M)']}M</td>
            <td>₹{r['Mkt Cap (B)']}B</td>
        </tr>"""

    st.markdown(f"""
    <table class="styled-table">
        <thead><tr>
            <th>Ticker</th><th>Price</th><th>Change</th>
            <th>Change %</th><th>Volume</th><th>Mkt Cap</th>
        </tr></thead>
        <tbody>{rows}</tbody>
    </table>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: CHART
# ══════════════════════════════════════════════════════════════════════════════
elif page_name == "Chart":
    st.markdown('<div class="page-title">Price Chart</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Historical price visualization</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        ticker = st.selectbox("Select Ticker", TICKERS)
    with col2:
        period = st.selectbox("Period", ["30D", "60D", "90D", "180D"])

    days_map = {"30D": 30, "60D": 60, "90D": 90, "180D": 180}
    df_chart = fake_ohlc(ticker, days_map[period])

    p, c, cp = real_price(ticker)
    sign = "+" if c >= 0 else ""
    col1, col2, col3 = st.columns(3)
    col1.metric("Current Price",  f"₹{p:,.2f}")
    col2.metric("Daily Change",   f"{sign}{c}",   f"{sign}{cp}%")
    col3.metric("Period High",    f"₹{df_chart['Price'].max():,.2f}")

    st.markdown('<div class="section-header"><span class="section-dot"></span>'
                f'<span class="section-title">{ticker} · {period}</span></div>', unsafe_allow_html=True)
    st.line_chart(df_chart.set_index("Date"), height=320)

    with st.expander("Raw Data"):
        st.dataframe(df_chart.sort_values("Date", ascending=False).reset_index(drop=True), height=200)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: PORTFOLIO  (placeholder — ready to build out)
# ══════════════════════════════════════════════════════════════════════════════
elif page_name == "Portfolio":
    st.markdown('<div class="page-title">Portfolio</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Track holdings & performance</div>', unsafe_allow_html=True)

    st.info("📌 Portfolio tracking coming soon — add positions, track P&L, view allocation breakdowns.")

    # Placeholder allocation donut
    alloc = pd.DataFrame({
        "Asset": ["AAPL", "MSFT", "NVDA", "TSLA", "Cash"],
        "Value": [28, 22, 18, 15, 17]
    })
    st.markdown('<div class="section-header"><span class="section-dot"></span>'
                '<span class="section-title">Sample Allocation</span></div>', unsafe_allow_html=True)
    st.bar_chart(alloc.set_index("Asset"), height=260)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: SETTINGS
# ══════════════════════════════════════════════════════════════════════════════
elif page_name == "Settings":
    st.markdown('<div class="page-title">Settings</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Customize your experience</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header"><span class="section-dot"></span>'
                '<span class="section-title">Appearance</span></div>', unsafe_allow_html=True)

    dark = st.toggle("Dark Mode", value=st.session_state.dark_mode)
    if dark != st.session_state.dark_mode:
        st.session_state.dark_mode = dark
        st.rerun()

    st.markdown('<div class="section-header"><span class="section-dot"></span>'
                '<span class="section-title">Data</span></div>', unsafe_allow_html=True)

    st.selectbox("Default Ticker", TICKERS)
    st.selectbox("Default Chart Period", ["30D", "60D", "90D", "180D"])
    st.number_input("Watchlist refresh (seconds)", min_value=10, max_value=300, value=60)

    st.markdown('<div class="section-header"><span class="section-dot"></span>'
                '<span class="section-title">Notifications</span></div>', unsafe_allow_html=True)

    st.toggle("Price alerts",       value=False)
    st.toggle("Market open/close",  value=True)
    st.toggle("Earnings reminders", value=False)

    if st.button("Save Settings"):
        st.success("Settings saved.")

