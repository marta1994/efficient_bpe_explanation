from tokenizer import Tokenizer

tokenizer = Tokenizer(8)
merges = tokenizer.train(['aaabdaaabac'])
for merge in merges:
    print(merge)
print(tokenizer._tokens_map)