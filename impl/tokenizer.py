from linked_array import LinkedArray
from max_priority_map import MaxPriorityMap

class Merge:
    def __init__(self, first, second, target):
        self.first = first
        self.second = second
        self.target = target
        
    def __str__(self):
        return f'first: {self.first}, second: {self.second}, target: {self.target}'
        
class StatsEntry:
    def __init__(self, pair, positions):
        self.pair = pair
        self.positions = positions
        
class TokenizerTrainer:
    def __init__(self, input_as_basic_tokens, merges_count, tokens_map):
        self._input_as_basic_tokens = input_as_basic_tokens
        self._merges_count = merges_count
        self._tokens_map = tokens_map
        
    def train(self, next_token):
        self._positions = [LinkedArray(basic_tokens) for basic_tokens in self._input_as_basic_tokens]
        self._calc_initial_stats()
        merges = []
        while len(merges) < self._merges_count:
            merge_stat = self._stats.pop()
            for position in list(merge_stat.positions):
                # The original collection may be modified in the loop
                if position not in merge_stat.positions:
                    continue
                inp_index = position[0]
                token_index = position[1]
                positions = self._positions[inp_index]
                prev_token_index = positions.get_previous_index(token_index)
                second_token_index = positions.get_next_index(token_index)
                next_token_index = positions.get_second_next_index(token_index)
                positions.replace_pair(token_index, next_token)
                merge_stat.positions.remove((inp_index, token_index))
                
                if prev_token_index != None:
                    pair = (positions.get_by_index(prev_token_index), merge_stat.pair[0])
                    if pair == merge_stat.pair:
                        merge_stat.positions.remove((inp_index, prev_token_index))
                    else:
                        stat = self._stats.delete_by_map_key(pair)
                        stat.positions.remove((inp_index, prev_token_index))
                        self._stats.push(stat)
                    new_pair = (pair[0], next_token)
                    stat = self._stats.delete_by_map_key(new_pair) if self._stats.contains(new_pair) else StatsEntry(new_pair, set())
                    stat.positions.add((inp_index, prev_token_index))
                    self._stats.push(stat)
                        
                if next_token_index != None:
                    pair = (merge_stat.pair[1], positions.get_by_index(next_token_index))
                    if pair == merge_stat.pair:
                        merge_stat.positions.remove((inp_index, second_token_index))
                    else:
                        stat = self._stats.delete_by_map_key(pair)
                        stat.positions.remove((inp_index, second_token_index))
                        self._stats.push(stat)
                    new_pair = (next_token, pair[1])
                    stat = self._stats.delete_by_map_key(new_pair) if self._stats.contains(new_pair) else StatsEntry(new_pair, set())
                    stat.positions.add((inp_index, token_index))
                    self._stats.push(stat)
                    
            merges.append(Merge(merge_stat.pair[0], merge_stat.pair[1], next_token))
            self._tokens_map[next_token] = self._tokens_map[merge_stat.pair[0]] + self._tokens_map[merge_stat.pair[1]]
            next_token += 1

        return merges
         
    def _calc_initial_stats(self):
        self._stats = MaxPriorityMap(lambda item: len(item.positions), lambda item: item.pair)
        stats = {}
        for k in range(len(self._input_as_basic_tokens)):
            basic_tokens = self._input_as_basic_tokens[k]
            for i in range(len(basic_tokens)-1):
                pair = (basic_tokens[i], basic_tokens[i+1])
                if pair not in stats:
                    stats[pair] = StatsEntry(pair, set())
                stats[pair].positions.add((k,i))
        for key in stats:
            self._stats.push(stats[key])

class Tokenizer:
    def __init__(self, dict_size):
        self._dict_size = dict_size
        self._merges = []
        self._chars_map = {}
        self._tokens_map = {}
        
    def train(self, strings):
        self._map_chars(strings)
        input_as_tokens = self._to_basic_token_ids(strings)
        trainer = TokenizerTrainer(input_as_tokens, self._dict_size - len(self._chars_map), self._tokens_map)
        self._merges = trainer.train(len(self._chars_map))
        return self._merges
        
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