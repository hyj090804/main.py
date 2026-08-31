import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(
    page_title="서울 연평균 기온 변화",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 서울의 100년간 연평균 기온 변화")
st.write("기상청 서울 지점(108)의 일별 기온 데이터를 이용해 연평균 기온을 계산했습니다.")

# 데이터 주소
URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/seoul.csv"

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv(URL)

    # 날짜를 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(df["날짜"], errors="coerce")

    # 평균기온을 숫자로 변환
    df["평균기온"] = pd.to_numeric(df["평균기온"], errors="coerce")

    # 필요한 데이터만 남기기
    df = df.dropna(subset=["날짜", "평균기온"])

    return df


df = load_data()

# 연도 추출
df["연도"] = df["날짜"].dt.year

# 연도별 평균기온 계산
yearly_temp = (
    df.groupby("연도")["평균기온"]
    .mean()
    .reset_index()
)

yearly_temp["평균기온"] = yearly_temp["평균기온"].round(2)

# 분석 기간
start_year = yearly_temp["연도"].min()
end_year = yearly_temp["연도"].max()

st.subheader(f"📈 {start_year}년~{end_year}년 서울 연평균 기온")

# 선 그래프
chart_data = yearly_temp.set_index("연도")

st.line_chart(
    chart_data,
    y="평균기온",
    x_label="연도",
    y_label="연평균 기온 (℃)"
)

# 간단한 설명
st.info(
    "그래프의 가로축은 연도, 세로축은 연평균 기온(℃)입니다. "
    "선의 전체적인 방향을 통해 장기간에 걸친 서울의 기온 변화를 확인할 수 있습니다."
)

# 데이터 확인
with st.expander("📋 연도별 평균기온 데이터 보기"):
    st.dataframe(
        yearly_temp,
        use_container_width=True,
        hide_index=True
    )
