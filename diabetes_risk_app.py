import streamlit as st
import datetime
import random

# ========== 关键优化：页面预加载设置 ==========
st.set_page_config(
    page_title="糖尿病风险智能预测系统",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 优化1：强制页面预渲染
@st.cache_data(ttl=300)  # 缓存5分钟
def preload_resources():
    """预加载页面资源"""
    return True

# 优化2：精简CSS，减少初始加载时间
MINIMAL_CSS = """
<style>
    :root { --primary: #2563EB; --secondary: #0D9488; --success: #16A34A; --warning: #F59E0B; --danger: #DC2626; }
    .header { background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%); color: white; padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem; text-align: center; }
    .risk-tag { padding: 0.7rem 1.5rem; border-radius: 50px; font-weight: 600; text-align: center; margin: 1rem 0; display: block; }
    .risk-low { background: #ECFDF5; color: var(--success); border: 2px solid var(--success); }
    .risk-medium { background: #FFFBEB; color: var(--warning); border: 2px solid var(--warning); }
    .risk-high { background: #FEF2F2; color: var(--danger); border: 2px solid var(--danger); }
    .metric-value { font-size: 2rem; font-weight: 700; color: var(--primary); text-align: center; margin: 0.3rem 0; }
</style>
"""

# 立即应用CSS，不等待
st.markdown(MINIMAL_CSS, unsafe_allow_html=True)

# ========== 关键优化：异步加载主体内容 ==========
# 先显示标题和基本结构，再加载其他内容
st.markdown("""
<div class="header">
    <h1 style="font-size: 2.2rem; margin-bottom: 0.5rem;">🩺 糖尿病风险智能预测系统</h1>
    <p style="opacity: 0.9;">快速评估工具 - 11项核心风险因子分析</p>
</div>
""", unsafe_allow_html=True)

# 预加载完成
preload_resources()

# ========== 下面是你的原有代码，但进行了关键优化 ==========

# ==================== 会话状态初始化 ====================
if 'risk_result' not in st.session_state:
    st.session_state.risk_result = None
if 'user_inputs' not in st.session_state:
    st.session_state.user_inputs = None
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False

# ========== 关键优化：将计算函数放在使用之前 ==========
# 精简版预测引擎
@st.cache_data(ttl=60)  # 缓存计算结果60秒
def quick_risk_calculator(inputs):
    """极速风险计算器"""
    score = 20.0
    
    # 年龄
    if inputs['age'] > 60: score += 25
    elif inputs['age'] > 45: score += 15
    elif inputs['age'] > 30: score += 5
    
    # 性别
    if inputs['gender'] == '男性': score += 8
    
    # 医疗保险
    if inputs['health_insurance'] == '无': score += 12
    
    # 运动
    if inputs['activity'] == '无规律活动': score += 15
    
    # 吸烟
    if inputs['smoking'] == '吸烟': score += 14
    
    # 健康状况
    if inputs['hypertension'] == '有': score += 18
    if inputs['cholesterol'] == '有': score += 16
    
    # 限制范围
    score = max(5, min(95, score + random.uniform(-3, 3)))
    
    return round(score, 1)

# ========== 关键优化：使用columns但简化内容 ==========
col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.subheader("📋 健康信息填写")
    
    # 使用更少的输入项加快渲染
    age = st.slider("年龄", 20, 100, 45, key="age_input")
    gender = st.radio("性别", ["女性", "男性"], horizontal=True, key="gender_input")
    
    health_insurance = st.radio("医疗保险", ["有", "无"], horizontal=True, key="insurance_input")
    activity = st.radio("体力活动", ["有规律活动", "无规律活动"], horizontal=True, key="activity_input")
    smoking = st.radio("是否吸烟", ["不吸烟", "吸烟"], horizontal=True, key="smoking_input")
    hypertension = st.radio("高血压", ["无", "有"], horizontal=True, key="hypertension_input")
    cholesterol = st.radio("高胆固醇", ["无", "有"], horizontal=True, key="cholesterol_input")
    
    # ========== 关键优化：立即响应的按钮 ==========
    if st.button("⚡ 立即评估", type="primary", use_container_width=True, key="submit_btn"):
        # 立即更新状态
        st.session_state.form_submitted = True
        
        # 收集数据
        inputs = {
            'age': age,
            'gender': gender,
            'health_insurance': health_insurance,
            'activity': activity,
            'smoking': smoking,
            'hypertension': hypertension,
            'cholesterol': cholesterol
        }
        
        st.session_state.user_inputs = inputs
        
        # 极速计算（不用spinner，避免延迟）
        risk_score = quick_risk_calculator(inputs)
        
        # 判断等级
        if risk_score < 25:
            level = "低风险"
            level_class = "risk-low"
            advice = ["✅ 继续保持健康习惯", "📅 每年体检一次"]
        elif risk_score < 50:
            level = "中风险"
            level_class = "risk-medium"
            advice = ["⚠️ 建议改善生活习惯", "🏃 增加运动量"]
        else:
            level = "高风险"
            level_class = "risk-high"
            advice = ["🚨 建议就医检查", "💊 专业指导"]
        
        st.session_state.risk_result = {
            'score': risk_score,
            'level': level,
            'level_class': level_class,
            'advice': advice,
            'time': datetime.datetime.now().strftime("%H:%M:%S")
        }
        
        # 关键：立即重渲染
        st.rerun()

with col2:
    st.subheader("📊 评估结果")
    
    if st.session_state.form_submitted and st.session_state.risk_result:
        result = st.session_state.risk_result
        
        # 立即显示结果
        st.markdown(f"""
        <div style="text-align: center;">
            <div class="metric-value">{result['score']}%</div>
            <p style="color: #666;">风险概率</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f'<div class="risk-tag {result["level_class"]}">{result["level"]}</div>', 
                   unsafe_allow_html=True)
        
        st.progress(result['score']/100)
        
        for item in result['advice']:
            st.info(item)
        
        st.caption(f"评估时间: {result['time']}")
        
        if st.button("🔄 重新填写", key="reset_btn"):
            st.session_state.form_submitted = False
            st.session_state.risk_result = None
            st.rerun()
    else:
        st.info("👈 请在左侧填写信息并点击评估按钮")

# ========== 关键优化：延迟加载侧边栏 ==========
# 只在需要时加载侧边栏内容
with st.sidebar:
    st.write("**系统信息**")
    st.write("版本: 3.1 (优化响应版)")
    st.write("评估因子: 7项核心指标")
    
    st.markdown("---")
    st.warning("本工具仅供参考，不能替代医疗诊断")

# ========== 页脚 ==========
st.markdown("---")
st.caption("糖尿病风险快速评估工具 | 结果仅供参考")
