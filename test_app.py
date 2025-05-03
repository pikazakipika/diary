# test_app.py
from app import app

def test_特定の日記が表示される():
    client = app.test_client()

    # Arrange: テスト用のファイルを作成
    with open("diary/2025-04-30.txt", "w", encoding="utf-8") as f:
        f.write("今日はテストを書いた。")

    # Act: ページにアクセス
    response = client.get("/diary/2025-04-30")
    html = response.data.decode("utf-8")

    # Assert: 内容が含まれていること
    assert "今日はテストを書いた。" in html

def test_新しい日記を投稿できる():
    client = app.test_client()

    # Act: フォーム送信
    response = client.post("/new", data={
        "date": "2025-05-01",
        "content": "フラスクで日記を投稿！"
    }, follow_redirects=True)
    html = response.data.decode("utf-8")

    # Assert: 投稿内容がちゃんと表示される
    assert "フラスクで日記を投稿！" in html

def test_既存の日記を編集できる():
    client = app.test_client()

    # Arrange: テスト用日記ファイルを作成
    test_date = "2025-05-01"
    filepath = f"diary/{test_date}.txt"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("編集前の内容です。")

    # Act: 編集画面にアクセスして投稿
    response = client.post(f"/edit/{test_date}", data={
        "content": "編集後の新しい内容です。"
    }, follow_redirects=True)

    # Assert: 編集後の内容が表示されていること
    assert response.status_code == 200
    assert "編集後の新しい内容です。" in response.data.decode("utf-8")

    # ファイルの中身も確認
    with open(filepath, "r", encoding="utf-8") as f:
        saved_content = f.read()
    assert saved_content == "編集後の新しい内容です。"

