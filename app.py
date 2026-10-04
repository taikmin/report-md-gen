"""업무보고 md 생성기 — Flask 로컬 서버 (Claude CLI 호출 방식)."""
import os
import shutil
import subprocess
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

from prompts import MONTHLY_PROMPT, WEEKLY_PROMPT

app = Flask(__name__, static_folder="static", static_url_path="")


def resolve_claude_cli() -> str:
    for name in ("claude", "claude.cmd", "claude.exe"):
        path = shutil.which(name)
        if path:
            return path
    raise RuntimeError(
        "claude CLI를 찾을 수 없습니다. Claude Code가 설치되어 있고 PATH에 등록되어 있어야 합니다."
    )


def call_claude_cli(system_prompt: str, user_text: str, timeout: int = 300) -> str:
    cli = resolve_claude_cli()
    cmd = [
        cli,
        "-p",
        "--append-system-prompt", system_prompt,
        "--max-turns", "1",
        user_text,
    ]
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )
    if result.returncode != 0:
        err = (result.stderr or result.stdout or "").strip()
        raise RuntimeError(f"claude CLI 실패 (exit={result.returncode}): {err[:500]}")
    return (result.stdout or "").strip()


@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.post("/api/generate")
def generate():
    data = request.get_json(silent=True) or {}
    report_type = data.get("type")
    text = (data.get("text") or "").strip()

    if report_type not in ("weekly", "monthly"):
        return jsonify({"error": "type은 'weekly' 또는 'monthly' 이어야 합니다."}), 400
    if not text:
        return jsonify({"error": "입력 내용이 비어 있습니다."}), 400

    system_prompt = WEEKLY_PROMPT if report_type == "weekly" else MONTHLY_PROMPT

    try:
        output = call_claude_cli(system_prompt, text)
        return jsonify({"output": output})
    except subprocess.TimeoutExpired:
        return jsonify({"error": "claude CLI 응답 시간 초과 (5분)."}), 504
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"호출 실패: {e}"}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
