import os
import markdown
from datetime import datetime

DIARY_DIR = "diary"
OUTPUT_DIR = "diary"
TEMPLATE_PATH = "template.html"
INDEX_PATH = "index.html"

def load_template():
    with open(TEMPLATE_PATH, encoding="utf-8") as f:
        return f.read()

def convert_md_to_html(md_path, template):
    date = os.path.splitext(os.path.basename(md_path))[0]
    with open(md_path, encoding="utf-8") as f:
        md = f.read()
    html_content = markdown.markdown(md)
    output_html = template.replace("{{ content }}", html_content).replace("{{ date }}", date)
    
    output_path = os.path.join(OUTPUT_DIR, f"{date}.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output_html)
    return date

def build_index(dates):
    items = "\n".join([f'<li><a href="./diary/{d}.html">{d}</a></li>' for d in sorted(dates, reverse=True)])
    index_html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>オレの日記</title>
  <link rel="stylesheet" href="./static/style.css">
</head>
<body>
  <div class="container">
    <h1>オレの日記</h1>
    <ul>
      {items}
    </ul>
    <div class="new-button">
      <p><em>Markdown で新しい日記を diary/ に追加してね！</em></p>
    </div>
  </div>
</body>
</html>"""
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(index_html)

def main():
    template = load_template()
    dates = []

    for fname in os.listdir(DIARY_DIR):
        if fname.endswith(".md"):
            path = os.path.join(DIARY_DIR, fname)
            date = convert_md_to_html(path, template)
            dates.append(date)

    build_index(dates)
    print("✅ ビルド完了！")

if __name__ == "__main__":
    main()
