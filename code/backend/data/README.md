# Training data

No production dataset is included. The training script uses a small, clearly
limited bootstrap set unless a CSV file is supplied with `--data`.

For real model training, prepare a CSV with these columns:

| Column | Description |
| --- | --- |
| `code` | Source-code sample to classify |
| `label` | `safe` or `vulnerable` |

Use independently reviewed, licensed examples and keep the classes balanced.
Do not put secrets, personal data, or proprietary source code in this directory.