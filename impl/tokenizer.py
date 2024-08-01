from to_tokens_converter import ToTokensConverter
from tokenizer_trainer import TokenizerTrainer

class Tokenizer:
    def __init__(self, dict_size):
        self._dict_size = dict_size
        self._chars_map = {}
        self._tokens_map = {}
        
    def to_tokens(self, strings):
        toTokensConverter = ToTokensConverter(self._tokens_map)
        return toTokensConverter.to_tokens(strings)
    
    def from_tokens(self, tokens):
        return [''.join(self._tokens_map[token] for token in token_str) for token_str in tokens]
        
    def train(self, strings):
        self._map_chars(strings)
        input_as_tokens = self._to_basic_token_ids(strings)
        trainer = TokenizerTrainer(
            input_as_tokens,
            self._dict_size - len(self._chars_map),
            self._tokens_map)
        trainer.train(len(self._chars_map))
        return self._tokens_map
        
    def _map_chars(self, strings):
        self._chars_map = {}
        self._tokens_map = {}
        ind = 0
        for text in strings:
            for char in text:
                if char not in self._chars_map:
                    self._chars_map[char] = ind
                    self._tokens_map[ind] = char
                    ind += 1
        self._chars_map['unknown'] = ind
        self._tokens_map[ind] = '□'
        
    def _to_basic_token_ids(self, strings):
        return [[self._chars_map[char] if char in self._chars_map else self._chars_map['unknown'] for char in string] for string in strings]