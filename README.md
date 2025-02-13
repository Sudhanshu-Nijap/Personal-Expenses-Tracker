# Personal Expense Tracker

A **Streamlit-based** web application that helps you track and manage your daily expenses efficiently. The app integrates with **Google Sheets** to store expense records, visualize expense trends, and provide insights through interactive charts.

---

## 🚀 Features

- 📌 **Add New Expenses** - Easily log your expenses with category selection and optional notes.
- 🗑 **Delete Expenses** - Remove unwanted expense records with a simple selection.
- 📊 **Expense Summary** - View expense trends using dynamic filtering (This Week, Month, Year, Custom Range).
- 📉 **Visual Analytics** - Interactive pie charts showing category-wise expense breakdown.
- 🛠 **Google Sheets Integration** - Securely store and manage expense records in Google Sheets.
- 🎨 **User-Friendly Interface** - Responsive, clean, and minimal design with Streamlit.

---

## 🛠 Tech Stack

- **Python** - Core programming language
- **Streamlit** - Web framework for UI
- **Google Sheets API** - Backend storage for expenses
- **OAuth2Client & gspread** - Authentication & communication with Google Sheets
- **Pandas** - Data processing and filtering
- **Plotly** - Interactive data visualizations

---

## 📂 Installation & Setup

### 1️⃣ Clone the Repository
```bash
 git clone https://github.com/Sudhanshu-Nijap/Personal-Expense-Tracker.git
 cd Personal-Expense-Tracker
```

### 2️⃣ Install Dependencies
```bash
pip install streamlit gspread oauth2client pandas plotly
```

### 3️⃣ Configure Google Sheets API
- Create a Google Cloud project and enable Google Sheets API.
- Generate service account credentials (`.json` keyfile) and place it in the project folder.
- Replace the `json_keyfile` path in `app.py` with your keyfile path.

### 4️⃣ Run the App
```bash
streamlit run app.py
```

---


## 🤝 Contributing

1. Fork the repository.
2. Create a new branch (`feature-new`).
3. Commit your changes (`git commit -m "Added new feature"`).
4. Push to your branch (`git push origin feature-new`).
5. Open a Pull Request.

---

## 📜 License
This project is licensed under the **MIT License**.

---

## 💡 Author
👨‍💻 Developed by **Sudhanshu Nijap** with ❤️

For any queries, feel free to reach out!

---

