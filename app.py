"""AlgoMentor AI: small standard-library backend for an algorithm learning demo."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import ast, json, os, random, re, urllib.request

ROOT = Path(__file__).parent
STATIC = ROOT / "static"
PORT = int(os.getenv("PORT", "8000"))

ALGORITHMS = {
 "bubble sort": {"idea":"Repeatedly compare neighboring values and swap them when they are in the wrong order. Each pass moves the largest unsorted value to the end.","steps":["Start at the left of the list.","Compare this value with the next one.","Swap them if the left value is bigger.","Move one place right and repeat.","After one full pass, the largest value is in its final place. Repeat on the shorter unsorted section."],"time":"Best O(n) with early exit; average/worst O(n²)","space":"O(1)","analogy":"Like lining up books by swapping neighboring books that are out of order.","real_world":"Imagine friends lining up for a group photo by height. Compare two neighbors; if the taller friend is in front, they swap. After a pass, the tallest person has bubbled to the end."},
 "binary search": {"idea":"Find a target in a sorted list by repeatedly checking the middle and discarding half the remaining values.","steps":["Set low and high to the first and last positions.","Check the middle value.","If it matches, stop.","If the middle is too small, search the right half; otherwise search the left half.","Repeat until found or no values remain."],"time":"O(log n)","space":"O(1) iterative","analogy":"Like finding a word in a dictionary by opening near the middle and choosing a half.","real_world":"Find a name in an alphabetized guest list: open to the middle, see whether it comes before or after, and ignore the half that cannot contain it."},
 "insertion sort": {"idea":"Grow a sorted section one item at a time by inserting each new item into its correct position.","steps":["Treat the first item as sorted.","Take the next item as the key.","Shift larger sorted items one place right.","Put the key into the gap.","Repeat for each remaining item."],"time":"Best O(n); average/worst O(n²)","space":"O(1)","analogy":"Like picking up cards and inserting each into the right place in your hand.","real_world":"You are holding numbered lunch tickets in order. Slide each new ticket into its correct gap while larger numbers move aside."},
 "merge sort": {"idea":"Split the list into halves until each piece has one item, then merge sorted pieces back together.","steps":["Split the list into two halves.","Keep splitting each half until pieces have one item.","Compare the first remaining item in each piece.","Move the smaller item into the result.","Continue until all pieces are merged."],"time":"O(n log n)","space":"O(n)","analogy":"Like sorting two small piles, then carefully combining them into one ordered pile.","real_world":"Two classrooms each line up students by height. Walk down both lines and combine them into one correctly ordered line."},
 "quick sort": {"idea":"Choose a pivot, partition values into smaller and larger groups, then sort each group recursively.","steps":["Choose a pivot value.","Move smaller values to one side and larger values to the other.","The pivot is now in its final position.","Repeat the process on each side."],"time":"Average O(n log n); worst O(n²)","space":"O(log n) average recursion","analogy":"Like choosing a height as a divider and sorting people into shorter and taller groups.","real_world":"At a party, choose one person as a height marker. Send shorter guests to one side and taller guests to the other, then organize each group."},
 "linear search": {"idea":"Check each item from the beginning until the target is found or the list ends.","steps":["Start with the first item.","Compare it with the target.","If equal, return its position.","Otherwise move to the next item.","If you reach the end, the target is not present."],"time":"O(n)","space":"O(1)","analogy":"Like checking every pocket for your keys one by one.","real_world":"Find your blue sock in a laundry basket: pick up each sock and check it until the blue one appears."},
 "selection sort": {"idea":"Find the smallest item in the unsorted section and swap it into the next sorted position.","steps":["Start at the first position.","Scan the remaining values to find the smallest.","Swap it into the current position.","Move the boundary one place right and repeat."],"time":"O(n²)","space":"O(1)","analogy":"Like repeatedly selecting the shortest person from a line and moving them to the next open place in line.","real_world":"A teacher finds the shortest student still waiting, brings them to the next open place, then repeats until the class is in height order."}
 ,"breadth first search": {"idea":"Visit the closest unvisited neighbors first, then move outward one layer at a time.","steps":["Put the starting node in a queue.","Remove the front node and inspect its neighbors.","Add each unvisited neighbor to the back of the queue.","Repeat until the goal is found or the queue is empty."],"time":"O(V + E)","space":"O(V)","analogy":"Like ripples spreading evenly across a pond.","real_world":"Find the fewest friend-to-friend introductions to reach someone in a social network by checking friends-of-friends layer by layer."},
 "depth first search": {"idea":"Follow one route as far as possible, then backtrack to the last choice point.","steps":["Start at the first node.","Choose an unvisited neighbor and keep going deeper.","When there is nowhere new to go, backtrack.","Continue until the goal is found or every path is explored."],"time":"O(V + E)","space":"O(V)","analogy":"Like exploring a maze hallway and returning when it ends.","real_world":"Explore every room in a building: go down one corridor fully, then return and try the next corridor."},
 "dijkstra": {"idea":"Grow the known shortest routes from a start by always expanding the closest place reached so far.","steps":["Set the starting place cost to zero and others to infinity.","Choose the unvisited place with the smallest known cost.","Update each neighbor if a cheaper route goes through this place.","Repeat until the destination is finalized."],"time":"O((V + E) log V) with a priority queue","space":"O(V)","analogy":"Like a delivery driver comparing the cheapest known route to nearby neighborhoods.","real_world":"Find the cheapest road route from a depot to every neighborhood when road costs are non-negative."}

}

def answer_for(prompt):
    q = prompt.lower()
    name = next((n for n in ALGORITHMS if n in q), None)
    if name:
        a = ALGORITHMS[name]
        return {"reply":f"{name.title()} made simple: {a['idea']}\n\nA fun real-world example: {a['real_world']}\n\nRemember: {a['analogy']}\n\nSteps:\n"+"\n".join(f"{i+1}. {s}" for i,s in enumerate(a['steps']))+f"\n\nTime: {a['time']}\nSpace: {a['space']}","algorithm":name}
    extra = {
        "breadth first search": ("BFS explores nearby nodes first, layer by layer.", "Imagine ripples spreading across a pond: check every nearby point before moving farther away.", "It is useful for the shortest path in an unweighted map.", "O(V + E) time and O(V) space."),
        "bfs": ("BFS explores nearby nodes first, layer by layer.", "Imagine ripples spreading across a pond: check every nearby point before moving farther away.", "It is useful for the shortest path in an unweighted map.", "O(V + E) time and O(V) space."),
        "depth first search": ("DFS follows one path as far as it can, then backtracks.", "Imagine exploring a maze: keep walking down one hallway until it ends, then return to the last junction.", "It is useful for exploring connected areas and solving maze-like problems.", "O(V + E) time and O(V) space."),
        "dfs": ("DFS follows one path as far as it can, then backtracks.", "Imagine exploring a maze: keep walking down one hallway until it ends, then return to the last junction.", "It is useful for exploring connected areas and solving maze-like problems.", "O(V + E) time and O(V) space."),
        "dijkstra": ("Dijkstra's algorithm grows the known shortest routes outward from a starting point.", "Imagine a delivery driver checking the cheapest road to every next neighborhood before choosing where to go.", "It finds shortest routes when road costs are non-negative.", "Usually O((V + E) log V) with a priority queue."),
        "recursion": ("Recursion solves a problem by calling the same kind of solution on a smaller problem, until it reaches a simple stopping case.", "Imagine opening nested gift boxes: each box contains a smaller box until you reach the gift.", "Every recursive solution needs a base case so it knows when to stop.", "Time and space depend on the number and size of recursive calls."),
    }
    for key, (idea, story, use, cost) in extra.items():
        if key in q:
            return {"reply": f"{key.upper()} made simple: {idea}\n\nA real-world story: {story}\n\nWhen it helps: {use}\n\nComplexity: {cost}", "algorithm": key}
    # Turn a plain-language task into a likely algorithm and a memorable story.
    if any(k in q for k in ("shortest route", "shortest path", "delivery route", "road map", "find a route", "cheapest route")):
        return {"algorithm":"dijkstra", "reply":"Suggested approach: Dijkstra’s algorithm.\n\nEasy idea: start where you are, keep the cheapest known trip to each nearby place, and always visit the place with the cheapest trip so far.\n\nReal-world story: imagine a delivery driver planning stops across town. They compare road costs and lock in the cheapest reachable neighborhood first.\n\nSteps: 1) Set the start place to cost 0. 2) Pick the unvisited place with the smallest known cost. 3) Check whether going through it makes nearby trips cheaper. 4) Repeat until you reach the destination.\n\nGood for non-negative road costs; usually O((V + E) log V) with a priority queue."}
    if any(k in q for k in ("maze", "fewest steps", "minimum moves", "shortest number of steps")):
        return {"algorithm":"breadth first search", "reply":"Suggested approach: Breadth-First Search (BFS).\n\nEasy idea: explore all places one step away before exploring places two steps away.\n\nReal-world story: ripples spread across a pond in rings. BFS checks every nearby square before moving farther, so the first time it reaches the goal is the route with the fewest moves.\n\nSteps: 1) Put the start in a queue. 2) Visit its unvisited neighbors. 3) Add each neighbor to the back of the queue. 4) Continue layer by layer until you reach the goal.\n\nTime: O(V + E). Space: O(V)."}
    if any(k in q for k in ("sorted list", "alphabetical list", "sorted array", "ordered list")) and any(k in q for k in ("find", "search", "look for", "locate")):
        return {"algorithm":"binary search", "reply":"Suggested approach: Binary search.\n\nEasy idea: because the list is already sorted, check the middle and throw away the half that cannot contain the answer.\n\nReal-world story: find a name in an alphabetized school register. Open near the middle, decide whether the name is earlier or later, then repeat with only that half.\n\nSteps: 1) Check the middle item. 2) If it is too small, keep the right half; if too big, keep the left half. 3) Repeat until found or the range is empty.\n\nTime: O(log n). The data must be sorted first."}
    if any(k in q for k in ("sort", "arrange", "order these", "rank these")):
        sort_name="merge sort" if any(k in q for k in ("large", "many", "millions", "big list")) else "insertion sort"
        a=ALGORITHMS[sort_name]
        return {"algorithm":sort_name, "reply":f"Suggested approach: {sort_name.title()}.\n\nEasy idea: {a['idea']}\n\nReal-world story: {a['real_world']}\n\nSteps:\n"+"\n".join(f"{i+1}) {step}" for i,step in enumerate(a['steps']))+f"\n\nTime: {a['time']}\nSpace: {a['space']}"}
    if any(k in q for k in ("find", "search", "look for", "locate")):
        a=ALGORITHMS["linear search"]
        return {"algorithm":"linear search", "reply":f"Suggested approach: Linear search.\n\nEasy idea: {a['idea']}\n\nReal-world story: {a['real_world']}\n\nSteps:\n"+"\n".join(f"{i+1}) {step}" for i,step in enumerate(a['steps']))+f"\n\nTime: {a['time']}\nSpace: {a['space']}"}
    if "big o" in q or "complex" in q or "time complexity" in q:
        return {"reply":"Big O describes how an algorithm's work grows as the input gets bigger. O(1) stays roughly constant, O(log n) grows slowly, O(n) grows with the list, and O(n²) can get slow quickly. For example, bubble sort is O(n²) because it may compare many pairs."}
    if "debug" in q or "error" in q or "bug" in q:
        return {"reply":"Paste a short code snippet in the Code Lab and choose its language. I can flag common learning-level issues such as off-by-one loop bounds, missing swaps, and suspicious comparisons. For a runtime error, include the exact message and a small input that reproduces it."}
    return {"reply":"I’m your algorithm study buddy. Ask me to explain an algorithm, compare two approaches, define Big O, or paste code into Code Lab for a beginner-friendly review. I can help with sorting, searching, recursion, and data structures."}

def explain_problem(problem):
    """Explain common algorithm prompts deterministically, including offline use."""
    q=problem.lower().replace("−", "-").replace("²", "^2")
    quadratic=("quadratic" in q or bool(re.search(r"b\s*\^2\s*-\s*4\s*a\s*\*?\s*c",q)) or ("x1" in q and "x2" in q and ("discriminant" in q or "square root" in q)))
    if quadratic:
        return {"algorithm":"Quadratic formula", "reply":(
            "This is the quadratic formula. It finds the x-values where a parabola crosses the x-axis for an equation written as ax² + bx + c = 0.\n\n"
            "Easy idea: first measure the discriminant, b² − 4ac. It tells us how many real answers there are. Then use the plus and minus versions of the formula to get the two roots.\n\n"
            "A real-world story: imagine a ball thrown through the air. Its height can be modeled by a quadratic equation; the roots tell you when the ball is at ground level. In other settings, the roots can mark when a design, profit, or distance reaches zero.\n\n"
            "Your steps, in plain language:\n"
            "1. Read a, b, and c from ax² + bx + c = 0.\n"
            "2. Compute d = √(b² − 4ac), the square root of the discriminant.\n"
            "3. Compute x1 = (−b + d) / (2a).\n"
            "4. Compute x2 = (−b − d) / (2a).\n"
            "5. Show both roots. The parentheses around 2a matter: divide the whole numerator by 2a.\n\n"
            "Quick check: if a=1, b=−3, c=2, then d=√(1)=1, so x1=2 and x2=1. Substituting either value into x²−3x+2 gives 0.\n\n"
            "Important checks: a must not be 0 (otherwise this is not a quadratic); if b²−4ac is negative, there are no real roots (use complex numbers if required); if it is 0, both roots are the same.\n\n"
            "Efficiency: O(1) time and O(1) extra space because it uses a fixed number of calculations."
        )}
    if "queue" in q and any(k in q for k in ("front", "first in first out", "fifo", "remove the next", "dequeue")):
        return {"algorithm":"Queue (FIFO)", "reply":(
            "This is a queue, which follows FIFO: First In, First Out. The person who joins first is served first.\n\n"
            "Real-world example: picture a line at a school lunch counter. New students join at the back; the student at the front is served and leaves first.\n\n"
            "Your steps mean: 1) Add each customer to the back of the queue. 2) Take the next customer from the front. 3) Serve them. 4) Repeat until no customers remain.\n\n"
            "For a standard queue, adding at the back and removing from the front each take O(1) time. The queue can hold up to O(n) customers."
        )}
    # Recognize a pasted numbered procedure and explain the steps as a procedure
    # instead of returning an unrelated generic algorithm.
    numbered_steps=sum(1 for line in problem.splitlines() if re.match(r"\s*(?:step\s*)?\d+[.):]",line,re.I))
    if numbered_steps >= 2:
        if os.getenv("OPENAI_API_KEY"):
            return api_reply("Explain this pasted algorithm accurately for a beginner. Identify its purpose if possible, explain its steps in easy language, give a fitting everyday example without inventing guarantees, point out assumptions or edge cases, and state complexity only if it can be determined. If something is unclear, say what is unclear.\n\nPasted algorithm:\n"+problem)
        # Offline fallback preserves the user's input and provides a useful,
        # honest explanation scaffold when the procedure is not recognized.
        clean=[re.sub(r"^\s*(?:step\s*)?\d+[.):]\s*", "", line, flags=re.I).strip() for line in problem.splitlines()]
        clean=[line for line in clean if line]
        intro="I can see a step-by-step procedure, but the goal is not clear enough for me to name the exact algorithm reliably. Here is what the steps say in order:"
        return {"algorithm":"Pasted step-by-step algorithm", "reply":intro+"\n"+"\n".join(f"{i+1}. {line}" for i,line in enumerate(clean))+"\n\nTo check whether it is correct, tell me what answer you expect, what each input means, and any limits. Then try a small example by hand and test edge cases such as zero, negative values, and empty input. I will avoid guessing a real-world use when the pasted steps do not reveal one."}
    if os.getenv("OPENAI_API_KEY"):
        return api_reply("Recommend an algorithm for this problem. If the user pasted algorithm steps, explain those steps instead of forcing a different algorithm. Teach in easy language, include a relevant real-world example, identify assumptions and edge cases, and give complexity only when supported.\n\nProblem or algorithm:\n"+problem)
    return answer_for(problem)

def api_reply(prompt):
    key=os.getenv("OPENAI_API_KEY")
    if not key: return answer_for(prompt)
    payload={"model":os.getenv("OPENAI_MODEL","gpt-4o-mini"),"messages":[{"role":"system","content":"You are AlgoMentor AI, a patient beginner-friendly algorithms tutor. Use plain language, small examples, and explain time/space complexity. If asked for code, label the language."},{"role":"user","content":prompt}],"temperature":0.4}
    req=urllib.request.Request(os.getenv("OPENAI_BASE_URL","https://api.openai.com/v1")+"/chat/completions",data=json.dumps(payload).encode(),headers={"Authorization":"Bearer "+key,"Content-Type":"application/json"},method="POST")
    try:
        with urllib.request.urlopen(req,timeout=25) as r: data=json.loads(r.read())
        return {"reply":data["choices"][0]["message"]["content"]}
    except Exception:
        return answer_for(prompt)

class Handler(BaseHTTPRequestHandler):
    def send_json(self, data, status=200):
        raw=json.dumps(data).encode(); self.send_response(status); self.send_header("Content-Type","application/json; charset=utf-8"); self.send_header("Content-Length",str(len(raw))); self.send_header("Access-Control-Allow-Origin","*"); self.end_headers(); self.wfile.write(raw)
    def do_OPTIONS(self): self.send_response(204); self.send_header("Access-Control-Allow-Origin","*"); self.send_header("Access-Control-Allow-Headers","Content-Type"); self.send_header("Access-Control-Allow-Methods","GET,POST,OPTIONS"); self.end_headers()
    def do_GET(self):
        path=self.path.split("?",1)[0]
        if path=="/api/health": return self.send_json({"ok":True,"app":"AlgoMentor AI","ai_enabled":bool(os.getenv("OPENAI_API_KEY"))})
        if path=="/api/algorithms": return self.send_json({"algorithms":ALGORITHMS})
        rel="index.html" if path=="/" else path.lstrip("/")
        target=(STATIC/rel).resolve()
        if not str(target).startswith(str(STATIC.resolve())) or not target.is_file(): return self.send_error(404)
        content_type={".html":"text/html; charset=utf-8",".css":"text/css; charset=utf-8",".js":"text/javascript; charset=utf-8"}.get(target.suffix,"application/octet-stream")
        body=target.read_bytes(); self.send_response(200); self.send_header("Content-Type",content_type); self.send_header("Content-Length",str(len(body))); self.end_headers(); self.wfile.write(body)
    def do_POST(self):
        try: data=json.loads(self.rfile.read(int(self.headers.get("Content-Length",0))))
        except Exception: return self.send_json({"error":"Send a JSON request body."},400)
        if self.path=="/api/explain-problem":
            problem=str(data.get("problem",""))[:5000].strip()
            if not problem: return self.send_json({"error":"Describe a problem first."},400)
            result=explain_problem(problem)
            result["problem"]=problem
            return self.send_json(result)
        if self.path=="/api/chat":
            prompt=str(data.get("message",""))[:5000].strip()
            if not prompt: return self.send_json({"error":"Message cannot be empty."},400)
            return self.send_json(api_reply(prompt))
        if self.path=="/api/explain":
            name=str(data.get("algorithm","bubble sort")).lower(); a=ALGORITHMS.get(name)
            return self.send_json({"algorithm":name,**a} if a else {"error":"Algorithm not found. Try one of the listed algorithms."},200 if a else 404)
        if self.path=="/api/debug": return self.send_json(debug_code(str(data.get("code",""))[:10000],str(data.get("language","python"))))
        if self.path=="/api/quiz": return self.send_json(make_quiz(str(data.get("topic","sorting"))))
        return self.send_json({"error":"Unknown endpoint."},404)
    def log_message(self, *_): pass

def debug_code(code, language):
    low=code.lower(); findings=[]; lang=language.lower(); compact=re.sub(r"\s+", "", low)
    if not code.strip(): return {"summary":"Paste some code first.","findings":[]}
    if lang == "python":
        try: ast.parse(code)
        except SyntaxError as e: findings.append({"level":"Syntax issue", "text":f"Python cannot parse this code near line {e.lineno or '?'}: {e.msg}. Check indentation, brackets, and colons."})
    # Focused static checks for the common quadratic-formula exercise.
    quadratic=(any(x in low for x in ("discriminant", "sqrt", "math.sqrt")) and "4" in low and "a" in low and "b" in low and "c" in low) or ("x1" in low and "x2" in low and "-b" in low and ("/2*a" in compact or "/(2*a)" in compact))
    if quadratic:
        if not re.search(r"\ba\s*(?:==|!=|<=|>=|<|>)\s*0\b", low):
            findings.append({"level":"Edge case", "text":"Check that a is not zero before using the quadratic formula. If a = 0, the equation is linear and division by 2a is invalid."})
        if ("sqrt" in low or "math.sqrt" in low) and not re.search(r"(?:discriminant|b\s*\*\*?\s*2|b\^2)[^\n]{0,100}<\s*0|<\s*0[^\n]{0,100}(?:discriminant|sqrt)|\b(?:d|disc|discriminant)\s*<\s*0",low):
            findings.append({"level":"Edge case", "text":"Handle a negative discriminant before taking a real square root. It means there are no real roots; use complex roots if that is part of the assignment."})
        if re.search(r"/\s*2\s*\*\s*a\b", low) and not re.search(r"/\s*\(\s*2\s*\*\s*a\s*\)",low):
            findings.append({"level":"Formula check", "text":"Add parentheses around the denominator: divide by (2 * a). Without them, many languages evaluate / 2 * a from left to right."})
        if not ("x1" in low and "x2" in low):
            findings.append({"level":"Completeness", "text":"A two-root quadratic solution should calculate and report both the plus and minus cases (often named x1 and x2)."})
    adjacent="arr[j]" in compact and "arr[j+1]" in compact
    unbounded_index=adjacent and re.search(r"range\(len\([^)]*\)\)",compact) and not re.search(r"range\(len\([^)]*\)-1\)",compact)
    if "bubble" in low or "sort" in low or adjacent:
        if unbounded_index: findings.append({"level":"Check this","text":"Review this loop boundary. Because the code reads item j + 1, stop j before the final index (for example, range(len(arr) - 1)) to avoid an out-of-range error."})
        has_swap=("arr[j],arr[j+1]=" in compact or "arr[j+1],arr[j]=" in compact or "swap" in low or "temp=" in compact or "inttemp=" in compact)
        if adjacent and not has_swap: findings.append({"level":"Check this","text":"I see neighboring values being compared, but no obvious swap. Make sure out-of-order neighbors are exchanged."})
    if "while" in low and ("low" in low or "left" in low): findings.append({"level":"Check this","text":"For a binary-search loop, confirm the boundary changes each iteration so the loop always makes progress."})
    if not findings: findings.append({"level":"Looks reasonable","text":f"No issue was found by the {language} static checks. Review a small input by hand and test boundary cases; this helper does not execute the code."})
    return {"summary":"Beginner code review (static checks; code was not executed).", "language":language, "findings":findings}

def make_quiz(topic):
    bank=[
      {"topic":"Sorting","q":"What happens during one full pass of bubble sort?","options":["The largest unsorted value moves to the end","The list is split in half","The smallest value is deleted","Every value is checked once with the target"],"answer":0,"why":"Neighbor swaps gradually move the biggest unsorted value to the right."},
      {"topic":"Searching","q":"Which search needs a sorted list to safely discard half the values?","options":["Linear search","Binary search","Depth-first search","Hash lookup"],"answer":1,"why":"Binary search uses sorted order to know which half cannot contain the target."},
      {"topic":"Sorting","q":"What is the average time complexity of merge sort?","options":["O(n²)","O(log n)","O(n log n)","O(1)"],"answer":2,"why":"It processes n values across about log n split-and-merge levels."},
      {"topic":"Sorting","q":"Which sort is often fast on a nearly sorted, small list?","options":["Insertion sort","Bogosort","Selection sort only","None"],"answer":0,"why":"Insertion sort can approach O(n) when values are already nearly in place."},
      {"topic":"Graphs","q":"Which algorithm explores a graph one layer of neighbors at a time?","options":["Depth-first search","Breadth-first search","Bubble sort","Binary search"],"answer":1,"why":"BFS uses a queue to visit nearby nodes first, layer by layer."},
      {"topic":"Graphs","q":"Which algorithm finds shortest routes when edge costs are non-negative?","options":["Dijkstra’s algorithm","Insertion sort","Depth-first search","Linear search"],"answer":0,"why":"Dijkstra repeatedly locks in the closest not-yet-finalized node."},
      {"topic":"Graphs","q":"What is a useful real-life analogy for depth-first search?","options":["Check each item in a basket","Follow one maze hallway, then backtrack","Sort cards into a hand","Open a dictionary in the middle"],"answer":1,"why":"DFS follows one branch deeply before returning to the last choice point."},
      {"topic":"Complexity","q":"What does O(n) usually mean as the input doubles?","options":["Work stays constant","Work roughly doubles","Work becomes zero","Work is always n²"],"answer":1,"why":"Linear work grows in proportion to the number of input items."},
      {"topic":"Sorting","q":"In selection sort, what is placed at the next open position?","options":["The smallest remaining item","A random item","The middle item","The largest item"],"answer":0,"why":"Each pass finds the smallest item in the unsorted part and moves it to the boundary."},
      {"topic":"Recursion","q":"Why does a recursive function need a base case?","options":["To make every call slower","To tell it when to stop","To sort the input","To create a graph"],"answer":1,"why":"The base case ends the chain of smaller calls so recursion does not continue forever."},
      {"topic":"Searching","q":"How does linear search find a target in an unsorted list?","options":["Check items one at a time","Discard half immediately","Sort the list in place","Use a pivot"],"answer":0,"why":"Without sorted order, checking each item is a reliable simple strategy."},
      {"topic":"Sorting","q":"Why can quick sort be slow in its worst case?","options":["It always copies every item twice","A poor pivot can make very uneven partitions","It requires sorted input","It never compares values"],"answer":1,"why":"Very uneven partitions can create about n levels of work, leading to O(n²)."}
    ]
    selected=random.sample(bank,5)
    questions=[]
    for item in selected:
        q=dict(item); correct=q["options"][q["answer"]]; options=list(q["options"]); random.shuffle(options); q["answer"]=options.index(correct); q["options"]=options; questions.append(q)
    return {"topic":topic,"questions":questions}


if __name__=="__main__":
    print(f"AlgoMentor AI running at http://localhost:{PORT}")
    ThreadingHTTPServer(("0.0.0.0",PORT),Handler).serve_forever()
