# Product Akinator

100 everyday products with 25 binary attributes. Local dataset validation before Kaggle publication.

## Run tests (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -q
```

The uniqueness test currently fails because three product pairs share identical binary patterns. Fix these by improving the attribute schema or labels, not by changing arbitrary values just to pass tests.
