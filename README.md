
# 🧠 Persona Finder

> A command-line tool that generates a psychological and behavioral persona of any Reddit user using OpenRouter LLMs and Reddit API.

👤 Built by **Preeth Jwo Martin**

---

## 🔍 What does it do?

Persona Finder analyzes a Reddit user's activity (posts + comments) and uses an AI model to generate a detailed persona report. This includes:

- Motivations
- Frustrations
- Behavioral habits
- MBTI-style personality breakdown
- Age, occupation, marital status, and more
- Archetype and a signature quote

The output is a beautifully formatted `.txt` file saved in the `/personas` folder.

---

## 📁 Folder Structure

```
project-root/
│
├── generate_persona.py        # Main CLI tool
├── .env                       # Store your API credentials
├── templates/
│   └── persona_template.txt   # The output template
├── personas/                  # Folder where persona files are saved
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/persona-finder.git
cd persona-finder
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your API keys

Create a `.env` file in the root directory (or update the existing one):

```env
REDDIT_CLIENT_ID=enter_here
REDDIT_CLIENT_SECRET=enter_here
REDDIT_USERNAME=enter_here
REDDIT_PASSWORD=enter_here
REDDIT_USER_AGENT=PersonaFinder by /u/your_reddit_username

OPENROUTER_API_KEY=enter_here
```

> 🔒 `.env` file is **private** and **never** to be **committed** to version control.


---

## 🚀 Try it Out (No Installation)

👉 [**Launch the Streamlit App**](https://personafinder.streamlit.app/)

> *(The link will open a web app version of this project — no setup, installation, or `.env` configuration needed!)*

---

## ▶️ Running the Tool

Run the script directly:

```bash
python generate_persona.py
```

Then, enter the Reddit profile URL when prompted, for example:

```
https://www.reddit.com/user/kojied/
```

This will generate a file like:

```
personas/kojied_persona.txt
```

This includes a detailed persona analysis in styled text.

---

## Output Preview

```
 ____                                   _____ _           _           
|  _ \ ___ _ __ ___  ___  _ __   __ _  |  ___(_)_ __   __| | ___ _ __ 
| |_) / _ \ '__/ __|/ _ \| '_ \ / _` | | |_  | | '_ \ / _` |/ _ \ '__|
|  __/  __/ |  \__ \ (_) | | | | (_| | |  _| | | | | | (_| |  __/ |   
|_|   \___|_|  |___/\___/|_| |_|\__,_| |_|   |_|_| |_|\__,_|\___|_|                                                     

                                   Persona Finder by Preeth Jwo Martin

==============================================================================================

NAME: kojied

----------------------------------------------------------------------------------------------
"New York City is equally adventurous to each, so who am I to judge how others enjoy this adventurous city."
----------------------------------------------------------------------------------------------

AGE: 30s
             
OCCUPATION: iOS developer

LOCATION: New York City

STATUS: Unknown

ARCHETYPE: Explorer (open to new experiences, passionate about innovation, and interested in understanding the world)
______________________________________________________________________________________________

PERSONALITY

INTROVERTED [■■■■■■■■------------] EXTROVERTED

INTUITIVE   [■■■■■■■■■-----------] SENSING

FEELING     [■■■■■■■■■■■■■■■■■---] THINKING

PERCEIVING  [■■■■■■■■■■■■■■------] JUDGING

______________________________________________________________________________________________

MOTIVATIONS

- Passionate about technology and innovation, particularly in the fields of AR, VR, and spatial computing.

- Interested in sustainable living and reducing individual impact on the environment.

- Shares ideas and opinions about various topics, from politics to pop culture.

______________________________________________________________________________________________

FRUSTRATIONS

- Feels violated by a change in environment and the behavior of younger individuals in a familiar social setting.

- Frustration with the current state of NFTs and their potential.

- Critical of companies and their treatment of ESG ratings and consumer activism.

______________________________________________________________________________________________

BEHAVIOUR & HABITS

- Frequents a local bar.

- Enjoys trying new foods and restaurants.

- Shares ideas and opinions online, often engaging with others on Reddit.

______________________________________________________________________________________________

GOALS & NEEDS

- To build a better life in the US, possibly through technology and innovation.

- To reduce individual impact on the environment.

- To engage in meaningful discussions and share ideas.


==============================================================================================```

---
```
## 🧠Powered By

- [OpenRouter.ai](https://openrouter.ai) — LLM API Gateway
- [PRAW](https://praw.readthedocs.io) — Python Reddit API Wrapper
- [Jinja2](https://jinja.palletsprojects.com) — Template Engine
- [Python Dotenv](https://pypi.org/project/python-dotenv/) — Secret Management

---
