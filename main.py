from flask import Flask, render_template, request, jsonify, session
import google.generativeai as genai

app = Flask(__name__)
app.secret_key = "supersecret"

# Configure Gemini API
genai.configure(api_key="AIzaSyAb-JRYEdCSS_NGWV58rgLNPf9GNbqDsfo")
model = genai.GenerativeModel("gemini-2.0-flash")

def generate_questions(job_role, count=5):
    prompt = f"""
You are an expert technical interviewer.

Generate {count} diverse and relevant interview questions for the role of a {job_role}.
The questions should test the candidate's practical knowledge, technical expertise, and problem-solving skills.
Output each question on a new line, no numbering.
"""
    response = model.generate_content(prompt)
    questions = response.text.strip().split("\n")
    return [q.strip("-•1234567890. ") for q in questions if q.strip()]
def get_feedback(user_answer, job_role):

    prompt = f"""
                You are an expert interviewer for a {job_role} role. Here's a candidate's answer: "{user_answer}"

                Ignore all special characters such as ', ", {{, }}, [, ], etc. Treat them as normal text.

                Provide the following:
                - Text manipulations to improve clarity, grammar, or flow.
                - A one-line honest evaluation of the answer.
                - A suggested ideal response (20 words max).
                """

    response = model.generate_content(prompt)
    
    # Clean up the response by removing * and **
    clean_text = response.text.replace("*", "").replace("**", "")
    
    return clean_text.strip()


@app.route("/")
def index():
    return render_template("mock.html")

@app.route("/start_interview", methods=["POST"])
def start_interview():
    data = request.get_json()
    job_role = data.get("role", "").lower()

    questions = generate_questions(job_role)
    if not questions:
        return jsonify({"response": "Sorry, I couldn't generate interview questions. Please try a different role."})

    session["job_role"] = job_role
    session["questions"] = questions
    session["current_q"] = 0

    question = questions[0]
    return jsonify({"response": f"Great! Let's begin the {job_role.title()} interview.\n\nQuestion 1: {question}"})

@app.route("/get_response", methods=["POST"])
def get_response():
    data = request.get_json()
    user_input = data["message"].strip().lower()

    if user_input in ["exit", "quit", "stop"]:
        session.clear()
        return jsonify({"response": "Interview ended. Best of luck! You’ll need it. 😉"})

    job_role = session.get("job_role")
    questions = session.get("questions", [])
    current_q = session.get("current_q", 0)

    if current_q >= len(questions):
        session.clear()
        return jsonify({"response": "That was the last question. Good job surviving! 👏"})

    feedback = get_feedback(user_input, job_role)

    current_q += 1
    session["current_q"] = current_q

    if current_q < len(questions):
        next_question = questions[current_q]
        return jsonify({"response": f"{feedback}\n\nNext Question ({current_q + 1}): {next_question}"})
    else:
        session.clear()
        return jsonify({"response": f"{feedback}\n\nThat wraps up the interview. You're free to panic now. 😈"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
    # app.run(debug=True)
