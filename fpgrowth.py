class FPNode:
    def __init__(self, item, count, parent):
        self.item = item
        self.count = count
        self.parent = parent
        self.children = {}
        self.link = None

def update_header(node, target_node):
    while node.link is not None:
        node = node.link
    node.link = target_node

def update_tree(items, node, header_table, count):
    if items[0] in node.children:
        node.children[items[0]].count += count
    else:
        new_node = FPNode(items[0], count, node)
        node.children[items[0]] = new_node
        if header_table[items[0]][1] is None:
            header_table[items[0]][1] = new_node
        else:
            update_header(header_table[items[0]][1], new_node)
    if len(items) > 1:
        update_tree(items[1:], node.children[items[0]], header_table, count)

def create_tree(transactions, min_support):
    # First scan: count item frequency
    freq = {}
    for transaction in transactions:
        for item in transaction:
            freq[item] = freq.get(item, 0) + 1
    # Remove infrequent items
    freq = {k: v for k, v in freq.items() if v >= min_support}
    if len(freq) == 0:
        return None, None
    header_table = {k: [v, None] for k, v in freq.items()}
    
    # Create the FP-tree
    root = FPNode(None, 1, None)
    for transaction in transactions:
        transaction_items = [item for item in transaction if item in freq]
        transaction_items.sort(key=lambda x: freq[x], reverse=True)
        if len(transaction_items) > 0:
            update_tree(transaction_items, root, header_table, 1)
    return root, header_table

def ascend_tree(node):
    path = []
    while node.parent is not None and node.parent.item is not None:
        node = node.parent
        path.append(node.item)
    return path

def find_prefix_path(base_item, node):
    cond_patterns = {}
    while node is not None:
        path = ascend_tree(node)
        if len(path) > 0:
            cond_patterns[frozenset(path)] = node.count
        node = node.link
    return cond_patterns

def mine_tree(header_table, min_support, prefix, freq_itemsets):
    sorted_items = [v[0] for v in sorted(header_table.items(), key=lambda x: x[1][0])]
    for base_item in sorted_items:
        new_freq_set = prefix.copy()
        new_freq_set.add(base_item)
        freq_itemsets.append((new_freq_set, header_table[base_item][0]))
        cond_patterns = find_prefix_path(base_item, header_table[base_item][1])
        cond_tree, cond_header = create_tree(
            [list(pattern) for pattern, count in cond_patterns.items() for _ in range(count)],
            min_support
        )
        if cond_header is not None:
            mine_tree(cond_header, min_support, new_freq_set, freq_itemsets)
