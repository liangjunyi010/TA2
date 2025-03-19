import pickle

with open("./Output/Adversarial/toxigen_adv.pkl", "rb") as f:
    data = pickle.load(f)

# 逐条打印，便于阅读
for i, text in enumerate(data, start=1):
    print(f"=== Entry {i} ===")
    # 如果你想把其中 \n 原样换行，可以再做一次替换
    # text = text.replace("\\n", "\n")
    print(text)
    print()
