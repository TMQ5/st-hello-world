import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# تحميل البيانات بعد التأكد من المسار الصحيح
file_path = "Riyadh_Aqqar.xlsx"

# قراءة البيانات من التبويبات الصحيحة
df_villas = pd.read_excel(file_path, sheet_name="Villas (الفلل)")
df_apartments = pd.read_excel(file_path, sheet_name="Apartments (الشقق)")

# تنظيف أسماء الأعمدة من أي مسافات زائدة
df_villas.columns = df_villas.columns.str.strip()
df_apartments.columns = df_apartments.columns.str.strip()

# التأكد من أن الأعمدة المهمة موجودة وإلا يتم عرض خطأ
required_columns = ["عدد الغرف", "المساحة", "السعر الإجمالي", "السعر المربع"]
for col in required_columns:
    if col not in df_villas.columns or col not in df_apartments.columns:
        st.error(f"❌ العمود '{col}' غير موجود في البيانات، تحقق من الاسم الصحيح!")
        st.stop()

# تحويل القيم النصية إلى أرقام والتعامل مع القيم المفقودة
for col in ["عدد الغرف", "المساحة", "السعر الإجمالي", "السعر المربع"]:
    df_villas[col] = pd.to_numeric(df_villas[col], errors="coerce")
    df_apartments[col] = pd.to_numeric(df_apartments[col], errors="coerce")

# إزالة القيم الفارغة بعد التحويل
df_villas.dropna(subset=required_columns, inplace=True)
df_apartments.dropna(subset=required_columns, inplace=True)

# ------------------------- واجهة Streamlit -------------------------

# عنوان التطبيق
st.title("🏡 بيت الجدة – اختيار المنزل المثالي للعائلة السعودية")
st.write("### تجمعات العائلة لا تكتمل إلا في بيت الجدة! ✨")
st.write("خلونا نكتشف معًا كم عدد الغرف التي نحتاجها؟ وما هي المساحة المناسبة؟")

# اختيار نوع العقار (فيلا أو شقة)
property_type = st.radio("اختر نوع العقار:", ["فيلا", "شقة"])

# تحديد بيانات العقار المختارة
df_selected = df_villas if property_type == "فيلا" else df_apartments

# اختيار عدد الغرف
num_rooms = st.slider("كم عدد الغرف التي تحتاجها؟", min_value=3, max_value=10, value=5)
st.write(f"🔹 اخترت {num_rooms} غرف!")

# اختيار مساحة البيت
space_options = {
    "صغيرة (300-400م²)": (300, 400),
    "متوسطة (400-600م²)": (400, 600),
    "كبيرة (600-1000م²)": (600, 1000),
}
selected_space = st.selectbox("ما هي المساحة المناسبة؟", list(space_options.keys()))
space_range = space_options[selected_space]
st.write(f"🔹 اخترت {selected_space}!")

# تصفية البيانات بناءً على الاختيارات
df_filtered = df_selected[
    (df_selected["عدد الغرف"] >= num_rooms) & 
    (df_selected["المساحة"].between(space_range[0], space_range[1]))
]

# عرض عدد المنازل المتاحة
st.write("### 🏠 المنازل المتاحة بهذه المواصفات:")
st.write(f"تم العثور على {df_filtered.shape[0]} منزلًا يتطابق مع اختياراتك!")

# ---------------------- المخططات البيانية ----------------------

# رسم توزيع عدد الغرف
fig, ax = plt.subplots(figsize=(8, 5))
sns.countplot(data=df_filtered, x="عدد الغرف", palette="Blues")
plt.title("توزيع عدد الغرف في المنازل المتاحة")
plt.xlabel("عدد الغرف")
plt.ylabel("عدد المنازل")
st.pyplot(fig)

# رسم توزيع المساحات
fig2, ax2 = plt.subplots(figsize=(8, 5))
sns.histplot(df_filtered["المساحة"], bins=30, kde=True, color="blue")
plt.title("توزيع المساحات في المنازل المتاحة")
plt.xlabel("المساحة (م²)")
plt.ylabel("عدد المنازل")
st.pyplot(fig2)

# ---------------------- عرض بيانات المنازل ----------------------

# عرض جدول المنازل المتاحة
st.write("### 🏡 تفاصيل المنازل المتاحة:")
st.dataframe(df_filtered[["عدد الغرف", "المساحة", "السعر الإجمالي", "السعر المربع"]].sort_values(by="السعر الإجمالي"))

# ---------------------- رسالة ختامية ----------------------
st.success("🎉 استمتع بتحليل البيانات واختيار بيت الجدة المثالي! لا تنسَ أن تشاركنا ذكرياتك الجميلة عن بيت الجدة 👵❤️")
