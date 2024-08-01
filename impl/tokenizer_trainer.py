from linked_array import LinkedArray
from max_priority_map import MaxPriorityMap

class StatsEntry:
    def __init__(self, pair, positions):
        self.pair = pair
        self.positions = positions


class TokenizerTrainer:
    def __init__(self, input_as_basic_tokens, target_merge_count, tokens_map):
        self._input_as_basic_tokens = input_as_basic_tokens
        self._target_merge_count = target_merge_count
        self._tokens_map = tokens_map
        
    def train(self, next_token):
        self._positions = [LinkedArray(basic_tokens) for basic_tokens in self._input_as_basic_tokens]
        self._calc_initial_stats()
        for _ in range(self._target_merge_count):
            merge_stat = self._stats.pop()
            for position in list(merge_stat.positions):
                # The original collection may be modified in the loop
                if position not in merge_stat.positions:
                    continue
                input_index = position[0]
                token_index = position[1]
                self._update_left_token(input_index, token_index, merge_stat, next_token)
                self._update_right_token(input_index, token_index, merge_stat, next_token)
                self._positions[input_index].replace_pair(token_index, next_token)
                merge_stat.positions.remove((input_index, token_index))
 
            self._tokens_map[next_token] = self._tokens_map[merge_stat.pair[0]] + self._tokens_map[merge_stat.pair[1]]
            next_token += 1
            
    def _update_right_token(self, input_index, token_index, merge_stat, new_token):
        positions = self._positions[input_index]
        second_token_index = positions.get_next_index(token_index)
        right_token_index = positions.get_second_next_index(token_index)
        if right_token_index == None:
            return
        pair = (merge_stat.pair[1], positions.get_by_index(right_token_index))
        self._remove_position_from_pair(merge_stat, pair, input_index, second_token_index)
        new_pair = (new_token, pair[1])
        self._add_position_to_pair(new_pair, input_index, token_index)
            
    def _update_left_token(self, input_index, token_index, merge_stat, new_token):
        positions = self._positions[input_index]
        left_token_index = positions.get_previous_index(token_index)
        if left_token_index == None:
            return
        pair = (positions.get_by_index(left_token_index), merge_stat.pair[0])
        self._remove_position_from_pair(merge_stat, pair, input_index, left_token_index)
        new_pair = (pair[0], new_token)
        self._add_position_to_pair(new_pair, input_index, left_token_index)
        
    def _remove_position_from_pair(self, merge_stat, pair, input_index, token_index):
        # self._stats does not contain merge_stat, because it is currently being processed.
        # We need to verify the current merge_stat as well as search in self._stats.
        if pair == merge_stat.pair:
            merge_stat.positions.remove((input_index, token_index))
        else:
            stat = self._stats.delete_by_map_key(pair)
            stat.positions.remove((input_index, token_index))
            if len(stat.positions) != 0:
                self._stats.push(stat)
        
    def _add_position_to_pair(self, pair, input_index, token_index):
        # Remove, update positions and insert again.
        # The priority map is sorted by positions count,
        # so to keep it sorted, we can not update positions of an object in the collection.
        stat = self._stats.delete_by_map_key(pair) if self._stats.contains(pair) else StatsEntry(pair, set())
        stat.positions.add((input_index, token_index))
        self._stats.push(stat)
         
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