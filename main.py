"""
Frame Detective — PresentMon Learning Game
==========================================
Entry point. Run:  python main.py
Opens the game in your default browser via a local HTTP server.
Requires Python 3.6+. No external packages needed.
"""

from app.server import Server


def main():
    server = Server(port=0)   # port=0 → OS picks a free port
    server.run()


if __name__ == "__main__":
    main()
