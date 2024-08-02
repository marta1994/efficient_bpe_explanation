class TokenNode:
    def __init__(self, basic_char: str, token: int, parent, children):
        self.parent = parent
        self.basic_char = basic_char
        self.token = token
        self.children = children

class ToTokensConverter:
    def __init__(self, token_map: dict, chars_map: dict):
        self._token_map = token_map
        self._chars_map = chars_map
        self._unk_key = 'unknown'
        self._init_token_tree()
        
    def to_tokens(self, strings):
        return [self._to_tokens(string) for string in strings]
    
    def _to_tokens(self, string):
        tokens = []
        char_index = 0
        while char_index < len(string):
            if string[char_index] not in self._chars_map:
                tokens.append(self._chars_map[self._unk_key])
                char_index += 1
                continue
            current_nodes = self._token_roots
            last_node_with_token = None
            last_index_with_token = char_index
            while char_index < len(string):
               if  string[char_index] in current_nodes:
                   node = current_nodes[string[char_index]]
                   if node.token != None:
                       last_node_with_token = node
                       last_index_with_token = char_index
                   current_nodes = node.children
                   char_index += 1
               else:
                   break
            tokens.append(last_node_with_token.token)
            char_index = last_index_with_token + 1
        return tokens
    
    def _init_token_tree(self):
        self._token_roots = {}
        for token in self._token_map:
            string = self._token_map[token]
            current_nodes = self._token_roots
            last_node = None
            for char in string:
                if char in current_nodes:
                    last_node = current_nodes[char]
                else:
                    last_node = TokenNode(char, None, last_node, {})
                    current_nodes[char] = last_node
                current_nodes = last_node.children
            if last_node.token != None:
                raise KeyError('The token is already taken')
            last_node.token = token