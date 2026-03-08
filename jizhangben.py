import streamlit as st
import random

st.set_page_config(page_title="好吃嘴的记账本", page_icon="🍽️", layout="centered")

# 自定义 CSS（保持不变）
st.markdown("""
<style>
    @media (max-width: 600px) {
        div[data-testid="column"] {
            width: 100% !important;
            flex: unset !important;
            margin-bottom: 20px;
        }
        .stButton button {
            margin-top: 5px;
        }
    }
    .stSelectbox, .stTextInput, .stNumberInput {
        width: 100%;
    }
    .stButton button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# ------------------ 缓存初始余额 ------------------
@st.cache_data(ttl=18000)
def get_initial_balance():
    return 0

st.title("🍽️ 好吃嘴的记账本")
st.write("---")

# ------------------ 初始化 ------------------
if '余额' not in st.session_state:
    st.session_state.余额 = get_initial_balance()
if '总支出' not in st.session_state:
    st.session_state.总支出 = 0.0
if '总收入' not in st.session_state:
    st.session_state.总收入 = 0.0
# ===== 新增：记录明细列表 =====
if '支出记录' not in st.session_state:
    st.session_state.支出记录 = []
if '收入记录' not in st.session_state:
    st.session_state.收入记录 = []

# 显示余额
balance = st.session_state.余额
if balance >= 1000:
    color = "green"
elif balance >= 0:
    color = "blue"
else:
    color = "red"
st.markdown(f"### 💰 当前余额：<span style='color:{color}'>{balance} 元</span>", unsafe_allow_html=True)
st.write("---")

col1, col2 = st.columns(2)

# ================== 支出部分 ==================
with col1:
    st.write("#### 💸 记录支出")
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
    if category == "食品":
        note = st.text_input("什么食品？", placeholder="例：奶茶 零食", key="food_note")
    elif category == "用品":
        note = st.text_input("什么用品？", placeholder="例：卫生巾 纸巾", key="用品_note")
    elif category == "衣服":
        note = st.text_input("什么衣服？", placeholder="例：T恤 裤子", key="cloth_note")
    else:
        note = st.text_input("什么出行？", placeholder="例：公交车 打车", key="travel_note")
    amount = st.number_input("金额", min_value=0.0, step=1.0, key="expense_amount")
    if st.button("✅ 确认支出", use_container_width=True):
        if amount > 0:
            st.session_state.余额 -= amount
            st.session_state.总支出 += amount
            # ===== 新增：记录支出明细 =====
            st.session_state.支出记录.append({
                "类别": category,
                "金额": amount,
                "备注": note or "无备注"
            })
            icon_map = {"食品": "🍔", "用品": "🧴", "衣服": "👕", "出行": "🚗"}
            st.success(f"支出 {amount} 元（{icon_map[category]} {category}：{note or '无备注'}）")
            st.rerun()
        else:
            st.warning("请输入金额")

# ================== 收入部分 ==================
with col2:
    st.write("#### 💰 记录收入")
    income_cat = st.selectbox(
        "收入类别",
        options=["红包", "转账", "意外收入"],
        format_func=lambda x: "🧧 红包" if x == "红包" else ("💸 转账" if x == "转账" else "🤑 意外收入"),
        key="income_cat_select"
    )
    if income_cat == "红包":
        income_note = st.text_input("来自谁？", placeholder="例：亲戚 朋友", key="hongbao_note")
    elif income_cat == "转账":
        income_note = st.text_input("来自谁？", placeholder="例：爸爸 妈妈", key="transfer_note")
    else:
        income_note = st.text_input("什么意外？", placeholder="例：捡到钱 彩票", key="unexpected_note")
    income_amount = st.number_input("金额", min_value=0.0, step=1.0, key="income_amount")
    if st.button("✅ 确认收入", use_container_width=True):
        if income_amount > 0:
            st.session_state.余额 += income_amount
            st.session_state.总收入 += income_amount
            # ===== 新增：记录收入明细 =====
            st.session_state.收入记录.append({
                "类别": income_cat,
                "金额": income_amount,
                "备注": income_note or "无备注"
            })
            icon_map = {"红包": "🧧", "转账": "💸", "意外收入": "🤑"}
            st.success(f"收入 {income_amount} 元（{icon_map[income_cat]} {income_cat}：{income_note or '无备注'}）")
            st.rerun()
        else:
            st.warning("请输入金额")

st.write("---")

# ================== 重置余额按钮 ==================
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

# ================== 重置统计按钮（独立） ==================
col_reset1, col_reset2, col_reset3 = st.columns([1, 2, 1])
with col_reset2:
    if st.button("🧹 重置统计", use_container_width=True):
        st.session_state.总支出 = 0.0
        st.session_state.总收入 = 0.0
        st.session_state.支出记录 = []
        st.session_state.收入记录 = []
        st.rerun()

st.write("---")

# ================== 收支明细统计 ==================
st.write("### 📊 收支明细统计")
col_stat_left, col_stat_right = st.columns(2)

# ---------- 支出明细 ----------
with col_stat_left:
    st.write("#### 💸 支出明细")
    cat_icons = {"食品": "🍔", "用品": "🧴", "衣服": "👕", "出行": "🚗"}
    # 计算每个类别的总额
    支出类别总额 = {cat: 0.0 for cat in cat_icons}
    for 记录 in st.session_state.支出记录:
        支出类别总额[记录["类别"]] += 记录["金额"]
    
    for cat in cat_icons:
        with st.expander(f"{cat_icons[cat]} {cat} 共 {支出类别总额[cat]:.1f} 元"):
            cat_records = [r for r in st.session_state.支出记录 if r["类别"] == cat]
            if cat_records:
                for r in cat_records:
                    st.write(f"  • {r['备注']}：{r['金额']} 元")
            else:
                st.write("  暂无记录")

# ---------- 收入明细 ----------
with col_stat_right:
    st.write("#### 💰 收入明细")
    income_icons = {"红包": "🧧", "转账": "💸", "意外收入": "🤑"}
    收入类别总额 = {cat: 0.0 for cat in income_icons}
    for 记录 in st.session_state.收入记录:
        收入类别总额[记录["类别"]] += 记录["金额"]
    
    for cat in income_icons:
        with st.expander(f"{income_icons[cat]} {cat} 共 {收入类别总额[cat]:.1f} 元"):
            cat_records = [r for r in st.session_state.收入记录 if r["类别"] == cat]
            if cat_records:
                for r in cat_records:
                    st.write(f"  • {r['备注']}：{r['金额']} 元")
            else:
                st.write("  暂无记录")

st.write("---")

# ================== 底部可爱提示 ==================
tips = [
    "🍭 少吃零食多存钱～",
    "🎀 今天也是精致的一天！",
    "🧁 记账的人最可爱！",
    "🐻 钱钱要省着花哦",
]
st.caption(f"✨ {random.choice(tips)}")








