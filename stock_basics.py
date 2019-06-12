import tushare as ts
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

# 调取股票基本面数据和行情数据
# 基本面数据
basics_data = ts.get_stock_basics()
print(basics_data.iloc[:3, :8])

# 上市公司分布
# 使用groupby对上市公司归属地进行汇总，
# 统计每个省份（直辖市）上市公司的总数
area = basics_data.groupby('area')['name']
print(area)
