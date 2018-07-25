final 2014
----------

1. In Figure 2 we see an example of randomized SkipList. Levels in the example
at the current stage are 0, 1, 2 and 3. Then we want to insert the key 7. To do
this we use the procedure

    for (nivmax = O; random() == O; nivmax ++);

which by chance returns us twice 0, followed by a 1. Draw the SkipList after
inserting the key.

**ans**: 7 is inserted on the 3rd level, between 4 and the 11.


|                   |
|---------7----     |
|---2-----7-11-     |
|-1-2-3-4-7-11- ... |


2. (a) Suppose we have used a self-structured list, tabulated,
to store N keys, and that after a certain number of accesses, the keys are
ordered in descending probability (that is, the probability that the key will
be accessed) in the table. Suppose in fact that the probability related to the
i-th key is 1/iH_N, i=1, ..., N, where H_N is the Harmonic number. (This is
Zipf's law, which happens often in practice.) Derive the average cost of
search in this case, and make the comparison with the case where the keys
are equiprobable.

**ans**:

E(N) = sum(ix1 / ixH_N) = 1/H_N * sum(1) = 1/H_N * N = N / H_N ~~> N / logN
E(N) = sum(i / N) = 1/N x sum(i) = N(N+1) / Nx2 = (N+1)/2      --> N

(b) Explain the link between the idea of the Question 2a method and the Splay
Tree. How valid is this comparison?

**ans**: Splay trees move each item to the root after each access. Therefore,
the tree will be sorted according to access probaility (which will be
proportional to the harmonic numbers) assuming accesses have been going on for a
while. So the element at the root (1/i=1) has twice the access probability as
l=2 (1/i=2), and at level n, probability proportional to 1/i=n will be a leaf.
This ensures average O(log N) access time.

    sum(1/i) = H_N ~ O(log N).

3. Suppose a red-black tree, with five nodes, and with key 4 at the root. The
child right of the root contains the key 5, while the left child (red) of the
root contains the key 2. Finally, the children of the node that contains the
key 2 respectively contain keys 1 and 3.

Draw the red-black tree (indicating the colors of the nodes), draw a tree 2-4
equivalent, and draw a "1-2-3 Deterministic Skip-List" equivalent.


Red black tree: *1* = red

     ^4^
    /   \
  *2*     5
  / \
1    3

2-4 tree (only one BLACK node allowed at each level!)

         2-4--
   /     | L      \
 1----   3----     5----
L L L L  L L L L  L L L L

1-2-3 Determinisitic Skip-List:

|           |
|---2---4---|
|-1-2-3-4-5-|

4. Draw the result of doing the following, starting from an empty tree, for a
SplayTree. Indicate substeps as needed.

(a) Insert the keys 1, 2, 3, 4, 5, in order.

        5
       /
      4
     /
    3
   /
  2
 /
1

(b) Access the key 2.

zig
      5
     /
    3
   / \
  2   4
 /
1

zig
    5
   /
  2
 / \
1   3
     \
      4

single right rotation
  2
 / \
1   5
   /
  3
   \
    4

(c) Then, in a separate operation, remove the key 2

1 is the max of LEFT subtree, so:

  1
   \
    5
   /
  3
   \
    4

5. For the Prim algorithm:
(a) Briefly explain the motivation to use a heap to store "best distances"
at each stage.

The nieve implementation requires looping over the |V| distances |V| times,
using nested loops. This gives a runtime of |V|^2. Using heaps, this operation
can be reduced to O(|V| log|V|).

(b) Give the complexity of the resulting algorithm using theta(.), |V| and |E|.

theta(  |E| log |V|  +  |V| log |V|) ... searching edges + findmin.
theta( (|E| + |V|) log|V|

(c) Explain clearly why the answer to question 5b shows that this approach
gives a worse result than the original algorithm in the case of a dense graph.

When the graph is dense |E| = |V|^2. When the graph is sparse, |E| = |V|.

The nieve implementaion runs in O(|V|^2).

When the graph is dense, the runtime is theta(|V|^2 log|V|) > |V|^2.
When the graph is sparse, the runtime is theta(|V| log|V|) < |V|^2.

6. In the context of hashing with double hashing:

(a) Explain with a simple example the need for tombstones.

Tombstones are used to delete elements, without interfering with other inserted
elements.

E.g., we added x and y. Y collides with the hash of x, so it is placed in a
second location (double hashing). If we then delete x by clearing the element,
and then search for y, the algorithm will find an empty element and stop
looking.

(b) In Duty 3 there was a suggested trick to reduce the cost of research,
by modifying the "collision paths". Give an example that shows the idea of
basis of this "trick", ie how could this idea reduce the cost of
research. (I only ask for one small example, not all the algorthme: none
mathematical notation is required.)

N/A

7. In the context of the "Threaded Lists" we have seen a route algorithm.
There was a mpf variable that indicated if we had arrived in a node going up by
a thread, or not. Give a simple example that shows that it is obligatory to be
able to know in which of the two cases we are.

Algo - follow right pointer, if it isn't a thread, follow left pointers untill
its done. If there is a right child, do this again, otherwise, follow the
thread.

If **mfp** is true, then we should print the value of the current node, since we
just found (and printed) the left child. Then, we continue searching to the
right.

inorder: 5-7-6-8-10

  7
 / \
5   8
   / \
  6   10


8. Mention a case where re-hashing may be needed.

Hashing functions only give constant-access times when only a small number of
probes, usually 1, are required to find the data associated with a given key.

Collision resolution strategies, such as external chaning and probing, require
multiple accesses to the table. This is OK if it is occasional, but if it is
required all of the time, then access times to the table cease to be constant.

We quantify this with the load_factor (lambda) variable = n_entries / tableSize.
When lambda is 0.4-0.5, we have good performance, but as we continue to add more
values to the table, performance will degrade. In this case, we can re-hash
to the prime value that is closest to double the size. This operations costs
O(n), where n is the number of values in the table. Since this only happens
occasionally, this is considered to add a small constant to the overall runtime.

With this larger table size, the load factor will approximately halve.


9. Show that the height of a red-black tree never exceeds 2 lg(N+1), where N
is the number of nodes.

N >= 2^B-1

N+1 >= 2^B
log(N+1) >= B x log2

Since no two layers can be RED sequentially, B >= 1/2 height

therefore log(N+1) >= B >= 1/2 height,

Therefore, 1/2 height <= log(N+1), height <= 2 log(N+1)


10. Give two reasons to take M a prime number in the open addressing method.

a) If M is prime, then mod M during double, triple, etc. hashing will produce the
most unique indicies (since index = h(x) mod M), this reduces the number of
colissions

b) Is M is prime, then the values are least likely to cluster (group in the
same area of the table), no matter the distribution of the input values.

