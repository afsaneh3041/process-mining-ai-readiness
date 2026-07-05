import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine

# تنظیمات صفحه
st.set_page_config(
    page_title="Process Mining Dashboard",
    page_icon="📊",
    layout="wide"
)

# اتصال به دیتابیس
@st.cache_resource
def get_engine():
    import os
    password = os.environ.get('DB_PASSWORD', 'YOUR_PASSWORD')
    return create_engine(f'postgresql://postgres:{password}@localhost:5432/process_mining')

engine = get_engine()

# خواندن داده‌ها
@st.cache_data
def load_data():
    summary = pd.read_sql("SELECT * FROM pm_process_summary", engine)
    readiness = pd.read_sql("SELECT * FROM pm_ai_readiness", engine)
    activities = pd.read_sql("SELECT * FROM pm_activity_analysis", engine)
    recommendations = pd.read_sql("SELECT * FROM pm_recommendations", engine)
    return summary, readiness, activities, recommendations

summary, readiness, activities, recommendations = load_data()

# هدر
st.title("📊 داشبورد فرآیندکاوی و ارزیابی آمادگی هوش مصنوعی")
st.markdown("---")

# KPI های کلی
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("تعداد فرآیندها", len(summary))
with col2:
    st.metric("کل کیس‌ها", summary['total_cases'].sum())
with col3:
    st.metric("کل رویدادها", summary['total_events'].sum())
with col4:
    st.metric("میانگین AI Score", f"{readiness['final_score'].mean():.1f}/10")

st.markdown("---")

# تب‌ها
tab1, tab2, tab3, tab4 = st.tabs(["📋 خلاصه فرآیندها", "🤖 AI Readiness", "⚡ فعالیت‌ها", "💡 توصیه‌ها"])

with tab1:
    st.subheader("وضعیت فرآیندها")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(summary, x='proc_def_name', y=['completed', 'active', 'suspended'],
                     title='وضعیت کیس‌های هر فرآیند',
                     barmode='stack',
                     color_discrete_map={'completed': '#2ecc71', 'active': '#3498db', 'suspended': '#e74c3c'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(summary, x='proc_def_name', y='avg_duration_days',
                     title='میانگین مدت اجرا (روز)',
                     color='avg_duration_days',
                     color_continuous_scale='RdYlGn_r')
        fig.add_hline(y=14, line_dash="dash", line_color="green", annotation_text="هدف: 14 روز")
        st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(summary, x='proc_def_name', y='completion_rate',
                     title='نرخ تکمیل (%)',
                     color='completion_rate',
                     color_continuous_scale='RdYlGn')
        fig.add_hline(y=80, line_dash="dash", line_color="green", annotation_text="هدف: 80%")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(summary, x='proc_def_name', y='rework_rate',
                     title='نرخ بازکاری (%)',
                     color='rework_rate',
                     color_continuous_scale='RdYlGn_r')
        fig.add_hline(y=10, line_dash="dash", line_color="green", annotation_text="هدف: 10%")
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("جدول خلاصه")
    st.dataframe(summary[['proc_def_name', 'total_cases', 'completed', 'active', 
                           'suspended', 'completion_rate', 'rework_rate', 'avg_duration_days']]
                 .rename(columns={
                     'proc_def_name': 'فرآیند',
                     'total_cases': 'کل کیس',
                     'completed': 'تکمیل',
                     'active': 'فعال',
                     'suspended': 'معلق',
                     'completion_rate': 'نرخ تکمیل%',
                     'rework_rate': 'نرخ بازکاری%',
                     'avg_duration_days': 'میانگین مدت (روز)'
                 }), use_container_width=True)

with tab2:
    st.subheader("ارزیابی آمادگی هوش مصنوعی")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(readiness, x='proc_def_name', y='final_score',
                     title='AI Readiness Score',
                     color='final_score',
                     color_continuous_scale='RdYlGn',
                     range_color=[0, 10])
        fig.add_hline(y=7, line_dash="dash", line_color="green", annotation_text="HIGH")
        fig.add_hline(y=5, line_dash="dash", line_color="orange", annotation_text="MEDIUM")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        categories = ['rework_score', 'duration_score', 'completion_score', 'resource_score', 'volume_score']
        labels = ['Rework', 'Duration', 'Completion', 'Resource', 'Volume']
        
        fig = go.Figure()
        for _, row in readiness.iterrows():
            values = [row[c] for c in categories]
            values.append(values[0])
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=labels + [labels[0]],
                fill='toself',
                name=row['proc_def_name']
            ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
            title='نمودار رادار AI Readiness'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # کارت‌های امتیاز
    st.subheader("جزئیات امتیازات")
    cols = st.columns(len(readiness))
    for i, (_, row) in enumerate(readiness.iterrows()):
        with cols[i]:
            color = "🟢" if row['final_score'] >= 7 else "🟡" if row['final_score'] >= 5 else "🔴"
            st.metric(
                label=f"{color} {row['proc_def_name']}",
                value=f"{row['final_score']}/10",
                delta=row['status']
            )

with tab3:
    st.subheader("تحلیل فعالیت‌ها")
    
    proc_filter = st.selectbox("انتخاب فرآیند:", ['همه'] + list(activities['proc_def_key'].unique()))
    
    if proc_filter != 'همه':
        df_filtered = activities[activities['proc_def_key'] == proc_filter]
    else:
        df_filtered = activities
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(df_filtered.sort_values('avg_duration_days', ascending=True),
                     x='avg_duration_days', y='act_name',
                     orientation='h',
                     title='میانگین مدت هر فعالیت (روز)',
                     color='avg_duration_days',
                     color_continuous_scale='RdYlGn_r')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(df_filtered.sort_values('deleted_count', ascending=True),
                     x='deleted_count', y='act_name',
                     orientation='h',
                     title='تعداد رویدادهای حذف شده هر فعالیت',
                     color='deleted_count',
                     color_continuous_scale='RdYlGn_r')
        st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.subheader("توصیه‌های بهبود")
    
    col1, col2 = st.columns(2)
    
    improvement = recommendations[recommendations['category'] == 'IMPROVEMENT']
    ai_recs = recommendations[recommendations['category'] == 'AI']
    
    with col1:
        st.markdown("### 🔧 توصیه‌های بهبود فرآیند")
        for _, row in improvement.iterrows():
            priority_color = "🔴" if row['priority'] == 1 else "🟡"
            st.info(f"{priority_color} **{row['proc_def_name']}**: {row['recommendation']}")
    
    with col2:
        st.markdown("### 🤖 پتانسیل هوش مصنوعی")
        for _, row in ai_recs.iterrows():
            st.success(f"✅ **{row['proc_def_name']}**: {row['recommendation']}")

st.markdown("---")
st.caption("Process Mining Dashboard | Powered by PM4Py & Streamlit")
