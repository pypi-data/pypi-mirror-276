
# HammingEncoder

HammingEncoder is the source code for paper.

## Installation

You can install HammingEncoder from PyPI:

```bash
pip install HammingEncoder
```
## Usage

Here's how to use the HammingEncoder package:

### Importing the package

```python
from HammingEncoder import HammingEncoder

# Example data
sequences = [
    ['0', '1', '2', '3', '4', '5', '1', '6', '5', '1', '7', '4', '5', '8', '5'], 
    ['0', '1', '4', '2', '3', '4', '5', '8', '5', '1', '7', '4', '5', '1', '5', '1', '5', '6', '5'],
    ['0', '1', '2', '3', '4', '5', '8', '5', '1', '5', '7', '5', '1', '8', '5', '1', '5', '1', '5', '1', '6', '4', '5'], 
    ['0', '4', '2', '3', '5', '7', '5', '1', '5', '4', '6', '5', '1', '5', '4', '5'],
    ]
labels = [0, 1, 0, 1]

# Initialize the encoder
encoder = HammingEncoder(sequences, labels, gap_constrain=5, label_number=2, Preset_set_pattern_num=1024, device='cpu')

# Fit the model
encoder.fit(n_epochs=100, patience=2, batch_size=64)

# Transform the data
encoded_data = encoder.transform(sequences)

print("Encoded data:", encoded_data)

# test
acc = encoder.test(sequences, labels)
print("Accuracy:", acc)