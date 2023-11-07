import hashlib

# Input sentence
sentence = "This is the start of a new beginning, with vast application opportunities"

# Split the sentence into words
words = sentence.split()

# Create a list of leaf nodes (hashes of each word)
leaf_nodes = [hashlib.sha256(word.encode()).hexdigest() for word in words]

# Function to compute the Merkle root
def compute_merkle_root(leaf_nodes):
    if len(leaf_nodes) == 1:
        return leaf_nodes[0]
    else:
        paired_nodes = [leaf_nodes[i] + leaf_nodes[i+1] for i in range(0, len(leaf_nodes), 2)]
        if len(leaf_nodes) % 2 != 0:
            paired_nodes.append(leaf_nodes[-1])
        return compute_merkle_root(paired_nodes)

# Compute the Merkle root
merkle_root = compute_merkle_root(leaf_nodes)

print("Merkle Root:", merkle_root)
