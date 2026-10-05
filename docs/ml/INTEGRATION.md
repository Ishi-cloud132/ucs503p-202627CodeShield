# CodeShield ML integration

This is an optional add-on. Existing backend and frontend routes remain
unchanged unless the new router is registered explicitly.

## Install and train

From `code/backend`, install the additional dependencies and generate the
baseline model:

```sh
pip install -r requirements-ml.txt
python ../../scripts/train_codeshield_ml.py
```

The default training set is a small bootstrap sample for demonstrating the
pipeline. For meaningful evaluation, provide a reviewed CSV with `code` and
`label` columns (`safe` or `vulnerable`):

```sh
python ../../scripts/train_codeshield_ml.py --data data/training.csv
```

The model and evaluation metrics are written under `code/backend/models/`.
Do not treat bootstrap metrics as evidence of production accuracy.

## Enable the route

In the FastAPI setup, register the router explicitly:

```python
from codeshield_ml.integration import register_codeshield_ml

register_codeshield_ml(app)
```

This exposes `POST /ml/scan` with a JSON body such as `{"code": "..."}`. It
returns existing-style static findings plus an optional `ml_assessment`. If
the model artifact is absent, the route continues with static analysis only.

The frontend helper is available at `frontend/src/services/codeshieldApi.js`;
it targets `http://127.0.0.1:8000/ml/scan` by default.