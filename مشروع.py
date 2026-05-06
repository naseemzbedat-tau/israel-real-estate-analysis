import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# ============================================
# 1. تحميل الداتا وتنظيفها
# ============================================

df = pd.read_csv('cleaned_yad2_data.csv')
df = df.drop(columns=['link'])  # شيل عمود اللينك مش بنحتاجه

# شيل القيم الغريبة (outliers)
df_clean = df[
    (df['price'] < 20_000_000) &   # أقل من 20 مليون
    (df['area_sqm'] < 500) &        # أقل من 500 متر
    (df['price'] > 100_000)         # أكتر من 100 ألف
]

# ============================================
# 2. تجهيز البيانات للرسم
# ============================================

# أشهر 10 مدن بعدد الإعلانات
top_cities = df_clean['city'].value_counts().head(10).index.tolist()

# فلتر الداتا على الـ 10 مدن بس
df_top = df_clean[df_clean['city'].isin(top_cities)]

# ============================================
# 3. إعداد الشكل — 4 رسومات بنفس الصفحة
# ============================================

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
# subplots(2, 2) = شبكة 2 صف × 2 عمود
# figsize = حجم الصورة الكلية

colors = ['#58a6ff','#3fb950','#f78166','#d2a8ff',
          '#ffa657','#79c0ff','#56d364','#ff7b72','#e3b341','#a5d6ff']

# ============================================
# رسم 1 — عدد الإعلانات لكل مدينة (axes[0,0])
# ============================================

city_counts = df_clean['city'].value_counts().head(10)

axes[0,0].barh(                          # barh = bar chart أفقي
    range(len(city_counts)),             # مواضع الأعمدة على محور Y
    city_counts.values,                  # القيم (عدد الإعلانات)
    color=colors
)
axes[0,0].set_yticks(range(len(city_counts)))
axes[0,0].set_yticklabels(city_counts.index)  # أسماء المدن
axes[0,0].set_title('Top 10 Cities by Listings')
axes[0,0].set_xlabel('Number of Listings')

# ============================================
# رسم 2 — متوسط السعر لكل مدينة (axes[0,1])
# ============================================

city_price = df_top.groupby('city')['price'].mean()  
# groupby = جمّع حسب المدينة
# .mean() = خد المتوسط

city_price = city_price.reindex(top_cities).sort_values(ascending=True)

axes[0,1].barh(
    range(len(city_price)),
    city_price.values / 1_000_000,   # قسّم على مليون عشان الأرقام تصغر
    color=colors
)
axes[0,1].set_yticks(range(len(city_price)))
axes[0,1].set_yticklabels(city_price.index)
axes[0,1].set_title('Average Price by City')
axes[0,1].set_xlabel('Average Price (Millions ₪)')

# ============================================
# رسم 3 — توزيع الأسعار Histogram (axes[1,0])
# ============================================

axes[1,0].hist(
    df_clean['price'] / 1_000_000,   # الأسعار بالملايين
    bins=50,                          # عدد الأعمدة بالـ histogram
    color='#58a6ff',
    edgecolor='white',
    alpha=1                        # شفافية
)
axes[1,0].set_title('Price Distribution')
axes[1,0].set_xlabel('Price (Millions ₪)')
axes[1,0].set_ylabel('Count')

# خط عمودي عند الـ median
axes[1,0].axvline(
    df_clean['price'].median() / 1_000_000,
    color='red',
    linestyle='--',
    linewidth=2,
    label=f'Median: {df_clean["price"].median()/1_000_000:.1f}M'
)
axes[1,0].legend()

# ============================================
# رسم 4 — علاقة المساحة بالسعر Scatter (axes[1,1])
# ============================================

sc = axes[1,1].scatter(
    df_clean['area_sqm'],            # محور X = المساحة
    df_clean['price'] / 1_000_000,  # محور Y = السعر
    alpha=0.3,                       # شفافية النقاط
    s=15,                            # حجم النقاط
    c=df_clean['rooms'],             # لون كل نقطة حسب عدد الغرف
    cmap='cool'                      # لوحة الألوان
)
axes[1,1].set_title('Area vs Price')
axes[1,1].set_xlabel('Area (sqm)')
axes[1,1].set_ylabel('Price (Millions ₪)')

# شريط الألوان على اليمين
plt.colorbar(sc, ax=axes[1,1], label='Rooms')

# ============================================
# 4. حفظ الصورة
# ============================================

plt.suptitle('Israel Real Estate Analysis', fontsize=16)
plt.tight_layout()   # ينظم المسافات بين الرسومات تلقائياً
plt.savefig('analysis.png', dpi=150, bbox_inches='tight')
plt.show()




#print(df['city'].unique())
