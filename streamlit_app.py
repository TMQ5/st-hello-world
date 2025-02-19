import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mticker

# تحميل البيانات بعد التنظيف
apartments_file = "apartments_data_cleaned.csv"
df_apartments = pd.read_csv(apartments_file)

# حساب متوسط السعر الإجمالي لكل حي واستبعاد القيم غير المنطقية
district_avg_price = df_apartments[df_apartments['السعر الاجمالي'] > 500].groupby('الحي')['السعر الاجمالي'].mean().reset_index()

# ترتيب الأحياء من الأقل إلى الأعلى في السعر الإجمالي
district_avg_price = district_avg_price.sort_values(by='السعر الاجمالي', ascending=True)

# أخذ أرخص 10 أحياء
top_cheapest_districts = district_avg_price.head(10)

# رسم المخطط مع التعديلات
fig, ax = plt.subplots(figsize=(12,6))
sns.barplot(y=top_cheapest_districts['الحي'], x=top_cheapest_districts['السعر الاجمالي'], palette="Blues", ax=ax)

# تعديل تنسيق الأرقام في المحور X لعرض الأرقام كاملة بدلاً من الصيغة العلمية
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: format(int(x), ',')))

# تعيين تسميات المحاور والعنوان
plt.xlabel("متوسط السعر الإجمالي", fontsize=15)
plt.ylabel("الحي", fontsize=15)
plt.title("ما هي الأحياء الأقل سعرًا في متوسط السعر الإجمالي", fontsize=20)

# عرض الرسم في Streamlit
st.pyplot(fig)
