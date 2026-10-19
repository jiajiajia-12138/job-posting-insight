import pandas as pd
df = pd.read_csv("data/jd_sample.csv")
print("shape:", df.shape)
print("columns:", df.columns.tolist())
print(df.head())
print("\n缺失值：")
print(df.isna().sum())
df["jd_text"] = df["jd_text"].str.strip('"')
# 2) 技能关键词标记
skills = ["SQL", "Python", "统计", "机器学习", "Spark", "ETL", "数据可视化"]
for s in skills:
    df[s] = df["jd_text"].str.contains(s, case=False, na=False)

# 3) 看每条 JD 命中了哪些技能
print(df[["company"] + skills])

# 4) 每个技能出现次数
print("\n技能出现次数：")
print(df[skills].sum().sort_values(ascending=False))