import pandas as pd
import os
import json

# 定义列名映射
column_mapping = {
    "监测井编号": "monitoring_well_id",
    "核查时间": "inspection_time",
    "经度": "longitude",
    "纬度": "latitude",
    "井深/m": "well_depth_m",
    "井管直径/mm": "well_diameter_mm",
    "水位/m": "water_level_m",
    "颜色": "color",
    "气味": "odor",
    "明显污染痕迹": "obvious_pollution_traces",
    "井台高度/m": "well_platform_height_m",
    "井管材质": "well_pipe_material",
    "水位计读数/m": "water_level_meter_reading_m",
    "异物": "foreign_objects",
    "pH 值": "pH_value",
    "电导率（us/cm）": "conductivity_us_cm",
    "温度（℃）": "temperature_C",
    "溶解氧（mg/L）": "dissolved_oxygen_mg_L",
    "氧化还原电位（mV）": "oxidation_reduction_potential_mV",
    "浊度（NTU）": "turbidity_NTU"
}

# 文件路径
file_path = 'webapp/src/etl/supervison-data.xlsx'
print("当前工作目录:", os.getcwd())

def transform_data(data_list):
    transformed_data = []
    
    for data in data_list:
        # Transform each item in the list
        new_data = {
            "id": data["monitoring_well_id"],
            "position": [data["longitude"], data["latitude"]]
        }
        
        # Add the rest of the key-value pairs (keeping them unchanged)
        for key, value in data.items():
            if key not in ["monitoring_well_id", "longitude", "latitude"]:
                new_data[key] = value
        
        transformed_data.append(new_data)
    
    return transformed_data

# 检查文件是否存在
if os.path.exists(file_path):
    # 读取 Excel 文件
    df = pd.read_excel(file_path)

    # 替换列名
    df.rename(columns=column_mapping, inplace=True)
    data_list = df.to_dict(orient='records')
    transformed_data = transform_data(data_list)

    output_file='test.json'
        # Write the transformed data to a new JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(transformed_data, f, ensure_ascii=False, indent=2)
#     # 将数据框转换为 JSON 字符串
#     json_data = df.to_json(orient='records', force_ascii=False, indent=4)

#     # 将 JSON 数据写入文件
#     with open('supervison-data.json', 'w', encoding='utf-8') as f:
#         f.write(json_data)

#     # 打印 JSON 数据
#     print(json_data)
# else:
#     print(f"文件 {file_path} 不存在")

