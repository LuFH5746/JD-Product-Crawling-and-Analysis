"""

该文件用于分析爬取的京东html文件, 生成csv文件

"""
import os
from bs4 import BeautifulSoup
import pandas as pd

# 定义一个函数来提取商品信息
def extract_product_info(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 查找所有商品条目
    products = soup.select('#J_goodsList > ul > li')
    
    # 提取每个商品的信息
    product_data = []
    for product in products:
        try:
            name = product.select_one('.p-name em').get_text(strip=True)
            price = product.select_one('.p-price i').get_text(strip=True)
            review_count = product.select_one('.p-commit strong').get_text(strip=True)
            shop_name = product.select_one('.p-shop a').get_text(strip=True) if product.select_one('.p-shop a') else ''
            
            product_data.append({
                '品名': name,
                '价格': price,
                '评价数': review_count,
                '店名': shop_name
            })
        except Exception as e:
            print(f"Error extracting data: {e}")
            continue
    
    return product_data

# 获取 ./htmls/ 目录
output_dir = "./htmls/"

# 确保目录存在
if not os.path.exists(output_dir):
    print(f"目录 {output_dir} 不存在")
else:
    # 找出所有的HTML文件
    html_files = [f for f in os.listdir(output_dir) if f.endswith('.html')]
    
    # 用于存储所有产品的信息
    all_products = []

    # 遍历HTML文件并提取信息
    for file in html_files:
        file_path = os.path.join(output_dir, file)
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
            all_products.extend(extract_product_info(html_content))

    # 将所有产品信息转换为DataFrame
    df = pd.DataFrame(all_products)

    # 将DataFrame保存为CSV文件
    csv_file_path = os.path.join(os.getcwd(), 'products.csv')
    df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')

    print(f"已成功创建CSV文件：{csv_file_path}")