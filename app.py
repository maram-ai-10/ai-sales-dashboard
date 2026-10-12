import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# إعدادات صفحة الموقع
st.set_page_config(page_title="AI Sales & Inventory Dashboard", layout="wide")

st.title("📊 لوحة تحليلات المبيعات وتوقعات الذكاء الاصطناعي")
st.markdown("مرحباً بكِ في لوحة التحكم التفاعلية الذكية لتحليل المخزون والتنبؤ بالمبيعات.")

# 1. قراءة البيانات
try:
    df = pd.read_excel('sales.xlsx')
    df['Total'] = df['Quantity'] * df['Price']
except Exception as e:
    st.error("يرجى التأكد من وجود ملف sales.xlsx داخل مجلد المشروع!")
    st.stop()

# 2. بطاقات المؤشرات الرئيسية (KPIs)
col1, col2, col3 = st.columns(3)
total_revenue = df['Total'].sum()
top_product = df.loc[df['Quantity'].idxmax()]['Product']
low_stock_count = len(df[df['Stock'] < 5])

col1.metric("إجمالي الإيرادات ($)", f"${total_revenue:,.2f}")
col2.metric("المنتج الأكثر مبيعاً", top_product)
col3.metric("تنبيهات انخفاض المخزون", f"{low_stock_count} منتجات", delta_color="inverse")

st.divider()

# 3. عرض جدول البيانات والرسوم البيانية
c1, c2 = st.columns([1, 1])

with c1:
    st.subheader("📋 جدول البيانات الحالي")
    st.dataframe(df, use_container_width=True)

with c2:
    st.subheader("📈 أداء المبيعات حسب المنتج")
    st.bar_chart(data=df.set_index('Product')['Total'], use_container_width=True)

st.divider()

# 4. قسم الذكاء الاصطناعي: التنبؤ بالمبيعات (Machine Learning)
st.subheader("🤖 التنبؤ الذكي بالمبيعات (Linear Regression)")
st.caption("يقوم النموذج بتوقع الكمية المتوقع بيعها بناءً على سعر المنتج المحدد.")

# تدريب نموذج انحدار خطي بسيط
X = df[['Price']].values
y = df['Quantity'].values


model = LinearRegression()
model.fit(X, y)

user_price = st.slider("حددي سعر المنتج لاختبار التوقع ($):", min_value=10, max_value=1000, value=150, step=10)
predicted_qty = model.predict(np.array([[user_price]]))[0]
predicted_qty = max(1, round(predicted_qty))

st.success(f"الكمية المتوقع بيعها عند سعر ${user_price} هي تقريباً: {predicted_qty} قطعة")











