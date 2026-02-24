"""app/views/quit.py — Shutdown view."""
import os
import time
import threading

def render_quit() -> str:
    def shutdown():
        time.sleep(1)
        print("  [SYSTEM] Shutting down server...")
        os._exit(0)

    threading.Thread(target=shutdown, daemon=True).start()

    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Disconnecting...</title>
    <style>
        body {
            background: #040a16;
            color: #00e5ff;
            font-family: 'Courier New', monospace;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
            overflow: hidden;
        }
        .msg {
            text-align: center;
            border: 1px solid #00e5ff;
            padding: 40px;
            box-shadow: 0 0 20px rgba(0, 229, 255, 0.2);
        }
    </style>
</head>
<body>
    <div class="msg">
        <h2>TERMINATING CONNECTION...</h2>
        <p>Server process is shutting down.</p>
        <p style="color: #666; font-size: 12px;">You may close this tab.</p>
    </div>
</body>
</html>
"""
