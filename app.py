# app.py
from flask import Flask, render_template, abort
from flask import request, redirect, url_for
from datetime import date
import markdown
import os

app = Flask(__name__)

@app.route("/diary/<date>")
def show_diary(date):
    filepath = f"diary/{date}.txt"
    if not os.path.exists(filepath):
        abort(404)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    html_content = markdown.markdown(content)  # ← ここで変換
    return render_template("diary.html", date=date, content=html_content)

@app.route("/")
def index():
    diary_dir = "diary"
    if not os.path.exists(diary_dir):
        os.makedirs(diary_dir)

    diary_files = [f.replace(".txt", "") for f in os.listdir(diary_dir) if f.endswith(".txt")]
    diary_files.sort(reverse=True)  # 最新が上に来るように
    return render_template("index.html", diaries=diary_files)

@app.route("/new", methods=["GET", "POST"])
def new_diary():
    if request.method == "POST":
        today = date.today().isoformat()  # ← 今日の日付
        content = request.form["content"]
        with open(f"diary/{today}.txt", "w", encoding="utf-8") as f:
            f.write(content)
        return redirect(url_for("show_diary", date=today))
    return render_template("new.html")

@app.route("/edit/<date>", methods=["GET", "POST"])
def edit_diary(date):
    filepath = f"diary/{date}.txt"
    if not os.path.exists(filepath):
        abort(404)

    if request.method == "POST":
        new_content = request.form["content"]
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        return redirect(url_for("show_diary", date=date))

    # GET時：既存内容を読み込んでフォームに表示
    with open(filepath, "r", encoding="utf-8") as f:
        existing_content = f.read()

    return render_template("edit.html", date=date, content=existing_content)

if __name__ == "__main__":
    app.run(host="192.168.11.8", port=5000, debug=True)
