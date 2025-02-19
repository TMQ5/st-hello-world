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
district_counts_apartments = df_apartments[df_apartments['الحي'] != ' الرياض ']['الحي'].value_counts().reset_index()
district_counts_apartments.columns = ['الحي', 'count']
top_districts_apartments = district_counts_apartments.head(10)

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



# إنشاء figure و 6 محاور (subplot) بدلاً من 4
fig, axes = plt.subplots(4, 2, figsize=(14, 15))

# تحديد الألوان: 
palette_apartments = "mako"  # ألوان خاصة بالشقق
palette_villas = "magma"  # ألوان خاصة بالفلل

# 1️⃣ عدد الشقق في كل حي
axes[0, 0].set_title(get_display(arabic_reshaper.reshape("ما هي الأحياء التي تحتوي على أكبر عدد من الشقق؟")))
sns.barplot(y=[get_display(arabic_reshaper.reshape(label)) for label in top_districts_apartments['الحي']], 
            x=top_districts_apartments['count'], palette=palette_apartments, orient='h', ax=axes[0, 0])
axes[0, 0].set_xlabel(get_display(arabic_reshaper.reshape("عدد الشقق")))
axes[0, 0].set_ylabel(get_display(arabic_reshaper.reshape("الحي")))
axes[0, 0].invert_yaxis()


# 2️⃣ عدد الفلل في كل حي
axes[0, 1].set_title(get_display(arabic_reshaper.reshape("ما هي الأحياء التي تحتوي على أكبر عدد من الفلل؟")))
sns.barplot(y=[get_display(arabic_reshaper.reshape(label)) for label in top_districts_villas['الحي']], 
            x=top_districts_villas['count'], palette=palette_villas, orient='h', ax=axes[0, 1])
axes[0, 1].set_xlabel(get_display(arabic_reshaper.reshape("عدد الفلل")))
axes[0, 1].set_ylabel(get_display(arabic_reshaper.reshape("الحي")))
axes[0, 1].invert_yaxis()

st.markdown("""
<div style="text-align: center; background-color: #f9f9f9; padding: 15px; border-radius: 10px; margin-top: 15px; font-size: 16px;">
    🔹 <strong>تدور شقة في حي مليان خيارات؟</strong> حي <strong>النرجس والملقا</strong> فيهم أكبر عدد من الشقق، يعني فرصتك تلقى اللي يناسبك أكبر!<br>
    🔹 <strong>تدور على حي مليان فلل؟</strong> حي <strong>المونسية والرمال</strong> من الأحياء اللي فيها أكبر عدد من الفلل، مثالية لو كنت تبحث عن مساحة مستقلة.
</div>
""", unsafe_allow_html=True)


# 3️⃣ متوسط السعر الإجمالي للشقق
axes[1, 0].set_title(get_display(arabic_reshaper.reshape("ما هي الأحياء الأقل سعراً في متوسط السعر الإجمالي للشقق؟")))
sns.barplot(y=[get_display(arabic_reshaper.reshape(label)) for label in top_cheapest_districts_apartments['الحي']], 
            x=top_cheapest_districts_apartments['السعر الاجمالي'], palette=palette_apartments, orient='h', ax=axes[1, 0])
axes[1, 0].set_xlabel(get_display(arabic_reshaper.reshape("متوسط السعر الإجمالي")))
axes[1, 0].set_ylabel(get_display(arabic_reshaper.reshape("الحي")))
axes[1, 0].invert_yaxis()
axes[1, 0].xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))


# 4️⃣ متوسط السعر الإجمالي للفلل
axes[1, 1].set_title(get_display(arabic_reshaper.reshape("ما هي الأحياء الأقل سعراً في متوسط السعر الإجمالي للفلل؟")))
sns.barplot(y=[get_display(arabic_reshaper.reshape(label)) for label in top_cheapest_districts_villas['الحي']], 
            x=top_cheapest_districts_villas['السعر الاجمالي'], palette=palette_villas, orient='h', ax=axes[1, 1])
axes[1, 1].set_xlabel(get_display(arabic_reshaper.reshape("متوسط السعر الإجمالي")))
axes[1, 1].set_ylabel(get_display(arabic_reshaper.reshape("الحي")))
axes[1, 1].invert_yaxis()
axes[1, 1].xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

# تدوير النصوص في المحور X
axes[1, 0].tick_params(axis='x', rotation=45)
axes[1, 1].tick_params(axis='x', rotation=45)


# 5️⃣  مقارنة المساحات في الأحياء المختلفة للشقق
title_apartments = get_display(arabic_reshaper.reshape("مقارنة المساحات في الأحياء المختلفة للشقق"))
xlabel_apartments = get_display(arabic_reshaper.reshape("الحي"))
ylabel_apartments = get_display(arabic_reshaper.reshape("متوسط المساحة (م²)"))

# تصفية البيانات للشقق
df_filtered_apartments = df_apartments[(df_apartments['المساحة'] <= 300) & 
                                        (df_apartments['السعر الاجمالي'] > 500) & 
                                        (df_apartments['الحي'] != ' ')]

# حساب المتوسط لكل حي
district_avg_space_apartments = df_filtered_apartments.groupby('الحي')['المساحة'].mean().reset_index()
district_avg_space_apartments = district_avg_space_apartments.sort_values(by='المساحة', ascending=True)
district_avg_space_apartments = district_avg_space_apartments.head(10)

# رسم Bar Plot
axes[3, 1].set_title(title_apartments, fontsize=14)
sns.barplot(x=district_avg_space_apartments['المساحة'], y=[get_display(arabic_reshaper.reshape(label)) for label in district_avg_space_apartments['الحي']], 
            palette=palette_apartments, ax=axes[3, 1])
axes[3, 1].set_xlabel(ylabel_apartments, fontsize=12)
axes[3, 1].set_ylabel(xlabel_apartments, fontsize=12)

# 6️⃣  مقارنة المساحات في الأحياء المختلفة للفلل
title_villas = get_display(arabic_reshaper.reshape("مقارنة المساحات في الأحياء المختلفة للفلل"))
xlabel_villas = get_display(arabic_reshaper.reshape("الحي"))
ylabel_villas = get_display(arabic_reshaper.reshape("متوسط المساحة (م²)"))

# تصفية البيانات للفلل
df_filtered_villas = df_villas[(df_villas['المساحة'] <= 300) & 
                                (df_villas['السعر الاجمالي'] > 500) & 
                                (df_villas['الحي'] != ' ')]

# حساب المتوسط لكل حي
district_avg_space_villas = df_filtered_villas.groupby('الحي')['المساحة'].mean().reset_index()
district_avg_space_villas = district_avg_space_villas.sort_values(by='المساحة', ascending=True)
district_avg_space_villas = district_avg_space_villas.head(10)

# رسم Bar Plot
axes[3, 0].set_title(title_villas, fontsize=14)
sns.barplot(x=district_avg_space_villas['المساحة'], y=[get_display(arabic_reshaper.reshape(label)) for label in district_avg_space_villas['الحي']], 
            palette=palette_villas, ax=axes[3, 0])
axes[3, 0].set_xlabel(ylabel_villas, fontsize=12)
axes[3, 0].set_ylabel(xlabel_villas, fontsize=12)


# حساب عدد الشقق لكل عدد غرف
room_counts_apartments = df_apartments["عدد الغرف"].value_counts().reset_index()
room_counts_apartments.columns = ["عدد الغرف", "count"]
top_rooms_apartments = room_counts_apartments.head(10)

# حساب عدد الفلل لكل عدد غرف
room_counts_villas = df_villas["عدد الغرف"].value_counts().reset_index()
room_counts_villas.columns = ["عدد الغرف", "count"]
top_rooms_villas = room_counts_villas.head(10)

# 7️⃣ توزيع عدد الغرف في الشقق
axes[2, 0].set_title(get_display(arabic_reshaper.reshape("ما هو توزيع عدد الغرف في الشقق؟")))
sns.barplot(x=top_rooms_apartments['عدد الغرف'], y=top_rooms_apartments['count'], palette=palette_apartments, ax=axes[2, 0])
axes[2, 0].set_xlabel(get_display(arabic_reshaper.reshape("عدد الغرف")))
axes[2, 0].set_ylabel(get_display(arabic_reshaper.reshape("عدد الشقق")))

# 8️⃣ توزيع عدد الغرف في الفلل
axes[2, 1].set_title(get_display(arabic_reshaper.reshape("ما هو توزيع عدد الغرف في الفلل؟")))
sns.barplot(x=top_rooms_villas['عدد الغرف'], y=top_rooms_villas['count'], palette=palette_villas, ax=axes[2, 1])
axes[2, 1].set_xlabel(get_display(arabic_reshaper.reshape("عدد الغرف")))
axes[2, 1].set_ylabel(get_display(arabic_reshaper.reshape("عدد الفلل")))

# تحسين توزيع الشكل
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
