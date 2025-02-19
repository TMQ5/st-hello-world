import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import arabic_reshaper
from bidi.algorithm import get_display
import matplotlib.ticker as ticker


# تحميل البيانات
apartments_file = "apartments_data_cleaned.csv"
villas_file = "villas_data_cleaned.csv"

df_apartments = pd.read_csv(apartments_file)
df_villas = pd.read_csv(villas_file)

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
district_counts_apartments = df_apartments['الحي'].value_counts().reset_index()
district_counts_apartments.columns = ['الحي', 'count']
top_districts_apartments = district_counts_apartments.head(10)

# حساب عدد الفلل في كل حي
district_counts_villas = df_villas['الحي'].value_counts().reset_index()
district_counts_villas.columns = ['الحي', 'count']
top_districts_villas = district_counts_villas.head(10)

# حساب متوسط السعر الإجمالي لكل حي للشقق
district_avg_price_apartments = df_apartments[df_apartments['السعر الاجمالي'] > 500].groupby('الحي')['السعر الاجمالي'].mean().reset_index()
district_avg_price_apartments = district_avg_price_apartments.sort_values(by='السعر الاجمالي', ascending=True)
top_cheapest_districts_apartments = district_avg_price_apartments.head(10)

# حساب متوسط السعر الإجمالي لكل حي للفلل
district_avg_price_villas = df_villas[df_villas['السعر الاجمالي'] > 500].groupby('الحي')['السعر الاجمالي'].mean().reset_index()
district_avg_price_villas = district_avg_price_villas.sort_values(by='السعر الاجمالي', ascending=True)
top_cheapest_districts_villas = district_avg_price_villas.head(10)

# إنشاء figure و 4 محاور (subplot)
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1️⃣ عدد الشقق في كل حي
axes[0, 0].set_title(get_display(arabic_reshaper.reshape("ما هي الأحياء التي تحتوي على أكبر عدد من الشقق؟")))
sns.barplot(y=[get_display(arabic_reshaper.reshape(label)) for label in top_districts_apartments['الحي']], x=top_districts_apartments['count'], palette="mako", orient='h', ax=axes[0, 0])
axes[0, 0].set_xlabel(get_display(arabic_reshaper.reshape("عدد الشقق")))
axes[0, 0].set_ylabel(get_display(arabic_reshaper.reshape("الحي")))
axes[0, 0].invert_yaxis()

# 2️⃣ عدد الفلل في كل حي
axes[0, 1].set_title(get_display(arabic_reshaper.reshape("ما هي الأحياء التي تحتوي على أكبر عدد من الفلل؟")))
sns.barplot(y=[get_display(arabic_reshaper.reshape(label)) for label in top_districts_villas['الحي']], x=top_districts_villas['count'], palette="mako", orient='h', ax=axes[0, 1])
axes[0, 1].set_xlabel(get_display(arabic_reshaper.reshape("عدد الفلل")))
axes[0, 1].set_ylabel(get_display(arabic_reshaper.reshape("الحي")))
axes[0, 1].invert_yaxis()

# 3️⃣ متوسط السعر الإجمالي للشقق
axes[1, 0].set_title(get_display(arabic_reshaper.reshape("ما هي الأحياء الأقل سعراً في متوسط السعر الإجمالي للشقق؟")))
sns.barplot(y=[get_display(arabic_reshaper.reshape(label)) for label in top_cheapest_districts_apartments['الحي']], x=top_cheapest_districts_apartments['السعر الاجمالي'], palette="mako", orient='h', ax=axes[1, 0])
axes[1, 0].set_xlabel(get_display(arabic_reshaper.reshape("متوسط السعر الإجمالي")))
axes[1, 0].set_ylabel(get_display(arabic_reshaper.reshape("الحي")))
axes[1, 0].invert_yaxis()
axes[1, 0].xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

# 4️⃣ متوسط السعر الإجمالي للفلل
axes[1, 1].set_title(get_display(arabic_reshaper.reshape("ما هي الأحياء الأقل سعراً في متوسط السعر الإجمالي للفلل؟")))
sns.barplot(y=[get_display(arabic_reshaper.reshape(label)) for label in top_cheapest_districts_villas['الحي']], x=top_cheapest_districts_villas['السعر الاجمالي'], palette="mako", orient='h', ax=axes[1, 1])
axes[1, 1].set_xlabel(get_display(arabic_reshaper.reshape("متوسط السعر الإجمالي")))
axes[1, 1].set_ylabel(get_display(arabic_reshaper.reshape("الحي")))
axes[1, 1].invert_yaxis()
axes[1, 1].xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

# تحسين توزيع الشكل
plt.tight_layout()
st.pyplot(fig)

# رسالة ختامية
st.markdown("<div style='text-align: center; direction: rtl; background-color: #eafbea; padding: 10px; border-radius: 10px;'>🎉 استمتع بتحليل البيانات واختيار بيت العمر المثالي 🏡</div>", unsafe_allow_html=True)
