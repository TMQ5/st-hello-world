import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# تحميل البيانات بعد التنظيف
villas_file = "villas_data_cleaned.csv"
apartments_file = "apartments_data_cleaned.csv"

df_villas = pd.read_csv(villas_file)
df_apartments = pd.read_csv(apartments_file)

# التحقق من صحة البيانات
required_columns = ["عدد الغرف", "المساحة", "السعر الاجمالي"]

for col in required_columns:
    if col not in df_villas.columns or col not in df_apartments.columns:
        st.error(f"❌ العمود '{col}' غير موجود في البيانات، تحقق من الاسم الصحيح!")
        st.stop()

# عنوان القصة
st.title("🏡 بيت الجدة - اختيار المنزل المثالي للعائلة السعودية")
st.write("### ✨ تجمعات العائلة لا تكتمل إلا في بيت الجدة!")
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
df_selected = df_villas[(df_villas['عدد الغرف'] >= num_rooms) & (df_villas['المساحة'].between(space_range[0], space_range[1]))]

# عرض إحصائيات المنازل المتاحة
st.write("### 🏠 المنازل المتاحة بهذه المواصفات:")
st.write(f"تم العثور على {df_selected.shape[0]} منزلًا يتطابق مع اختياراتك!")

# رسم المخططات البيانية
fig, ax = plt.subplots(figsize=(8, 5))
sns.countplot(data=df_selected, x='عدد الغرف', palette='Blues')
plt.title("توزيع عدد الغرف في المنازل المتاحة")
plt.xlabel("عدد الغرف")
plt.ylabel("عدد المنازل")
st.pyplot(fig)

fig2, ax2 = plt.subplots(figsize=(8, 5))
sns.histplot(df_selected["المساحة"], bins=30, kde=True, color='blue')
plt.title("توزيع المساحات في المنازل المتاحة")
plt.xlabel("المساحة (م²)")
plt.ylabel("عدد المنازل")
st.pyplot(fig2)

# عرض جدول المنازل المتاحة
st.write("### 🏡 تفاصيل المنازل المتاحة:")
st.dataframe(df_selected[['عدد الغرف', 'المساحة', 'السعر الاجمالي']].sort_values(by='السعر الاجمالي'))

# رسالة ختامية
st.success("🎉 استمتع بتحليل البيانات واختيار بيت الجدة المثالي! لا تنسَ أن تشاركنا ذكرياتك الجميلة عن بيت الجدة 👵❤️")
