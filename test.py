import pickle

with open("Output/Adversarial/toxigen_adv_1.pkl", "rb") as f:
    data = pickle.load(f)

for i, text in enumerate(data, start=1):
    print(f"=== Entry {i} ===")
    print(text)
    print()
