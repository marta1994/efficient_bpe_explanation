class Merge:
    def __init__(self, first, second, target):
        self.first = first
        self.second = second
        self.target = target

class NaiveTokenizer:
    def __init__(self, min_token_occurance):
        self.min_token_occurance = min_token_occurance
        self._merges = []
        self._chars_map = {}
        self._tokens_map = {}
    
    def train(self, strings):
        # Map characters in the dataset to integers: initial tokens
        self._map_chars(strings)
        self._create_merges(self._to_basic_token_ids(strings))
        return self._tokens_map
        
    def to_tokens(self, strings):
        return [self._to_tokens(string) for string in strings]
    
    def _to_tokens(self, string):
        tokens = self._to_basic_token_ids([string])[0]
        for merge in self._merges:
            tokens = self._replace_token(tokens, (merge.first, merge.second), merge.target)
        return tokens
    
    def from_tokens(self, tokens_list):
        return [''.join([self._tokens_map[token] for token in tokens]) for tokens in tokens_list]
    
    def _to_basic_token_ids(self, strings):
        return [[self._chars_map[char] if char in self._chars_map else self._chars_map['unknown'] for char in string] for string in strings]
    
    def _create_merges(self, tokenized_strings):
        self._merges = []
        next_token = len(self._chars_map)
        while True:
            stats = self._count_pairs_stats(tokenized_strings)
            pair = max(stats, key=stats.get)
            if stats[pair] < self.min_token_occurance:
                break
            self._merges.append(Merge(pair[0], pair[1], next_token))
            tokenized_strings = [self._replace_token(s, pair, next_token) for s in tokenized_strings]
            self._tokens_map[next_token] = self._tokens_map[pair[0]] + self._tokens_map[pair[1]]
            next_token += 1
            
    
    def _count_pairs_stats(self, tokenized_strings):
        stats = {}
        for tokenized_str in tokenized_strings:
            for pair in zip(tokenized_str, tokenized_str[1:]):
                if pair not in stats:
                    stats[pair] = 1
                else:
                    stats[pair] += 1
        return stats

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
    
    def _replace_token(self, token_str, pair, token):
        res = []
        i = 0
        while i < len(token_str):
            if i < len(token_str)-1 and (token_str[i], token_str[i + 1]) == pair:
                res.append(token)
                i += 2
            else:
                res.append(token_str[i])
                i += 1
        return res