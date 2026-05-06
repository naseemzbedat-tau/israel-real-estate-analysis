import pandas as pd
import matplotlib.pyplot as plt


# ============================================
# Load and clean data
# ============================================

df = pd.read_csv('cleaned_yad2_data.csv')
df = df.drop(columns=['link'])  # Remove link column

# Remove outliers
df_clean = df[
    (df['price'] < 20_000_000) &   # Less than 20 million
    (df['area_sqm'] < 500) &        # Less than 500 square meters
    (df['price'] > 100_000)         # More than 100 thousand
]

# ============================================
# 2. Prepare data for visualization
# ============================================

# Top 10 cities by number of listings
top_cities = df_clean['city'].value_counts().head(10).index.tolist()

# Filter data to only include the top 10 cities
df_top = df_clean[df_clean['city'].isin(top_cities)]

# ============================================
# 3. Prepare the figure — 4 plots in the same page
# ============================================

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
# subplots(2, 2)
# figsize

colors = ['#58a6ff','#3fb950','#f78166','#d2a8ff',
          '#ffa657','#79c0ff','#56d364','#ff7b72','#e3b341','#a5d6ff']

# ============================================
# Chart 1 - Number of listings per city (axes[0,0])
# ============================================

city_counts = df_clean['city'].value_counts().head(10)

axes[0,0].barh(                          # barh = horizontal bar chart
    range(len(city_counts)),             # positions of the bars on the Y-axis
    city_counts.values,                
    color=colors
)
axes[0,0].set_yticks(range(len(city_counts)))
axes[0,0].set_yticklabels(city_counts.index)  # names of cities on Y-axis
axes[0,0].set_title('Top 10 Cities by Listings')
axes[0,0].set_xlabel('Number of Listings')

# ============================================
# Chart 2 — Average price per city (axes[0,1])
# ============================================

city_price = df_top.groupby('city')['price'].mean()  
# groupby = group the data by city
# .mean() = caculate the average price for each city

city_price = city_price.reindex(top_cities).sort_values(ascending=True)

axes[0,1].barh(
    range(len(city_price)),
    city_price.values / 1_000_000,   # Divide by million to make the numbers smaller
    color=colors
)
axes[0,1].set_yticks(range(len(city_price)))
axes[0,1].set_yticklabels(city_price.index)
axes[0,1].set_title('Average Price by City')
axes[0,1].set_xlabel('Average Price (Millions ₪)')

# ============================================
# Chart 3 — Price Distribution Histogram (axes[1,0])
# ============================================

axes[1,0].hist(
    df_clean['price'] / 1_000_000,   
    bins=50,                         #number of bins
    color='#58a6ff',
    edgecolor='white',
    alpha=1                        #alpha = transparency
)
axes[1,0].set_title('Price Distribution')
axes[1,0].set_xlabel('Price (Millions ₪)')
axes[1,0].set_ylabel('Count')

# Add a vertical line for the median price
axes[1,0].axvline(
    df_clean['price'].median() / 1_000_000,
    color='red',
    linestyle='--',
    linewidth=2,
    label=f'Median: {df_clean["price"].median()/1_000_000:.1f}M'
)
axes[1,0].legend()

# ============================================
# Chart 4 — Relationship between area and price Scatter (axes[1,1])
# ============================================

sc = axes[1,1].scatter(
    df_clean['area_sqm'],            # X-axis = area
    df_clean['price'] / 1_000_000,  # Y-axis = price
    alpha=0.3,                       # transparency of points
    s=15,                            # size of points
    c=df_clean['rooms'],             # color each point by number of rooms
    cmap='cool'                      # color palette
)
axes[1,1].set_title('Area vs Price')
axes[1,1].set_xlabel('Area (sqm)')
axes[1,1].set_ylabel('Price (Millions ₪)')

plt.colorbar(sc, ax=axes[1,1], label='Rooms')

# ============================================
# 4. Save the image
# ============================================

plt.suptitle('Israel Real Estate Analysis', fontsize=16)
plt.tight_layout()   # Adjust layout to prevent overlap
plt.savefig('analysis.png', dpi=150, bbox_inches='tight')
plt.show()




#print(df['city'].unique())
