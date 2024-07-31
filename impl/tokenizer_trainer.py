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
    def __init__(self, input_as_basic_tokens, target_merge_count, tokens_map, merges):
        self._input_as_basic_tokens = input_as_basic_tokens
        self._target_merge_count = target_merge_count
        self._tokens_map = tokens_map
        self._merges = merges
        
    def train(self, next_token):
        self._positions = [LinkedArray(basic_tokens) for basic_tokens in self._input_as_basic_tokens]
        self._calc_initial_stats()
        while len(self._merges) < self._target_merge_count:
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
                    
            self._merges.append(Merge(merge_stat.pair[0], merge_stat.pair[1], next_token))
            self._tokens_map[next_token] = self._tokens_map[merge_stat.pair[0]] + self._tokens_map[merge_stat.pair[1]]
            next_token += 1
         
    def _calc_initial_stats(self):
        self._stats = MaxPriorityMap(
            heap_key = lambda item: len(item.positions),
            map_key = lambda item: item.pair)
        stats = {}
        for string_ind in range(len(self._input_as_basic_tokens)):
            basic_tokens = self._input_as_basic_tokens[string_ind]
            for char_ind in range(len(basic_tokens)-1):
                pair = (basic_tokens[char_ind], basic_tokens[char_ind+1])
                if pair not in stats:
                    stats[pair] = StatsEntry(pair, set())
                stats[pair].positions.add((string_ind, char_ind))
        for key in stats:
            self._stats.push(stats[key])