from collections import defaultdict, Counter
import random

sample_text = """
The quick brown fox jumps over the lazy dog.
The dog barked at the fox. The fox ran away quickly.
A quick brown dog outpaced a lazy fox.
The fox and the dog became friends in the end.
The dog and the fox lived happily ever after.
Artificial intelligence is changing the world rapidly.
Machine learning helps computers learn from experience.
"""

def tokenize(text):
    return text.lower().split()

tokens = tokenize(sample_text)
print(f"Total tokens: {len(tokens)}")

def build_chain(tokens, order=2):
    chain = defaultdict(list)
    for i in range(len(tokens) - order):
        key = tuple(tokens[i:i+order])
        chain[key].append(tokens[i+order])
    return chain

ORDER = 2
chain = build_chain(tokens, ORDER)
print(f"Unique keys: {len(chain)}")

def show_probabilities(phrase):
    key = tuple(phrase.lower().split()[:ORDER])
    if key not in chain:
        print(f"  '{phrase}' not found.\n")
        return
    counts = Counter(chain[key])
    total = sum(counts.values())
    print(f"\nAfter '{' '.join(key)}':")
    for word, count in counts.most_common():
        pct = count / total * 100
        bar = "█" * int(pct / 5)
        print(f"  '{word}' → {pct:.1f}%  {bar}")

print("\n=== PROBABILITY TABLE ===")
show_probabilities("the fox")
show_probabilities("the dog")

def generate_text(seed=None, num_words=30):
    if seed:
        start = tuple(seed.lower().split()[:ORDER])
        if start not in chain:
            start = random.choice(list(chain.keys()))
    else:
        start = random.choice(list(chain.keys()))
    result = list(start)
    for _ in range(num_words - ORDER):
        key = tuple(result[-ORDER:])
        if key not in chain:
            break
        result.append(random.choice(chain[key]))
    return " ".join(result)

print("\n=== GENERATED TEXT ===")
print("\nSeed 'the fox':")
print(generate_text(seed="the fox", num_words=25))

print("\nRandom start:")
print(generate_text(num_words=25))

print("\n=== COMPARING ORDERS ===")
for order in [1, 2, 3]:
    c = build_chain(tokens, order)
    start = random.choice(list(c.keys()))
    result = list(start)
    for _ in range(20 - order):
        key = tuple(result[-order:])
        if key not in c:
            break
        result.append(random.choice(c[key]))
    print(f"\nOrder {order}: {' '.join(result)}")