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
required_columns_villas = ["عدد الغرف", "المساحة", "السعر الاجمالي"]
required_columns_apartments = ["عدد الغرف", "السعر الاجمالي"]

for col in required_columns_villas:
    if col not in df_villas.columns:
        st.error(f"❌ العمود '{col}' غير موجود في بيانات الفلل، تحقق من الاسم الصحيح!")
        st.stop()

for col in required_columns_apartments:
    if col not in df_apartments.columns:
        st.error(f"❌ العمود '{col}' غير موجود في بيانات الشقق، تحقق من الاسم الصحيح!")
        st.stop()

# عنوان القصة
st.title("🏡 بيت العمر - اختيار المنزل المثالي للعائلة السعودية")
st.write("### ✨ اختر نوع المنزل: شقة أم فيلا؟")

# اختيار نوع العقار
property_type = st.radio("اختر نوع العقار", ["شقة", "فيلا"])

if property_type == "شقة":
    st.subheader("🏢 استكشاف خيارات الشقق")
    num_rooms = st.slider("كم عدد الغرف التي تحتاجها؟", min_value=1, max_value=10, value=3)
    st.write(f"🔹 اخترت {num_rooms} غرف!")
    
    df_selected = df_apartments[df_apartments['عدد الغرف'] >= num_rooms]
    
    st.write("### 🏡 المنازل المتاحة بهذه المواصفات:")
    st.write(f"تم العثور على {df_selected.shape[0]} شقة تتطابق مع اختياراتك!")
    
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(data=df_selected, x='عدد الغرف', palette='Blues')
    plt.title("توزيع عدد الغرف في الشقق المتاحة")
    plt.xlabel("عدد الغرف")
    plt.ylabel("عدد الشقق")
    st.pyplot(fig)
    
    st.write("### 🏡 تفاصيل الشقق المتاحة:")
    st.dataframe(df_selected[['عدد الغرف', 'السعر الاجمالي']].sort_values(by='السعر الاجمالي'))
    
else:
    st.subheader("🏠 استكشاف خيارات الفلل")
    num_rooms = st.slider("كم عدد الغرف التي تحتاجها؟", min_value=3, max_value=10, value=7)
    st.write(f"🔹 اخترت {num_rooms} غرف!")
    
    space_options = {"صغيرة (300-400م²)": (300, 400), "متوسطة (400-600م²)": (400, 600), "كبيرة (600-1000م²)": (600, 1000)}
    selected_space = st.selectbox("ما هي المساحة المناسبة؟", list(space_options.keys()))
    space_range = space_options[selected_space]
    st.write(f"🔹 اخترت {selected_space}!")
    
    df_selected = df_villas[(df_villas['عدد الغرف'] >= num_rooms) & (df_villas['المساحة'].between(space_range[0], space_range[1]))]
    
    st.write("### 🏡 المنازل المتاحة بهذه المواصفات:")
    st.write(f"تم العثور على {df_selected.shape[0]} فيلا تتطابق مع اختياراتك!")
    
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(data=df_selected, x='عدد الغرف', palette='Blues')
    plt.title("توزيع عدد الغرف في الفلل المتاحة")
    plt.xlabel("عدد الغرف")
    plt.ylabel("عدد الفلل")
    st.pyplot(fig)
    
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    sns.histplot(df_selected["المساحة"], bins=30, kde=True, color='blue')
    plt.title("توزيع المساحات في الفلل المتاحة")
    plt.xlabel("المساحة (م²)")
    plt.ylabel("عدد الفلل")
    st.pyplot(fig2)
    
    st.write("### 🏡 تفاصيل الفلل المتاحة:")
    st.dataframe(df_selected[['عدد الغرف', 'المساحة', 'السعر الاجمالي']].sort_values(by='السعر الاجمالي'))

# رسالة ختامية
st.success("🎉 استمتع بتحليل البيانات واختيار بيت العمر المثالي! 🏠")
