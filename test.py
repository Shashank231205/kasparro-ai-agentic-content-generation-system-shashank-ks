from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

print("Downloading tokenizer...")
AutoTokenizer.from_pretrained("facebook/bart-base")

print("Downloading model...")
AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-base")

print("DONE")
