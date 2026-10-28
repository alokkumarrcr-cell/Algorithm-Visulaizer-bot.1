# AlgoMentor AI — Algorithm Learning Bot

AlgoMentor AI is a beginner-friendly algorithm learning website built for a live student project demonstration. Learners can visualize sorting, practice with quizzes, compare algorithms, receive static code-review hints, and ask an AI tutor questions in plain language. A light sky-blue dashboard and deep-blue navigation keep the learning steps easy to scan. The tutor also uses fun real-world stories—like friends lining up by height—to explain each algorithm.

## Project structure

```text
algobloom/
├── app.py                 # Python HTTP backend and tutor API
├── README.md              # Setup, project brief, demo plan, and viva guide
├── .env.example           # Optional AI API configuration
└── static/
    ├── index.html         # App screens and navigation
    ├── style.css          # Responsive blue-and-white UI
    └── app.js             # Visualizer, quizzes, tracking, and interactions
```

## Run locally

Requires Python 3.9+; no third-party packages are required.

```bash
python app.py
```

Open [http://localhost:8000](http://localhost:8000). To change the port, set `PORT` before starting the server. Run `python app.py` from the project root; do not open `static/index.html` when you need the backend APIs. The stylesheet and script use relative paths so the design also appears in a direct file preview, while tutor/debug API features need the Python server.

### Optional AI tutor API

The tutor works without a key using built-in beginner explanations. For generated answers, set an API key and optionally the model/base URL. Keep the key on the server and out of browser code.

PowerShell example:

```powershell
$env:OPENAI_API_KEY = "your-key"
$env:OPENAI_MODEL = "gpt-4o-mini"
python app.py
```

`OPENAI_BASE_URL` defaults to `https://api.openai.com/v1` and supports compatible chat-completions endpoints. Never commit a real key.

## Problem statement

Many learners find algorithms abstract: they can read code without understanding what each operation changes, how performance grows, or where their reasoning has gaps. AlgoMentor AI turns algorithm concepts into interactive visual steps, quick feedback, plain-language explanations, and progress signals.

## Main features

- Interactive bubble, insertion, selection, merge, and quick sort visualizer; linear/binary search; and BFS, DFS, and Dijkstra graph traversal visualizers; custom numeric lists, shuffle, step, play, speed, comparisons, and swap counts.
- **Problem Explainer** sidebar page: describe a real problem or paste algorithm steps. Common algorithms and the quadratic formula have offline explanations, worked examples, real-world stories, assumptions, and edge cases; an optional AI API handles broader pasted procedures.
- Plain-language concept cards, fun real-world stories, analogies, step lists, and time/space complexity.
- Randomized quizzes draw from sorting, searching, graphs, recursion, and complexity. Answers are shuffled, explained, tracked, and grouped into review gaps.
- Side-by-side complexity and use-case comparison.
- Beginner static code-review hints for Python, Java, and C, including Python syntax, common sort boundaries, and quadratic-formula denominator and edge-case checks. This is a learning aid, not a compiler or secure code runner; pasted code is never executed.
- Tutor chat: built-in responses work offline; optional OpenAI-compatible API can generate answers.
- Browser-local progress dashboard with streak, best streak, quiz accuracy, explored topics, practice sessions, and learning gaps.
- Responsive sidebar and phone layout.

## Backend API

| Method | Route | Purpose |
| --- | --- | --- |
| GET | `/api/health` | Backend status and optional AI availability |
| GET | `/api/algorithms` | Algorithm descriptions and complexity |
| POST | `/api/explain` | Explain one supported algorithm |
| POST | `/api/explain-problem` | Explain a problem statement or pasted algorithm procedure |
| POST | `/api/quiz` | Return a quiz set |
| POST | `/api/debug` | Return static beginner code-review hints |
| POST | `/api/chat` | Tutor response (AI API or offline fallback) |

Example: `curl -X POST http://localhost:8000/api/explain -H "Content-Type: application/json" -d '{"algorithm":"bubble sort"}'`

## Tracking and privacy

Progress is stored in the learner's browser using `localStorage`; it is not uploaded to the Python backend. Clearing browser storage clears this demo progress. The optional tutor sends the user's submitted chat prompt to the configured AI endpoint. Avoid entering personal or confidential information.

## Test and demo checklist

1. Start the server and confirm `http://localhost:8000/api/health` returns `ok: true`.
2. Open the visualizer, shuffle or enter numbers, step through bubble sort, then play to completion. Show comparisons, swaps, and complexity.
3. Take a quiz, intentionally miss an answer, and show the accuracy and review-gap panel.
4. Compare Bubble sort and Merge sort.
5. In Problem Explainer, choose **Quadratic formula** and review the worked example and edge cases. In Code Lab, review a correct quadratic implementation, then try a denominator such as `/ 2*a` to see the hint. Explain that review hints are static and code is not executed.
6. Ask the tutor to explain binary search. Repeat with an API key to demonstrate generated chat if network access is available.
7. Return to Overview and show the streak and practice chart. Progress persists in that browser.

## Suggested team registration

Register your actual project members and institution through your event's official process. Suggested roles: UI/UX and frontend, algorithms and visualizer, Python backend and AI integration, testing and presentation. Replace these role descriptions with your real member names; the app does not register a team on your behalf.

## Judge presentation / viva notes

- **Problem:** algorithm learning often feels abstract and gives learners few immediate signals about misconceptions.
- **Solution:** a visual, interactive tutor that breaks algorithms into steps and connects practice results to a review plan.
- **Technology:** Python standard-library HTTP server; HTML, CSS, JavaScript; optional chat-completions API; `localStorage` for local progress.
- **Applications:** classroom demonstrations, self-study, coding-club practice, and introductory interview preparation.
- **Limitations:** without an API key, open-ended pasted procedures outside the built-in examples get a cautious step-by-step fallback and may need more context for exact identification. API output depends on network/key/model availability. Code review uses static checks, not execution. Quiz tracking is per-browser rather than a multi-user account system.
- **Possible next steps:** implement dedicated traces for every listed algorithm, add authenticated learner profiles and durable database storage, expand quizzes and adaptive recommendations, and add unit/integration tests and accessibility review.

## Team details

Add your team name, members, institution, and event name here before presenting.
