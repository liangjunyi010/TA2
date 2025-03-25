import pickle

with open("Dataset/ToxiGen/toxigen.pkl", "rb") as f:
    data = pickle.load(f)

for i, text in enumerate(data, start=1):
    print(f"=== Entry {i} ===")
    print(text)
    print()
