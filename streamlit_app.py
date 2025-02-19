import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# تحميل البيانات المنظفة
file_path = "Riyadh_Aqqar.xlsx"
df_villas = pd.read_excel(file_path, sheet_name="Villas (الفلل)")
df_apartments = pd.read_excel(file_path, sheet_name="Apartments (الشقق)")

# 🏡 عنوان القصة التفاعلية
st.title("🏡 بيت الجدة – اختيار المنزل المثالي للعائلة السعودية")
st.write("### تجمعات العائلة لا تكتمل إلا في بيت الجدة! ✨")
st.write("خلونا نكتشف معًا كم عدد الغرف التي نحتاجها؟ وما هي المساحة المناسبة؟")

# 🔹 اختيار عدد الغرف المطلوبة
num_rooms = st.slider("كم عدد الغرف التي يحتاجها بيت الجدة؟", min_value=3, max_value=10, value=7)
st.write(f"🔹 اخترت {num_rooms} غرف لبيت الجدة!")

# 🔹 اختيار مساحة البيت المناسبة
space_options = {
    "صغيرة (300-400م²)": (300, 400),
    "متوسطة (400-600م²)": (400, 600),
    "كبيرة (600-1000م²)": (600, 1000)
}
selected_space = st.selectbox("ما هي المساحة المناسبة؟", list(space_options.keys()))
space_range = space_options[selected_space]
st.write(f"🔹 اخترت {selected_space} لبيت الجدة!")

# 🔍 تصفية البيانات بناءً على الاختيارات
df_selected = df_villas[(df_villas['عدد الغرف'] >= num_rooms) & (df_villas['المساحة'].between(space_range[0], space_range[1]))]

# 🔹 التأكد من أن `المساحة` بيانات رقمية وإزالة القيم الفارغة
df_selected["المساحة"] = pd.to_numeric(df_selected["المساحة"], errors="coerce")
df_selected = df_selected.dropna(subset=["المساحة"])

# 📊 عرض إحصائيات المنازل المتاحة
st.write("### 🏠 المنازل المتاحة بهذه المواصفات:")
st.write(f"🔹 تم العثور على **{df_selected.shape[0]}** منزلًا يتطابق مع اختياراتك!")

# 📈 رسم توزيع عدد الغرف
fig, ax = plt.subplots(figsize=(8, 5))
sns.countplot(data=df_selected, x="عدد الغرف", palette="Blues")
plt.title("توزيع عدد الغرف في المنازل المتاحة")
plt.xlabel("عدد الغرف")
plt.ylabel("عدد المنازل")
st.pyplot(fig)

# 📉 رسم توزيع المساحات بعد التعديل
fig2, ax2 = plt.subplots(figsize=(8, 5))
sns.histplot(df_selected["المساحة"], bins=30, kde=True, color="blue")
plt.xlabel("المساحة بالمتر المربع")
plt.ylabel("عدد العقارات")
plt.title("توزيع المساحات في المنازل المتاحة")
st.pyplot(fig2)

# 📊 عرض جدول المنازل المتاحة مع الأسعار
st.write("### 🏡 تفاصيل المنازل المتاحة:")
st.dataframe(df_selected[['عدد الغرف', 'المساحة', 'السعر الإجمالي', 'السعر المتر']].sort_values(by='السعر الإجمالي'))

# 🎉 رسالة ختامية
st.success("🎉 استمتع بتحليل البيانات واختيار بيت الجدة المثالي! لا تنسَ أن تشاركنا ذكرياتك الجميلة عن بيت الجدة 👵❤️")
