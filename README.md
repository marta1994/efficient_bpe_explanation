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

## BPE optimization

While the naive BPE training algorithm provides a clear understanding of the process, it leaves room for improvement in terms of efficiency. Let's identify some key areas where we can potentially enhance the time complexity:

* **Redundant Pair Counting**: Recalculating all pair occurrences after every merge seems excessive. Can we devise a smarter way to update the counts incrementally?

* **Efficient Pair Selection**: Finding the most frequent pair currently involves iterating through all pair counts. Can we employ a more efficient data structure to streamline this selection process?

* **Streamlined Text Representation**: Storing the text in its raw form might lead to suboptimal performance when replacing pairs. Could we adopt a representation that facilitates faster merging operations?

By addressing these bottlenecks, we can pave the way for a more performant BPE training algorithm. Let's delve into the specifics of each optimization opportunity and explore how to implement them effectively.

### Efficient Pair Selection with a Heap

Instead of linearly searching through all possible pairs to find the most frequent one, we can leverage a [heap (priority queue)][priority_queue] data structure for efficient retrieval.

* **Maintaining the Heap**: At each step of the merging process, we'll keep a heap that stores all the current pairs along with their frequency counts. The heap is organized based on the "count" field, ensuring that the pair with the highest count (the most frequent one) always sits at the top.

* **Quick Retrieval**: When it's time to decide which pair to merge, we simply peek at the top of the heap. This gives us immediate access to the most frequent pair without having to scan the entire list.

* **Updating the Heap**: As merges occur and new pairs are formed, we'll need to update the heap accordingly. This involves potentially removing existing pairs, adding new ones, and adjusting the heap structure to maintain the correct order.

### Streamlining Pair Replacement with Position Tracking

To efficiently replace all occurrences of a selected pair, we'll augment our heap objects with position information:

* **Positions Set**: Alongside the pair itself and its count, we'll include a set of position identifiers (EG integers, pairs of integers depending on the input format) representing the positions where this pair appears in the text.

* **Targeted Replacement**: Once we've identified the most frequent pair from the heap, we can directly access its positions set and iterate through it. This allows us to pinpoint the exact locations where the pair needs to be replaced with the new token, eliminating the need for a full text scan.

**Updated Object Structure:**
```
{
    pair: (token, token)
    positions: set<position_index> 
    count: int  # heap key, derived from len(positions)
}
```

### Handling Neighboring Pairs with a Priority Map

Replacing a pair not only affects its own occurrences but also impacts the neighboring pairs in the text. Let's consider how to efficiently manage these changes. When we replace a pair like "ba" with "Z" in string "abac" with respective positions `[p1, p2, p3, p4]`, the original pairs "ab" and "ac" disappear, while new pairs "aZ" and "Zc" emerge. We need to reflect these changes in our heap to maintain accurate pair counts and positions.

![affected neighbors][affected_neighbors]

To achieve this, we require the ability to retrieve heap items based on their "pair" key, not just their priority (count). This allows us to modify the positions set of relevant pairs, removing old positions and adding new ones. A combination of a map (for efficient key-based retrieval) and a priority queue (for maintaining the count-based order) emerges as the ideal solution. This "priority map" enables us to:

* Quickly locate heap items associated with specific pairs.
* Update their position sets to reflect the impact of merges.
* Maintain the heap's priority order based on the updated counts.

#### [Max priroty map implementation][max_priority_map]

The [`MaxPriorityMap`][max_prority_map_class] class implements a combination of a max-heap ([priority queue][priority_queue]) and a [map][associative_array]. It allows efficient storage and retrieval of items based on two keys: a `heap_key` used for maintaining the heap's priority order, and a `map_key` used for quick item lookup. The heap ensures that the item with the highest `heap_key` value is always at the top, while the map provides direct access to items using their `map_key`. The class includes methods for pushing new items, popping the maximum item, checking for item existence, deleting items by `map_key`, and maintaining the heap's structural integrity through `_heapify_up` and `_heapify_down` operations.


[bpe_walk_through]: https://github.com/marta1994/efficient_bpe_explanation/blob/main/blob/bpe_walk_through.gif
[bpe_wiki]: https://en.wikipedia.org/wiki/Byte_pair_encoding
[priority_queue]: https://en.wikipedia.org/wiki/Priority_queue
[affected_neighbors]: https://github.com/marta1994/efficient_bpe_explanation/blob/main/blob/affected_neighbors.gif
[max_priority_map]: https://github.com/marta1994/efficient_bpe_explanation/blob/main/impl/max_priority_map.py
[max_prority_map_class]: https://github.com/marta1994/efficient_bpe_explanation/blob/main/impl/max_priority_map.py#L1
[associative_array]: https://en.wikipedia.org/wiki/Associative_array