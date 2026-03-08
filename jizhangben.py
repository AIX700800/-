import streamlit as st
import random

# ------------------ 页面配置 ------------------
st.set_page_config(
    page_title="好吃嘴的记账本",
    page_icon="🍽️",
    layout="centered"
)
import streamlit as st

st.set_page_config(page_title="好吃嘴的记账本", page_icon="🍽️", layout="centered")

# ========== 添加自定义 CSS 以优化手机显示 ==========  
st.markdown("""
<style>
    /* 当屏幕宽度小于 600px 时，让两列垂直堆叠 */
    @media (max-width: 600px) {
        div[data-testid="column"] {
            width: 100% !important;
            flex: unset !important;
            margin-bottom: 20px;
        }
        /* 增加一些内边距，让内容更透气 */
        .stButton button {
            margin-top: 5px;
        }
    }
    /* 统一调整输入框宽度 */
    .stSelectbox, .stTextInput, .stNumberInput {
        width: 100%;
    }
    /* 让按钮宽度自适应 */
    .stButton button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# 然后继续你的原有代码...

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
    # ===== 新增：统计变量初始化 =====
if '总支出' not in st.session_state:
    st.session_state.总支出 = 0.0
if '总收入' not in st.session_state:
    st.session_state.总收入 = 0.0

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
        note = st.text_input("什么食品？", placeholder="例：奶茶 零食", key="food_note")
    elif category == "用品":
        note = st.text_input("什么用品？", placeholder="例：卫生巾 纸巾", key="用品_note")
    elif category == "衣服":
        note = st.text_input("什么衣服？", placeholder="例：T恤 裤子", key="cloth_note")
    else:  # 出行
        note = st.text_input("什么出行？", placeholder="例：公交车 打车", key="travel_note")
    
    # 支出金额输入
    amount = st.number_input("金额", min_value=0.0, step=1.0, key="expense_amount")
    
    if st.button("✅ 确认支出", use_container_width=True):
        if amount > 0:
            st.session_state.余额 -= amount
            st.session_state.总支出 += amount
            icon_map = {"食品": "🍔", "用品": "🧴", "衣服": "👕", "出行": "🚗"}
            st.success(f"支出 {amount} 元（{icon_map[category]} {category}：{note or '无备注'}）")
            st.rerun()
        else:
            st.warning("请输入金额")

# ================== 收入部分 ==================
with col2:
    st.write("#### 💰 记录收入")
    
    # 收入类别选择（带图标）
    income_cat = st.selectbox(
        "收入类别",
        options=["红包", "转账", "意外之财"],
       format_func=lambda x: "🧧 红包" if x == "红包" else ("💸 转账" if x == "转账" else "🤑 意外收入"),
        key="income_cat_select"
    )

    
    # 根据类别显示对应的备注输入框
    if income_cat == "红包":
        income_note = st.text_input("来自谁？", placeholder="例：亲戚 朋友", key="hongbao_note")
    elif income_cat == "转账":
        income_note = st.text_input("来自谁？", placeholder="例：爸爸 妈妈", key="transfer_note")
    else:  # 意外收入
        income_note = st.text_input("什么意外？", placeholder="例：捡到钱 彩票", key="unexpected_note")
    
    # 收入金额输入
    income_amount = st.number_input("金额", min_value=0.0, step=1.0, key="income_amount")
    
    if st.button("✅ 确认收入", use_container_width=True):
        if income_amount > 0:
            st.session_state.余额 += income_amount
            st.session_state.总收入 += income_amount
            # 显示带图标的成功消息
            icon_map = {"红包": "🧧", "转账": "💸", "意外收入": "🤑"}
            st.success(f"收入 {income_amount} 元（{icon_map[income_cat]} {income_cat}：{income_note or '无备注'}）")
            st.rerun()
        else:
            st.warning("请输入金额")

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
st.write("---")
st.write("### 📊 收支统计")

# 使用三列布局让数字和按钮居中
col_stat1, col_stat2, col_stat3 = st.columns(3)
with col_stat1:
    st.metric("总支出", f"{st.session_state.总支出:.1f} 元")
with col_stat2:
    st.metric("总收入", f"{st.session_state.总收入:.1f} 元")
with col_stat3:
    if st.button("🧹 重置统计", use_container_width=True):
        st.session_state.总支出 = 0.0
        st.session_state.总收入 = 0.0
        st.rerun()

st.write("---")  # 可选分隔线







