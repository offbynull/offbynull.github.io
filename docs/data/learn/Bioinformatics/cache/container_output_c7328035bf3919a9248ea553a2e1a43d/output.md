<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The Pevzner book goes on to discuss other common tasks that a suffix tree can help with:

 * Finding the longest repeating substring within a sequence.

   This is just a search down the suffix tree (starting at root) with the condition that an edge has > 1 occurrence. In the example execution above, the longest repeating substring in "banana" is "ana": The edge "a" has 3 occurrences, which leads to edge "na" which has 2 occurrences, which leads to no more edges with occurrences of > 1.

 * Finding the longest shared substring between two sequences.

   The obvious way to do this is to generate a suffix tree for each sequence and cross-check. However, the Pevzner book recommends another way: Concatenate the two strings together, both with an end marker but different ones (e.g. first one uses § while the other one uses ¶). Then, each leaf node gets a color (state) depending on the starting position of the suffix: blue if its limb starts within sequence 1 / red if its limb starts within sequence 2. For internal nodes, the color is set to purple if that node has children with different colors, otherwise its color remains consistent with the color of its children.


   ```{svgbob}
   * "Colored suffix tree for bad§fade¶"

        ¶
      .---r
      | e¶
      +----r
      | fade¶
      +-------r
      | §fade¶
      +--------b
      |     e¶
   p--+   .----r
      | d | §fade¶
      +---p--------b
      |      e¶
      |    .----r
      | ad | §fade¶
      +----p--------b
      | bad§fade¶
      '-----------b
   ```

   Search down the suffix tree (starting at root) with the condition that an edge has purples at both ends. The longest shared sequence between "bad" and "fade" is "ad".

   The coloring concept makes it difficult to understand what's happening here. The code for this section tracks how many occurrences an edge has and where those occurrences occur. Use that to set a flag on the node: {first, second, both}. Then this becomes the "longest repeating substring" problem except that there's an extra check on the node to ensure that occurrences are happening in both sequences.

 * Finding the shortest non-shared substring between two sequences.

   This is a play on the longest shared substring problem described above. The suffix tree is built the same way and searched the same way, but how the tree searched is different. 

   ```{svgbob}
   * "Colored suffix tree for bad§fade¶"

        ¶
      .---r
      | e¶
      +----r
      | fade¶
      +-------r
      | §fade¶
      +--------b
      |     e¶
   p--+   .----r
      | d | §fade¶
      +---p--------b
      |      e¶
      |    .----r
      | ad | §fade¶
      +----p--------b
      | bad§fade¶
      '-----------b
   ```

   Search down the suffix tree (starting at the root) until a non-purple node is encountered. Capture the sequence up to the node _before_ the non-purple node + the first element of the edge to the non-purple node (skip capturing if that element is an end marker). Of all the strings captured, the shortest one is the shortest non-shared substring. The shortest non-shared substring between "bad" and fade" is either "e", "b", or "f" (all are valid choices).

   The simplest way to think about this is that the shortest non-shared substring must be 1 appended element past one of the shared substrings (it can't be less -- if "abc" is shared then so is "ab"). You know for certain that, after appending that element, the substring is unique because the destination node is non-purple (blue means the substring is in sequence 1 / red in sequence 2). In this case, directly coming from the root node is considered a shared substring of "" (empty string):

   * d[e¶] ⟵ first char of non-shared edge is e, captured "de"
   * d[§fade¶] ⟵ first char of non-shared edge is end marker (§), skip
   * [¶] ⟵ first char of non-shared edge is end marker (¶), skip 
   * [e¶] ⟵ first char of non-shared edge is e, captured "e"
   * [§fade¶] ⟵ first char of non-shared edge is end marker (§), skip 
   * [fade¶] ⟵ first char of non-shared edge is f, captured "f"
   * ad[e¶] ⟵ first char of non-shared edge is e, captured "e"
   * ad[§fade¶] ⟵ first char of non-shared edge is end marker (§), skip
   * [bad§fade¶] ⟵ first char of non-shared edge is b, captured "b"

   Of the captured strings ["e", "de", "f", "e", "b"], the shortest length is 1 -- any captured string of length 1 can be considered the shortest non-shared string.
</div>

