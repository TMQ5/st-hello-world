import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# تحميل البيانات من ملف الإكسل
file_path = "Riyadh_Aqqar.xlsx"
df_land = pd.read_excel(file_path, sheet_name="Land (الاراضي)")
df_villas = pd.read_excel(file_path, sheet_name="Villas (الفلل)")
df_apartments = pd.read_excel(file_path, sheet_name="Apartments (الشقق)")

# عنوان القصة
st.title("🏡 بيت الجدة – اختيار المنزل المثالي للعائلة السعودية")
st.write("### تجمعات العائلة لا تكتمل إلا في بيت الجدة! ✨")
st.write("خلونا نكتشف معًا كم عدد الغرف التي نحتاجها؟ وما هي المساحة المناسبة؟")

# اختيار عدد الغرف
num_rooms = st.slider("كم عدد الغرف التي يحتاجها بيت الجدة؟", min_value=3, max_value=10, value=7)
st.write(f"🔹 اخترت {num_rooms} غرف لبيت الجدة!")

# اختيار مساحة البيت
space_options = {"صغيرة (300-400م²)": (300, 400), "متوسطة (400-600م²)": (400, 600), "كبيرة (600-1000م²)": (600, 1000)}
selected_space = st.selectbox("ما هي المساحة المناسبة؟", list(space_options.keys()))
space_range = space_options[selected_space]
st.write(f"🔹 اخترت {selected_space} لبيت الجدة!")

# تصفية البيانات بناءً على الاختيارات
filtered_df = df_villas[(df_villas['عدد الغرف'] >= num_rooms) & (df_villas['المساحة'].between(space_range[0], space_range[1]))]

# عرض إحصائيات المنازل المتاحة
st.write("### 🏠 المنازل المتاحة بهذه المواصفات:")
st.write(f"تم العثور على {filtered_df.shape[0]} منزلًا يتطابق مع اختياراتك!")

# رسم المخططات البيانية
fig, ax = plt.subplots(figsize=(8, 5))
sns.countplot(data=filtered_df, x='عدد الغرف', palette='Blues')
plt.title("توزيع عدد الغرف في المنازل المتاحة")
plt.xlabel("عدد الغرف")
plt.ylabel("عدد المنازل")
st.pyplot(fig)

fig2, ax2 = plt.subplots(figsize=(8, 5))
sns.countplot(data=filtered_df, x='المساحة', palette='Greens')
plt.title("توزيع المساحات في المنازل المتاحة")
plt.xlabel("المساحة (م²)")
plt.ylabel("عدد المنازل")
st.pyplot(fig2)

# عرض جدول المنازل المتاحة
st.write("### 🏡 تفاصيل المنازل المتاحة:")
st.dataframe(filtered_df[['عدد الغرف', 'المساحة', 'السعر الاجمالي', 'السعر المربع']].sort_values(by='السعر الاجمالي'))

# رسالة ختامية
st.success("🎉 استمتع بتحليل البيانات واختيار بيت الجدة المثالي! لا تنسَ أن تشاركنا ذكرياتك الجميلة عن بيت الجدة 👵❤️")
