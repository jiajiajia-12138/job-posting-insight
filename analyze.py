import pandas as pd

# 1. 读数据
df = pd.read_csv("data/jd_sample.csv", encoding="utf-8-sig")
df["jd_text"] = df["jd_text"].str.strip('"')

# 2. 技能关键词标记
skills = ["SQL", "Python", "统计", "机器学习", "Spark", "ETL", "数据可视化"]
for s in skills:
    df[s] = df["jd_text"].str.contains(s, case=False, na=False)

# 3. 输出：每条 JD 命中情况
print("=== 每条 JD 技能命中 ===")
print(df[["company"] + skills].to_string(index=False))

# 4. 输出：技能频次
print("\n=== 技能出现次数 ===")
print(df[skills].sum().sort_values(ascending=False).to_string())

# 5. 输出：0 命中的 JD（值得人工回看）
no_hit = df[~df[skills].any(axis=1)]
print("\n=== 未命中任何关键词的 JD ===")
print(no_hit[["company", "title"]].to_string(index=False))

import os

# 6. 读取 LLM 语义抽取结果并与关键词法对比
print("\n=== LLM 语义抽取 vs 关键词法 ===")
llm_file = "data/llm_extract_results.csv"
if os.path.exists(llm_file):
    llm_df = pd.read_csv(llm_file, encoding="gbk")
    for _, row in llm_df.iterrows():
        print(f"\n公司: {row['company']}")
        print(f"关键词命中数: {row['keyword_hits']}")
        print(f"LLM抽出的技能: {row['llm_extracted_skills']}")
        print(f"结论: {row['conclusion']}")
else:
    print("未找到 LLM 抽取结果文件。")

# 6. 画图：技能出现频次横向柱状图
import matplotlib.pyplot as plt

# 设置中文字体，防止中文显示成方块（Windows 默认用黑体）
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 获取频次数据并排序
skill_counts = df[skills].sum().sort_values(ascending=True)  # 横向图，升序排

plt.figure(figsize=(10, 6))
# 画横向柱状图
bars = plt.barh(skill_counts.index, skill_counts.values, color='skyblue')

# 在柱子末端标上数字
for bar in bars:
    plt.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
             str(int(bar.get_width())), va='center')

plt.title("央企/国企/银行/券商数据岗技能需求频次 (样本量 N=16)")
plt.xlabel("出现次数")
plt.xlim(0, max(skill_counts.values) + 2)  # 给数字留点空间
plt.tight_layout()

# 保存图片
plt.savefig("skill_distribution.png", dpi=300)
print("\n已生成图表：skill_distribution.png")

# 如果你在本地运行，这行会弹窗展示；如果在服务器可以不写
# plt.show()