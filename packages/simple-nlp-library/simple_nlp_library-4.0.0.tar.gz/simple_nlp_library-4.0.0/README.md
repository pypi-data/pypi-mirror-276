# simple_nlp_library
Simple NLP library

## usage

### installation
```
python3 -m pip install --upgrade simple-nlp-library
```

### api

#### semantic_tokens

```python
stop_words = preprocessing.stop_words()
preprocessing.semantic_tokens(stop_words, "The quick brown fox jumps over the lazy dog")
```

#### cosine_similarity
```python
metrics.cosine_similarity([1.0, 1.0, 1.0], [4.0, 4.0, 4.0])
```

#### inserting_distance
```python
metrics.inserting_distance("simple", "simpler")
```

#### inserting_similarity
```python
metrics.inserting_similarity("simple", "simpler")
```

#### jaccard_similarity
```python
metrics.jaccard_similarity([1, 2, 3], [1, 2, 3, 4])
```

#### embeddings
```python
vectors = embeddings.vectors()
vector = vectors["facebook"]
```

#### sentence similarity
```python
vectors = embeddings.vectors()
stop_words = preprocessing.stop_words()
metrics.cosine_similarity(
    embeddings.tokens_vector(vectors, preprocessing.semantic_tokens(stop_words, "the slow brown bear jumped over the lazy dog")),
    embeddings.tokens_vector(vectors, preprocessing.semantic_tokens(stop_words, "the quick red fox jumped over the lazy cat")),
)
```
