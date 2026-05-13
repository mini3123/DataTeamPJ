import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="장소별 범죄 통계 대시보드",
    page_icon="📍",
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
/* 헤더 내부 텍스트 강제 흰색 */
.page-header, .page-header * { color: #ffffff !important; }
.header-org { font-size: 11px; font-weight: 600; color: rgba(255,255,255,0.88) !important; letter-spacing: 2px; text-transform: uppercase; }
.header-title { font-size: 22px; font-weight: 700; color: #ffffff !important; }
.header-gold-line { height: 2px; background: linear-gradient(90deg, #c9a84c 0%, transparent 55%); margin-top: 12px; }
.header-subbar { background: #0d2461; border-radius: 0 0 8px 8px; padding: 8px 28px; font-size: 13px; font-weight: 600; margin-bottom: 20px; }
.header-subbar, .header-subbar * { color: #ffffff !important; }

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

.chart-card { background: #ffffff; border: 1px solid #dde3ee; border-radius: 10px; padding: 18px 20px; margin-bottom: 12px; }
.chart-title { font-size: 14px; font-weight: 700; color: #0d2461 !important; margin-bottom: 4px; }
.chart-sub { font-size: 11px; color: #4a5568 !important; margin-bottom: 12px; }
.page-footer { border-top: 1px solid #dde3ee; padding: 10px 0 4px; font-size: 11px; color: #4a5568 !important; }
</style>
""", unsafe_allow_html=True)

CHART_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="#f8faff",
    font=dict(family="Inter, sans-serif", color="#1e2a3a"),
)

@st.cache_data
def load_data():
    return pd.read_csv("경찰청_범죄 발생 장소별 통계_20241231.csv", encoding="cp949")

df = load_data()
PLACE_COLM = [c for c in df.columns if c not in ["범죄대분류","범죄중분류"]]

PLACE_GROUPS = {
    "주거시설": ["단독주택_다가구_다중","아파트","다세대_연립","오피스텔_원룸"],
    "도로/교통": ["일반도로","통행로_보도_골목길","고속도로","자동차 전용도로"],
    "상업시설": ["백화점","대형할인점","슈퍼마켓_소매점","편의점","시장_노점"],
    "유흥/숙박": ["숙박업소_호텔_모텔_여관","음식점","카페","주점","단란_유흥주점_나이트_클럽_카바레"],
    "공공/교육": ["학교","공원_놀이시설","관공서","의료기관","종교시설"],
}

# ── 헤더
st.markdown("""
<div class="page-header">
    <div class="header-badge-row">
        <div class="header-star"></div>
        <div class="header-org">경찰청 · Korea National Police Agency</div>
    </div>
    <div class="header-title">📍 장소별 범죄 통계</div>
    <div class="header-gold-line"></div>
</div>
<div class="header-subbar">2024년 경찰청 범죄 통계 · 62개 장소 발생 패턴 분석</div>
""", unsafe_allow_html=True)

# ── 사이드바 필터
category = ["전체"] + sorted(df["범죄대분류"].unique().tolist())
selected_category = st.sidebar.selectbox("범죄 대분류 선택", category)
filtered = df if selected_category == "전체" else df[df["범죄대분류"] == selected_category]

category2 = ["전체"] + sorted(filtered["범죄중분류"].unique().tolist())
selected_category2 = st.sidebar.selectbox("범죄 중분류 선택", category2)
if selected_category2 != "전체":
    filtered = filtered[filtered["범죄중분류"] == selected_category2]

place_sum = filtered[PLACE_COLM].sum()
place_sum = place_sum[~place_sum.index.str.contains("기타|미상")]
place_sum = place_sum.sort_values(ascending=False)
top_places = place_sum.head(15).index.tolist()
selected_place = st.sidebar.selectbox("장소 선택", top_places)

st.sidebar.markdown("---")
st.sidebar.page_link("pages/3_챗봇.py", label="👮 안전이 챗봇으로 상담하기")

st.sidebar.markdown("""
<div style="text-align:center; padding: 20px 8px 12px;">
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
c1, c2, c3 = st.columns(3)
c1.metric("총 발생 건수", f"{int(filtered[PLACE_COLM].sum().sum()):,} 건")
c2.metric("최다 발생 장소", place_sum.idxmax())
c3.metric("최다 범죄 유형", filtered.groupby("범죄중분류")[PLACE_COLM].sum().sum(axis=1).idxmax())

st.markdown("<br>", unsafe_allow_html=True)

# ── 카테고리별 막대
st.markdown('<div class="chart-card"><div class="chart-title">장소 카테고리별 범죄 발생 건수</div><div class="chart-sub">5개 카테고리 기준</div>', unsafe_allow_html=True)
grp_sums = {}
for grp, cols in PLACE_GROUPS.items():
    valid = [c for c in cols if c in filtered.columns]
    grp_sums[grp] = int(filtered[valid].sum().sum())

grp_df = pd.DataFrame(list(grp_sums.items()), columns=["카테고리","건수"]).sort_values("건수", ascending=False)
fig_grp = px.bar(
    grp_df, x="카테고리", y="건수",
    color="건수",
    color_continuous_scale=[[0,"#eef2fa"],[0.5,"#1a4db3"],[1,"#0d2461"]],
)
fig_grp.update_traces(
    marker_line_width=0,
    text=grp_df["건수"].apply(lambda x: f"{x:,}"),
    textposition="outside",
    textfont=dict(color="#111111", size=11),
)
fig_grp.update_layout(
    **CHART_BASE,
    coloraxis_showscale=False,
    xaxis=dict(title="", color="#111111", tickfont=dict(color="#111111"), gridcolor="#eef0f6", linecolor="#dde3ee"),
    yaxis=dict(title="발생 건수", title_font=dict(color="#111111"), color="#111111", tickfont=dict(color="#111111"), gridcolor="#eef0f6", linecolor="#dde3ee"),
    margin=dict(t=10, b=10),
)
st.plotly_chart(fig_grp, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── TOP10 + 도넛
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-card"><div class="chart-title">TOP 10 범죄 발생 장소</div><div class="chart-sub">기타·미상 제외</div>', unsafe_allow_html=True)
    top_n = place_sum.head(10).reset_index()
    top_n.columns = ["장소","건수"]
    fig_bar = px.bar(
        top_n, x="건수", y="장소", orientation="h",
        color="건수",
        color_continuous_scale=[[0,"#eef2fa"],[0.5,"#1a4db3"],[1,"#0d2461"]],
    )
    fig_bar.update_traces(
        marker_line_width=0,
        text=top_n["건수"].apply(lambda x: f"{int(x):,}"),
        textposition="outside",
        textfont=dict(color="#111111", size=10),
    )
    fig_bar.update_layout(
        **CHART_BASE,
        coloraxis_showscale=False,
        xaxis=dict(title="발생 건수", title_font=dict(color="#111111"), color="#111111", tickfont=dict(color="#111111"), gridcolor="#eef0f6", linecolor="#dde3ee"),
        yaxis=dict(title="", color="#111111", tickfont=dict(color="#111111")),
        height=400, margin=dict(t=10, b=10),
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown(f'<div class="chart-card"><div class="chart-title">{selected_place} · 범죄 유형 분포</div><div class="chart-sub">대분류 기준</div>', unsafe_allow_html=True)
    place_crime = df.groupby("범죄대분류")[selected_place].sum().reset_index()
    place_crime.columns = ["범죄유형","건수"]
    place_crime = place_crime[place_crime["건수"] > 0]
    place_crime["비율"] = place_crime["건수"] / place_crime["건수"].sum() * 100
    place_crime["범죄유형"] = place_crime.apply(lambda x: x["범죄유형"] if x["비율"] >= 2 else "기타", axis=1)
    place_crime = place_crime.groupby("범죄유형")["건수"].sum().reset_index()

    fig_pie = px.pie(
        place_crime, names="범죄유형", values="건수", hole=0.45,
        color_discrete_sequence=["#0d2461","#1a4db3","#3a6fd8","#6e9ef5","#a8c4f8","#c9a84c","#e8c97a","#9aa0ae"],
    )
    fig_pie.update_layout(**CHART_BASE, legend_font_color="#1e2a3a", height=400, margin=dict(t=10))
    fig_pie.update_traces(textfont=dict(color="#ffffff", family="Inter"))
    st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="page-footer">데이터 출처 : 경찰청 공공데이터포털 (2024년 기준)</div>', unsafe_allow_html=True)