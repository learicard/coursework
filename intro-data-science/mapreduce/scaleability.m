## scaleability

for N items
past: max N^m operations, "polynomial time algos"
	m = 1 - linear time algo
	m = 2 - quadratic time algo
	m = exp - does not scale!!!

now:  max N^m/k operations, for large K "parallelized polynomial time algos"
soon: max N*log(N) operations, one pass at streaming data

out of core processing: works off disk
in core processing: works in CPU

scale out: more computers
scale up: more memory/cpu

## indexing is fast

CREATE INDEX seq_idx ON sequence(seq);

SELECT seq
  FROM sequence
 WHERE seq = 'GATTACA'; # will automatically use seq_idx! SQL advantage

## splitting up processes: read trimming
by using k cores, we can scale on inherently linear problems

sometimes benificial to pre-sort/map and then group similar items into the 
same worker (or set of workers), where they are finally reduced.

Data --> Map --> Shuffle --> Reduce --> Output

Map: Takes objects and returns objects (you don't need to program
                                        in parallel, done for you)
Reduce: Takes object and returns transformed object.

Can iterate over map/reduce to continuously shrink your data.

MAP REDUCE:

files = a bag of (key, value) pairs!
input = a bag of (Ikey, value) pairs
output = a bag of (Okey, value) pairs

we assume that each of these pairs will fit on one machine.


Step1: MAP - applied in parallel to all (key, value) pairs

I = (inputKey, value)
O = bag (intermediateKey, value)

map(inKey, inVal) -> list(outKey, intermediateVal)

Step2: REDUCE - groups all intermediate keys, passes this bag to REDUCE fxn

I = bag (intermediateKey, value)
O = bag (values)

reduce(outKey, list(intermediateVal) --> list(outVal)

Inspired by List, Scheme, Haskell (functional programming languages)

EX:

map(String inKey, string inVal) // (document name, document contents):
	for each word w in inVal:
		EmitIntermediate(w, 1); // grab all of the words

combine(string outKey, Iterator intermediateValue): // merges similar keys
	returns (outKey, intermediateValue)             // (saves network traffic)

reduce(String outKey, Iterator intermediateValue): // outKey = word
	int result = 0;
	for each v in intermediateValue:
		result += v;
	EmitFinal(outKey, result);  // create a giant list of all the words

# faster algo: precount word counts per document pre shuffle phase
# NB: bottlneck is often transfer of data across network.
map(String inKey, string inVal)
	for each word w in inVal:
		---


## Matrix Multiplication

C = A X B;
A has dims = L, M
B has dims = M, N

Map phase:
	for each (x, y) of A, emit ((x, y), A[x, y]) for z in 1...N
	for each (y, z) of B, emit ((x, y), B[y, z]) for x in 1...L

Reduce phase:
	key = (x, z)
	val = Sum(A[x,y]*B[y,z])

1 Reducer per output cell
Each reducer computes Sum(A[x,y]*B[y,z])
	So cell 1,1 of output req all vals from A[1, :] and B[:, 1]
	However we do not have a standard matrix, but a sparse matrix.

	So during map, we send duplicates of each cell to the apprpopriate 
	reducer to allow it to compute the dot product.


## Parallel Architectures: Shared Nothing
	Only network connects computers
	The only way to scale to 1000s of computers!
	Data is partitioned into chunks (~64MB)
		Chunks replicated for fault tolerance (diff. racks, > 3)

