#!/usr/bin/env python3
import argparse
import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

import PyPtt

PTT_ID = os.environ.get("PTT_ID", "seagal")
PTT_PW = os.environ.get("PTT_PW", "5256012")
DEFAULT_MAX_CHECK_COUNT = 300
DEFAULT_MAX_POSTS = 8
DEFAULT_MAX_PUSHES = 12
DEFAULT_BODY_CHARS = 1200
BOARD = "Stock"


def get_run_config(now: Optional[datetime] = None):
    if now is None:
        now = datetime.now()

    h = now.hour
    if 0 <= h < 7:
        slot = "Premarket (盤前)"
        start_time = (now - timedelta(days=1)).replace(hour=21, minute=30, second=0, microsecond=0)
        threshold = 20
    elif 7 <= h < 11:
        slot = "Morning (早盤)"
        start_time = now.replace(hour=5, minute=10, second=0, microsecond=0)
        threshold = 50
    elif 11 <= h < 16:
        slot = "Midday (盤中)"
        start_time = now.replace(hour=9, minute=30, second=0, microsecond=0)
        threshold = 50
    else:
        slot = "Evening (盤後)"
        start_time = now.replace(hour=13, minute=50, second=0, microsecond=0)
        threshold = 50

    return slot, start_time, now, threshold


def parse_ptt_date(date_str: Optional[str]) -> Optional[datetime]:
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str.strip(), "%a %b %d %H:%M:%S %Y")
    except Exception:
        return None


def parse_push_count(push_value: Any) -> int:
    if push_value is None:
        return 0
    if isinstance(push_value, int):
        return push_value
    s = str(push_value).strip()
    if not s:
        return 0
    if s == "爆":
        return 100
    if s.startswith("X"):
        return -10
    try:
        return int(s)
    except ValueError:
        return 0


def clean_article_content(raw: str, max_chars: int) -> str:
    if not raw:
        return ""

    lines = [line.rstrip() for line in raw.splitlines()]
    cleaned: List[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped == "--":
            break
        if stripped.startswith("※ 發信站:"):
            continue
        if stripped.startswith("※ 文章網址:"):
            continue
        if stripped.startswith("※ 編輯:"):
            continue
        if stripped.startswith("來自:"):
            continue
        cleaned.append(stripped)

    text = "\n".join(cleaned).strip()
    if len(text) > max_chars:
        text = text[: max_chars - 1].rstrip() + "…"
    return text


def format_pushes(comments: List[Dict[str, Any]], max_count: int = 12) -> List[str]:
    meaningful: List[str] = []
    seen = set()
    for comment in comments or []:
        c_type = str(comment.get("type", "")).upper()
        c_content = str(comment.get("content", "")).strip()
        c_author = str(comment.get("author", "")).strip()
        if c_type not in {"PUSH", "BOO"}:
            continue
        if len(c_content) < 5:
            continue
        normalized = (c_type, c_content)
        if normalized in seen:
            continue
        seen.add(normalized)
        prefix = "推" if c_type == "PUSH" else "噓"
        meaningful.append(f"{prefix} {c_author}: {c_content}")
        if len(meaningful) >= max_count:
            break
    return meaningful


def fetch_recent_posts(
    ptt_bot: PyPtt.API,
    board: str,
    start_time: datetime,
    end_time: datetime,
    threshold: int,
    max_check_count: int,
    body_chars: int,
    max_pushes: int,
) -> List[Dict[str, Any]]:
    newest_index = ptt_bot.get_newest_index(PyPtt.NewIndex.BOARD, board)
    results: List[Dict[str, Any]] = []

    for index in range(newest_index, max(newest_index - max_check_count, 0), -1):
        try:
            post = ptt_bot.get_post(board=board, index=index)
        except Exception:
            continue

        post_time = parse_ptt_date(post.get("date"))
        if post_time is None:
            continue

        if post_time < start_time:
            break
        if post_time > end_time:
            continue

        push_count = parse_push_count(post.get("push_number"))
        title = post.get("title", "")
        if push_count < threshold:
            continue
        if "公告" in title:
            continue

        results.append(
            {
                "index": post.get("index", index),
                "aid": post.get("aid", ""),
                "title": post.get("title", ""),
                "author": post.get("author", ""),
                "date": post.get("date", ""),
                "dt": post_time,
                "url": post.get("url", ""),
                "push_number": push_count,
                "content": clean_article_content(post.get("content", ""), body_chars),
                "comments": format_pushes(post.get("comments", []), max_pushes),
            }
        )

    results.sort(key=lambda x: (x["push_number"], x["dt"]), reverse=True)
    return results


def render_markdown(
    slot: str,
    start_time: datetime,
    end_time: datetime,
    threshold: int,
    checked_count: int,
    posts: List[Dict[str, Any]],
    max_posts: int,
) -> str:
    lines: List[str] = []
    lines.append("# PTT 股市版摘要資料")
    lines.append("")
    lines.append(f"- 時段：{slot}")
    lines.append(f"- 搜尋區間：{start_time.strftime('%Y-%m-%d %H:%M')} ~ {end_time.strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"- 熱門門檻：>={threshold} 推")
    lines.append(f"- 最多回看篇數：{checked_count}")
    lines.append(f"- 符合條件文章數：{len(posts)}")
    lines.append("")

    if not posts:
        lines.append("本時段未找到符合門檻的熱門文章。")
        return "\n".join(lines)

    lines.append("## 熱門文章清單")
    for idx, post in enumerate(posts[:max_posts], 1):
        lines.append(
            f"{idx}. [{post['title']}]({post['url']})｜{post['push_number']} 推｜{post['author']}｜{post['dt'].strftime('%m/%d %H:%M')}"
        )
    lines.append("")

    for idx, post in enumerate(posts[:max_posts], 1):
        lines.append(f"## {idx}. {post['title']}")
        lines.append(f"- 推文數：{post['push_number']}")
        lines.append(f"- 作者：{post['author']}")
        lines.append(f"- 發文時間：{post['dt'].strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"- 原文連結：{post['url']}")
        lines.append("")
        lines.append("### 內文重點原料")
        lines.append(post["content"] or "（內文空白或無法取得）")
        lines.append("")
        lines.append("### 推文重點原料")
        if post["comments"]:
            for comment in post["comments"]:
                lines.append(f"- {comment}")
        else:
            lines.append("- （無足夠具資訊量的推/噓文可整理）")
        lines.append("")

    lines.append("## 使用說明")
    lines.append("請根據以上原料，為最熱門的 3 個主題整理成 digest：每個主題都要同時吸收內文與推文觀點，不要只抄標題。")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch PTT Stock board posts for the current digest slot.")
    parser.add_argument("--board", default=BOARD)
    parser.add_argument("--max-check-count", type=int, default=DEFAULT_MAX_CHECK_COUNT)
    parser.add_argument("--max-posts", type=int, default=DEFAULT_MAX_POSTS)
    parser.add_argument("--max-pushes", type=int, default=DEFAULT_MAX_PUSHES)
    parser.add_argument("--body-chars", type=int, default=DEFAULT_BODY_CHARS)
    args = parser.parse_args()

    slot, start_time, end_time, threshold = get_run_config()

    if not PTT_ID or not PTT_PW:
        print("PTT_ID / PTT_PW 未設定。", file=sys.stderr)
        return 1

    ptt_bot = PyPtt.API()
    try:
        ptt_bot.login(PTT_ID, PTT_PW)
        posts = fetch_recent_posts(
            ptt_bot=ptt_bot,
            board=args.board,
            start_time=start_time,
            end_time=end_time,
            threshold=threshold,
            max_check_count=args.max_check_count,
            body_chars=args.body_chars,
            max_pushes=args.max_pushes,
        )
        print(f"目前進入看板：{args.board}", file=sys.stderr)
        print(f"搜尋到 {len(posts)} 篇符合條件熱門文章", file=sys.stderr)
        print(
            render_markdown(
                slot=slot,
                start_time=start_time,
                end_time=end_time,
                threshold=threshold,
                checked_count=args.max_check_count,
                posts=posts,
                max_posts=args.max_posts,
            )
        )
        return 0
    except Exception as e:
        print(f"PTT 摘要抓取失敗：{e}", file=sys.stderr)
        return 1
    finally:
        try:
            ptt_bot.logout()
        except Exception:
            pass


if __name__ == "__main__":
    raise SystemExit(main())
