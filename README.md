# Project Overview

This repository contains the core scripts for your application, including agent logic, Gradio interface, judging functions, and utilities. Sensitive information such as API keys should **not** be included in the repository.

---

## 📁 File Structure

```
├── chat_agent.py
├── gradio_main.py
├── judge.py
├── utils.py
├── api_keys.py   
└── README.md
```

---

## 🔒 Excluding `api_keys.py`

Make sure your API key file is never committed to GitHub. Add the following to your `.gitignore`:

```
api_keys.py
```

If you want to provide an example template for contributors, you can create:

```
api_keys.example.py
```

And document the required variables inside it.

---

## 🚀 How to Run the Project

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Create your `api_keys.py` file based on your own environment (not tracked by git).

3. Launch the application (example):

   ```bash
   python gradio_main.py
   ```

---

## 🛠 Requirements

Add your Python module dependencies into a `requirements.txt` file to help others install necessary packages.

---

## 🤝 Contributing

Feel free to fork the project and submit pull requests. Do not include any sensitive information in commits.

---

## 📄 License

Add a license of your choice here (MIT, Apache 2.0, etc.).
