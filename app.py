import streamlit as st
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage


st.title("LLM QAアプリ (LangChain × Streamlit)")

# アプリ概要・操作説明
st.markdown("""
### アプリ概要
このWebアプリは、選択した専門家の視点でLLM（大規模言語モデル）に質問できるQAシステムです。AIエンジニア・医療コンサルタント・法律アドバイザーの3種類から専門家を選び、質問を入力して送信すると、その分野の専門家としてLLMが回答します。

### 操作方法
1. **専門家の種類を選択**：ラジオボタンから相談したい専門家を選んでください。
2. **質問を入力**：テキストボックスに質問内容を入力してください。
3. **送信ボタンをクリック**：LLMが専門家として回答を返します。
""")


# 専門家の種類をラジオボタンで選択
expert_types = {
    "AIエンジニア": "あなたは優秀なAIエンジニアです。AIやプログラミング、テクノロジーに関する質問に専門的かつ分かりやすく答えてください。",
    "医療コンサルタント": "あなたは経験豊富な医療コンサルタントです。健康や医療に関する質問に専門的かつ丁寧に答えてください。",
    "法律アドバイザー": "あなたは信頼できる法律アドバイザーです。法律や契約、権利に関する質問に分かりやすく答えてください。"
}

def get_llm_answer(input_text: str, expert_key: str) -> str:
    """
    入力テキストと専門家選択値を受け取り、LLMの回答を返す
    """
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    system_message = expert_types.get(expert_key, "あなたは有能なアシスタントです。")
    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=input_text),
    ]
    result = llm(messages)
    return result.content if hasattr(result, 'content') else str(result)

selected_expert = st.radio("専門家の種類を選択してください：", list(expert_types.keys()))
user_input = st.text_input("質問を入力してください：", "")

if st.button("送信"):
    if user_input.strip() == "":
        st.warning("質問を入力してください。")
    else:
        with st.spinner("LLMに問い合わせ中..."):
            try:
                answer = get_llm_answer(user_input, selected_expert)
                st.success("回答:")
                st.write(answer)
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")