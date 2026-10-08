"""南一中考試小幫手：抓學校官網「考試資訊」，交給校內 LLM 整理後回答。

執行：streamlit run app.py
"""
import datetime

import requests
import streamlit as st
from bs4 import BeautifulSoup
from openai import OpenAI

BASE = "https://www.tnfsh.tn.edu.tw/latestevent/"
LIST_URL = BASE + "index.aspx?Parser=9,3,17"  # 官網「考試資訊」列表

# key 從 .streamlit/secrets.toml 讀，不寫在程式裡
client = OpenAI(
    base_url="http://192.168.16.233:4000/v1",
    api_key=st.secrets["EXO_API_KEY"],
)


def get_soup(url):
    html = requests.get(url, timeout=15).text
    return BeautifulSoup(html, "html.parser")


@st.cache_data(ttl=600)  # 10 分鐘內重複提問不重抓，對學校網站友善
def fetch_exams(n=8):
    """抓列表頁前 n 則公告，再進內頁抓內文，整理成一段純文字。"""
    items = []
    for li in get_soup(LIST_URL).select("ul.list li")[1:n + 1]:  # 第一個 li 是表頭
        a = li.find("a")
        unit, date = [s.get_text(strip=True) for s in li.select("span.w15")]
        link = BASE + a["href"]

        # 內頁的內文在「公布單位」和「您的瀏覽器，不支援script」之間
        text = get_soup(link).get_text(" ", strip=True)
        body = text.split("公布單位")[-1].split("您的瀏覽器")[0].lstrip(" ：")[:500]

        items.append(f"標題：{a['title']}\n公布日期：{date}（{unit}）\n內文：{body}\n連結：{link}")
    return "\n\n".join(items)


def ask(question, data):
    system = (
        f"你是臺南一中的校園小幫手。今天是 {datetime.date.today()}。"
        "只根據提供的公告回答，用繁體中文條列近期的考試或報名截止：日期、對象、重點。"
        "已經過去的不要列；公告沒寫日期的就說「詳見附件」；公告沒寫的（例如對象）不要猜，資料裡沒有的不要自己編。"
        "每一項最後附上公告連結。"
    )
    response = client.chat.completions.create(
        model="gpt-oss-120b",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": f"公告：\n{data}\n\n問題：{question}"},
        ],
        reasoning_effort="low",
    )
    return response.choices[0].message.content


st.title("南一中考試小幫手")
st.caption("⚠️ 只能在校內網路使用（AI 在校內的叢集上），回答僅供參考，請以學校公告為準。")
question = st.text_input("想問什麼？", "最近學校有什麼重要考試？")

if st.button("問問看"):
    with st.spinner("抓取學校公告中…"):
        data = fetch_exams()
    with st.expander("抓到的原始公告（這就是交給 AI 的資料）"):
        st.text(data)
    with st.spinner("AI 整理中…"):
        st.markdown(ask(question, data))
