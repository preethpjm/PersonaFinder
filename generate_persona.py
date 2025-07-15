import praw
import os
from dotenv import load_dotenv
from openai import OpenAI
from jinja2 import Template
import re

#credentials
load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

def query_llm(prompt):
    try:
        completion = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct",
            extra_headers={
                "HTTP-Referer": "https://github.com/your-repo",
                "X-Title": "PersonaFinderApp"
            },
            messages=[
                {"role": "system", "content": "You are an expert persona analyst."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2048,
            temperature=0.7
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"[Error querying LLM: {str(e)}]"

def parse_llm_response(response_text):
    def extract_section(header):
        pattern = rf"\*\*{re.escape(header)}:\*\*\s*(.*?)(?=\n\*\*|$)"
        match = re.search(pattern, response_text, re.DOTALL)
        return match.group(1).strip() if match else ""

    def extract_bullet_list(section_text):
        lines = section_text.splitlines()
        return [line.strip("•- ").strip() for line in lines if line.strip()]

    def extract_key_value_pairs(section_text):
        items = []
        for line in section_text.splitlines():
            line = line.strip("•- ").strip()
            if "(" in line and ")" in line:
                parts = line.rsplit("(", 1)
                items.append((parts[0].strip(), parts[1].strip(")")))
            else:
                items.append((line, ""))
        return items

    parsed = {}

    parsed["motivations"] = extract_key_value_pairs(extract_section("Motivations"))
    parsed["frustrations"] = extract_key_value_pairs(extract_section("Frustrations"))
    parsed["behaviors"] = extract_key_value_pairs(extract_section("Behavioral habits"))
    parsed["goals"] = extract_bullet_list(extract_section("Goals and needs"))
    parsed["quote"] = extract_section("Short quote").strip('"')

    # Personality example: "52% Introverted, 25% Intuitive, 90% Feeling, 65% Perceiving"
    personality_line = extract_section("Personality")
    parsed["personality_bars"] = generate_personality_bars(personality_line)
    parsed["age"] = extract_section("Age")
    parsed["occupation"] = extract_section("Occupation")
    parsed["status"] = extract_section("Status")
    parsed["location"] = extract_section("Location")
    parsed["archetype"] = extract_section("Archetype")

    return parsed

def generate_personality_bars(personality_text):
    traits = personality_text.split(",")
    scores = {}
    for trait in traits:
        match = re.match(r"(\d+)%\s+(\w+)", trait.strip())
        if match:
            percent = int(match.group(1))
            label = match.group(2).capitalize()
            scores[label] = percent

    def bar(left, right):
        left_score = scores.get(left.capitalize(), 0)
        bar_length = 20
        left_len = round(left_score / 100 * bar_length)
        right_len = bar_length - left_len
        return f"{left.upper():<11} [" + "■" * left_len + "-" * right_len + f"] {right.upper()}"

    return [
        bar("Introverted", "Extroverted"),
        bar("Intuitive", "Sensing"),
        bar("Feeling", "Thinking"),
        bar("Perceiving", "Judging"),
    ]



def build_persona(username):
    redditor = reddit.redditor(username)
    posts = []
    comments = []
    try:
        posts = [sub.title + " " + sub.selftext for sub in redditor.submissions.new(limit=20)]
        comments = [c.body for c in redditor.comments.new(limit=50)]
    except Exception as e:
        print(f"Error accessing user data for {username}: {e}")
        return

    all_text = "\n".join(posts + comments)
    if not all_text.strip():
        print(f"No data found for user '{username}'. Cannot build persona.")
        return

    prompt = f"""
Given the following Reddit posts and comments from a user, infer:

- Motivations
- Frustrations
- Behavioral habits
- Personality traits (Analyze the personality based on the following text.
For each MBTI dimension show the dominant side of each of the 4 pairs, along with how strongly the person leans toward that side.
Format the output like this (example values):
52% Introverted, 25% Intuitive, 90% Feeling, 65% Perceiving
(Note: A lower percentage in a trait implies the person leans toward the opposite. For example, 25% Intuitive = 75% Sensing.)
- Goals and needs
- Age (just a number or range not the resoning for it, example: 18 or 20s)
- Occupation
- Marital Status (Come to a conclusion be it : Single/ Married/ Unknown. one of the three)
- Location (if implied, mention only one)
- Archetype (based on MBTI or tone. just the Archetype, ommit the reasoning. example: Explorer)
- Generate a short quote that best represents this user (less than 140 characters and just the quote)

Text:
{all_text}

Respond clearly under each heading using bullet points. Use exactly these headings in bold:
**Motivations:**
**Frustrations:**
**Behavioral habits:**
**Personality:**
**Goals and needs:**
**Age:**
**Occupation:**
**Status:**
**Location:**
**Archetype:**
**Short quote:**

Each section must be present, even if minimal data exists. Do not skip or rename any heading. Do not include markdown bullets or formatting in the values.
"""

    llm_response = query_llm(prompt)
#    print("\n--- LLM Raw Response ---")
#    print(llm_response)
#    print("------------------------\n")

    parsed_data = parse_llm_response(llm_response)
    print(parsed_data)

# Add remaining fields
    parsed_data.update({
        "name": username,
        "status": "Unknown",  # or logic if available
    })

    template_path = os.getenv("TEMPLATE_PATH", "templates/persona_template.txt")
    with open(template_path, encoding="utf-8") as f:
         template = Template(f.read())

    rendered = template.render(**parsed_data)
    # Create 'personas' directory if it doesn't exist
    os.makedirs("personas", exist_ok=True)
    # Save the rendered persona to a text file
    with open(f"personas/{username}_persona.txt", "w", encoding="utf-8") as f:
        f.write(rendered)

if __name__ == "__main__":
    profile_url = input("Enter Reddit profile URL (e.g., https://www.reddit.com/user/kojied/): ").strip()
    if not profile_url.startswith("https://www.reddit.com/user/"):
        print("Invalid URL. Please enter a valid Reddit user profile link.")
    else:
        username = profile_url.rstrip("/").split("/user/")[-1].split("/")[0]
        build_persona(username)
