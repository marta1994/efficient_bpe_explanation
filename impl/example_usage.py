from tokenizer import Tokenizer

tokenizer = Tokenizer(10)
strings = ['aaabdaaabac', 'abdbdbdaaabb', 'ccbdaaadabb', 'bbdbdbaacd']
token_map = tokenizer.train(strings)
print(token_map)
tokens = tokenizer.to_tokens(strings)
print('tokens: ', tokens)
str_from_tokens = tokenizer.from_tokens(tokens)
print('string from tokens: ', str_from_tokens)
print('strings are equal :', strings == str_from_tokens)