import pandas as pd
import streamlit as st
from google import genai
from google.genai import types
import os
import json
from datetime import datetime, timedelta

HISTORY_FILE = "chat_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_history(messages):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

st.set_page_config(
    page_title="안전이 챗봇",
    page_icon="👮",
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

/* 셀렉트박스·입력창 밝게 */
[data-baseweb="select"] > div:first-child { background-color: #f0f4ff !important; border-color: #b8c8e8 !important; }
[data-baseweb="select"] span { color: #0d2461 !important; font-weight: 600 !important; }
[data-baseweb="input"] { background-color: #f0f4ff !important; border-color: #b8c8e8 !important; }
[data-baseweb="input"] input { color: #0d2461 !important; }

/* 사이드바 버튼 밝게 */
[data-testid="stSidebar"] .stButton > button {
    background-color: #f0f4ff !important;
    color: #0d2461 !important;
    border: 1px solid #b8c8e8 !important;
    font-weight: 600 !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background-color: #dce8ff !important;
    border-color: #1a4db3 !important;
}

/* 헤더 내부 텍스트 강제 흰색 */
.page-header, .page-header * { color: #ffffff !important; }
.header-org { font-size: 11px; font-weight: 600; color: rgba(255,255,255,0.88) !important; letter-spacing: 2px; text-transform: uppercase; }
.header-title { font-size: 22px; font-weight: 700; color: #ffffff !important; }
.header-gold-line { height: 2px; background: linear-gradient(90deg, #c9a84c 0%, transparent 55%); margin-top: 12px; }
.header-subbar { background: #0d2461; border-radius: 0 0 8px 8px; padding: 8px 28px; font-size: 13px; font-weight: 600; margin-bottom: 16px; }
.header-subbar, .header-subbar * { color: #ffffff !important; }
.page-header { background: #0d2461; border-radius: 10px 10px 0 0; padding: 20px 28px 16px; }
.header-badge-row { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
.header-star {
    width: 22px; height: 22px; background: #c9a84c; flex-shrink: 0;
    clip-path: polygon(50% 0%,61% 35%,98% 35%,68% 57%,79% 91%,50% 70%,21% 91%,32% 57%,2% 35%,39% 35%);
}

hr { border-color: #dde3ee !important; }
.sidebar-char { text-align: center; padding: 12px 4px 0; }
.sidebar-char-name { font-size: 13px; font-weight: 700; color: #0d2461 !important; margin-top: 4px; }
.sidebar-char-sub { font-size: 10px; color: #4a5568 !important; margin-top: 2px; }
</style>
""", unsafe_allow_html=True)

POLICE_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 180" width="120" height="170">
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
"""

SYSTEM_PROMPT = """당신은 경찰청 범죄 통계 데이터를 기반으로 시민 안전을 도와주는 귀여운 경찰관 캐릭터 '안전이'입니다.

친절하고 따뜻한 말투로 안전 정보를 제공합니다. 존댓말을 사용하고 공손하게 응답하세요.
사용자가 특정 시간이나 장소를 언급하면 아래 통계 데이터를 참고해 안전 정보를 제공하세요.

--- 현재 날짜·시간 ---
{current_datetime}

위 정보를 바탕으로 '오늘', '내일', '모레', '이번 주말' 등 상대적 표현이 나오면 실제 날짜와 요일을 계산해서 자연스럽게 언급해 주세요.
예) 사용자가 "내일 저녁"이라고 하면 → 실제 내일 요일을 파악해 "수요일 저녁이군요!" 처럼 응답하세요.

시간 표현 관련 중요 규칙:
- 사용자가 시간을 언급할 때 오전/오후(AM/PM)가 명시되어 있지 않으면, 안전 정보를 제공하기 전에 반드시 먼저 "오전인가요, 오후인가요?"라고 확인 질문을 하세요.
- 예) "내일 10시에 친구집에 가요" → "10시가 오전인가요, 오후인가요? 😊 시간대에 따라 안전 정보가 달라질 수 있어요!"
- 단, "새벽", "아침", "점심", "저녁", "밤", "심야" 같은 시간대 표현이 함께 있으면 오전/오후를 묻지 않아도 됩니다.
- 예) "새벽 2시", "저녁 7시", "밤 11시" → 이미 시간대가 명확하므로 바로 안전 정보 제공

응답 형식:
1. 📊 해당 시간대·장소에서 발생 건수가 많은 범죄 유형 상위 2~3개 (구체적인 수치 포함)
2. ⚠️ 위험도 평가: 낮음 / 보통 / 높음 (수치 기반 판단)
3. 🛡️ 해당 범죄 유형에 맞는 맞춤형 예방 수칙 2~3가지
   - 절도가 많으면 → 소지품 관리, 귀중품 노출 자제 등
   - 폭행·강력범죄가 많으면 → 혼잡한 장소·늦은 밤 주의, 동행 권장 등
   - 성범죄가 많으면 → 혼자 이동 자제, 안전귀가 앱 활용 등
   - 교통범죄가 많으면 → 무단횡단 주의, 음주운전 신고 등

추가 안내:
- 통계 데이터는 2024년 기준입니다.
- 범죄 유형별로 다른 예방 수칙을 제시하고, 단순 "주의하세요"가 아닌 구체적 행동 지침을 주세요.
- 과도한 공포감 조성 없이 실용적인 정보를 제공하세요.

--- 범죄 통계 데이터 ---
{crime_data}"""


@st.cache_data
def build_crime_context():
    df_time = pd.read_csv("경찰청_범죄 발생 시간대 및 요일_20191231.csv", encoding="cp949")
    df_place = pd.read_csv("경찰청_범죄 발생 장소별 통계_20241231.csv", encoding="cp949")

    TIME_COLM = [
        "0시00분-02시59분", "03시00분-05시59분", "06시00분-08시59분", "09시00분-11시59분",
        "12시00분-14시59분", "15시00분-17시59분", "18시00분-20시59분", "21시00분-23시59분"
    ]
    TIME_LAB = ["0~3시", "3~6시", "6~9시", "9~12시", "12~15시", "15~18시", "18~21시", "21~24시"]
    DAY_COLM = ["월", "화", "수", "목", "금", "토", "일"]
    PLACE_COLM = [c for c in df_place.columns if c not in ["범죄대분류", "범죄중분류"]]

    time_total = df_time[TIME_COLM].sum()
    day_total  = df_time[DAY_COLM].sum()
    place_total = df_place[PLACE_COLM].sum().sort_values(ascending=False)
    place_total = place_total[~place_total.index.str.contains("기타|미상")]

    def top_crimes_str(series, n=3):
        top = series.nlargest(n)
        return ", ".join(f"{k}({int(v):,}건)" for k, v in top.items())

    # 시간대별: 총계 + 주요 범죄 유형
    lines = ["[시간대별 범죄 현황 (총계 + 주요 범죄 유형) - 2024년]"]
    for lab, col, cnt in zip(TIME_LAB, TIME_COLM, time_total):
        top = top_crimes_str(df_time.groupby("범죄중분류")[col].sum())
        lines.append(f"  {lab}: {int(cnt):,}건 / 주요유형: {top}")

    # 요일별: 총계 + 주요 범죄 유형
    lines.append("\n[요일별 범죄 현황 (총계 + 주요 범죄 유형) - 2024년]")
    for day, col, cnt in zip(DAY_COLM, DAY_COLM, day_total):
        top = top_crimes_str(df_time.groupby("범죄중분류")[col].sum())
        lines.append(f"  {day}요일: {int(cnt):,}건 / 주요유형: {top}")

    # 장소별: 총계 + 주요 범죄 유형
    lines.append("\n[장소별 범죄 현황 TOP 15 (총계 + 주요 범죄 유형) - 2024년]")
    for place, cnt in place_total.head(15).items():
        top = top_crimes_str(df_place.groupby("범죄중분류")[place].sum())
        lines.append(f"  {place}: {int(cnt):,}건 / 주요유형: {top}")

    return "\n".join(lines)


# ── 사이드바
st.sidebar.markdown(
    f'<div class="sidebar-char">{POLICE_SVG}'
    f'<div class="sidebar-char-name">안전이 👮</div>'
    f'<div class="sidebar-char-sub">경찰청 범죄 통계 안전 상담</div></div>',
    unsafe_allow_html=True
)
st.sidebar.markdown("---")

st.sidebar.markdown("**💡 예시 질문**")
EXAMPLES = [
    "밤 11시에 편의점에 가도 안전할까요?",
    "주말 저녁 공원 산책해도 괜찮을까요?",
    "새벽 2시 귀가 시 주의할 점은?",
    "금요일 밤 주점 근처를 지나야 해요",
]
for i, ex in enumerate(EXAMPLES):
    if st.sidebar.button(ex, key=f"ex{i}", use_container_width=True):
        st.session_state.queued_msg = ex
        st.rerun()

st.sidebar.markdown("---")
if st.sidebar.button("🔄 대화 초기화", use_container_width=True):
    st.session_state.messages = []
    save_history([])
    st.rerun()

_raw_key = st.secrets.get("GEMINI_API_KEY", "") or os.environ.get("GEMINI_API_KEY", "")
# ASCII가 아닌 플레이스홀더는 빈 값으로 처리
api_key = _raw_key if (_raw_key and _raw_key.isascii() and _raw_key.startswith("AIza")) else ""
if not api_key:
    api_key = st.sidebar.text_input("🔑 Gemini API 키", type="password", placeholder="AIza...")
    st.sidebar.caption(".streamlit/secrets.toml 에 저장하면 매번 입력 불필요")

# ── 메인 헤더
st.markdown("""
<div class="page-header">
    <div class="header-badge-row">
        <div class="header-star"></div>
        <div class="header-org">경찰청 · Korea National Police Agency</div>
    </div>
    <div class="header-title">👮 안전이 챗봇</div>
    <div class="header-gold-line"></div>
</div>
<div class="header-subbar">방문 예정 시간과 장소를 알려주시면 범죄 통계 기반 안전 정보를 알려드립니다</div>
""", unsafe_allow_html=True)

if not api_key:
    st.warning("⬅️ 사이드바에 Gemini API 키를 입력하면 채팅을 시작할 수 있습니다.")
    st.info("무료 API 키 발급: [aistudio.google.com](https://aistudio.google.com)")
    st.stop()

# ── 채팅 상태
if "messages" not in st.session_state:
    st.session_state.messages = load_history()

queued = st.session_state.pop("queued_msg", None)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="👮" if msg["role"] == "assistant" else "🧑"):
        st.markdown(msg["content"])

chat_prompt = st.chat_input("예: 내일 저녁 9시에 지하철역 근처를 걸어야 하는데 안전한가요?")
user_input = queued if queued else chat_prompt

if user_input:
    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    crime_data = build_crime_context()
    now = datetime.now()
    day_names = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
    tomorrow = now + timedelta(days=1)
    current_datetime = (
        f"오늘: {now.year}년 {now.month}월 {now.day}일 {day_names[now.weekday()]} "
        f"{now.hour:02d}시 {now.minute:02d}분\n"
        f"내일: {tomorrow.month}월 {tomorrow.day}일 {day_names[tomorrow.weekday()]}"
    )
    system_with_data = SYSTEM_PROMPT.format(crime_data=crime_data, current_datetime=current_datetime)

    # 핵심 수정 부분: 딕셔너리가 아닌 types.Content/Part 객체로 구성
    full_contents = []
    for msg in st.session_state.messages:
        role = "model" if msg["role"] == "assistant" else "user"
        # 각 메시지를 SDK 규격에 맞게 변환
        content_obj = types.Content(
            role=role, 
            parts=[types.Part(text=msg["content"])]
        )
        full_contents.append(content_obj)

    with st.chat_message("assistant", avatar="👮"):
        try:
            client = genai.Client(api_key=api_key)
            config = types.GenerateContentConfig(
                system_instruction=system_with_data,
                max_output_tokens=4096,
            )
            MODELS = ["gemini-2.5-flash", "gemini-2.0-flash"]

            def stream_gemini(model_name):
                for chunk in client.models.generate_content_stream(
                    model=model_name,
                    contents=full_contents,
                    config=config,
                ):
                    if chunk.text:
                        yield chunk.text

            answer = None
            for model_name in MODELS:
                try:
                    answer = st.write_stream(stream_gemini(model_name))
                    break
                except Exception as model_err:
                    err_str = str(model_err)
                    if "503" in err_str or "UNAVAILABLE" in err_str or "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                        if model_name == MODELS[-1]:
                            raise
                        continue
                    raise

        except Exception as e:
            err = str(e)
            if "API_KEY" in err.upper() or "invalid" in err.lower():
                answer = "❌ API 키가 올바르지 않아요. 사이드바에서 키를 다시 확인해 주세요!"
            elif "503" in err or "UNAVAILABLE" in err:
                answer = "⏳ 현재 Gemini 서버가 혼잡합니다. 잠시 후 다시 시도해 주세요!"
            else:
                answer = f"❌ 오류가 발생했어요: {err}"
            st.error(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    save_history(st.session_state.messages)

st.caption("⚠️ 경찰청 통계(2024년) 기반 참고 정보이며, 실제 안전을 보장하지 않습니다.")