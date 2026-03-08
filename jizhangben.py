
import streamlit as st

# 页面标题
st.title("📒 jizhangben")
st.write("---")

# 初始化余额为0
if '余额' not in st.session_state:
    st.session_state.余额 = 0

# 显示当前余额
st.write(f"### 💰 当前余额：{st.session_state.余额} 元")
st.write("---")

# 创建两列布局
col1, col2 = st.columns(2)

with col1:
    st.write("#### 💸 记录支出")
    支出 = st.number_input("花了多少钱", min_value=0.0, step=1.0, key="支出输入")
    if st.button("确认支出", use_container_width=True):
        st.session_state.余额 -= 支出
        st.success(f"支出 {支出} 元成功！")
        st.rerun()

with col2:
    st.write("#### 💰 记录收入")
    收入 = st.number_input("进了多少钱", min_value=0.0, step=1.0, key="收入输入")
    if st.button("确认收入", use_container_width=True):
        st.session_state.余额 += 收入
        st.success(f"收入 {收入} 元成功！")
        st.rerun()

st.write("---")

# 添加一个重置按钮（可以重置为0）
col3, col4 = st.columns(2)
with col3:
    if st.button("🔄 重置为0", use_container_width=True):
        st.session_state.余额 = 0
        st.rerun()

with col4:
    if st.button("💰 重置为500", use_container_width=True):
        st.session_state.余额 = 500
        st.rerun()

# 显示操作记录（可选）
st.write("---")
st.caption("点击按钮记录收支，余额会自动更新")


