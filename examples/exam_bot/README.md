# 南一中考試小幫手（Streamlit 範例）

抓學校官網「考試資訊」的公告，交給校內 LLM（gpt-oss-120b）整理，回答「最近學校有什麼重要考試？」。
完整說明見網站的「實作範例」頁：https://letranger.github.io/exo-llm/exambot.html

## 1. 安裝套件
```
pip install -r requirements.txt
```

## 2. 放 API key（存成檔案，不寫在程式裡）
把 `.streamlit/secrets.toml.example` 複製一份，改名成 `.streamlit/secrets.toml`，填入老師給你的 key：
```toml
EXO_API_KEY = "sk-你的API key"
```
`secrets.toml` 已列在 `.gitignore`，不會被上傳到 GitHub。不要把這個檔案傳給別人。

## 3. 執行
```
streamlit run app.py
```
瀏覽器會自動打開 http://localhost:8501 。要在校內網路才連得到叢集。
