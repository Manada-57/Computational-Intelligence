import csv
import math
from collections import Counter

# ---------- READ DATA ----------
def read_dataset(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        # Sniff the delimiter (handles commas, tabs, semicolons)
        content = file.read(2048)
        dialect = csv.Sniffer().sniff(content)
        file.seek(0)

        reader = csv.reader(file, dialect)
        raw_data = [row for row in reader if row] # skip empty lines

    # Clean whitespace from every cell to ensure consistency
    data = [[cell.strip() for cell in row] for row in raw_data]

    attributes = data[0][:-1]
    dataset = data[1:]
    return attributes, dataset

# ---------- ENTROPY ----------
def entropy(data, label="S"):
    if not data:
        return 0
    labels = [row[-1] for row in data]
    total = len(labels)
    counts = Counter(labels)

    print(f"\nEntropy Calculation for {label}")
    print("Class Counts:", dict(counts))

    ent = 0
    for cls in counts:
        p = counts[cls] / total
        print(f"P({cls}) = {counts[cls]}/{total} = {p:.4f}")
        ent -= p * math.log2(p) if p > 0 else 0

    print(f"Entropy({label}) = {ent:.4f}")
    return ent

# ---------- SPLIT ----------
def split_data(data, attr_index, value):
    return [row for row in data if row[attr_index] == value]

# ---------- INFORMATION GAIN ----------
def information_gain(data, attr_index, attr_name):
    print("\n" + "-"*40)
    print(f"Calculating Information Gain for {attr_name}")

    # 1. Total Entropy
    total_entropy = entropy(data, "S")

    # 2. Tabulate Class Splits
    values = sorted(list(set(row[attr_index] for row in data)))
    classes = sorted(list(set(row[-1] for row in data)))

    print(f"\nClass Split Table for {attr_name}:")
    header = f"{'Value':<15} | " + " | ".join([f"{c:<5}" for c in classes]) + " | Total"
    print(header)
    print("-" * len(header))

    for v in values:
        subset = split_data(data, attr_index, v)
        counts = Counter(row[-1] for row in subset)
        row_str = f"{v:<15} | " + " | ".join([f"{counts[c]:<5}" for c in classes])
        print(f"{row_str} | {len(subset)}")

    # 3. Weighted Entropy Calculations
    weighted_entropy = 0
    for v in values:
        subset = split_data(data, attr_index, v)
        weight = len(subset) / len(data)

        sub_ent = entropy(subset, f"{attr_name}={v}")

        print(f"Weight = {len(subset)}/{len(data)} = {weight:.4f}")
        print(f"Weighted Entropy = {weight:.4f} * {sub_ent:.4f} = {weight*sub_ent:.4f}")

        weighted_entropy += weight * sub_ent

    print(f"\nTotal Weighted Entropy({attr_name}) = {weighted_entropy:.4f}")
    ig = total_entropy - weighted_entropy
    print(f"Information Gain({attr_name}) = {total_entropy:.4f} - {weighted_entropy:.4f}")
    print(f"Information Gain({attr_name}) = {ig:.4f}")

    return ig

# ---------- FIND ROOT ----------
def find_root(data, attributes):
    gains = {}
    print("\n" + "="*50)
    print("STARTING FEATURE EVALUATION")
    for i, attr in enumerate(attributes):
        ig = information_gain(data, i, attr)
        gains[attr] = ig

    print("\n" + "="*50)
    print("FINAL INFORMATION GAINS SUMMARY")
    for attr in gains:
        print(f"{attr:<20} : {round(gains[attr], 4)}")

    return max(gains, key=gains.get)

# ---------- MAJORITY CLASS ----------
def majority_class(data):
    labels = [row[-1] for row in data]
    return Counter(labels).most_common(1)[0][0]


# ---------- BUILD TREE (ID3) ----------
def build_tree(data, attributes):

    labels = [row[-1] for row in data]

# CASE 1: All same class
    if labels.count(labels[0]) == len(labels):
        return labels[0]

# CASE 2: No attributes left
    if len(attributes) == 0:
        return majority_class(data)

# Compute information gain for all attributes
    gains = {}
    for i, attr in enumerate(attributes):
        gains[attr] = information_gain(data, i, attr)

# Choose best attribute
    best_attr = max(gains, key=gains.get)
    best_index = attributes.index(best_attr)

    tree = {best_attr: {}}

# Get unique values
    values = set(row[best_index] for row in data)

    for v in values:
        subset = split_data(data, best_index, v)

        if not subset:
            tree[best_attr][v] = majority_class(data)
        else:
# Remove used attribute
            new_attributes = attributes[:best_index] + attributes[best_index+1:]

# Remove column from dataset
        new_subset = []
        for row in subset:
            new_row = row[:best_index] + row[best_index+1:]
            new_subset.append(new_row)

        subtree = build_tree(new_subset, new_attributes)
        tree[best_attr][v] = subtree

    return tree

# ---------- PRINT TREE ----------
def print_tree(tree, indent=""):
    if not isinstance(tree, dict):
        print(indent + "->", tree)
        return

    for attr in tree:
        for value in tree[attr]:
            print(indent + f"{attr} = {value}")
            print_tree(tree[attr][value], indent + " ")
# ---------- MAIN ----------
def main():
    try:
        filename = input("Enter file name (e.g., data.csv or data.txt): ").strip()
        attributes, data = read_dataset(filename)

        print(f"\nDataset loaded: {len(attributes)} attributes, {len(data)} rows.")
        print("Attributes found:", attributes)

        if not data:
            print("Error: The dataset contains no records.")
            return

        root = find_root(data, attributes)
        print("\n" + "!"*30)
        print("RESULT: BEST ROOT NODE =", root)
        print("!"*30)
        #res=build_tree(data,attributes)
        #print_tree(res)

    except FileNotFoundError:
        print("Error: File not found. Please check the filename.")
    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == "__main__":
    main()
