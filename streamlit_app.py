import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import arabic_reshaper
from bidi.algorithm import get_display
import matplotlib.ticker as ticker

# تحميل البيانات
df_apartments = pd.read_csv("apartments_data_cleaned.csv")
df_villas = pd.read_csv("villas_data_cleaned.csv")



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
# تصفية البيانات للشقق
df_filtered_apartments = df_apartments[(df_apartments['المساحة'] <= 300) & 
                                        (df_apartments['السعر الاجمالي'] > 500) & 
                                        (df_apartments['الحي'] != ' ')]

# التحقق من أن البيانات ليست فارغة
if not df_filtered_apartments.empty:
    # حساب المتوسط لكل حي
    district_avg_space_apartments = df_filtered_apartments.groupby('الحي')['المساحة'].mean().reset_index()
    district_avg_space_apartments = district_avg_space_apartments.sort_values(by='المساحة', ascending=True)
    district_avg_space_apartments = district_avg_space_apartments.head(10)
else:
    district_avg_space_apartments = None  # تعيينها إلى None إذا كانت البيانات فارغة


# حساب عدد الفلل في كل حي
district_counts_villas = df_villas[df_villas['الحي'] != ' الرياض ']['الحي'].value_counts().reset_index()
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



# تحديد الألوان:
palette_apartments = "mako"  # ألوان خاصة بالشقق
palette_villas = "magma"  # ألوان خاصة بالفلل

### 1️⃣ **عدد الشقق و عدد الفلل في كل حي**
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# عدد الشقق في كل حي
axes[0].set_title(get_display(arabic_reshaper.reshape("ما هي الأحياء التي تحتوي على أكبر عدد من الشقق؟")))
if district_avg_space_apartments is not None and not district_avg_space_apartments.empty:
    sns.barplot(x=district_avg_space_apartments['المساحة'], 
                y=[get_display(arabic_reshaper.reshape(label)) for label in district_avg_space_apartments['الحي']], 
                palette=palette_apartments, ax=axes[0])
else:
    st.warning("لا توجد بيانات كافية لعرض مقارنة المساحات للشقق.")

sns.barplot(y=[get_display(arabic_reshaper.reshape(label)) for label in top_districts_apartments['الحي']], 
            x=top_districts_apartments['count'], palette=palette_apartments, orient='h', ax=axes[0])
axes[0].set_xlabel(get_display(arabic_reshaper.reshape("عدد الشقق")))
axes[0].set_ylabel(get_display(arabic_reshaper.reshape("الحي")))
axes[0].invert_yaxis()

# عدد الفلل في كل حي
axes[1].set_title(get_display(arabic_reshaper.reshape("ما هي الأحياء التي تحتوي على أكبر عدد من الفلل؟")))
sns.barplot(y=[get_display(arabic_reshaper.reshape(label)) for label in top_districts_villas['الحي']], 
            x=top_districts_villas['count'], palette=palette_villas, orient='h', ax=axes[1])
axes[1].set_xlabel(get_display(arabic_reshaper.reshape("عدد الفلل")))
axes[1].set_ylabel(get_display(arabic_reshaper.reshape("الحي")))
axes[1].invert_yaxis()

plt.tight_layout()
st.pyplot(fig)

### 2️⃣ **متوسط السعر الإجمالي للشقق والفلل**
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# متوسط السعر الإجمالي للشقق
axes[0].set_title(get_display(arabic_reshaper.reshape("ما هي الأحياء الأقل سعراً في متوسط السعر الإجمالي للشقق؟")))
sns.barplot(y=[get_display(arabic_reshaper.reshape(label)) for label in top_cheapest_districts_apartments['الحي']], 
            x=top_cheapest_districts_apartments['السعر الاجمالي'], palette=palette_apartments, orient='h', ax=axes[0])
axes[0].set_xlabel(get_display(arabic_reshaper.reshape("متوسط السعر الإجمالي")))
axes[0].set_ylabel(get_display(arabic_reshaper.reshape("الحي")))
axes[0].invert_yaxis()
axes[0].xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

# متوسط السعر الإجمالي للفلل
axes[1].set_title(get_display(arabic_reshaper.reshape("ما هي الأحياء الأقل سعراً في متوسط السعر الإجمالي للفلل؟")))
sns.barplot(y=[get_display(arabic_reshaper.reshape(label)) for label in top_cheapest_districts_villas['الحي']], 
            x=top_cheapest_districts_villas['السعر الاجمالي'], palette=palette_villas, orient='h', ax=axes[1])
axes[1].set_xlabel(get_display(arabic_reshaper.reshape("متوسط السعر الإجمالي")))
axes[1].set_ylabel(get_display(arabic_reshaper.reshape("الحي")))
axes[1].invert_yaxis()
axes[1].xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

plt.tight_layout()
st.pyplot(fig)

### 3️⃣ **مقارنة المساحات للشقق والفلل**
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# المساحات في الأحياء المختلفة للشقق
axes[0].set_title(get_display(arabic_reshaper.reshape("مقارنة المساحات في الأحياء المختلفة للشقق")))
sns.barplot(x=district_avg_space_apartments['المساحة'], 
            y=[get_display(arabic_reshaper.reshape(label)) for label in district_avg_space_apartments['الحي']], 
            palette=palette_apartments, ax=axes[0])
axes[0].set_xlabel(get_display(arabic_reshaper.reshape("متوسط المساحة (م²)")))
axes[0].set_ylabel(get_display(arabic_reshaper.reshape("الحي")))

# المساحات في الأحياء المختلفة للفلل
axes[1].set_title(get_display(arabic_reshaper.reshape("مقارنة المساحات في الأحياء المختلفة للفلل")))
sns.barplot(x=district_avg_space_villas['المساحة'], 
            y=[get_display(arabic_reshaper.reshape(label)) for label in district_avg_space_villas['الحي']], 
            palette=palette_villas, ax=axes[1])
axes[1].set_xlabel(get_display(arabic_reshaper.reshape("متوسط المساحة (م²)")))
axes[1].set_ylabel(get_display(arabic_reshaper.reshape("الحي")))

plt.tight_layout()
st.pyplot(fig)

### 4️⃣ **توزيع عدد الغرف في الشقق والفلل**
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# توزيع عدد الغرف في الشقق
axes[0].set_title(get_display(arabic_reshaper.reshape("ما هو توزيع عدد الغرف في الشقق؟")))
sns.barplot(x=top_rooms_apartments['عدد الغرف'], y=top_rooms_apartments['count'], palette=palette_apartments, ax=axes[0])
axes[0].set_xlabel(get_display(arabic_reshaper.reshape("عدد الغرف")))
axes[0].set_ylabel(get_display(arabic_reshaper.reshape("عدد الشقق")))

# توزيع عدد الغرف في الفلل
axes[1].set_title(get_display(arabic_reshaper.reshape("ما هو توزيع عدد الغرف في الفلل؟")))
sns.barplot(x=top_rooms_villas['عدد الغرف'], y=top_rooms_villas['count'], palette=palette_villas, ax=axes[1])
axes[1].set_xlabel(get_display(arabic_reshaper.reshape("عدد الغرف")))
axes[1].set_ylabel(get_display(arabic_reshaper.reshape("عدد الفلل")))

plt.tight_layout()
st.pyplot(fig)

# رسالة ختامية
st.markdown("<div style='text-align: center; direction: rtl; background-color: #eafbea; padding: 10px; border-radius: 10px;'>🎉  ✨🔮 الحين جاء دورك!😁 وش رأيك تختار بيت العمر المثالي وتستمتع بتحليل البيانات   🏡</div>", unsafe_allow_html=True)
# تنظيف عمود الحي بإزالة المسافات الزائدة في البداية والنهاية
df_apartments['الحي'] = df_apartments['الحي'].astype(str).str.strip()
df_villas['الحي'] = df_villas['الحي'].astype(str).str.strip()

# تصفية البيانات لاستبعاد "الرياض" والقيم الفارغة
df_apartments_filtered = df_apartments[(df_apartments['الحي'] != 'الرياض') & (df_apartments['الحي'].notna()) & (df_apartments['الحي'] != '')]
df_villas_filtered = df_villas[(df_villas['الحي'] != 'الرياض') & (df_villas['الحي'].notna()) & (df_villas['الحي'] != '')]

# # عنوان اختيار نوع العقار بنفس تنسيق الحي وعدد الغرف
st.markdown("<h4 style='text-align: right;'>  :اختر نوع العقار 🏡</h4>", unsafe_allow_html=True)

# # عنصر الاختيار بمحاذاة اليمين
property_type = st.radio("", ["شقة", "فيلا"], horizontal=True)




# اختيار الحي بناءً على نوع العقار
st.markdown("<h4 style='text-align: right;'>:اختر الحي 📍</h4>", unsafe_allow_html=True)
if property_type == "شقة":
    selected_district = st.selectbox("", df_apartments_filtered['الحي'].unique())
    filtered_df = df_apartments_filtered[df_apartments_filtered['الحي'] == selected_district]
else:
    selected_district = st.selectbox("", df_villas_filtered['الحي'].unique())
    filtered_df = df_villas_filtered[df_villas_filtered['الحي'] == selected_district]

# تأكد من أن final_filtered_df معرف دائمًا
final_filtered_df = pd.DataFrame()

# التحقق من أن الفلترة السابقة ليست فارغة قبل تحديد عدد الغرف والمساحة
if not filtered_df.empty:
    # اختيار عدد الغرف
    st.markdown("<h4 style='text-align: right;'>  :اختر عدد الغرف 🛏️</h4>", unsafe_allow_html=True)
    room_options = sorted(filtered_df['عدد الغرف'].dropna().unique())  # إزالة القيم الفارغة
    selected_rooms = st.selectbox("", room_options) if room_options else None

    # اختيار المساحة
    st.markdown("<h4 style='text-align: right;'>:اختر المساحة 📏</h4>", unsafe_allow_html=True)
    space_options = sorted(filtered_df['المساحة'].dropna().unique())  # إزالة القيم الفارغة
    selected_space = st.selectbox("", space_options) if space_options else None

    # تصفية البيانات بناءً على عدد الغرف والمساحة (تأكد من أن القيم ليست None)
    if selected_rooms is not None and selected_space is not None:
        final_filtered_df = filtered_df[
            (filtered_df['عدد الغرف'] == selected_rooms) & 
            (filtered_df['المساحة'] == selected_space)
        ]

# التحقق من عدم كون final_filtered_df فارغًا قبل استخدامه
if not final_filtered_df.empty:
    avg_price = final_filtered_df['السعر الاجمالي'].mean()
    count_properties = len(final_filtered_df)

    st.markdown(f"""
    <div style="text-align: right;">
        <h3> :الإحصائيات 📊</h3>
        <p>متوسط السعر الإجمالي: <strong>{avg_price:,.0f}</strong> ريال</p>
        <p>عدد {property_type} بهذه المواصفات: <strong>{count_properties}</strong></p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="text-align: right; color: red;">
        ❌ لا توجد عقارات بهذه المواصفات في البيانات.
    </div>
    """, unsafe_allow_html=True)
