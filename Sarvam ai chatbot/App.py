import streamlit as st
from sarvamai import SarvamAI
import uuid
import time
import os

client = SarvamAI(api_subscription_key="sk_s3im7cou_BASO9RWhApDtPVrzcEydb9hY")

st.set_page_config(page_title="Dolver AI", layout="wide")

# ---------- CSS ----------
st.markdown("""
<style>

.block-container{
    max-width:900px;
    margin:auto;
}

/* chat row */

.chat-row{
    display:flex;
    margin:12px 0;
    animation: slideUp .25s ease;
}

.chat-ai{
    justify-content:flex-start;
}

.chat-user{
    justify-content:flex-end;
}

/* bubbles */

.bubble-ai{
    background:#ECECEC;
    color:#000000;
    padding:12px 16px;
    border-radius:18px;
    max-width:65%;
    font-size:15px;
}

.bubble-user{
    background:#CDE7B0;
    color:#000000;
    padding:12px 16px;
    border-radius:18px;
    max-width:65%;
    font-size:15px;
}

/* animation */

@keyframes slideUp{
    from{
        transform:translateY(20px);
        opacity:0;
    }
    to{
        transform:translateY(0);
        opacity:1;
    }
}

/* thinking animation */

.typing span{
    animation: blink 1.4s infinite;
    font-size:22px;
}

.typing span:nth-child(2){animation-delay:.2s}
.typing span:nth-child(3){animation-delay:.4s}

@keyframes blink{
    0%{opacity:.2}
    20%{opacity:1}
    100%{opacity:.2}
}

</style>
""", unsafe_allow_html=True)

# ---------- SESSION ----------
if "chats" not in st.session_state:
    st.session_state.chats = {}

if "current_chat" not in st.session_state:
    cid = str(uuid.uuid4())
    st.session_state.chats[cid] = {"title":"New Chat","messages":[]}
    st.session_state.current_chat = cid

# ---------- SIDEBAR ----------
with st.sidebar:

    st.markdown("""
<div style="margin-bottom:7px;">
    <h1 style="margin-bottom:0;">🤖 Dolver AI</h1>
    <p style="margin-top:0;color:gray;">[Powered by Sarvam AI]</p>
</div>
""", unsafe_allow_html=True)

    if st.button("➕ New Chat"):
        cid = str(uuid.uuid4())
        st.session_state.chats[cid] = {"title":"New Chat","messages":[]}
        st.session_state.current_chat = cid
        st.rerun()

    st.divider()
    st.markdown("### Chats")

    for cid,chat in st.session_state.chats.items():
        if st.button(chat["title"],key=cid):
            st.session_state.current_chat = cid
            st.rerun()

# ---------- CHAT ----------
chat = st.session_state.chats[st.session_state.current_chat]
messages = chat["messages"]

# ---------- WELCOME ----------
if len(messages)==0:
    st.markdown(
    "<h1 style='text-align:center'>Where should we begin?</h1>",
    unsafe_allow_html=True
    )

# ---------- SHOW CHAT ----------
for m in messages:

    if m["role"]=="assistant":
        st.markdown(f"""
        <div class="chat-row chat-ai">
        <div class="bubble-ai">{m["content"]}</div>
        </div>
        """,unsafe_allow_html=True)

    else:
        st.markdown(f"""
        <div class="chat-row chat-user">
        <div class="bubble-user">{m["content"]}</div>
        </div>
        """,unsafe_allow_html=True)

# ---------- INPUT ----------
user_input = st.chat_input("Ask anything...")

if user_input:

    messages.append({"role":"user","content":user_input})

    if chat["title"]=="New Chat":
        chat["title"]=user_input[:30]

    # show user message immediately
    st.markdown(f"""
    <div class="chat-row chat-user">
    <div class="bubble-user">{user_input}</div>
    </div>
    """,unsafe_allow_html=True)

    # ---------- THINKING DOTS ----------
    thinking = st.empty()

    thinking.markdown("""
    <div class="chat-row chat-ai">
        <div class="bubble-ai typing">
            <span>.</span><span>.</span><span>.</span>
        </div>
    </div>
    """,unsafe_allow_html=True)

    # ---------- AI RESPONSE ----------
    response = client.chat.completions(
        model="sarvam-105b",
        messages=messages
    )

    ai_reply = response.choices[0].message.content

    thinking.empty()

    # ---------- STREAMING LETTERS ----------
    placeholder = st.empty()

    typed_text = ""

    for char in ai_reply:
        typed_text += char

        placeholder.markdown(f"""
        <div class="chat-row chat-ai">
        <div class="bubble-ai">{typed_text}</div>
        </div>
        """,unsafe_allow_html=True)

        time.sleep(0.015)

    messages.append({"role":"assistant","content":ai_reply})
