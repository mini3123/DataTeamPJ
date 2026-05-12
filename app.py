import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="경찰청 범죄 통계 대시보드",
    page_icon="🚔",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.stApp { background-color: #f4f6fa; font-family: 'Inter', sans-serif; }

h1, h2, h3 { color: #0d2461 !important; }
p, div, label, .stCaption { color: #3a4660 !important; font-family: 'Inter', sans-serif !important; }

[data-testid="stSidebar"] { background: #ffffff !important; border-right: 1px solid #dde3ee !important; }
[data-testid="stSidebar"] * { color: #0d2461 !important; }

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
[data-testid="stMetricLabel"] { color: #4a5568 !important; font-size: 11px !important; font-weight: 500 !important; }
[data-testid="stMetricValue"] { color: #0d2461 !important; font-size: 22px !important; font-weight: 700 !important; }

/* 헤더 내부 텍스트 강제 흰색 */
.page-header, .page-header * { color: #ffffff !important; }
.header-org { color: rgba(255,255,255,0.88) !important; }
.header-subbar, .header-subbar * { color: #ffffff !important; }

hr { border-color: #dde3ee !important; }

.mod-card { background: #ffffff; border: 1px solid #dde3ee; border-radius: 10px; padding: 20px 22px; height: 100%; }
.mod-tag { display: inline-block; background: #eef2fa; color: #1a4db3; font-size: 10px; font-weight: 700; padding: 3px 9px; border-radius: 10px; margin-bottom: 10px; letter-spacing: 0.5px; }
.mod-title { font-size: 15px; font-weight: 700; color: #0d2461; margin-bottom: 10px; }
.mod-info { font-size: 13px; color: #6a7485; line-height: 1.9; margin-bottom: 14px; }
/* 보러가기 텍스트 링크 */
[data-testid="stPageLink"] { margin-top: 6px !important; }
[data-testid="stPageLink"] a {
    color: #1a4db3 !important; font-size: 13px !important; font-weight: 600 !important;
    text-decoration: underline !important; background: none !important; padding: 0 !important;
}
[data-testid="stPageLink"] a:hover { color: #0d2461 !important; }
[data-testid="stPageLink"] a *, [data-testid="stPageLink"] a p { color: inherit !important; }

.section-label { font-size: 11px; font-weight: 600; color: #4a5568; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 10px; }
.ov-card { background: #ffffff; border: 1px solid #dde3ee; border-radius: 8px; padding: 12px 14px; display: flex; align-items: flex-start; gap: 11px; }
.ov-icon { width: 32px; height: 32px; border-radius: 8px; background: #eef2fa; display: flex; align-items: center; justify-content: center; font-size: 15px; flex-shrink: 0; }
.ov-label { font-size: 10px; color: #4a5568; margin-bottom: 3px; }
.ov-val { font-size: 14px; font-weight: 700; color: #0d2461; }
.ov-desc { font-size: 11px; color: #4a5568; margin-top: 3px; line-height: 1.5; }
.pill { display: inline-block; font-size: 10px; font-weight: 600; padding: 2px 8px; border-radius: 10px; margin-right: 4px; margin-top: 5px; }
.pill-py { background: #fff8e6; color: #a07000; border: 1px solid #f0d080; }
.pill-st { background: #fff0f4; color: #b00040; border: 1px solid #f0a0b8; }
.pill-pl { background: #eef2fa; color: #1a4db3; border: 1px solid #b0c4f0; }
.page-footer { border-top: 1px solid #dde3ee; padding: 10px 0 4px; font-size: 11px; color: #4a5568; }
</style>
""", unsafe_allow_html=True)

# ── 헤더
st.markdown("""
<div class="page-header">
    <div class="header-badge-row">
        <div class="header-star"></div>
        <div class="header-org">경찰청 · Korea National Police Agency</div>
    </div>
    <div class="header-title">🚔 범죄 통계 대시보드</div>
    <div class="header-gold-line"></div>
</div>
<div class="header-subbar">경찰청 공공데이터포털 · 2024 기준 분석</div>
""", unsafe_allow_html=True)

# ── 데이터 로드
@st.cache_data
def load_time():
    return pd.read_csv("경찰청_범죄 발생 시간대 및 요일_20191231.csv", encoding="cp949")

@st.cache_data
def load_place():
    return pd.read_csv("경찰청_범죄 발생 장소별 통계_20241231.csv", encoding="cp949")

df_t = load_time()
df_p = load_place()

TIME_COLM = [
    "0시00분-02시59분","03시00분-05시59분","06시00분-08시59분","09시00분-11시59분",
    "12시00분-14시59분","15시00분-17시59분","18시00분-20시59분","21시00분-23시59분"
]
TIME_LAB = ["0~3시","3~6시","6~9시","9~12시","12~15시","15~18시","18~21시","21~24시"]
PLACE_COLM = [c for c in df_p.columns if c not in ["범죄대분류","범죄중분류"]]

total_crime = int(df_t[TIME_COLM].sum().sum())
peak_time   = TIME_LAB[df_t[TIME_COLM].sum().values.argmax()]
place_sum   = df_p[PLACE_COLM].sum()
place_sum   = place_sum[~place_sum.index.str.contains("기타|미상")]
peak_place  = place_sum.idxmax()

# ── KPI
k1, k2, k3 = st.columns(3)
k1.metric("총 범죄 건수", f"{total_crime:,} 건")
k2.metric("최다 발생 시간대", peak_time)
k3.metric("최다 발생 장소", peak_place)

st.markdown("<br>", unsafe_allow_html=True)

# ── 모듈 카드
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="mod-card">
        <div class="mod-tag">MODULE 01</div>
        <div class="mod-title">⏰ 시간대 & 요일 분석</div>
        <div class="mod-info">
            · 2024년 경찰청 공공데이터 기준<br>
            · 시간대 8구간 범죄 발생 패턴<br>
            · 요일별 발생 빈도 분석<br>
            · 현재 시간대 위험도 게이지
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/1_시간대_요일.py", label="시간대 분석 보러가기 →")

with col2:
    st.markdown("""
    <div class="mod-card">
        <div class="mod-tag">MODULE 02</div>
        <div class="mod-title">📍 장소별 통계 분석</div>
        <div class="mod-info">
            · 2024년 경찰청 공공데이터 기준<br>
            · 62개 장소 범죄 발생 통계<br>
            · 장소 카테고리별 분류 분석<br>
            · TOP 10 위험 장소 시각화
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/2_장소별.py", label="장소별 분석 보러가기 →")

with col3:
    st.markdown("""
    <div class="mod-card">
        <div class="mod-tag">MODULE 03</div>
        <div class="mod-title">👮 안전이 챗봇</div>
        <div class="mod-info">
            · Gemini AI 기반 안전 상담<br>
            · 시간대·장소 범죄 위험도 안내<br>
            · 실시간 안전 수칙 제공<br>
            · 맞춤형 대화형 인터페이스
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/3_챗봇.py", label="챗봇 이용하기 →")

st.markdown("<br>", unsafe_allow_html=True)

# ── 데이터 개요
st.markdown('<div class="section-label">데이터 개요</div>', unsafe_allow_html=True)
ov1, ov2, ov3 = st.columns(3)

with ov1:
    st.markdown("""
    <div class="ov-card">
        <div class="ov-icon">📁</div>
        <div>
            <div class="ov-label">데이터셋</div>
            <div class="ov-val">2개 파일</div>
            <div class="ov-desc">시간대·요일 / 장소별<br>경찰청 공공데이터</div>
        </div>
    </div>""", unsafe_allow_html=True)

with ov2:
    st.markdown("""
    <div class="ov-card">
        <div class="ov-icon">📅</div>
        <div>
            <div class="ov-label">분석 기간</div>
            <div class="ov-val">2024</div>
            <div class="ov-desc">각 데이터셋 기준 연도<br>별도 적용</div>
        </div>
    </div>""", unsafe_allow_html=True)

with ov3:
    st.markdown("""
    <div class="ov-card">
        <div class="ov-icon">🔧</div>
        <div>
            <div class="ov-label">분석 도구</div>
            <div class="ov-val">Tech Stack</div>
            <span class="pill pill-py">Python</span>
            <span class="pill pill-st">Streamlit</span>
            <span class="pill pill-pl">Plotly</span>
        </div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="page-footer">데이터 출처 : 경찰청 공공데이터포털</div>', unsafe_allow_html=True)