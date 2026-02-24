# CourierOptimizer

NordicExpress courier optimizer — reads deliveries from a CSV, validates them, and produces an optimized delivery route based on your chosen criterion.

---

## Requirements

- Python 3.10+
- Dependencies installed in a virtual environment (`.venv`)

Install dependencies:

```bash
pip install python-dotenv
```

---

## How to start

1. **Open a terminal and navigate into the package folder:**

```bash
cd courrier_optimizer
```

2. **Set the Python path so imports resolve correctly (run once per terminal session):**

```powershell
# Windows PowerShell
$env:PYTHONPATH = "C:\path\to\CourierOptimizer\courrier_optimizer"
```

3. **Run the program:**

```powershell
& "..\venv\Scripts\python.exe" "__main__.py"
```

Or if your virtual environment is named `.venv`:

```powershell
& "..\.venv\Scripts\python.exe" "__main__.py"
```

---

## What the program asks you

The CLI will guide you through 5 steps:

| Step | What to enter |
|------|---------------|
| Name | Your name (or press Enter for default) |
| Transport mode | `1` Car, `2` Bicycle, `3` Walking |
| Objective | `1` Fastest, `2` Cheapest, `3` Lowest CO2 |
| Depot coordinates | `lat,lon` — e.g. `59.919623,10.735394` (or Enter for default) |
| Input CSV path | Path to your CSV file (or Enter to use `Input/input.csv`) |

---

## Input CSV format

The input file must have these 5 columns, separated by `;` or `,`:

```
customer;latitude;longitude;priority;weight_kg
Bilal;59.91;10.73;High;2.0
Anna;59.92;10.74;Medium;1.5
Erik;59.90;10.72;Low;3.0
```

**Validation rules:**
- `priority` must be exactly `High`, `Medium`, or `Low`
- `latitude` must be a float between -90 and 90
- `longitude` must be a float between -180 and 180
- `weight_kg` must be a number ≥ 0
- `customer` must contain only letters (e.g. `Anna` or `Anna Hansen`)

Invalid rows are skipped with a warning and written to `Output/rejected.csv`.

---

## Output files

| File | Contents |
|------|----------|
| `Output/route.csv` | Ordered stops with distance, ETA, cost, and CO2 per leg |
| `Output/rejected.csv` | Rows that failed validation |
| `Output/run.log` | Full log with parameters, warnings, and timing |
