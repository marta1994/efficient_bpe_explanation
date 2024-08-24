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

### Tackling Pair Replacement Efficiency: Linked array

Replacing pairs directly in a simple array presents a challenge: when we merge two elements into one, we need to shift all subsequent elements to the left, leading to potentially costly operations, especially for large texts and frequent merges.

A linked list offers a solution with its ability to efficiently insert and delete elements. However, linked lists lack direct index access, making it difficult to track the positions of pairs within the text, which is crucial for our BPE algorithm.

Enter the linked array, a hybrid data structure that marries the strengths of both arrays and linked lists. It maintains a doubly linked list of elements, where each node also stores its corresponding index in an array. This allows for:

* **Fast Merging**: We can efficiently remove the two nodes representing the pair and insert a new node with the merged token, all without shifting the remaining elements.
* **Direct Index Access**: The array provides immediate access to any element's position, essential for updating our priority map.

The [`LinkedArray`][linked_array] class presents a specialized data structure tailored for efficient pair replacement in BPE training. It establishes a fixed-size array, initialized with an existing sequence of tokens, and a corresponding doubly linked list to facilitate seamless element manipulation.

#### Key Methods and Functionality

* `\_\_init\_\_(items)`:
  * Constructs the linked array from an initial array of tokens items.
  * Creates a doubly linked list, where each node stores a token and its corresponding array index.
  * Populates the fixed-size array with references to these linked list nodes.
* `get_by_index(index)`: Provides direct access to the token at the specified index in the array.
* `get_next_index(index)`:
  * Retrieves the index of the next token in the sequence, following the token at the given index.
  * Returns None if the index is out of bounds, points to a None value, or refers to the last token in the list.
  * Essential for traversing the linked list and identifying neighboring pairs during merging.
* `replace_pair(index, new_item)`: 
  * Core method for pair replacement in BPE training.
  * Replaces the pair of tokens starting at index with the new_item.
  * Updates both the linked list (removing the two original nodes and inserting a new one) and the array (setting the index of the second token in the pair to None and updating the index of the new node).

#### Example Usage

Consider the string "abcddbcdabdcbabab".  If we replace the first pair "ab" with "Z", the linked array efficiently handles this merge, resulting in:

* String: "Zcddbcdabdcbabab"
* Array:
  * 0 -> "Z"
  * 1 -> None
  * 2 -> "c"
  * 3 -> "d"
  * ... (rest of the indices remain unchanged)

![Linked array][linked_array_gif]

In essence, the [`LinkedArray`][linked_array] acts as a bridge between the direct index access of arrays and the flexible insertion/deletion capabilities of linked lists. It's specifically designed to optimize the pair replacement process in BPE tokenization, contributing to a more performant and streamlined algorithm.

## BPE Tokenizer Training: A Visual Guide

Let's embark on a journey to understand the inner workings of BPE tokenizer training through a hands-on example. We'll take the string `"aaabdaaadac"` and illustrate how the algorithm progressively merges pairs of characters to build a vocabulary of subwords.

In this exploration, we'll leverage the optimized data structures we've discussed: the priority map for efficient pair selection and the linked array for streamlined text representation and merging.

### Initial Setup

We begin by initializing our priority map and linked array with the input string. The priority map will store all unique pairs of characters along with their counts and positions in the text. The linked array will provide a flexible representation of the string, enabling efficient pair replacement.

The initial state of these structures is depicted below:

![Example: initial setup][initial_setup_example]

### Step 1: Merging the Most Frequent Pair

As illustrated in the image below, our priority map identifies the pair {a, a} as the most frequent, occurring 4 times in our string at positions 0, 1, 5, and 6. We'll introduce a new token, "Z", to replace these occurrences. Starting with the first position (index 0), we consider the indices of the pair itself (0 and 1), its right neighbor (index 2), and its left neighbor (which is `None` in this case, as 'a' is the first character). After the merge at position 0, we remove this position from the set of pair positions associated with {a, a} in the priority map.

![Example: mergeing the first pair][first_pair_example]

[bpe_walk_through]: https://github.com/marta1994/efficient_bpe_explanation/blob/main/blob/bpe_walk_through.gif
[bpe_wiki]: https://en.wikipedia.org/wiki/Byte_pair_encoding
[priority_queue]: https://en.wikipedia.org/wiki/Priority_queue
[affected_neighbors]: https://github.com/marta1994/efficient_bpe_explanation/blob/main/blob/affected_neighbors.gif
[max_priority_map]: https://github.com/marta1994/efficient_bpe_explanation/blob/main/impl/max_priority_map.py
[max_prority_map_class]: https://github.com/marta1994/efficient_bpe_explanation/blob/main/impl/max_priority_map.py#L1
[associative_array]: https://en.wikipedia.org/wiki/Associative_array
[linked_array]: https://github.com/marta1994/efficient_bpe_explanation/blob/main/impl/linked_array.py#L8
[linked_array_gif]: https://github.com/marta1994/efficient_bpe_explanation/blob/main/blob/linked_array.gif
[initial_setup_example]: https://github.com/marta1994/efficient_bpe_explanation/blob/main/blob/example_initial.png
[first_pair_example]: https://github.com/marta1994/efficient_bpe_explanation/blob/main/blob/example_first_pair.gif