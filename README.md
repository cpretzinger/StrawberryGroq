# 🍓 Strawberry Groq - Retro Style

A Streamlit-powered chat interface showcasing Groq's language models with a classic Apple ][e terminal aesthetic.

![Retro Interface](https://raw.githubusercontent.com/yourusername/StrawberryGroq/main/screenshot.png)

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- A Groq API key (get it from [console.groq.com](https://console.groq.com))
- Git

### Step-by-Step Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/StrawberryGroq.git
   cd StrawberryGroq
   ```

2. **Set Up Virtual Environment**
   ```bash
   # For macOS/Linux
   python3 -m venv venv
   source venv/bin/activate

   # For Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create Configuration Files**
   ```bash
   # Create necessary directories and files
   mkdir .streamlit
   touch .env
   touch .gitignore
   touch .streamlit/config.toml
   touch .streamlit/style.css
   ```

5. **Set Up Environment Variables**
   ```bash
   # Create and edit .env file
   echo "GROQ_API_KEY=your_groq_api_key" > .env
   ```
   Replace `your_groq_api_key` with your actual Groq API key.

6. **Run the Application**
   ```bash
   streamlit run main.py
   ```
   Visit `http://localhost:8501` in your browser.

## 📁 Project Structure
```
.
├── README.md
├── main.py                # Main application file
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables
├── .gitignore           # Git ignore rules
└── .streamlit/          # Streamlit configuration
    ├── config.toml      # Streamlit settings
    └── style.css        # Custom CSS for retro theme
```

## 🎨 Custom Theme
This project includes a custom Apple ][e terminal theme! The retro styling includes:
- Classic green phosphor color
- CRT screen effects (flicker and scanlines)
- Authentic terminal font
- Retro UI elements

## 🔧 Configuration

### Environment Variables (.env)
Create a `.env` file in the project root:
```bash
GROQ_API_KEY=your_groq_api_key
STREAMLIT_THEME_BASE=dark
STREAMLIT_THEME_PRIMARY_COLOR=#33FF33
STREAMLIT_THEME_BACKGROUND_COLOR=#000000
STREAMLIT_THEME_TEXT_COLOR=#33FF33
STREAMLIT_THEME_FONT=monospace
```

### Git Ignore (.gitignore)
Essential files to ignore for Python projects:
```
# Virtual Environment
venv/
env/
.env

# Python
__pycache__/
*.py[cod]
*.so

# macOS
.DS_Store

# VS Code
.vscode/

# Other
*.log
```

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments
- Inspired by the classic Apple ][e terminal
- Powered by Groq's language models
- Built with Streamlit

## ❓ Troubleshooting

### Common Issues

1. **"ModuleNotFoundError" when running the app**
   ```bash
   # Make sure you've activated the virtual environment
   source venv/bin/activate  # macOS/Linux
   .\venv\Scripts\activate   # Windows
   
   # Reinstall dependencies
   pip install -r requirements.txt
   ```

2. **"No module named 'dotenv'"**
   ```bash
   pip install python-dotenv
   ```

3. **"Could not find your Groq API key"**
   - Check that your `.env` file exists
   - Verify the API key is correct
   - Make sure the key starts with "gsk_"

4. **Theme not working**
   - Verify `.streamlit/style.css` exists
   - Check file permissions
   - Restart the Streamlit server

### Still Having Issues?
Create an issue in the GitHub repository with:
- Your operating system
- Python version (`python --version`)
- Error message
- Steps to reproduce

## 📱 Contact
- Create an issue on GitHub
- CP 2024 Dev in Dev :) Have fun and thank you to J. Gravelle