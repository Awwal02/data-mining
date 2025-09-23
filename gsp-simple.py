
def generate_candidates(frequent_seqs, k):
    seqs = []
    for i in frequent_seqs:
        for j in frequent_seqs:
            if i[1:] == j[:-1]:
                candidate = i +  [j[-1]]
                if candidate not in seqs:
                    seqs.append(candidate)
    # if k == 2:
    print("seqs")
    print(seqs)
    return seqs

def count_sequences(sequences, candidate):
    support = 0
    for seq in sequences:
        it = iter(seq)
        if all(item in it for item in candidate):
            support += 1
    return support

def gsp(sequences, min_support):
    items = set(item for seq in sequences for item in seq)
    freq_seqs = [[item] for item in items]

    k=1
    results = []
    while freq_seqs:
        next_freq = []
        for seq in freq_seqs:
            support = count_sequences(sequences, seq)
            if support >= min_support:
                results.append((seq, support))
                next_freq.append(seq)

        freq_seqs = generate_candidates(next_freq, k+1)
        k += 1
    return results


sequences = [
    ["I", "like", "apple", "pie"],
    ["I", "like", "banana"],
    ["I", "like", "apple"],
    ["apple", "pie", "is", "good"]
]

patterns = gsp(sequences, min_support=2)
for p, sup in patterns:
    print(p, "-> support:", sup)
