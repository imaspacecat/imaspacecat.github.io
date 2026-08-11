#!/usr/bin/env python3
from pathlib import Path

import markdown

POSTS = Path("posts")
TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} · λ</title>
    <link rel="stylesheet" href="../styles.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Jacquard+12&family=Jacquarda+Bastarda+9&family=Slabo+27px&display=swap" rel="stylesheet">
</head>
<body class="slabo-27px-regular">
    <nav class="title-bar">
        <a href="/">home</a>
        <a href="/posts/">posts</a>
    </nav>
    <div class="content post">
        <h1 class="jacquarda-bastarda-9-regular">{title}</h1>
        <p class="post-date">{date}</p>
        {body}
    </div>
</body>
</html>
"""
INDEX = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>posts · λ</title>
    <link rel="stylesheet" href="../styles.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Jacquard+12&family=Jacquarda+Bastarda+9&family=Slabo+27px&display=swap" rel="stylesheet">
</head>
<body class="slabo-27px-regular">
    <nav class="title-bar">
        <a href="/">home</a>
        <a href="/posts/">posts</a>
    </nav>
    <div class="content">
        <h1 class="jacquarda-bastarda-9-regular">posts</h1>
        <br>
        <ul class="post-list">
{items}
        </ul>
    </div>
</body>
</html>
"""


def parse(text: str) -> tuple[dict[str, str], str]:
    meta: dict[str, str] = {}
    if text.startswith("---"):
        _, front, body = text.split("---", 2)
        for line in front.strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        return meta, body.lstrip("\n")
    return meta, text


def main() -> None:
    md = markdown.Markdown(extensions=["fenced_code", "tables"])
    posts = []
    for path in sorted(POSTS.glob("*.md")):
        meta, body = parse(path.read_text())
        title = meta.get("title", path.stem)
        date = meta.get("date", "")
        html = md.convert(body)
        md.reset()
        (POSTS / f"{path.stem}.html").write_text(
            TEMPLATE.format(title=title, date=date, body=html)
        )
        posts.append((date, title, path.stem))

    posts.sort(reverse=True)
    items = "\n".join(
        f'            <li><a href="{slug}.html">{title}</a>'
        + (f' <span class="post-date">{date}</span>' if date else "")
        + "</li>"
        for date, title, slug in posts
    ) or '            <li>nothing here yet.</li>'
    (POSTS / "index.html").write_text(INDEX.format(items=items))
    print(f"built {len(posts)} post(s)")


if __name__ == "__main__":
    main()
