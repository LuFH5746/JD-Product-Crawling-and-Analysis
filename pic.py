import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
import os

# 设置中文字体以解决乱码问题
matplotlib.rcParams['font.sans-serif'] = ['SimSun']  # 使用黑体
matplotlib.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题

# 设置参数
num_lowest_shops = 5  # 可以根据需要调整这个值

# 读取CSV文件
csv_file_path = os.path.join(os.getcwd(), 'products.csv')
df = pd.read_csv(csv_file_path, encoding='utf-8-sig')

# 处理评价数列中的“万+”
def process_evaluation_number(eval_str):
    if isinstance(eval_str, str) and eval_str.endswith('万+'):
        return int(float(eval_str[:-2]) * 10000)
    elif isinstance(eval_str, str) and eval_str.isdigit():
        return int(eval_str)
    else:
        return 0  # 如果无法解析，默认返回0

df['评价数'] = df['评价数'].apply(process_evaluation_number)

# 确保价格列为字符串类型
df['价格'] = df['价格'].astype(str)

# 清理价格列中的逗号和其他非数字字符
df['价格'] = df['价格'].str.replace(',', '').str.replace('元', '').str.strip()

# 转换为浮点数类型
df['价格'] = df['价格'].astype(float)

# 生成价格分布图
plt.figure(figsize=(12, 6))
sns.histplot(df['价格'], bins=30, kde=True)
plt.title('价格分布图')
plt.xlabel('价格')
plt.ylabel('频数')

# 在X轴上增加刻度（精确到50元）
x_min = int(min(df['价格']))
x_max = int(max(df['价格'])) + 50
x_ticks = range(x_min, x_max, 50)
plt.xticks(x_ticks)
plt.savefig('price_distribution.png')
plt.close()  # 关闭图形以避免显示

# 计算每个店家的产品数量和平均价格
shop_stats = df.groupby('店名').agg({
    '品名': 'count',
    '价格': 'mean'
}).reset_index()
shop_stats.columns = ['店名', '产品数量', '平均价格']

# 生成气泡图
plt.figure(figsize=(30, 20))  # 增加图形大小以减少店名重叠
scatter = plt.scatter(
    shop_stats['产品数量'],
    shop_stats['店名'],
    s=shop_stats['产品数量'] * 50,  # 大小与产品数量成正比
    c=shop_stats['平均价格'],       # 颜色与平均价格成正比
    cmap='coolwarm',                # 颜色映射
    alpha=0.6                       # 透明度
)

plt.colorbar(scatter, label='平均价格')
plt.title('店家产品数量及平均价格气泡图')
plt.xlabel('产品数量')
plt.ylabel('店名')
plt.yticks(rotation=0)  # 保持店名垂直排列
plt.tight_layout()
plt.savefig('bubble_chart.png')
plt.close()  # 关闭图形以避免显示

print("图表已生成并保存为 price_distribution.png 和 bubble_chart.png")
