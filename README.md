# 📈 Stocker

**Stocker** is a Streamlit-based web application that visualizes stock price trends and estimated market capitalization over time. It also features an integrated AI assistant powered by Cerebras, which provides comparisons and analysis between stocks.

> 🚀 Future versions will incorporate real-time analysis based on current financial trends and news.

---

## ⚙️ Setup Instructions

### 🐧 WSL (Windows Subsystem for Linux)

This setup assumes WSL is already installed.  
If not, follow the [official guide to install WSL](https://docs.microsoft.com/en-us/windows/wsl/install-win10).

#### Step 1: Enable WSL
1. Open the Start Menu and search for **"Turn Windows features on or off"**.
2. Check ✅ **Windows Subsystem for Linux**.
3. Click OK and restart your computer if prompted.

#### Step 2: Connect VS Code to WSL
1. Open Visual Studio Code.
2. Install the **Remote - WSL** extension.
3. Click the green button in the bottom-left corner.
4. Select **"Reopen in WSL"**.

---

### 🐍 Python Virtual Environment

From within your WSL terminal:

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/stocker.git
cd stocker

# 2. Create a virtual environment
python3 -m venv venv

# 3. Activate the virtual environment
source venv/bin/activate

# 4. Install dependencies
```

### 🔐 Environment Variables
Create a `.env` file in the root of the project:

```bash
pip install -r requirements.txt
```
Then add your Cerebras API key:
```bash
CEREBRAS_API_KEY=your_api_key_here
```
`.env` is already included in `.gitignore` and won’t be tracked when push.

### 🚀 Running the App
To launch the Streamlit dashboard:

```bash
streamlit run app.py
```

### 🧪 Running Tests
If you're using pytest, you can run:

```bash
pytest
```

### 📂 Project Structure
```bash
stocker/
├── app.py                 # Main Streamlit app
├── data_utils.py          # Stock data retrieval (yfinance)
├── cerebras_utils.py      # AI analysis using Cerebras API
├── plots.py               # Chart rendering with Plotly
├── requirements.txt       # Python dependencies
├── .env                   # API key (not tracked in Git)
├── .env.example           # Example env template
├── README.md              # Project documentation
└── .github/workflows/     # CI workflows (lint, test)

```

To be continued...




