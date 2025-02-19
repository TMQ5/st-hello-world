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
st.title("🏡 بيت العمر - اختيار المنزل المثالي")
st.write("### ✨ اختر نوع المنزل: شقة أم فيلا؟")

# اختيار نوع العقار
property_type = st.radio("اختر نوع العقار", ["شقة", "فيلا"])

if property_type == "شقة":
    df_selected = df_apartments
    st.write("### 🏢 استكشاف خيارات الشقق")
else:
    df_selected = df_villas
    st.write("### 🏠 استكشاف خيارات الفلل")

# اختيار عدد الغرف
num_rooms = st.slider("كم عدد الغرف التي تحتاجها؟", min_value=3, max_value=10, value=7)
st.write(f"🔹 اخترت {num_rooms} غرف!")

# اختيار مساحة المنزل
space_options = {"صغيرة (50-100م²)": (50, 100), "متوسطة (100-200م²)": (100, 200), "كبيرة (200-400م²)": (200, 400)}
selected_space = st.selectbox("ما هي المساحة المناسبة؟", list(space_options.keys()))
space_range = space_options[selected_space]
st.write(f"🔹 اخترت {selected_space}!")

# تصفية البيانات بناءً على الاختيارات
df_filtered = df_selected[(df_selected['عدد الغرف'] >= num_rooms) & (df_selected['المساحة'].between(space_range[0], space_range[1]))]

# عرض إحصائيات المنازل المتاحة
st.write("### 🏠 المنازل المتاحة بهذه المواصفات:")
st.write(f"تم العثور على {df_filtered.shape[0]} منزلًا يتطابق مع اختياراتك!")

# رسم المخططات البيانية
fig, ax = plt.subplots(figsize=(8, 5))
sns.countplot(data=df_filtered, x='عدد الغرف', palette='Blues')
plt.title("توزيع عدد الغرف في المنازل المتاحة")
plt.xlabel("عدد الغرف")
plt.ylabel("عدد المنازل")
st.pyplot(fig)

fig2, ax2 = plt.subplots(figsize=(8, 5))
sns.histplot(df_filtered["المساحة"], bins=30, kde=True, color='blue')
plt.title("توزيع المساحات في المنازل المتاحة")
plt.xlabel("المساحة (م²)")
plt.ylabel("عدد المنازل")
st.pyplot(fig2)

# عرض جدول المنازل المتاحة
st.write("### 🏡 تفاصيل المنازل المتاحة:")
st.dataframe(df_filtered[['عدد الغرف', 'المساحة', 'السعر الاجمالي']].sort_values(by='السعر الاجمالي'))

# رسالة ختامية
st.success("🎉 استمتع بتحليل البيانات واختيار بيت العمر المثالي! 🏡✨")
