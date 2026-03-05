import os
from pathlib import Path


def test_create_text(client, auth_headers):
    fileName = "The secret garden.txt"
    cwd = os.getcwd()
    cwd_ = cwd.split("\\")
    path = cwd_[0]
    for c in cwd_[1:-3]:
        path = path + "\\" + c
    texts_file_path = Path(path + "\\documents\\" + fileName)

    content = texts_file_path.read_text(encoding="utf-8")

    blocks = content.split("=== TEXT ===")
    title = None
    text_content= None
    for block in blocks:
        if "=== END ===" not in block:
            continue

        header, body = block.split("\n\n", 1)

        for line in header.splitlines():
            if line.startswith("Title:"):
                title = line.replace("Title:", "").strip()

        text_content = body.replace("=== END ===", "").strip()

        if not title or not text_content:
            continue


    payload = {
        "title": title,
        "content": text_content,
        "language": "en"
    }

    res = client.post(
        "/texts",
        json=payload,
        headers=auth_headers,
    )

    assert res.status_code == 200
    data = res.json()

    assert data["title"] == "THE SECRET GARDEN"
    #assert len(data["questions"]) <= 5



