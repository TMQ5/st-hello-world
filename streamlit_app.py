import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import arabic_reshaper
from bidi.algorithm import get_display

# تحميل البيانات بعد التنظيف
villas_file = "villas_data_cleaned.csv"
apartments_file = "apartments_data_cleaned.csv"

df_villas = pd.read_csv(villas_file)
df_apartments = pd.read_csv(apartments_file)

# التحقق من صحة البيانات
required_columns = ["عدد الغرف", "السعر الاجمالي", "الحي"]
for col in required_columns:
    if col not in df_apartments.columns:
        st.error(f"❌ العمود '{col}' غير موجود في بيانات الشقق، تحقق من الاسم الصحيح!")
        st.stop()

# عنوان القصة
st.title("🏡 بيت العمر.. الحلم الذي يستحق كل خطوة!")
st.markdown(
    """
    <div style="text-align: center;">
        🏙️ إذا كنت تدور على بيت العمر في الرياض، فأنت في المكان الصح! 🤩
        <br> هنا بتلقى كل التفاصيل اللي تحتاجها قبل ما تاخذ القرار، عشان تشتري بيتك بثقة وراحة بال.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="text-align: center;">
        🔍 وش جمعنا لك؟
        <br> ✅ أكثر الأحياء طلبًا وأفضلها من حيث الخدمات
        <br> ✅ متوسط الأسعار في كل منطقة 💰
        <br> ✅ عدد الغرف والمساحات المناسبة لك 🏡
    </div>
    """,
    unsafe_allow_html=True
)

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
title_text_1 = get_display(arabic_reshaper.reshape('ما هي الأحياء التي تحتوي على أكبر عدد من الشقق'))
title_text_2 = get_display(arabic_reshaper.reshape('ما هي الأحياء الأقل سعرًا في متوسط السعر الإجمالي'))
xlabel_text = get_display(arabic_reshaper.reshape('الحي'))
ylabel_text_1 = get_display(arabic_reshaper.reshape('عدد الشقق'))
ylabel_text_2 = get_display(arabic_reshaper.reshape('متوسط السعر الإجمالي'))

# رسم المخططات البيانية
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# الرسم الأول - عدد الشقق في كل حي
sns.barplot(ax=axes[0], x=top_districts['الحي'], y=top_districts['count'], palette="mako")
axes[0].set_xticklabels([get_display(arabic_reshaper.reshape(label.get_text())) for label in axes[0].get_xticklabels()], rotation=45)
axes[0].set_xlabel(xlabel_text, fontsize=12)
axes[0].set_ylabel(ylabel_text_1, fontsize=12)
axes[0].set_title(title_text_1, fontsize=16)

# الرسم الثاني - متوسط الأسعار في كل حي
sns.barplot(ax=axes[1], x=top_cheapest_districts['الحي'], y=top_cheapest_districts['السعر الاجمالي'], palette="mako")
axes[1].set_xticklabels([get_display(arabic_reshaper.reshape(label.get_text())) for label in axes[1].get_xticklabels()], rotation=45)
axes[1].set_xlabel(xlabel_text, fontsize=12)
axes[1].set_ylabel(ylabel_text_2, fontsize=12)
axes[1].set_title(title_text_2, fontsize=16)

st.pyplot(fig)

# رسالة ختامية
st.markdown(
    """
    <div style="text-align: center;">
        🎉 استمتع بتحليل البيانات واختار بيت العمر المثالي 🏡
    </div>
    """,
    unsafe_allow_html=True
)
