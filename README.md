# Efficient BPE Tokenization from Scratch

This repository provides a clear, educational implementation of Byte Pair Encoding (BPE) tokenization in plain Python. The focus is on algorithmic understanding, not raw performance.

### Key Points:

* **From First Principles**: Learn how BPE training and conversion work under the hood.
* **No Black Boxes**: No external libraries or optimizations (C++, multithreading) are used.
* **For Learning, Not Production**: This is NOT a library, but a resource to deepen your understanding.

### Ideal For:

* Students and practitioners curious about the inner workings of BPE.
* Those who want to build their own custom tokenization pipelines.
* Anyone who prefers learning by doing over abstract theory.

## Byte Pair Encoding (BPE): Text Compression Made Visual

[BPE][bpe_wiki] is like teaching a computer a new language, where words are broken down into smaller, more manageable chunks. It's a bit like creating a shorthand for efficient text processing.

The original algorithm works by iteratively finding the most common pairs of characters and replacing them with a new symbol. Think of it as finding the most popular phrases in a text and giving them a unique code. This process continues until no more pairs can be found, effectively compressing the original text.

To decompress, we simply reverse the process using a lookup table. It's like translating the shorthand back into the original language.

**See BPE in action:**

![bpe walk through][bpe_walk_through]

### Naive BPE Training: Step-by-Step Analysis

Let's break down the core steps of the naive BPE training algorithm, along with their associated time complexities:

1. **Count Pair Occurrences: O(N)**\
Tally the frequency of each character pair in the text. This step involves examining the entire text, leading to a time complexity of O(N), where N represents the length of the text.

2. **Find Most Frequent Pair: O(N)**\
Identify the pair with the highest frequency among all counted pairs. This process necessitates iterating through the pair counts, resulting in a time complexity of O(N).

3. **Replace and Merge: O(N)**\
Replace all occurrences of the most frequent pair with a new token, effectively merging those characters. This replacement requires another pass through the text, contributing an additional O(N) to the time complexity.

4. **Iterate Until Convergence: O(N * M)**\
Repeat steps 1-3 until a predefined stopping criterion is met. Each iteration encompasses the previous steps, and the total number of iterations is determined by the number of merges, M. Therefore, this step multiplies the combined complexity of the previous steps by M.

In conclusion, the naive BPE training algorithm has a time complexity of **O(N * M)**, where N is the text length and M is the number of merges performed.

[bpe_walk_through]: https://github.com/marta1994/efficient_bpe_explanation/blob/main/blob/bpe_walk_through.gif
[bpe_wiki]: https://en.wikipedia.org/wiki/Byte_pair_encoding