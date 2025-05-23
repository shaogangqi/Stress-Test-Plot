# Dynamic Plot Stress Test App
This project consists of a **Flask web application** (`app.py`) that dynamically generates complex matplotlib plots based on an integer input and a **Playwright test script** (`plot.spec.js`) that performs automated stress testing of the `/plot/<n>` endpoint by requesting a large number of random plots and validating the results.

---
## Project Structure
├── app.py # Flask backend serving dynamic     matplotlib plots
├── plot.spec.js # Playwright script for stress     testing the API
├── failed_plots/ # Folder to store plots that    failed validation
└── all_plots/ # (optional) Folder where all tested plots are saved
---

## Features

### `app.py` (Flask App)

- **Endpoint**: `/plot/<int:n>`
- **Input**: An integer `n` (1–99999)
- **Output**: A PNG image containing a 3x3 grid of varied and computationally challenging subplots
- **Purpose**: Simulate edge cases and stress conditions for plotting systems, including:
  - Noisy sine waves
  - Zipf bar distributions
  - High-density scatter plots
  - Random walks with outliers
  - Heatmaps with possible NaNs
  - Discontinuous functions (e.g., `tan(x)`)
  - Text-heavy subplots
  - Polar plots
  - Conditional failures (empty plot every 29th seed)

---

### `plot.spec.js` (Playwright Test)

- **Purpose**: Automatically test 1000 random values of `n` from 1–99999 (currently set to 10 for example)
- **Behavior**:
  - Requests each `/plot/<n>` endpoint
  - Verifies:
    - HTTP status is 200
    - Content-Type is `image/png`
    - Image data is not suspiciously small (< 1000 bytes)
  - Saves:
    - All responses to `all_plots/`
    - Failed cases to `failed_plots/`
  - Logs pass/fail results to console
  - Asserts all tests must pass

---

## 🛠️ Setup Instructions

### 1. Install Python Dependencies

Make sure you have Python 3 installed. Then install the required packages:

```
pip install flask matplotlib numpy

```

### 2. Run the Flask App

Start the server with:

```
python app.py

```
The app will be available at: http://127.0.0.1:5000/

You can manually test it by visiting:
```
http://127.0.0.1:5000/plot/123

```
### 3. Run the Playwright Test
#### 3.1 Install Playwright and Dependencies
If you haven’t already, install Playwright and Node modules:
```
npm init -y
npm install @playwright/test
npx playwright install

```
#### 3.2 Run the Test Script
```
npx playwright test plot.spec.js

```
Make sure app.py is running before executing the test.

##  Expected Results
Console Output: Logs ✅ Passed /plot/<n> or ❌ Failed at /plot/<n> with reason

Images:

All tested plots are saved in all_plots/

Any failed plots are saved in failed_plots/ for inspection

Final Assertion: If any failures occur, test fails with a detailed list of failed cases

### 2.1 Notes
You can adjust the number of test cases in plot.spec.js by changing:
```
const testCases = getRandomUniqueInts(10, 1, 99999); // Increase 10 to 1000 for full run

```
Be cautious when running thousands of tests—it may consume a lot of memory or CPU due to Matplotlib rendering.

### 2.2 Example Output
```
✅ Passed /plot/34812
✅ Passed /plot/49321
❌ Failed at /plot/29000 — saved to failed_plots/plot_29000.png
...
Failures detected: [
  { n: 29000, status: 200, contentType: 'image/png', length: 932 }
]

```