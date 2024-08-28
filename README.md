# Efficient BPE Tokenization from Scratch

**TL;DR:** Dive into the [`tokenizer.py`][tokenizer_impl] file to explore a clear, educational implementation of BPE tokenization in plain Python, focused on algorithmic understanding. 

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

The original algorithm works by iteratively finding the most common pairs of characters and replacing them with a new symbol. Think of it as finding the most popular phrases in a text and giving them a unique code. It's worth noting that BPE is inherently **not deterministic**, as there might be multiple pairs with the same highest frequency at any given step. This means that different runs of the algorithm on the same text might produce slightly different vocabularies. This process continues until no more pairs can be found, effectively compressing the original text.

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

The [`max_priority_map.py`][max_prority_map_class] implements a combination of a max-heap ([priority queue][priority_queue]) and a [map][associative_array]. It allows efficient storage and retrieval of items based on two keys: a `heap_key` used for maintaining the heap's priority order, and a `map_key` used for quick item lookup. The heap ensures that the item with the highest `heap_key` value is always at the top, while the map provides direct access to items using their `map_key`. The class includes methods for pushing new items, popping the maximum item, checking for item existence, deleting items by `map_key`, and maintaining the heap's structural integrity through `_heapify_up` and `_heapify_down` operations.

### Tackling Pair Replacement Efficiency: Linked array

Replacing pairs directly in a simple array presents a challenge: when we merge two elements into one, we need to shift all subsequent elements to the left, leading to potentially costly operations, especially for large texts and frequent merges.

A linked list offers a solution with its ability to efficiently insert and delete elements. However, linked lists lack direct index access, making it difficult to track the positions of pairs within the text, which is crucial for our BPE algorithm.

Enter the linked array, a hybrid data structure that marries the strengths of both arrays and linked lists. It maintains a doubly linked list of elements, where each node also stores its corresponding index in an array. This allows for:

* **Fast Merging**: We can efficiently remove the two nodes representing the pair and insert a new node with the merged token, all without shifting the remaining elements.
* **Direct Index Access**: The array provides immediate access to any element's position, essential for updating our priority map.

The [`linked_array.py`][linked_array] presents a specialized data structure tailored for efficient pair replacement in BPE training. It establishes a fixed-size array, initialized with an existing sequence of tokens, and a corresponding doubly linked list to facilitate seamless element manipulation.

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

In essence, the [`linked_array.py`][linked_array] acts as a bridge between the direct index access of arrays and the flexible insertion/deletion capabilities of linked lists. It's specifically designed to optimize the pair replacement process in BPE tokenization, contributing to a more performant and streamlined algorithm.

## BPE Tokenizer Training: A Visual Guide

Let's embark on a journey to understand the inner workings of BPE tokenizer training through a hands-on example. We'll take the string `"aaabdaaadac"` and illustrate how the algorithm progressively merges pairs of characters to build a vocabulary of subwords.

In this exploration, we'll leverage the optimized data structures we've discussed: the priority map for efficient pair selection and the linked array for streamlined text representation and merging.

### Initial Setup

We begin by initializing our priority map and linked array with the input string. The priority map will store all unique pairs of characters along with their counts and positions in the text. The linked array will provide a flexible representation of the string, enabling efficient pair replacement.

The initial state of these structures is depicted below:

![Example: initial setup][initial_setup_example]

### Merging the Most Frequent Pair

As illustrated in the image below, our priority map identifies the pair {a, a} as the most frequent, occurring 4 times in our string at positions 0, 1, 5, and 6. We'll introduce a new token, "Z", to replace these occurrences. Starting with the first position (index 0), we consider the indices of the pair itself (0 and 1), its right neighbor (index 2), and its left neighbor (which is `None` in this case, as 'a' is the first character). After the merge at position 0, we remove this position from the set of pair positions associated with {a, a} in the priority map.

![Example: mergeing the first pair][first_pair_example]

### Updating Neighboring Pairs

The merging process necessitates adjustments to the neighboring pairs in our priority map. We need to remove the pair starting with the left neighbor of the merged pair (if it exists) and the pair starting with the second token of the merged pair. In our current scenario, since the merged pair doesn't have a left neighbor, we only remove the right neighbor pair {a, a} at positions {1, 2}. Subsequently, we introduce new pairs formed by the merge. We add a pair starting with the left neighbor (if it exists) and ending with the merged token, and another pair starting with the merged token and ending with the right neighbor. Again, due to the absence of a left neighbor, we only add one new pair: {Z, b} at positions {0, 2}.

![Example: updating the first neighboring pairs][updating_neightbors_1_example]

### Merging the Next Occurrence

Moving on to the next available position for the pair {a, a}, we skip position 1 (as it was removed in the previous merge) and proceed to position 5. Here, we focus on the indices 4, 5, 6, and 7, representing the left neighbor, the pair itself, and the right neighbor. We merge {a, a} at positions {5, 6}, deleting these tokens and inserting "Z" at position 5.

![Example: merging the next occurrence][merging_next_occurrence_example]

### Updating Neighboring Pairs for the next occurrence

Following the merge, we adjust the neighboring pairs in the priority map. The left neighbor pair {d, a} at positions {4, 5} is deleted entirely since it only occurred once. We then locate the right neighbor pair {a, a} at positions {6, 7} and remove position 6 from its set of positions.

Next, we introduce the new pairs formed by the merge. The left neighbor pair becomes {d, Z} at positions {4, 5}. As this pair is new, we create a fresh entry in the priority map with its position. The right neighbor pair is now {Z, a} at positions {5, 7}. This pair already exists in the map, so we remove it, add the new position to its set (resulting in two positions), and reinsert it into the priority map. This ensures the map remains sorted correctly based on the updated pair counts. Notably, {Z, a} has now become one of the most frequent pairs and could be selected for the next merge step.

![Example: updating the second neighboring pairs][updating_neighbors_2_example]

## Time Complexity Analysis of the Optimized BPE Tokenizer Training

Let's break down the time complexity of the optimized BPE tokenizer algorithm, considering the key operations and data structures involved:

 1. **Initialization:**\
 Building the initial priority map requires iterating through the text and counting pair occurrences, which takes O(N) time, where N is the text length.
 Constructing the linked array also takes O(N) time, as we create nodes and populate the array with references.
 2. **Merging Iterations:**\
 Each iteration involves the following steps:
   * **Finding the most frequent pair:** This is now a constant-time operation O(1) thanks to the priority map.
   * **Replacing the pair in the linked array:** This takes O(1) time as we directly access and modify the relevant nodes and array indices.
   * **Updating neighboring pairs in the priority map:**
     * Retrieving and modifying existing pairs based on their keys takes O(log M) time, where M is the number of unique pairs in the map (which is bounded by the vocabulary size).
     * Inserting new pairs or re-inserting modified pairs also takes O(log M) time.
     * In the worst case, we might need to update all M pairs in the map, leading to a potential O(M log M) complexity for this step.
 3. **Overall Complexity:**
The total number of iterations (merges) is M.
Each iteration has a worst-case complexity of O(M log M) due to the priority map updates.
Therefore, the overall time complexity of the optimized BPE tokenizer is **O(N + M * M log M)**.

**Comparison to Naive Algorithm:**

The naive algorithm had a time complexity of O(N * M), where each iteration involved re-calculating pair counts and searching for the most frequent pair, both taking O(N) time.
The optimized algorithm significantly improves upon this by using a priority map and linked array, reducing the per-iteration complexity to O(M log M) in the worst case.

## Efficient Text-to-Token Conversion: The Challenge

Once our BPE tokenizer is trained, we possess a valuable map connecting token IDs to their corresponding strings.  For example:

* 1 -> "not"
* 2 -> "be"
* 3 -> "to"
* 4 -> "or"
* 5 -> " "

The task remains to efficiently convert raw text into a sequence of these token IDs.  Given this dictionary, we aim to transform the text **"to be or not to be"** into the array **[3, 5, 2, 5, 4, 5, 1, 5, 3, 5, 2, 5]**. While a naive approach might involve iterating through the text and searching for matches, we can achieve superior performance through a trie-based solution.

### Optimizing Text-to-Token Conversion with a Trie

Instead of a naive linear search, we can leverage a trie (prefix tree) for efficient text-to-token conversion. The trie, constructed from the BPE vocabulary, enables fast prefix matching and handles potential token ambiguities through backtracking. During conversion, we traverse the input text from the beginning, always prioritizing the longest possible token match at each position. See the full implementation in [`to_tokens_converter.py`][to_tokens_converter].

For a detailed understanding of tries, refer to the [Trie Wikipedia page][trie].

Here is an example of how to build a prefix tree from a vocabulary list:

![Build a trie][build_trie]

Here is an example of how a text is converted to a list of tokens:

![Convert to tokens][to_tokens]

## Performance Comparison: Naive vs. Optimized BPE

Let's see how the optimized BPE algorithm stacks up against the naive approach on a real-world dataset. We used the [Kaggle "Natural Language Processing with Disaster Tweets"][kaggle_dataset] dataset, running both algorithms in a default Kaggle notebook.

| Task               | Naive Algorithm | Optimized Algorithm | Improvement | Dataset Size |
|--------------------|-----------------:|---------------------:|-------------:|----------------|
| Training           | 27 minutes      | 38 seconds          | **43X**      | ~1 MB (770K characters) |
| Conversion (same dataset) | 13 minutes      | 0.48 seconds        | **1608X**    | ~1 MB (770K characters) |

The optimized algorithm demonstrates a dramatic improvement in both training and conversion times, highlighting the effectiveness of the implemented optimizations. This performance boost makes the optimized approach far more suitable for handling larger datasets and real-world NLP applications.

In conclusion, I hope this exploration of BPE tokenization, from its naive implementation to optimized techniques, has shed light on the fascinating world of algorithmic efficiency in natural language processing. Happy coding!

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
[updating_neightbors_1_example]: https://github.com/marta1994/efficient_bpe_explanation/blob/main/blob/example_modifying_first_pairs.gif
[merging_next_occurrence_example]: https://github.com/marta1994/efficient_bpe_explanation/blob/main/blob/example_second_pair.gif
[updating_neighbors_2_example]: https://github.com/marta1994/efficient_bpe_explanation/blob/main/blob/example_modifying_second_pairs.gif
[trie]: https://en.wikipedia.org/wiki/Trie
[build_trie]: https://github.com/marta1994/efficient_bpe_explanation/blob/main/blob/build_trie.gif
[to_tokens]: https://github.com/marta1994/efficient_bpe_explanation/blob/main/blob/convert_to_tokens.gif
[tokenizer_impl]: https://github.com/marta1994/efficient_bpe_explanation/blob/main/impl/tokenizer.py
[to_tokens_converter]: https://github.com/marta1994/efficient_bpe_explanation/blob/main/impl/to_tokens_converter.py
[kaggle_dataset]: https://www.kaggle.com/competitions/nlp-getting-started/data?select=train.csv