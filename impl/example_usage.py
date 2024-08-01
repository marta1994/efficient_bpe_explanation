from tokenizer import Tokenizer

tokenizer = Tokenizer(10)
strings = ['aaabdaaabac', 'abdbdbdaaabb', 'ccbdaaadabb', 'bbdbdbaacd']
merges = tokenizer.train(strings)
for merge in merges:
    print(merge)
print(tokenizer._tokens_map)
tokens = tokenizer.to_tokens(strings)
print('tokens: ', tokens)
str_from_tokens = tokenizer.from_tokens(tokens)
print('string from tokens: ', str_from_tokens)
print('strings are equal :', strings == str_from_tokens)