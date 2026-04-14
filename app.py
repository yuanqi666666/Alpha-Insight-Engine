import streamlit as st
import wrds
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# --- 页面设置 ---
st.set_page_config(page_title="Alpha Insight Engine", layout="wide")
st.title("🚀 Alpha Insight Engine | 深度价值分析报告")

# --- 侧边栏：登录与设置 ---
st.sidebar.header("🔑 WRDS 账户认证")
wrds_username = st.sidebar.text_input("WRDS Username", placeholder="输入你的用户名")

# 只有输入了用户名，才尝试连接
if wrds_username:
    try:
        # 使用 st.cache_resource 避免每次操作都重新连接，提高速度
        @st.cache_resource
        def get_wrds_connection(username):
            return wrds.Connection(wrds_username=username)
        
        db = get_wrds_connection(wrds_username)
        st.sidebar.success("✅ WRDS 已连接")
        
        # --- 输入参数 ---
        st.sidebar.header("📊 查询参数")
        ticker = st.sidebar.text_input("美股代码 (Ticker)", value="NVDA").strip().upper()
        sel_date = st.sidebar.date_input("选择分析基准日期", value=datetime(2024, 4, 8).date())
        
        analyze_btn = st.sidebar.button("生成深度价值报告", type="primary")

        # --- 绘图函数 ---
        def plot_financial_engine(df, idx):
            fig, axes = plt.subplots(4, 1, figsize=(12, 22))
            plot_configs = [
                (['roa', 'roe', 'roc'], 'Profitability Metrics (ROA/ROE/ROC)', 0),
                (['current_ratio', 'quick_ratio'], 'Liquidity Analysis (Current/Quick)', 1),
                (['roa_ma'], 'ROA 4-Quarter Moving Average (Trend)', 2),
                (['ret'], 'Quarterly Returns (%)', 3)
            ]
            
            for cols, title, i in plot_configs:
                for col in cols:
                    axes[i].plot(df['datadate'], df[col], label=col.upper(), marker='o', markersize=4, alpha=0.7)
                    axes[i].scatter(df.loc[idx, 'datadate'], df.loc[idx, col], 
                                   color='red', s=130, edgecolors='black', zorder=10)
                
                if i == 0:
                    axes[i].axhline(y=0.05, color='gray', linestyle='--', label='Industry Baseline (5%)')
                axes[i].set_title(title, fontsize=14, fontweight='bold')
                axes[i].legend()
                axes[i].grid(True, linestyle=':', alpha=0.6)
            
            plt.tight_layout()
            st.pyplot(fig) # 在 Streamlit 中显示图表

        # --- 主分析逻辑 ---
        if analyze_btn:
            query = f"""
            SELECT datadate, prccq,
                   (niq / NULLIF(atq, 0)) as roa,
                   (niq / NULLIF(ceqq, 0)) as roe,
                   (oiadpq / NULLIF(atq - lctq, 0)) as roc,
                   (actq / NULLIF(lctq, 0)) as current_ratio,
                   ((cheq + rectq) / NULLIF(lctq, 0)) as quick_ratio
            FROM comp.fundq
            WHERE tic = '{ticker}' AND datadate >= '2020-01-01' AND datadate <= '2026-01-01'
            ORDER BY datadate
            """
            
            with st.spinner('正在从 WRDS 提取数据并计算...'):
                df = db.raw_sql(query)
                
                if df is None or df.empty:
                    st.error(f"❌ 未找到 {ticker} 的相关财务数据。")
                else:
                    df['datadate'] = pd.to_datetime(df['datadate'])
                    df['roa_ma'] = df['roa'].rolling(window=4).mean() 
                    df['ret'] = df['prccq'].pct_change()            
                    
                    idx = (df['datadate'] - pd.to_datetime(sel_date)).abs().idxmin()
                    latest = df.loc[idx]
                    
                    # 结果展示
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("分析对象", ticker)
                        st.metric("选定季度节点", str(latest['datadate'].date()))
                    
                    with col2:
                        if latest['current_ratio'] < 1.2:
                            st.warning("🔴 偿债风险提示：Current Ratio 低于 1.2")
                        else:
                            st.success("🟢 财务健康状况：短期偿债能力良好")

                    # 收益计算
                    post_data = df.loc[idx:]
                    if len(post_data) > 1:
                        total_gain = (post_data['prccq'].iloc[-1] / latest['prccq'] - 1) * 100
                        st.info(f"💰 **价值模拟**：若在该点入场并持有至今，总收益率为 **{total_gain:.2f}%**")
                    
                    # 风险指标
                    recent_rets = df.loc[idx:, 'ret'].dropna()
                    if len(recent_rets) >= 2:
                        vol = recent_rets.std() * np.sqrt(4)
                        sharpe = (recent_rets.mean() / recent_rets.std()) * np.sqrt(4) if recent_rets.std() != 0 else 0
                        
                        st.subheader("📈 风险与专业指标 (自选定日期起)")
                        c_a, c_b = st.columns(2)
                        c_a.metric("年化波动率", f"{vol:.2%}")
                        c_b.metric("夏普比率 (Sharpe Ratio)", f"{sharpe:.2f}")

                    # 绘图
                    plot_financial_engine(df, idx)

    except Exception as e:
        st.error(f"连接或查询出错: {e}")
else:
    st.info("👈 请在左侧侧边栏输入您的 WRDS 用户名以开始。第一次连接时，您的终端可能会提示输入密码或进行二次验证。")

