import pandas as pd
import json

# 读取CSV文件
df = pd.read_csv('webapp/src/etl/positions.csv')

# 将x和y列的值转换为嵌套列表形式
data = df[['x', 'y']].values.tolist()

output_file='positions.json'
    # Write the transformed data to a new JSON file
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)

# 如果你想将其保存为json文件，可以取消下面的注释并指定文件路径
# with open('output.json', 'w') as f:
#     json.dump(data, f, indent=4)
