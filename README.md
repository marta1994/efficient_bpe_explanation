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

[bpe_walk_through]: https://github.com/marta1994/efficient_bpe_explanation/blob/main/blob/bpe_walk_through.gif
[bpe_wiki]: https://en.wikipedia.org/wiki/Byte_pair_encoding