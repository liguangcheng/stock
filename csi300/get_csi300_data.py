import akshare as ak
import numpy as np
from datetime import datetime

# 获取沪深300成分股列表
df_index = ak.index_stock_cons_csindex(symbol="000300")  # 沪深300指数代码

# 检查列名
print("列名列表：", df_index.columns.tolist())

# 根据实际列名调整代码
if '成分券代码' in df_index.columns:
    stock_codes = df_index['成分券代码'].tolist()  # 使用 '成分券代码' 列
    stock_names = df_index['成分券名称'].tolist()  # 使用 '成分券名称' 列
else:
    raise ValueError("列名不匹配，请检查数据格式！")

# 获取所有 A 股的实时行情数据
df_spot = ak.stock_zh_a_spot_em()

# 存储股票代码、名称和当前价格
stock_data_list = []

# 筛选出沪深300成分股的实时行情
for code, name in zip(stock_codes, stock_names):
    stock_data = df_spot[df_spot['代码'] == code]  # 根据代码筛选
    if not stock_data.empty:
        current_price = stock_data['最新价'].values[0]  # 最新价格
        stock_data_list.append({
            '股票代码': code,
            '股票名称': name,
            '当前价格': current_price if not np.isnan(current_price) else np.nan  # 保留 NaN
        })

# 按照当前价格从高到低排序，NaN 值放到末尾
sorted_stock_data = sorted(stock_data_list, key=lambda x: x['当前价格'] if not np.isnan(x['当前价格']) else -np.inf, reverse=True)

# 输出排序后的结果（带序号）
print("沪深300成分股当前价格从高到低排序：")
for index, item in enumerate(sorted_stock_data, start=1):  # 添加序号
    price = item['当前价格']
    price_str = "NaN" if np.isnan(price) else f"{price:.2f}"  # 格式化价格
    print(f"序号: {index}, 股票代码: {item['股票代码']}, 股票名称: {item['股票名称']}, 当前价格: {price_str}")

print(datetime.now())