import streamlit as st
import random
from supabase import create_client, Client
import json
import datetime  # 用于记录实时时间

# ------------------ 页面配置 ------------------
st.set_page_config(
    page_title="好吃嘴的记账本",
    page_icon="🍽️",
    layout="centered"
)

# ========== 自定义 CSS 优化手机显示 ==========
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

# ------------------ Supabase 配置 ------------------
# ⚠️ 重要：替换成你实际的 URL 和 Key
SUPABASE_URL = "https://gfrkctjpdmkkueljdhke.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdmcmtjdGpwZG1ra3VlbGpkaGtlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzI5NDgzOTYsImV4cCI6MjA4ODUyNDM5Nn0.KD0xZE7LJHFggIla7cbuZm1qiMDlDzgOyBKHcJWa_Tw"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def load_data():
    """从 Supabase 加载数据"""
    try:
        # 使用你的实际表名（可能是 accounts 或 jizhang_data）
        response = supabase.table("accounts").select("*").execute()
        if response.data:
            data_dict = {}
            for item in response.data:
                try:
                    data_dict[item['key']] = json.loads(item['value'])
                except:
                    data_dict[item['key']] = item['value']
            return data_dict
    except Exception as e:
        st.error(f"加载数据失败：{e}")
    return {}

def save_data(key, value):
    """保存数据到 Supabase"""
    try:
        # 先删除旧数据
        supabase.table("accounts").delete().eq("key", key).execute()
        # 插入新数据
        supabase.table("accounts").insert({
            "key": key,
            "value": json.dumps(value, ensure_ascii=False)
        }).execute()
    except Exception as e:
        st.error(f"保存数据失败：{e}")

# ------------------ 缓存初始余额 ------------------
@st.cache_data(ttl=18000)
def get_initial_balance():
    return 497.27

# ------------------ 标题 ------------------
st.title("🍽️ 好吃嘴的记账本")
st.write("---")

# ------------------ 加载数据到 session_state ------------------
loaded_data = load_data()
if loaded_data:
    # 从 Supabase 加载数据
    st.session_state.余额 = loaded_data.get("余额", get_initial_balance())
    st.session_state.总支出 = loaded_data.get("总支出", 0.0)
    st.session_state.总收入 = loaded_data.get("总收入", 0.0)
    st.session_state.支出记录 = loaded_data.get("支出记录", [])
    st.session_state.收入记录 = loaded_data.get("收入记录", [])
else:
    # 首次使用，初始化默认值
    st.session_state.余额 = get_initial_balance()
    st.session_state.总支出 = 0.0
    st.session_state.总收入 = 0.0
    st.session_state.支出记录 = []
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
            "出行": "🚗 出行",
            "现金": "💵 现金"
        }[x],
        key="cat_select"
    )
  if category == "食品":
    note = st.text_input("什么食品？", placeholder="例：奶茶 零食", key="food_note")
elif category == "用品":
    note = st.text_input("什么用品？", placeholder="例：卫生巾 纸巾", key="用品_note")
elif category == "衣服":
    note = st.text_input("什么衣服？", placeholder="例：T恤 裤子", key="cloth_note")
elif category == "出行":
    note = st.text_input("什么出行？", placeholder="例：公交车 打车", key="travel_note")
else:  # 现金
    note = st.text_input("什么现金支出？", placeholder="例：买菜 零花钱", key="cash_note")
    amount = st.number_input("金额", min_value=0.0, step=1.0, key="expense_amount")
    
    if st.button("✅ 确认支出", use_container_width=True, key="expense_btn"):
        if amount > 0:
            # 获取当前实时时间（精确到秒）
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 更新数据
            st.session_state.余额 -= amount
            st.session_state.总支出 += amount
            # 记录支出明细（带实时时间）
            st.session_state.支出记录.append({
                "类别": category,
                "金额": amount,
                "备注": note or "无备注",
                "时间": current_time  # 实时时间
            })
            
            # 保存到 Supabase
            save_data("余额", st.session_state.余额)
            save_data("总支出", st.session_state.总支出)
            save_data("支出记录", st.session_state.支出记录)
            
            cat_icons = {"食品": "🍔", "用品": "🧴", "衣服": "👕", "出行": "🚗", "现金": "💵"}
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
    
    if st.button("✅ 确认收入", use_container_width=True, key="income_btn"):
        if income_amount > 0:
            # 获取当前实时时间（精确到秒）
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 更新数据
            st.session_state.余额 += income_amount
            st.session_state.总收入 += income_amount
            # 记录收入明细（带实时时间）
            st.session_state.收入记录.append({
                "类别": income_cat,
                "金额": income_amount,
                "备注": income_note or "无备注",
                "时间": current_time  # 实时时间
            })
            
            # 保存到 Supabase
            save_data("余额", st.session_state.余额)
            save_data("总收入", st.session_state.总收入)
            save_data("收入记录", st.session_state.收入记录)
            
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
        save_data("余额", 0)
        st.rerun()
with col4:
    if st.button("💰 重置为500", use_container_width=True):
        st.session_state.余额 = 500
        save_data("余额", 500)
        st.rerun()

st.write("---")

# ================== 重置统计按钮 ==================
col_reset1, col_reset2, col_reset3 = st.columns([1, 2, 1])
with col_reset2:
    if st.button("🧹 重置统计", use_container_width=True):
        st.session_state.总支出 = 0.0
        st.session_state.总收入 = 0.0
        st.session_state.支出记录 = []
        st.session_state.收入记录 = []
        # 保存到 Supabase
        save_data("总支出", 0.0)
        save_data("总收入", 0.0)
        save_data("支出记录", [])
        save_data("收入记录", [])
        st.rerun()

st.write("---")

# ================== 收支明细统计（带实时时间显示） ==================
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
                    # 显示时间和备注
                    st.write(f"  • {r['时间']} {r['备注']}：{r['金额']} 元")
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
                    # 显示时间和备注
                    st.write(f"  • {r['时间']} {r['备注']}：{r['金额']} 元")
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





