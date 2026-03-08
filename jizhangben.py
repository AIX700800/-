import streamlit as st
import random

# ------------------ 页面配置 ------------------
st.set_page_config(
    page_title="好吃嘴的记账本",
    page_icon="🍽️",
    layout="centered"
)

# ------------------ 可爱的背景装饰（随机飘浮的emoji） ------------------
def draw_background_emoji():
    emoji_list = ["🌸", "🍀", "✨", "🎈", "🧸", "🍰", "🐼", "🦊"]
    # 随机选几个放在页面角落
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.markdown(f"<h1 style='text-align: center; opacity: 0.3;'>{random.choice(emoji_list)}</h1>", unsafe_allow_html=True)

# 显示装饰（放在最上面）
draw_background_emoji()

# ------------------ 缓存初始余额（5小时） ------------------
@st.cache_data(ttl=18000)  # 5小时缓存
def get_initial_balance():
    return 0

# ------------------ 标题 ------------------
st.title("🍽️ 好吃嘴的记账本")
st.write("---")

# ------------------ 初始化余额 ------------------
if '余额' not in st.session_state:
    st.session_state.余额 = get_initial_balance()

# ------------------ 显示当前余额 ------------------
balance = st.session_state.余额
if balance >= 1000:
    color = "green"
elif balance >= 0:
    color = "blue"
else:
    color = "red"
st.markdown(f"### 💰 当前余额：<span style='color:{color}'>{balance} 元</span>", unsafe_allow_html=True)
st.write("---")

# ------------------ 两列布局：支出 & 收入 ------------------
col1, col2 = st.columns(2)

# ================== 支出部分 ==================
with col1:
    st.write("#### 💸 记录支出")
    
    # 支出类别选择（带图标）
    category = st.selectbox(
        "选择类别",
        options=["食品", "用品", "衣服", "出行"],
        format_func=lambda x: {
            "食品": "🍔 食品",
            "用品": "🧴 用品",
            "衣服": "👕 衣服",
            "出行": "🚗 出行"
        }[x],
        key="cat_select"
    )
    
    # 根据类别显示对应的备注输入框
    if category == "食品":
        note = st.text_input("什么食品？", placeholder="例：火锅、奶茶", key="food_note")
    elif category == "用品":
        note = st.text_input("什么用品？", placeholder="例：洗发水、纸巾", key="用品_note")
    elif category == "衣服":
        note = st.text_input("什么衣服？", placeholder="例：T恤、裤子", key="cloth_note")
    else:  # 出行
        note = st.text_input("什么出行？", placeholder="例：打车、公交卡", key="travel_note")
    
    # 支出金额输入
    amount = st.number_input("金额", min_value=0.0, step=1.0, key="expense_amount")
    
    if st.button("✅ 确认支出", use_container_width=True):
        if amount > 0:
            st.session_state.余额 -= amount
            icon_map = {"食品": "🍔", "用品": "🧴", "衣服": "👕", "出行": "🚗"}
            st.success(f"支出 {amount} 元（{icon_map[category]} {category}：{note or '无备注'}）")
            st.rerun()
        else:
            st.warning("请输入金额")

# ================== 收入部分 ==================
with col2:
    st.write("#### 💰 记录收入")

    st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
    # 收入备注
    income_note = st.text_input("收入来源？", placeholder="例：工资、红包", key="income_note")
    
    # 收入金额输入
    income_amount = st.number_input("金额", min_value=0.0, step=1.0, key="income_amount")
    
    if st.button("✅ 确认收入", use_container_width=True):
        if income_amount > 0:
            st.session_state.余额 += income_amount
            st.success(f"收入 {income_amount} 元（{income_note or '无备注'}）")
            st.rerun()
        else:
            st.warning("请输入金额")

st.write("---")

# ------------------ 重置按钮 ------------------
col3, col4 = st.columns(2)
with col3:
    if st.button("🔄 重置为0", use_container_width=True):
        st.session_state.余额 = 0
        st.rerun()
with col4:
    if st.button("💰 重置为500", use_container_width=True):
        st.session_state.余额 = 500
        st.rerun()

st.write("---")

# ------------------ 底部可爱提示 ------------------
tips = [
    "🍭 少吃零食多存钱～",
    "🎀 今天也是精致的一天！",
    "🧁 记账的人最可爱！",
    "🐻 钱钱要省着花哦",
]
st.caption(f"✨ {random.choice(tips)}")

# 再加一行漂浮装饰
draw_background_emoji()



