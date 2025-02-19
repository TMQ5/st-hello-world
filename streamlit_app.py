import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import arabic_reshaper
from bidi.algorithm import get_display

# تحميل البيانات
apartments_file = "apartments_data_cleaned.csv"
df_apartments = pd.read_csv(apartments_file)

# إعداد الصفحة والعنوان
st.set_page_config(layout="wide")

st.markdown("<h1 style='text-align: center; direction: rtl;'>🏡 بيت العمر.. الحلم الذي يستحق كل خطوة!</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; direction: rtl;'>📊 إذا كنت تبحث عن بيت العمر في الرياض، فأنت في المكان الصحيح! 🤩🏙️ <br> هنا ستجد كل التفاصيل التي تحتاجها قبل اتخاذ القرار، لتتمكن من شراء بيتك بثقة وراحة بال.</p>", unsafe_allow_html=True)

# تنسيق النقاط الرئيسية في المنتصف بشكل متناسق
st.markdown("""
<div style="text-align: center; direction: rtl;">
✅ 🔍 <strong>أكثر الأحياء طلبًا وأفضلها من حيث الخدمات</strong> <br>
✅ 💰 <strong>متوسط الأسعار في كل منطقة</strong> <br>
✅ 🏡 <strong>عدد الغرف والمساحات المناسبة لك</strong> <br>
</div>
""", unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center; direction: rtl;'>🔥 باستخدام الأرقام، ستعرف أي خيار هو الأفضل لك!</h3>", unsafe_allow_html=True)

# حساب عدد الشقق في كل حي
district_counts = df_apartments[df_apartments['الحي'] != ' الرياض ']['الحي'].value_counts().reset_index()
district_counts.columns = ['الحي', 'count']
top_districts = district_counts.head(10)

# تجهيز النصوص العربية
title_text_1 = get_display(arabic_reshaper.reshape(' ما هي الأحياء التي تحتوي على أكبر عدد من الشقق؟'))
xlabel_text_1 = get_display(arabic_reshaper.reshape('الحي'))
ylabel_text_1 = get_display(arabic_reshaper.reshape('عدد الشقق'))

# رسم مخطط عدد الشقق
fig, ax = plt.subplots(figsize=(6, 4))
sns.barplot(y=top_districts['الحي'], x=top_districts['count'], palette="mako", orient='h', ax=ax)
ax.set_yticklabels([get_display(arabic_reshaper.reshape(label.get_text())) for label in ax.get_yticklabels()])
ax.set_xlabel(xlabel_text_1, fontsize=12)
ax.set_ylabel(ylabel_text_1, fontsize=12)
ax.set_title(title_text_1, fontsize=14)
ax.invert_yaxis()  # جعل الترتيب من اليمين لليسار

# حساب متوسط السعر الإجمالي لكل حي
district_avg_price = df_apartments[df_apartments['السعر الاجمالي'] > 500].groupby('الحي')['السعر الاجمالي'].mean().reset_index()
district_avg_price = district_avg_price.sort_values(by='السعر الاجمالي', ascending=True)
top_cheapest_districts = district_avg_price.head(10)

# تجهيز النصوص العربية للرسم الثاني
title_text_2 = get_display(arabic_reshaper.reshape('ما هي الأحياء الأقل سعراً في متوسط السعر الإجمالي للشقق؟'))
xlabel_text_2 = get_display(arabic_reshaper.reshape(' متوسط السعر الإجمالي'))
ylabel_text_2 = get_display(arabic_reshaper.reshape('الحي'))

# رسم مخطط متوسط السعر
fig2, ax2 = plt.subplots(figsize=(6, 4))
sns.barplot(y=top_cheapest_districts['الحي'], x=top_cheapest_districts['السعر الاجمالي'], palette="mako", orient='h', ax=ax2)
ax2.set_yticklabels([get_display(arabic_reshaper.reshape(label.get_text())) for label in ax2.get_yticklabels()])
ax2.set_xlabel(xlabel_text_2, fontsize=12)
ax2.set_ylabel(ylabel_text_2, fontsize=12)
ax2.set_title(title_text_2, fontsize=14)
ax2.invert_yaxis()  # جعل الترتيب من اليمين لليسار

# عرض المخططات جنبًا إلى جنب
col1, col2 = st.columns(2)
with col1:
    st.pyplot(fig)
with col2:
    st.pyplot(fig2)

# رسالة ختامية
st.markdown("<div style='text-align: center; direction: rtl; background-color: #eafbea; padding: 10px; border-radius: 10px;'>🎉 استمتع بتحليل البيانات واختيار بيت العمر المثالي 🏡</div>", unsafe_allow_html=True)
