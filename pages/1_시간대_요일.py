import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="시간대 & 요일 범죄 통계 대시보드",
    page_icon="⏰",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.stApp { background-color: #f4f6fa; font-family: 'Inter', sans-serif; }
h1, h2, h3 { color: #0d2461 !important; }
p, div, label, .stCaption { color: #1e2a3a !important; font-family: 'Inter', sans-serif !important; }

[data-testid="stSidebar"] { background: #ffffff !important; border-right: 1px solid #dde3ee !important; }
[data-testid="stSidebar"] * { color: #0d2461 !important; }

/* 셀렉트박스 배경 밝게 */
[data-baseweb="select"] > div:first-child {
    background-color: #f0f4ff !important;
    border-color: #b8c8e8 !important;
}
[data-baseweb="select"] span { color: #0d2461 !important; font-weight: 600 !important; }
[data-baseweb="popover"] { background-color: #ffffff !important; }
[data-baseweb="menu"] { background-color: #ffffff !important; }
ul[role="listbox"] { background-color: #ffffff !important; }
li[role="option"] { background-color: #ffffff !important; color: #0d2461 !important; }
li[role="option"]:hover { background-color: #eef2fa !important; color: #0d2461 !important; }

.stSelectbox label { color: #0d2461 !important; font-weight: 600 !important; font-size: 13px !important; }

.page-header { background: #0d2461; border-radius: 10px 10px 0 0; padding: 20px 28px 16px; }
.header-badge-row { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
.header-star {
    width: 22px; height: 22px; background: #c9a84c; flex-shrink: 0;
    clip-path: polygon(50% 0%,61% 35%,98% 35%,68% 57%,79% 91%,50% 70%,21% 91%,32% 57%,2% 35%,39% 35%);
}
.header-org { font-size: 11px; font-weight: 600; color: rgba(255,255,255,0.9); letter-spacing: 2px; text-transform: uppercase; }
.header-title { font-size: 22px; font-weight: 700; color: #ffffff; }
.header-gold-line { height: 2px; background: linear-gradient(90deg, #c9a84c 0%, transparent 55%); margin-top: 12px; }
.header-subbar { background: #0d2461; border-radius: 0 0 8px 8px; padding: 8px 28px; font-size: 13px; font-weight: 600; color: #ffffff; margin-bottom: 20px; }

[data-testid="stMetric"] {
    background: #ffffff !important;
    border: 1px solid #dde3ee !important;
    border-top: 2.5px solid #0d2461 !important;
    border-radius: 8px !important;
    padding: 14px 16px !important;
}
[data-testid="stMetricLabel"] { color: #4a5568 !important; font-size: 12px !important; font-weight: 600 !important; }
[data-testid="stMetricValue"] { color: #0d2461 !important; font-size: 22px !important; font-weight: 700 !important; }

hr { border-color: #dde3ee !important; }

/* 헤더 내부 텍스트 강제 흰색 */
.page-header, .page-header * { color: #ffffff !important; }
.header-org { color: rgba(255,255,255,0.88) !important; }
.header-subbar, .header-subbar * { color: #ffffff !important; }

.chart-card { background: #ffffff; border: 1px solid #dde3ee; border-radius: 10px; padding: 18px 20px; margin-bottom: 12px; }
.chart-title { font-size: 14px; font-weight: 700; color: #0d2461; margin-bottom: 4px; }
.chart-sub { font-size: 11px; color: #4a5568; margin-bottom: 12px; }

.page-footer { border-top: 1px solid #dde3ee; padding: 10px 0 4px; font-size: 11px; color: #4a5568; }
</style>
""", unsafe_allow_html=True)

# ── 차트 공통 레이아웃
CHART_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="#f8faff",
    font=dict(family="Inter, sans-serif", color="#3a4660"),
)

@st.cache_data
def load_data():
    return pd.read_csv("경찰청_범죄 발생 시간대 및 요일_20191231.csv", encoding="cp949")

df = load_data()

TIME_COLM = [
    "0시00분-02시59분","03시00분-05시59분","06시00분-08시59분","09시00분-11시59분",
    "12시00분-14시59분","15시00분-17시59분","18시00분-20시59분","21시00분-23시59분"
]
TIME_LAB = ["0~3시","3~6시","6~9시","9~12시","12~15시","15~18시","18~21시","21~24시"]
DAY_COLM = ["월","화","수","목","금","토","일"]

# ── 헤더
st.markdown("""
<div class="page-header">
    <div class="header-badge-row">
        <div class="header-star"></div>
        <div class="header-org">경찰청 · Korea National Police Agency</div>
    </div>
    <div class="header-title">⏰ 시간대 & 요일 범죄 통계</div>
    <div class="header-gold-line"></div>
</div>
<div class="header-subbar">2024년 경찰청 범죄 통계 · 시간대 및 요일별 발생 패턴 분석</div>
""", unsafe_allow_html=True)

# ── 사이드바 필터
category = ["전체"] + sorted(df["범죄대분류"].unique().tolist())
selected_category = st.sidebar.selectbox("범죄 대분류 선택", category)
filtered = df if selected_category == "전체" else df[df["범죄대분류"] == selected_category]

category2 = ["전체"] + sorted(filtered["범죄중분류"].unique().tolist())
selected_category2 = st.sidebar.selectbox("범죄 중분류 선택", category2)
if selected_category2 != "전체":
    filtered = filtered[filtered["범죄중분류"] == selected_category2]

st.sidebar.markdown("---")
st.sidebar.page_link("pages/3_챗봇.py", label="👮 안전이 챗봇으로 상담하기")

# ── 사이드바 경찰관 캐릭터
st.sidebar.markdown("""
<div style="text-align:center; padding: 28px 8px 12px;">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 180" width="148" height="210">
  <rect x="30" y="14" width="60" height="27" rx="9" fill="#1a3b6e"/>
  <rect x="18" y="35" width="84" height="11" rx="5" fill="#0d2461"/>
  <path d="M58,18 L62,18 L65,24 L62,31 L60,33 L58,31 L55,24 Z" fill="#c9a84c"/>
  <circle cx="60" cy="24" r="3.5" fill="#0d2461"/>
  <circle cx="60" cy="72" r="27" fill="#f8c89a"/>
  <ellipse cx="34" cy="72" rx="6" ry="8" fill="#f8c89a"/>
  <ellipse cx="86" cy="72" rx="6" ry="8" fill="#f8c89a"/>
  <circle cx="50" cy="68" r="6.5" fill="#1a1a1a"/>
  <circle cx="70" cy="68" r="6.5" fill="#1a1a1a"/>
  <circle cx="52" cy="66" r="2.5" fill="white"/>
  <circle cx="72" cy="66" r="2.5" fill="white"/>
  <path d="M44 61 Q50 58 56 61" stroke="#5c3d1a" stroke-width="2.5" fill="none" stroke-linecap="round"/>
  <path d="M64 61 Q70 58 76 61" stroke="#5c3d1a" stroke-width="2.5" fill="none" stroke-linecap="round"/>
  <ellipse cx="60" cy="77" rx="3" ry="2.5" fill="#e8a575"/>
  <path d="M51 84 Q60 93 69 84" stroke="#c07858" stroke-width="2.2" fill="none" stroke-linecap="round"/>
  <ellipse cx="42" cy="82" rx="7" ry="5" fill="#f4a4a4" opacity="0.55"/>
  <ellipse cx="78" cy="82" rx="7" ry="5" fill="#f4a4a4" opacity="0.55"/>
  <rect x="52" y="97" width="16" height="14" fill="#f8c89a"/>
  <rect x="20" y="109" width="80" height="58" rx="10" fill="#1a4db3"/>
  <polygon points="60,109 65,117 60,150 55,117" fill="#0a1428"/>
  <polygon points="50,109 60,120 52,114" fill="#2558c8"/>
  <polygon points="70,109 60,120 68,114" fill="#2558c8"/>
  <path d="M43,122 L47,118 L51,122 L51,130 L47,134 L43,130 Z" fill="#c9a84c"/>
  <circle cx="47" cy="126" r="3" fill="#0d2461"/>
  <rect x="20" y="109" width="17" height="11" rx="4" fill="#1560bf"/>
  <rect x="83" y="109" width="17" height="11" rx="4" fill="#1560bf"/>
  <rect x="21" y="112" width="15" height="2.5" fill="#c9a84c" rx="1"/>
  <rect x="84" y="112" width="15" height="2.5" fill="#c9a84c" rx="1"/>
  <rect x="3" y="109" width="20" height="46" rx="10" fill="#1a4db3"/>
  <rect x="97" y="109" width="20" height="46" rx="10" fill="#1a4db3"/>
  <ellipse cx="13" cy="158" rx="12" ry="9" fill="#eeeeee"/>
  <ellipse cx="107" cy="158" rx="12" ry="9" fill="#eeeeee"/>
  <rect x="20" y="159" width="80" height="11" rx="3" fill="#0a1428"/>
  <rect x="50" y="160" width="20" height="9" rx="2" fill="#7a5a10"/>
  <rect x="55" y="162" width="10" height="5" rx="1" fill="#c9a84c"/>
  <rect x="26" y="168" width="28" height="14" rx="5" fill="#0d2461"/>
  <rect x="66" y="168" width="28" height="14" rx="5" fill="#0d2461"/>
  <ellipse cx="40" cy="180" rx="19" ry="6" fill="#111111"/>
  <ellipse cx="80" cy="180" rx="19" ry="6" fill="#111111"/>
</svg>
<div style="font-size:12px; color:#0d2461; font-weight:700; margin-top:6px; letter-spacing:0.5px;">안전 지킴이 👮</div>
<div style="font-size:10px; color:#4a5568; margin-top:2px;">경찰청 범죄 통계 시스템</div>
</div>
""", unsafe_allow_html=True)

# ── KPI
k1, k2, k3 = st.columns(3)
k1.metric("총 범죄 건수", f"{int(filtered[TIME_COLM].sum().sum()):,} 건")
k2.metric("최다 발생 시간대", TIME_LAB[filtered[TIME_COLM].sum().values.argmax()])
k3.metric("최다 발생 요일", DAY_COLM[filtered[DAY_COLM].sum().values.argmax()])

st.markdown("<br>", unsafe_allow_html=True)

# ── 위험도 게이지 + 시간대 막대
time_ranges = [0, 3, 6, 9, 12, 15, 18, 21]
now = datetime.now().hour
time_idx = sum(1 for t in time_ranges if now >= t) - 1
current_crime = int(filtered[TIME_COLM[time_idx]].sum())
max_crime = int(filtered[TIME_COLM].sum().max())
danger_score = int(current_crime / max_crime * 100)

col_gauge, col_time = st.columns([1, 2])

with col_gauge:
    crime_label = selected_category2 if selected_category2 != "전체" else (selected_category if selected_category != "전체" else "전체 범죄")
    st.markdown(f'<div class="chart-card"><div class="chart-title">실시간 위험도 분석</div><div class="chart-sub">{TIME_LAB[time_idx]} 기준 · {crime_label}</div>', unsafe_allow_html=True)
    if danger_score <= 30:
        gauge_color, danger_label = "#1a7a3a", "안전"
    elif danger_score <= 60:
        gauge_color, danger_label = "#e8a020", "유의"
    elif danger_score <= 90:
        gauge_color, danger_label = "#c0001e", "위험"
    else:
        gauge_color, danger_label = "#800010", "고위험"
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge",
        value=danger_score,
        gauge={
            "axis": {
                "range": [0, 100],
                "tickvals": [15, 45, 75, 95],
                "ticktext": ["안전", "유의", "위험", "고위험"],
                "tickcolor": "#dde3ee",
                "tickfont": {"color": "#1e2a3a", "size": 10, "family": "Inter"},
            },
            "bar": {"color": gauge_color, "thickness": 0.22},
            "bgcolor": "#f8faff",
            "borderwidth": 0,
            "steps": [
                {"range": [0,  30], "color": "#e8f5ee"},
                {"range": [30, 60], "color": "#fff8ec"},
                {"range": [60, 90], "color": "#fff0f2"},
                {"range": [90,100], "color": "#ffe0e0"},
            ],
        }
    ))
    fig_gauge.add_annotation(
        x=0.5, y=0.22,
        text=f"<b>{danger_label}</b>",
        font=dict(size=30, color=gauge_color, family="Inter"),
        showarrow=False, xref="paper", yref="paper",
    )
    fig_gauge.update_layout(**CHART_BASE, height=270, margin=dict(t=40, b=30, l=30, r=30))
    st.plotly_chart(fig_gauge, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_time:
    st.markdown('<div class="chart-card"><div class="chart-title">시간대별 범죄 발생 건수</div><div class="chart-sub">8개 구간 기준</div>', unsafe_allow_html=True)
    time_sum = filtered[TIME_COLM].sum().values
    bar_colors = [
        "#c0001e" if v >= max_crime * 0.66 else "#e8a020" if v >= max_crime * 0.33 else "#1a4db3"
        for v in time_sum
    ]
    fig_time = go.Figure(go.Bar(
        x=TIME_LAB, y=time_sum,
        marker_color=bar_colors,
        marker_line_width=0,
        text=[f"{int(v):,}" for v in time_sum],
        textposition="outside",
        textfont=dict(color="#3a4660", size=10, family="Inter"),
    ))
    fig_time.update_layout(
        **CHART_BASE,
        xaxis=dict(title="시간대", color="#1e2a3a", tickfont=dict(color="#1e2a3a"), gridcolor="#eef0f6", linecolor="#dde3ee"),
        yaxis=dict(title="범죄 발생 건수", color="#1e2a3a", tickfont=dict(color="#1e2a3a"), gridcolor="#eef0f6", linecolor="#dde3ee"),
        height=260, margin=dict(t=10, b=10), showlegend=False,
    )
    st.plotly_chart(fig_time, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── 요일 방사형 + TOP5
col_day, col_top5 = st.columns(2)

with col_day:
    st.markdown('<div class="chart-card"><div class="chart-title">요일별 범죄 발생 건수</div><div class="chart-sub">방사형 차트</div>', unsafe_allow_html=True)
    day_sum = filtered[DAY_COLM].sum().values
    day_df = pd.DataFrame({"요일": DAY_COLM, "건수": day_sum.tolist()})
    fig_day = px.bar_polar(
        day_df, r="건수", theta="요일",
        color="건수",
        color_continuous_scale=[[0,"#eef2fa"],[0.5,"#1a4db3"],[1,"#0d2461"]],
    )
    fig_day.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        polar=dict(
            bgcolor="#f8faff",
            radialaxis=dict(color="#1e2a3a", tickfont=dict(color="#1e2a3a"), gridcolor="#dde3ee"),
            angularaxis=dict(color="#1e2a3a", tickfont=dict(color="#1e2a3a")),
        ),
        font=dict(family="Inter", color="#3a4660"),
        coloraxis_showscale=False,
        height=340, margin=dict(t=50, b=10),
    )
    st.plotly_chart(fig_day, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_top5:
    st.markdown('<div class="chart-card"><div class="chart-title">범죄 발생 TOP 5 유형</div><div class="chart-sub">중분류 기준</div>', unsafe_allow_html=True)
    crime_sum = filtered.groupby("범죄중분류")[TIME_COLM].sum().sum(axis=1)
    top5 = crime_sum.nlargest(5).reset_index()
    top5.columns = ["범죄유형","건수"]
    fig_top5 = px.bar(
        top5, x="건수", y="범죄유형", orientation="h",
        color="건수",
        color_continuous_scale=[[0,"#eef2fa"],[0.5,"#1a4db3"],[1,"#0d2461"]],
    )
    fig_top5.update_traces(
        marker_line_width=0,
        text=top5["건수"].apply(lambda x: f"{int(x):,}"),
        textposition="outside",
        textfont=dict(color="#3a4660", size=10),
    )
    fig_top5.update_layout(
        **CHART_BASE,
        coloraxis_showscale=False,
        xaxis=dict(title="발생 건수", color="#1e2a3a", tickfont=dict(color="#1e2a3a"), gridcolor="#eef0f6", linecolor="#dde3ee"),
        yaxis=dict(title="", color="#1e2a3a", tickfont=dict(color="#1e2a3a")),
        height=320, margin=dict(t=10, b=10),
    )
    st.plotly_chart(fig_top5, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── 도넛 차트
st.markdown('<div class="chart-card"><div class="chart-title">범죄 대분류 비율</div><div class="chart-sub">3% 미만 기타 처리</div>', unsafe_allow_html=True)
pie_data = df.groupby("범죄대분류")[TIME_COLM].sum().sum(axis=1).reset_index()
pie_data.columns = ["범죄대분류","건수"]
pie_data["비율"] = pie_data["건수"] / pie_data["건수"].sum() * 100
pie_data["범죄대분류"] = pie_data.apply(lambda x: x["범죄대분류"] if x["비율"] >= 3 else "기타", axis=1)
pie_data = pie_data.groupby("범죄대분류")["건수"].sum().reset_index()

fig_pie = px.pie(
    pie_data, names="범죄대분류", values="건수", hole=0.45,
    color_discrete_sequence=["#0d2461","#1a4db3","#3a6fd8","#6e9ef5","#a8c4f8","#c9a84c","#e8c97a","#9aa0ae"],
)
fig_pie.update_layout(**CHART_BASE, legend_font_color="#3a4660", margin=dict(t=20))
fig_pie.update_traces(textfont=dict(color="#ffffff", family="Inter"))
st.plotly_chart(fig_pie, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="page-footer">데이터 출처 : 경찰청 공공데이터포털 (2024년 기준)</div>', unsafe_allow_html=True)