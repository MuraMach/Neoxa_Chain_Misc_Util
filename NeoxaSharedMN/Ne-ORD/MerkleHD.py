import hashlib

# Input sentences
sentences = [
    "This is the start of a new beginning,",
    "with vast application opportunities"
]

# Function to compute the Merkle root for a list of data
def compute_merkle_root(data):
    leaf_nodes = [hashlib.sha256(item.encode()).hexdigest() for item in data]

    if len(leaf_nodes) == 1:
        return leaf_nodes[0]
    else:
        paired_nodes = [leaf_nodes[i] + leaf_nodes[i+1] for i in range(0, len(leaf_nodes), 2)]
        if len(leaf_nodes) % 2 != 0:
            paired_nodes.append(leaf_nodes[-1])
        return compute_merkle_root(paired_nodes)

# Compute the Merkle roots for each sentence
merkle_roots = [compute_merkle_root(sentence.split()) for sentence in sentences]

# Create a higher-level Merkle tree that references lower-level Merkle roots
higher_level_data = merkle_roots

# Compute the Merkle root for the higher-level data
higher_level_merkle_root = compute_merkle_root(higher_level_data)

print("Higher-Level Merkle Root:", higher_level_merkle_root)
