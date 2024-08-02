import unittest

from tokenizer_for_test import NaiveTokenizer
from tokenizer import Tokenizer

class TestTokenizer(unittest.TestCase):
    
    def test_basic_string(self):
       train_input = ['aaabdaaabac']
       test_input = ['aaabaaabdabacabdaaabac']
       self._test_input(train_input, test_input, 2)
       
    def test_real_string(self):
       train_input = ['I have always been interested in learning different languages- though the only French the Duolingo owl has taught me is, Je m’appelle Manan .',
                      'My short stints at learning a third language helped me realise that vocabulary is not sufficient- contexts, semantics and syntactic features were also important to truly grasp the meaning from a language.',
                      'So when I started doing NLP tasks recently, I felt really perplexed about how something like a bag-of-words which considers each word in a very independent light could really be efficient- and I got answers to this question when I learnt what word embeddings are and how they work.',
                      'In this article, I’m going to be talking about word embeddings, specifically the word2vec model and how to take its advantage using the easy to use Gensim library.',
                      'Word embeddings',
                      'The emergence of language was a pivotal movement in the evolution of humanity.',
                      'Although all species have their ways of communicating, we as humans are unique in having been the only ones who have mastered cognitive language communication.',
                      'So while I know that “rat” refers to a small hairy rodent, my dog or my computer (at least in essence) doesn’t know that.']
       test_input = ['Therefore, any task aimed at processing language must first begin with focusing on how to represent the words essentially.',
                     'A preliminary method is a “bag of words” model which encodes words using a one-hot scheme.',
                     'If our dataset contains the sentences:',
                     '“I like the new movie!”, “I love the weather.”',
                     'Then we can have a vector representation of the words as:',
                     'However, as you might have noticed, that this representation is not very effective at showing the semantic and syntactic relationships between words- they are encoded as individual its in a vector space and there is no way you can tell the words “love” and “like” have a similar connotation.',
                     'This is where word embeddings come in. ',
                     'Word embeddings are basically representations where contexts and similarities are captured by encoding in a vector space- similar words would have similar representations. ',
                     'We’re going to be discussing word2vec which is an effective word embedding technique.',
                     'Word2Vec',
                     'Word2Vec creates a representation of each word present in our vocabulary into a vector. ',
                     'Words used in similar contexts or having semantic relationships are captured effectively through their closeness in the vector space- effectively speaking similar words will have similar word vectors! History.',
                     'Word2vec was created, patented, and published in 2013 by a team of researchers led by Tomas Mikolov at Google.',
                     'Let us consider a classic example: “king”, “queen”, “man”, “girl”, “prince”',
                     'In a hypothetical world, vectors could then define the weight of each criteria (for example royalty, masculinity, femininity, age etc.) for each of the given words in our vocabulary.',
                     'What we then observe is:',
                     'As expected, “king”, “queen”, “prince” have similar scores for “royalty” and “girl”, “queen” have similar scores for “femininity”.',
                     'An operation that removes “man” from “king”, would yield in a vector very close to “queen” ( “king”- “man” = “queen”)',
                     'Vectors “king” and “prince” have the same characteristics, except for age, telling us how they might possibly be semantically related to each other.']
       self._test_input(train_input, test_input, 4)
       
    def _test_input(self, train_input, test_input, min_token_occurance):
       tokenizer = Tokenizer(min_token_occurance)
       naive_tokenizer = NaiveTokenizer(min_token_occurance)
       train_char_set = set(''.join(train_input))
       test_char_set = set(''.join(test_input))
       unknown_test_characters = test_char_set - train_char_set
       test_input_with_unknowns = [''.join(char if char not in unknown_test_characters else '□' for char in inp) for inp in test_input]
       
       naive_tokenizer.train(train_input)
       tokenizer.train(train_input)
       naive_tokens = naive_tokenizer.to_tokens(test_input)
       tokens = tokenizer.to_tokens(test_input)
       string_from_naive_tokens = naive_tokenizer.from_tokens(naive_tokens)
       string_from_tokens = tokenizer.from_tokens(tokens)
       
       self.assertEqual(string_from_naive_tokens, string_from_tokens)
       self.assertEqual(test_input_with_unknowns, string_from_tokens)
                
if __name__ == '__main__':
    unittest.main()