from flask import Flask, render_template_string
import tkinter as tk
from tkinter import ttk
from threading import Thread

# -----------------------
# Flask Web Server
# -----------------------
app = Flask(__name__)
messages = []

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Incoming Messages</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="1">
<style>
body {
    font-family: Arial, sans-serif;
    background: #f2f2f2;
    padding: 20px;
}
.container {
    background: white;
    border-radius: 10px;
    padding: 20px;
}
.message {
    background: #e6f0ff;
    margin: 10px 0;
    padding: 10px;
    border-radius: 6px;
}
</style>
</head>
<body>
<div class="container">
<h2>📩 Messages from Mac</h2>
{% for msg in messages %}
<div class="message">{{ msg }}</div>
{% endfor %}
</div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_PAGE, messages=messages)

def run_server():
    app.run(host="0.0.0.0", port=8000)

# -----------------------
# Tkinter UI (Mac)
# -----------------------
def send_message():
    msg = message_entry.get()
    if msg.strip():
        messages.append(msg)
        message_entry.delete(0, tk.END)

root = tk.Tk()
root.title("Mac → iPhone Messenger")
root.geometry("400x800")
root.resizable(False, False)

style = ttk.Style()
style.theme_use("clam")

frame = ttk.Frame(root, padding=20)
frame.pack(expand=True, fill="both")

title = ttk.Label(frame, text="Send Message to iPhone", font=("Arial", 16))
title.pack(pady=10)

message_entry = ttk.Entry(frame, font=("Arial", 12))
message_entry.pack(fill="x", pady=10)

send_btn = ttk.Button(frame, text="Send", command=send_message)
send_btn.pack(pady=10)

status = ttk.Label(frame, text="Server running on port 8000", foreground="green")
status.pack()

Thread(target=run_server, daemon=True).start()
root.mainloop()
