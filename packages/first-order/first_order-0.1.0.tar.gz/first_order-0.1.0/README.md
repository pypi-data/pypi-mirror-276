# first-order

Pure Python first-order logic evaluator

```python
from first_order import ForAll, Term

w = Term("w")
x = Term("x")
y = Term("y")

s1 = x & y
s2 = w | ~x
s3 = s1 >> s2

print(ForAll(x, s3))
# output: (∀ x: ((x & y) >> (w | ~x)))

print(s3 @ {"x": True, "y": True, "w": False})
# output: False
```

## Installation

From pypi:

```sh
pip install first-order
```

Latest commit:

```sh
pip install git+https://github.com/olivi-r/first-order.git#egg=first-order
```

## Syntax

This project uses simple constructs to abstract the creation of first-order logic sentences:

- `&` conjunction
- `|` disjunction
- `~` negation
- `>>` implication

Two special functions are required to create sentences with quantifiers:

- `Exists` existential quantifier
- `ForAll` universal quantifier

```python
from first_order import Exists, ForAll, Term

x = Term("x")
z = Term("z")

s_forall = ForAll(z, x | z)
s_exists = Exists(z, x | z)

print(s_forall @ {"x": False})
# output: False

print(s_exists @ {"x": False})
# output: True
```

## Interpretations

Interpretations can be applied to the sentence through the usage of the `@` operator (as seen in previous examples), this takes a mapping from the names of terms used in the sentence and their respective values.

Unbound terms result in an error being thrown.

```python
from first_order import Term

x = Term("x")
y = Term("y")

print((x | y) @ {"x": True})
# output:
# Traceback (most recent call last):
#     ...
# KeyError: 'y'
```

Terms attatched to quantifiers do not need to be in the interpretation (unless the same term name is used elsewhere)

```python
from first_order import Exists, Term

x = Term("x")
y = Term("y")

print(Exists(y, x | y) @ {"x": True})
# output: True
```
