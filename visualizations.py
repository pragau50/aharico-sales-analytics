import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib.gridspec import GridSpec

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.facecolor'] = 'white'

def create_all_charts(df):
    """Create all 8 visualization charts from Aharico data"""

    # 1. REVENUE BY CITY (Bar Chart)
    print("Creating Chart 1: Revenue by City...")
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    city_rev = df.groupby('city')['revenue'].sum().sort_values(ascending=False)
    colors1 = sns.color_palette("husl", len(city_rev))
    ax1.bar(city_rev.index, city_rev.values, color=colors1, edgecolor='black', linewidth=0.7)
    ax1.set_title('Revenue by City - Aharico', fontsize=14, fontweight='bold')
    ax1.set_xlabel('City', fontsize=11)
    ax1.set_ylabel('Revenue (₹)', fontsize=11)
    plt.xticks(rotation=45, ha='right')
    ax1.grid(axis='y', alpha=0.3)
    for i, v in enumerate(city_rev.values):
        ax1.text(i, v + 500, f'₹{v:,.0f}', ha='center', va='bottom', fontsize=9)
    plt.tight_layout()
    plt.show()

    # 2. MONTHLY REVENUE TREND (Line Chart)
    print("Creating Chart 2: Monthly Revenue Trend...")
    fig2, ax2 = plt.subplots(figsize=(12, 5))
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['month'] = df['order_date'].dt.to_period('M')
    monthly_rev = df.groupby('month')['revenue'].sum()
    monthly_rev.index = monthly_rev.index.to_timestamp()
    ax2.plot(monthly_rev.index, monthly_rev.values, marker='o', linewidth=2.5,
             markersize=8, color='#2E86AB', markerfacecolor='#A23B72')
    ax2.fill_between(monthly_rev.index, monthly_rev.values, alpha=0.2, color='#2E86AB')
    ax2.set_title('Monthly Revenue Trend', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Month', fontsize=11)
    ax2.set_ylabel('Revenue (₹)', fontsize=11)
    ax2.grid(True, alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    for x, y in zip(monthly_rev.index, monthly_rev.values):
        ax2.text(x, y + 1000, f'₹{y:,.0f}', ha='center', va='bottom', fontsize=9)
    plt.tight_layout()
    plt.show()

    # 3. REVENUE BY SEGMENT (Pie Chart)
    print("Creating Chart 3: Revenue by Segment...")
    fig3, ax3 = plt.subplots(figsize=(10, 8))
    segment_rev = df.groupby('segment')['revenue'].sum().sort_values(ascending=False)
    colors3 = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    wedges, texts, autotexts = ax3.pie(segment_rev.values, labels=segment_rev.index,
                                         autopct='%1.1f%%', colors=colors3, startangle=90,
                                         textprops={'fontsize': 11, 'weight': 'bold'})
    ax3.set_title('Revenue by Segment', fontsize=14, fontweight='bold', pad=20)
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(10)
    plt.tight_layout()
    plt.show()

    # 4. TOP 5 PRODUCTS BY REVENUE (Horizontal Bar Chart)
    print("Creating Chart 4: Top 5 Products by Revenue...")
    fig4, ax4 = plt.subplots(figsize=(10, 6))
    product_rev = df.groupby('product')['revenue'].sum().sort_values(ascending=True).tail(5)
    colors4 = sns.color_palette("viridis", len(product_rev))
    ax4.barh(product_rev.index, product_rev.values, color=colors4, edgecolor='black', linewidth=0.7)
    ax4.set_title('Top 5 Products by Revenue', fontsize=14, fontweight='bold')
    ax4.set_xlabel('Revenue (₹)', fontsize=11)
    ax4.set_ylabel('Product', fontsize=11)
    ax4.grid(axis='x', alpha=0.3)
    for i, v in enumerate(product_rev.values):
        ax4.text(v + 500, i, f'₹{v:,.0f}', va='center', fontsize=9)
    plt.tight_layout()
    plt.show()

    # 5. PAYMENT MODE DISTRIBUTION (Bar Chart)
    print("Creating Chart 5: Payment Mode Distribution...")
    fig5, ax5 = plt.subplots(figsize=(10, 5))
    payment_count = df['payment_mode'].value_counts()
    colors5 = sns.color_palette("Set2", len(payment_count))
    ax5.bar(payment_count.index, payment_count.values, color=colors5, edgecolor='black', linewidth=0.7)
    ax5.set_title('Payment Mode Distribution', fontsize=14, fontweight='bold')
    ax5.set_xlabel('Payment Mode', fontsize=11)
    ax5.set_ylabel('Number of Orders', fontsize=11)
    plt.xticks(rotation=45, ha='right')
    ax5.grid(axis='y', alpha=0.3)
    for i, v in enumerate(payment_count.values):
        ax5.text(i, v + 5, f'{v}', ha='center', va='bottom', fontsize=9)
    plt.tight_layout()
    plt.show()

    # 6. ORDER STATUS DISTRIBUTION (Pie Chart)
    print("Creating Chart 6: Order Status Distribution...")
    fig6, ax6 = plt.subplots(figsize=(10, 8))
    status_count = df['order_status'].value_counts()
    status_colors = {'delivered': '#2ECC71', 'pending': '#F39C12', 'cancelled': '#E74C3C'}
    colors6 = [status_colors.get(status, '#95A5A6') for status in status_count.index]
    wedges, texts, autotexts = ax6.pie(status_count.values, labels=status_count.index,
                                        autopct='%1.1f%%', colors=colors6, startangle=90,
                                        textprops={'fontsize': 11, 'weight': 'bold'})
    ax6.set_title('Order Status Distribution', fontsize=14, fontweight='bold', pad=20)
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(10)
    plt.tight_layout()
    plt.show()

    # 7. AGE GROUP VS REVENUE (Bar Chart)
    print("Creating Chart 7: Age Group vs Revenue...")
    fig7, ax7 = plt.subplots(figsize=(10, 5))
    # Create age bins
    df['age_group'] = pd.cut(df['age'], bins=[0, 25, 35, 50, 100],
                              labels=['18-25', '26-35', '36-50', '50+'])
    age_rev = df.groupby('age_group')['revenue'].sum().sort_values(ascending=False)
    colors7 = sns.color_palette("coolwarm", len(age_rev))
    ax7.bar(age_rev.index, age_rev.values, color=colors7, edgecolor='black', linewidth=0.7)
    ax7.set_title('Revenue by Age Group', fontsize=14, fontweight='bold')
    ax7.set_xlabel('Age Group', fontsize=11)
    ax7.set_ylabel('Revenue (₹)', fontsize=11)
    ax7.grid(axis='y', alpha=0.3)
    for i, v in enumerate(age_rev.values):
        ax7.text(i, v + 500, f'₹{v:,.0f}', ha='center', va='bottom', fontsize=9)
    plt.tight_layout()
    plt.show()

    # 8. CITY WISE ORDER COUNT (Bar Chart)
    print("Creating Chart 8: City wise Order Count...")
    fig8, ax8 = plt.subplots(figsize=(10, 5))
    city_count = df['city'].value_counts().sort_values(ascending=False)
    colors8 = sns.color_palette("muted", len(city_count))
    ax8.bar(city_count.index, city_count.values, color=colors8, edgecolor='black', linewidth=0.7)
    ax8.set_title('Order Count by City', fontsize=14, fontweight='bold')
    ax8.set_xlabel('City', fontsize=11)
    ax8.set_ylabel('Number of Orders', fontsize=11)
    plt.xticks(rotation=45, ha='right')
    ax8.grid(axis='y', alpha=0.3)
    for i, v in enumerate(city_count.values):
        ax8.text(i, v + 5, f'{v}', ha='center', va='bottom', fontsize=9)
    plt.tight_layout()
    plt.show()

    print("\n✅ All 8 charts created successfully!")


if __name__ == "__main__":
    # Load data
    from sqlalchemy import create_engine
    engine = create_engine('mysql+mysqlconnector://root:root123@localhost/messy_practice')
    df = pd.read_sql('SELECT * FROM aharico_clean', engine)

    # Create all charts
    create_all_charts(df)
