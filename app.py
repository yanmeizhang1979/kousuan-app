# app.py
from flask import Flask, render_template, request
import random

app = Flask(__name__)

def generate_questions(start, end, count, op_type):
    questions = []
    attempts = 0
    max_attempts = count * 20

    if op_type == "add":
        while len(questions) < count and attempts < max_attempts:
            a = random.randint(start, end)
            b = random.randint(start, end)
            s = a + b
            if s <= end:
                if random.random() < 0.3:
                    if random.choice([True, False]):
                        questions.append(f"（ ）＋ {b} = {s}")
                    else:
                        questions.append(f"{a} ＋（ ）= {s}")
                else:
                    questions.append(f"{a} ＋ {b} = _____")
            attempts += 1

    elif op_type == "sub":
        while len(questions) < count and attempts < max_attempts:
            a = random.randint(start, end)
            b = random.randint(start, a)
            diff = a - b
            if diff >= start:
                if random.random() < 0.3:
                    if random.choice([True, False]):
                        questions.append(f"（ ）－ {b} = {diff}")
                    else:
                        questions.append(f"{a} －（ ）= {diff}")
                else:
                    questions.append(f"{a} － {b} = _____")
            attempts += 1

    elif op_type == "mul":
        for _ in range(count):
            a = random.randint(max(1, start), end)
            b = random.randint(max(1, start), end)
            p = a * b
            if random.random() < 0.3:
                if random.choice([True, False]):
                    questions.append(f"（ ）× {b} = {p}")
                else:
                    questions.append(f"{a} ×（ ）= {p}")
            else:
                questions.append(f"{a} × {b} = _____")

    elif op_type == "div":
        for _ in range(count):
            divisor = random.randint(max(1, start), end)
            quotient = random.randint(1, max(1, end))
            dividend = divisor * quotient
            if random.random() < 0.3:
                if random.choice([True, False]):
                    questions.append(f"（ ）÷ {divisor} = {quotient}")
                else:
                    questions.append(f"{dividend} ÷（ ）= {quotient}")
            else:
                questions.append(f"{dividend} ÷ {divisor} = _____")

    # 补足数量（防止范围太小导致题目不足）
    while len(questions) < count:
        questions.append("1 ＋ 1 = _____")
    return questions[:count]

@app.route('/', methods=['GET', 'POST'])
def index():
    questions = []
    form_data = {'start': '1', 'end': '10', 'count': '20', 'op': 'add'}
    
    if request.method == 'POST':
        try:
            start = int(request.form['start'])
            end = int(request.form['end'])
            count = min(100, max(1, int(request.form['count'])))
            op_type = request.form['op']
            form_data.update(request.form)
            questions = generate_questions(start, end, count, op_type)
        except Exception as e:
            questions = [f"❌ 输入错误：{str(e)}"]

    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>小学口算题生成器</title>
        <style>
            body {{ font-family: "Microsoft YaHei", sans-serif; padding: 15px; background:#f9f9f9; }}
            input, select, button {{ padding: 10px; margin: 6px 0; width: 100%; box-sizing: border-box; border:1px solid #ccc; border-radius:6px; }}
            .question {{ background:white; padding:10px; margin:6px 0; border-radius:6px; box-shadow:0 1px 2px rgba(0,0,0,0.05); }}
            .grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }}
            @media (min-width: 600px) {{ .grid {{ grid-template-columns: repeat(4, 1fr); }} }}
            button {{ background:#4CAF50; color:white; font-weight:bold; }}
            h2 {{ text-align:center; color:#2c3e50; }}
        </style>
    </head>
    <body>
        <h2>📱 小学口算题生成器</h2>
        <form method="post">
            范围：<input type="number" name="start" value="{form_data['start']}" min="0"> 到 
            <input type="number" name="end" value="{form_data['end']}" min="1"><br>
            题量：<input type="number" name="count" value="{form_data['count']}" min="1" max="100"><br>
            题型：<select name="op">
                <option value="add" {"selected" if form_data["op"]=="add" else ""}>加法</option>
                <option value="sub" {"selected" if form_data["op"]=="sub" else ""}>减法</option>
                <option value="mul" {"selected" if form_data["op"]=="mul" else ""}>乘法</option>
                <option value="div" {"selected" if form_data["op"]=="div" else ""}>除法</option>
            </select><br>
            <button type="submit">🔥 生成题目</button>
        </form>
        <hr>
        <div class="grid">
            {''.join(f'<div class="question">{q}</div>' for q in questions)}
        </div>
        <footer style="text-align:center; margin-top:30px; color:#777; font-size:0.9em;">
            💡 手机可长按复制题目 | 分享给老师/家长
        </footer>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)