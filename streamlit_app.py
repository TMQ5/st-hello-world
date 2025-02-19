import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# تحميل البيانات النظيفة
df_villas = pd.read_csv("villas_data_cleaned.csv")
df_apartments = pd.read_csv("apartments_data_cleaned.csv")

# ✅ إضافة عنوان Streamlit
st.title("🏡 تحليل الفلل والشقق في الرياض")

# ✅ اختيار نوع العقار (فلل أو شقق)
property_type = st.radio("اختر نوع العقار:", ["الفلل", "الشقق"])

# ✅ تصفية البيانات حسب الاختيار
if property_type == "الفلل":
    df_selected = df_villas
    st.subheader("📊 تحليل بيانات الفلل")
else:
    df_selected = df_apartments
    st.subheader("📊 تحليل بيانات الشقق")

# ✅ إظهار بعض الإحصائيات
st.write(f"عدد العقارات المتاحة: {df_selected.shape[0]}")

# ✅ رسم توزيع المساحات
fig, ax = plt.subplots(figsize=(8, 5))
sns.histplot(df_selected['المساحة'], bins=30, kde=True, color='blue')
plt.xlabel("المساحة بالمتر المربع")
plt.ylabel("عدد العقارات")
plt.title("توزيع المساحات")
st.pyplot(fig)

# ✅ رسم توزيع الأسعار
fig2, ax2 = plt.subplots(figsize=(8, 5))
sns.histplot(df_selected['السعر الاجمالي'], bins=30, kde=True, color='green')
plt.xlabel("السعر بالريال")
plt.ylabel("عدد العقارات")
plt.title("توزيع الأسعار")
st.pyplot(fig2)

# ✅ عرض جدول البيانات النظيفة
st.write("📋 **بيانات العقارات:**")
st.dataframe(df_selected)

st.success("🎉 استمتع بتحليل البيانات! 🚀")
