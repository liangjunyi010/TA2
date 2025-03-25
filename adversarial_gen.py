import os
import pickle
from tqdm import tqdm
import torch
import transformers
from transformers import AutoTokenizer
from args import *

if not os.path.exists(f"./Output/Adversarial"):
    os.makedirs(f"./Output/Adversarial")


def adv_gen(data, model):
    tokenizer = AutoTokenizer.from_pretrained(model)

    pipeline = transformers.pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        torch_dtype=torch.float16,
        trust_remote_code=True,
        device_map="auto",
        return_full_text=False,
    )

    out = []
    for p in tqdm(data, total=len(data)):
        sequences = pipeline(
            p,
            max_length=args.max_token,
            do_sample=True,
            top_k=1,
            num_return_sequences=1,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.eos_token_id,
            repetition_penalty=1.5,
        )

        res = sequences[0]["generated_text"]
        if args.verbose:
            print(f"\033[92mResponse: {res}\033[0m")
        out.append(res)

    with open(f"./Output/Adversarial/{args.dataset}_adv.pkl", "wb") as f:
        pickle.dump(out, f)


if __name__ == "__main__":
    print(f"\033[92mProcessing {args.dataset}... ...\033[0m")

    if args.dataset == "tqa":
        with open("./Dataset/TruthfulQA/tqa_prompt.pkl", "rb") as f:
            tqa_prompt = pickle.load(f)

        adv_gen(tqa_prompt, "tiiuae/falcon-7b")

    if args.dataset == "toxigen":
        with open("./Dataset/ToxiGen/toxigen_prompt.pkl", "rb") as f:
            toxigen_prompt = pickle.load(f)

        toxigen_prompt = toxigen_prompt[:10]
        adv_gen(toxigen_prompt, "meta-llama/Llama-2-13b-hf")

    if args.dataset == "bold":
        with open("./Dataset/BOLD/new_bold_prompt.pkl", "rb") as f:
            bold_prompt = pickle.load(f)

        adv_gen(bold_prompt, "tiiuae/falcon-7b")

    print(f"\033[92mFinished processing {args.dataset}!\033[0m")
