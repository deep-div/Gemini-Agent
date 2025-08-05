---

```markdown
# Gemini-Agent

A modular AI agent framework powered by Gemini, designed to enable tool-based interactions and intelligent task execution using Streamlit for a smooth web interface.

## 📁 Project Structure

```

Gemini-Agent/
├── .streamlit/                # Streamlit configuration files
├── src/
│   ├── **pycache**/           # Python cache
│   ├── images/                # Image assets used in the app
│   ├── gemini\_history.py      # Handles history and memory
│   ├── gemini\_llm.py          # Gemini LLM API integration
│   ├── gemini\_tool\_selector.py # Tool selection logic
│   ├── gemini\_tools\_defination.py # Tool definitions
│   ├── gemini\_tools.py        # Tool execution logic
│   ├── streamlit\_app.py       # Main Streamlit app
│   ├── system\_prompt.py       # System prompt setup
│   └── utils.py               # Utility functions
├── .env                       # Environment variables
├── .gitattributes
├── .gitignore
├── Dockerfile
├── README.md
└── requirements.txt           # Python dependencies

````

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Gemini-Agent.git
cd Gemini-Agent
````

### 2. Install Dependencies

Make sure you have Python 3.10+ installed.

```bash
pip install -r requirements.txt
```

### 3. Activate Virtual Environment (if not already)

Ensure your virtual environment is activated. If you're using `.venv`, run:

* On Windows:

  ```bash
  .venv\Scripts\activate
  ```

* On macOS/Linux:

  ```bash
  source .venv/bin/activate
  ```

### 4. Run the App

Navigate to the `src` folder and run:

```bash
cd src
py -m streamlit run streamlit_app.py
```

> If you're using Linux/macOS:

```bash
python3 -m streamlit run streamlit_app.py
```

## 🛠 Features

* Modular tool definitions and selection
* Gemini LLM integration
* Session history handling
* Customizable system prompts
* Visual interface with Streamlit

## 📄 License

This project is licensed under the MIT License.

---

Happy Building! ✨

```

---

```
