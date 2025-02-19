import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import arabic_reshaper
from bidi.algorithm import get_display

# تحميل بيانات الشقق
apartments_file = "apartments_data_cleaned.csv"
df_apartments = pd.read_csv(apartments_file)

# التأكد من توفر الأعمدة المطلوبة
required_columns = ["الحي", "السعر الاجمالي"]
for col in required_columns:
    if col not in df_apartments.columns:
        st.error(f"❌ العمود '{col}' غير موجود في البيانات، تحقق من الاسم الصحيح!")
        st.stop()

# 🏡 المقدمة
st.title("🏡 بيت العمر.. الحلم الذي يستحق كل خطوة!")

st.write("""
إذا كنت تدور على بيت العمر في الرياض، فأنت في المكان الصح! 🤩🏙️  
هنا بتلقى كل التفاصيل اللي تحتاجها قبل ما تاخذ القرار، عشان تشتري بيتك بثقة وراحة بال.

📊 **وش جمعنا لك؟**  
✅ أكثر الأحياء طلبًا وأفضلها من حيث الخدمات 🔍  
✅ متوسط الأسعار في كل منطقة 💰  
✅ عدد الغرف والمساحات المناسبة لك 🏡  

🔥 باستخدام الأرقام، بتعرف أي خيار هو الأفضل لك!
""")

# حساب عدد الشقق في كل حي
district_counts = df_apartments[df_apartments['الحي'] != ' الرياض ']['الحي'].value_counts().reset_index()
district_counts.columns = ['الحي', 'count']

# أخذ أكثر 10 أحياء بها شقق
top_districts = district_counts.head(10)

# حساب متوسط السعر الإجمالي لكل حي واستبعاد القيم غير المنطقية
district_avg_price = df_apartments[df_apartments['السعر الاجمالي'] > 500].groupby('الحي')['السعر الاجمالي'].mean().reset_index()

# ترتيب الأحياء من الأقل إلى الأعلى في السعر الإجمالي
district_avg_price = district_avg_price.sort_values(by='السعر الاجمالي', ascending=True)

# أخذ أرخص 10 أحياء
top_cheapest_districts = district_avg_price.head(10)

# تجهيز النصوص العربية
title_text1 = get_display(arabic_reshaper.reshape('ما هي الأحياء التي تحتوي على أكبر عدد من الشقق'))
xlabel_text1 = get_display(arabic_reshaper.reshape('الحي'))
ylabel_text1 = get_display(arabic_reshaper.reshape('عدد الشقق'))

title_text2 = get_display(arabic_reshaper.reshape('ما هي الأحياء الأقل سعرًا في متوسط السعر الإجمالي'))
xlabel_text2 = get_display(arabic_reshaper.reshape('الحي'))
ylabel_text2 = get_display(arabic_reshaper.reshape('متوسط السعر الإجمالي'))

# إنشاء الرسمين البيانيين بجانب بعضهما
fig, axes = plt.subplots(1, 2, figsize=(18, 6))

# الرسم الأول - أكثر 10 أحياء تحتوي على شقق
ax1 = sns.barplot(ax=axes[0], x=top_districts['الحي'], y=top_districts['count'], palette="viridis")
ax1.set_xticklabels([get_display(arabic_reshaper.reshape(label.get_text())) for label in ax1.get_xticklabels()], rotation=45)
ax1.set_xlabel(xlabel_text1, fontsize=12)
ax1.set_ylabel(ylabel_text1, fontsize=12)
ax1.set_title(title_text1, fontsize=14)

# الرسم الثاني - أقل 10 أحياء من حيث متوسط السعر الإجمالي
ax2 = sns.barplot(ax=axes[1], x=top_cheapest_districts['الحي'], y=top_cheapest_districts['السعر الاجمالي'], palette="viridis")
ax2.set_xticklabels([get_display(arabic_reshaper.reshape(label.get_text())) for label in ax2.get_xticklabels()], rotation=45)
ax2.set_xlabel(xlabel_text2, fontsize=12)
ax2.set_ylabel(ylabel_text2, fontsize=12)
ax2.set_title(title_text2, fontsize=14)

# عرض الرسم في Streamlit
st.pyplot(fig)



# st.write("### ✨ اختر نوع المنزل: شقة أم فيلا؟")

# # اختيار نوع العقار
# property_type = st.radio("اختر نوع العقار", ["شقة", "فيلا"])

# if property_type == "شقة":
#     st.subheader("🏢 استكشاف خيارات الشقق")
#     num_rooms = st.slider("كم عدد الغرف التي تحتاجها؟", min_value=1, max_value=10, value=3)
#     st.write(f"🔹 اخترت {num_rooms} غرف!")
    
#     df_selected = df_apartments[df_apartments['عدد الغرف'] >= num_rooms]
    
#     st.write("### 🏡 المنازل المتاحة بهذه المواصفات:")
#     st.write(f"تم العثور على {df_selected.shape[0]} شقة تتطابق مع اختياراتك!")
    
#     fig, ax = plt.subplots(figsize=(8, 5))
#     sns.countplot(data=df_selected, x='عدد الغرف', palette='Blues')
#     plt.title("توزيع عدد الغرف في الشقق المتاحة")
#     plt.xlabel("عدد الغرف")
#     plt.ylabel("عدد الشقق")
#     st.pyplot(fig)
    
#     st.write("### 🏡 تفاصيل الشقق المتاحة:")
#     st.dataframe(df_selected[['عدد الغرف', 'السعر الاجمالي']].sort_values(by='السعر الاجمالي'))
    
# else:
#     st.subheader("🏠 استكشاف خيارات الفلل")
#     num_rooms = st.slider("كم عدد الغرف التي تحتاجها؟", min_value=3, max_value=10, value=7)
#     st.write(f"🔹 اخترت {num_rooms} غرف!")
    
#     space_options = {"صغيرة (300-400م²)": (300, 400), "متوسطة (400-600م²)": (400, 600), "كبيرة (600-1000م²)": (600, 1000)}
#     selected_space = st.selectbox("ما هي المساحة المناسبة؟", list(space_options.keys()))
#     space_range = space_options[selected_space]
#     st.write(f"🔹 اخترت {selected_space}!")
    
#     df_selected = df_villas[(df_villas['عدد الغرف'] >= num_rooms) & (df_villas['المساحة'].between(space_range[0], space_range[1]))]
    
#     st.write("### 🏡 المنازل المتاحة بهذه المواصفات:")
#     st.write(f"تم العثور على {df_selected.shape[0]} فيلا تتطابق مع اختياراتك!")
    
#     fig, ax = plt.subplots(figsize=(8, 5))
#     sns.countplot(data=df_selected, x='عدد الغرف', palette='Blues')
#     plt.title("توزيع عدد الغرف في الفلل المتاحة")
#     plt.xlabel("عدد الغرف")
#     plt.ylabel("عدد الفلل")
#     st.pyplot(fig)
    
#     fig2, ax2 = plt.subplots(figsize=(8, 5))
#     sns.histplot(df_selected["المساحة"], bins=30, kde=True, color='blue')
#     plt.title("توزيع المساحات في الفلل المتاحة")
#     plt.xlabel("المساحة (م²)")
#     plt.ylabel("عدد الفلل")
#     st.pyplot(fig2)
    
#     st.write("### 🏡 تفاصيل الفلل المتاحة:")
#     st.dataframe(df_selected[['عدد الغرف', 'المساحة', 'السعر الاجمالي']].sort_values(by='السعر الاجمالي'))

# # رسالة ختامية
# st.success("🎉 استمتع بتحليل البيانات واختيار بيت العمر المثالي! 🏠")
