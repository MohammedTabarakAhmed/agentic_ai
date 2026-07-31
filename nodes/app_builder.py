"""
state (notebook)
        ↓
app_builder picks up notebook
        ↓
reads → user_goal + search_results + retrieved_docs
        ↓
builds prompt with all 3
        ↓
sends to LLM (llama-3.3-70b via Groq)
    - SystemMessage → "you are a senior SWE"
    - HumanMessage  → prompt with all context
        ↓
LLM generates all app files as JSON
{
    "app.py":      "code...",
    "index.html":  "code...",
    "styles.css":  "code..."
}
        ↓
json.loads() converts string → python dict
        ↓
writes → generated_files back to state
        ↓
puts notebook down → returns to supervisor
        ↓
supervisor sees generated_files is filled → replies "done"
        ↓
END
"""

from state import AgentState
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
import json
import re
from dotenv import load_dotenv
load_dotenv()

llm=ChatGroq(model="llama-3.3-70b-versatile")


def build_basic_ui_files(user_goal: str) -> dict[str, str]:
    goal_text = (user_goal or "a beautiful web experience").strip()
    words = re.sub(r"[^a-z0-9]+", " ", goal_text.lower()).split()
    if words:
        brand_words = words[:3]
        brand_name = "".join(word.capitalize() for word in brand_words)
    else:
        brand_name = "NovaFind"

    if not brand_name:
        brand_name = "NovaFind"

    is_calculator = 'calculator' in goal_text.lower()

    if is_calculator:
        html = f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>{brand_name}</title>
  <link rel=\"stylesheet\" href=\"styles.css\" />
</head>
<body>
  <main class=\"calculator-shell\">
    <div class=\"calculator-card\">
      <h1>{brand_name}</h1>
      <div class=\"display\" id=\"display\">0</div>
      <div class=\"buttons\">
        <button class=\"btn\" data-value=\"7\">7</button>
        <button class=\"btn\" data-value=\"8\">8</button>
        <button class=\"btn\" data-value=\"9\">9</button>
        <button class=\"btn operator\" data-value=\"/\">/</button>
        <button class=\"btn\" data-value=\"4\">4</button>
        <button class=\"btn\" data-value=\"5\">5</button>
        <button class=\"btn\" data-value=\"6\">6</button>
        <button class=\"btn operator\" data-value=\"*\">*</button>
        <button class=\"btn\" data-value=\"1\">1</button>
        <button class=\"btn\" data-value=\"2\">2</button>
        <button class=\"btn\" data-value=\"3\">3</button>
        <button class=\"btn operator\" data-value=\"-\">-</button>
        <button class=\"btn\" data-value=\"0\">0</button>
        <button class=\"btn\" data-value=\".\">.</button>
        <button class=\"btn operator\" data-value=\"=\">=</button>
        <button class=\"btn operator\" data-value=\"+\">+</button>
      </div>
    </div>
  </main>
  <script src=\"script.js\"></script>
</body>
</html>
"""
        css = """body {
  margin: 0;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: Inter, Arial, sans-serif;
  background: linear-gradient(135deg, #f8fafc, #e2e8f0);
  color: #0f172a;
}

.calculator-shell {
  width: min(92%, 360px);
}

.calculator-card {
  background: white;
  border-radius: 24px;
  padding: 24px;
  box-shadow: 0 18px 45px rgba(15, 23, 42, 0.12);
}

h1 {
  margin: 0 0 14px;
  text-align: center;
}

.display {
  background: #0f172a;
  color: white;
  border-radius: 12px;
  padding: 16px;
  font-size: 1.4rem;
  text-align: right;
  margin-bottom: 14px;
}

.buttons {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
}

.btn {
  border: none;
  border-radius: 10px;
  padding: 14px;
  font-size: 1rem;
  background: #e2e8f0;
  cursor: pointer;
}

.operator {
  background: #4f46e5;
  color: white;
}
"""
        script = """const display = document.getElementById('display');
const buttons = document.querySelectorAll('.btn');
let current = '0';
let operator = '';
let previous = null;

buttons.forEach((button) => {
  button.addEventListener('click', () => {
    const value = button.dataset.value;

    if (/\d|\./.test(value)) {
      if (current === '0' && value !== '.') {
        current = value;
      } else {
        current += value;
      }
      display.textContent = current;
      return;
    }

    if (value === '=') {
      if (previous !== null && operator) {
        const a = Number(previous);
        const b = Number(current);
        if (operator === '+') current = String(a + b);
        if (operator === '-') current = String(a - b);
        if (operator === '*') current = String(a * b);
        if (operator === '/') current = String(a / b);
        display.textContent = current;
      }
      previous = null;
      operator = '';
      return;
    }

    previous = current;
    operator = value;
    current = '0';
  });
});
"""
    else:
        html = f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>{brand_name}</title>
  <link rel=\"stylesheet\" href=\"styles.css\" />
</head>
<body>
  <main class=\"hero\">
    <div class=\"card\">
      <p class=\"brand\">{brand_name}</p>
      <h1>Find something beautiful</h1>
      <p class=\"subtitle\">A calm, clean place to explore {goal_text}</p>
      <form class=\"search-box\">
        <input type=\"text\" placeholder=\"Search here\" />
        <button type=\"submit\">Go</button>
      </form>
    </div>
  </main>
  <script src=\"script.js\"></script>
</body>
</html>
"""
        css = """body {
  margin: 0;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: Inter, Arial, sans-serif;
  background: linear-gradient(135deg, #f8fafc, #e2e8f0);
  color: #0f172a;
}

.hero {
  width: min(92%, 560px);
}

.card {
  background: white;
  border-radius: 24px;
  padding: 36px 32px;
  text-align: center;
  box-shadow: 0 18px 45px rgba(15, 23, 42, 0.12);
}

.brand {
  margin: 0 0 10px;
  font-size: 0.95rem;
  font-weight: 700;
  letter-spacing: 0.24em;
  text-transform: uppercase;
  color: #6366f1;
}

h1 {
  margin: 0 0 10px;
  font-size: 2rem;
}

.subtitle {
  margin: 0 0 20px;
  color: #475569;
}

.search-box {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  margin-top: 12px;
}

.search-box input {
  flex: 1;
  padding: 12px 14px;
  border: 1px solid #cbd5e1;
  border-radius: 999px;
  outline: none;
}

.search-box button {
  border: none;
  border-radius: 999px;
  padding: 12px 16px;
  background: #4f46e5;
  color: white;
  cursor: pointer;
}
"""
        script = """const form = document.querySelector('.search-box');
const input = document.querySelector('.search-box input');
const result = document.querySelector('.subtitle');

if (form && input && result) {
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const value = input.value.trim();
    if (value) {
      result.textContent = `You searched for: ${value}`;
    }
  });
}
"""

    return {
        "index.html": html,
        "styles.css": css,
        "script.js": script,
    }


def app_builder(state: AgentState):
    fallback_files = build_basic_ui_files(state['user_goal'])

    try:
        prompt = f"""
            You are an expert app builder, FAANG senior developer.

            User wants: {state['user_goal']}

            Development plan to follow: {state['plan_steps']}

            Research from web: {state['search_results']}

            Relevant docs: {state['retrieved_docs']}

            Previous review feedback (if any): {state['review_feedback']}
            This is attempt number: {state['retry_count']}

            If review feedback exists, fix those specific issues.
            If this is a retry, improve on previous attempt.

            Create a simple, polished landing page that is centered vertically and horizontally.
            Use a unique site name and include a clean search bar in the middle.
            Reply ONLY with a JSON object like this:
            {{
            "filename.py": "code here",
            "index.html": "code here",
            "styles.css": "code here"
            }}
            No explanation. Just the JSON.
            """

        response = llm.invoke([
            SystemMessage(content='You are a senior SWE that can build web sites and application better than anyone.'),
            HumanMessage(content=prompt)
        ])

        content = response.content.strip()
        content = content.replace("```json", "").replace("```", "").strip()  # json issue
        generated_files = json.loads(content, strict=False)

        if isinstance(generated_files, dict) and generated_files:
            generated_files.setdefault("index.html", fallback_files["index.html"])
            generated_files.setdefault("styles.css", fallback_files["styles.css"])
            generated_files.setdefault("script.js", fallback_files["script.js"])
            return {
                "generated_files": generated_files,
                "retry_count": state['retry_count'] + 1,
            }
    except Exception:
        pass

    return {
        "generated_files": fallback_files,
        "retry_count": state['retry_count'] + 1,
    }

