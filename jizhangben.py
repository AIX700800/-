import streamlit as st
import random
from supabase import create_client, Client
import json

# ------------------ Supabase 配置 ------------------
SUPABASE_URL = "https://你的项目.supabase.co"
SUPABASE_KEY = "你的 anon key"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def load_data():
    try:
        response = supabase.table("jizhang_data").select("*").execute()
        if response.data:
            return {item['key']: json.loads(item['value']) for item in response.data}
    except Exception as e:
        st.error(f"加载数据失败：{e}")
    return {}

def save_data(key, value):
    try:
        supabase.table("jizhang_data").delete().eq("key", key).execute()
        supabase.table("jizhang_data").insert({"key": key, "value": json.dumps(value)}).execute()
    except Exception as e:
        st.error(f"保存数据失败：{e}")

# ------------------ 页面配置 ------------------
st.set_page_config(page_title="好吃嘴的记账本", page_icon="🍽️", layout="centered")

# 自定义 CSS（略，同前）
st.markdown("""
<style>
    @media (max-width: 600px) {
        div[data-testid="column"] { width: 100% !important; flex: unset !important; margin-bottom: 20px; }
        .stButton button { margin-top: 5px; }
    }
    .stSelectbox, .stTextInput, .stNumberInput { width: 100%; }
    .stButton button { width: 100%; }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=18000)
def get_initial_balance():
    return 0

st.title("🍽️ 好吃嘴的记账本")
st.write("---")

# ------------------ 加载数据 ------------------
loaded = load_data()
if loaded:
    st.session_state.余额 = loaded.get("余额", get_initial_balance())
    st.session_state.总支出 = loaded.get("总支出", 0.0)
    st.session_state.总收入 = loaded.get("总收入", 0.0)
    st.session_state.支出记录 = loaded.get("支出记录", [])
    st.session_state.收入记录 = loaded.get("收入记录", [])
else:
    st.session_state.余额 = get_initial_balance()
    st.session_state.总支出 = 0.0
    st.session_state.总收入 = 0.0
    st.session_state.支出记录 = []
    st.session_state.收入记录 = []

# 显示余额（略，同前）
balance = st.session_state.余额
color = "green" if balance >= 1000 else ("blue" if balance >= 0 else "red")
st.markdown(f"### 💰 当前余额：<span style='color:{color}'>{balance} 元</span>", unsafe_allow_html=True)
st.write("---")

col1, col2 = st.columns(2)

# 支出部分（略，但每个修改后要保存）
with col1:
    # ... 前面的界面代码 ...
    if st.button("✅ 确认支出", use_container_width=True, key="expense_btn"):
        if amount > 0:
            st.session_state.余额 -= amount
            st.session_state.总支出 += amount
            st.session_state.支出记录.append({
                "类别": category,
                "金额": amount,
                "备注": note or "无备注"
            })
            # 保存
            save_data("余额", st.session_state.余额)
            save_data("总支出", st.session_state.总支出)
            save_data("支出记录", st.session_state.支出记录)
            st.success(f"支出 {amount} 元成功！")
            st.rerun()
        else:
            st.warning("请输入金额")

# 收入部分类似，保存 "总收入" 和 "收入记录"

# 重置余额按钮（也要保存）
if st.button("🔄 重置为0", use_container_width=True):
    st.session_state.余额 = 0
    save_data("余额", 0)
    st.rerun()

# 重置统计按钮（也要保存）
if st.button("🧹 重置统计", use_container_width=True):
    st.session_state.总支出 = 0.0
    st.session_state.总收入 = 0.0
    st.session_state.支出记录 = []
    st.session_state.收入记录 = []
    save_data("总支出", 0.0)
    save_data("总收入", 0.0)
    save_data("支出记录", [])
    save_data("收入记录", [])
    st.rerun()

# 显示明细统计（略，同前）
# 底部提示（略）









