import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import smtplib
from email.message import EmailMessage
import os

# ======================
# EMAIL SETTINGS
# ======================
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "APP_PASSWORD_HERE"  # App Password

# ======================
# SEND EMAIL FUNCTION
# ======================
def send_email():
    to_email = email_entry.get()
    subject = subject_entry.get()
    body = message_text.get("1.0", tk.END).strip()

    if not to_email or not body:
        messagebox.showerror("Error", "Email and message are required")
        return

    msg = EmailMessage()
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    # Attachment
    if attached_file:
        with open(attached_file, "rb") as f:
            file_data = f.read()
            file_name = os.path.basename(attached_file)

        msg.add_attachment(
            file_data,
            maintype="application",
            subtype="octet-stream",
            filename=file_name
        )

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        messagebox.showinfo("Success", "Email sent successfully ✅")
        clear_fields()

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ======================
# ATTACH FILE
# ======================
attached_file = None

def attach_file():
    global attached_file
    attached_file = filedialog.askopenfilename()
    if attached_file:
        file_label.config(text=os.path.basename(attached_file))

def clear_fields():
    email_entry.delete(0, tk.END)
    subject_entry.delete(0, tk.END)
    message_text.delete("1.0", tk.END)
    file_label.config(text="No file attached")

# ======================
# TKINTER UI
# ======================
root = tk.Tk()
root.title("Email Sender")
root.geometry("400x700")
root.resizable(False, False)

style = ttk.Style()
style.theme_use("clam")

frame = ttk.Frame(root, padding=20)
frame.pack(expand=True, fill="both")

title = ttk.Label(frame, text="📧 Send Email", font=("Arial", 16))
title.pack(pady=10)

# Email To
ttk.Label(frame, text="To Email").pack(anchor="w")
email_entry = ttk.Entry(frame)
email_entry.pack(fill="x", pady=5)

# Subject
ttk.Label(frame, text="Subject").pack(anchor="w")
subject_entry = ttk.Entry(frame)
subject_entry.pack(fill="x", pady=5)

# Message
ttk.Label(frame, text="Message").pack(anchor="w")
message_text = tk.Text(frame, height=10)
message_text.pack(fill="both", pady=5)

# Attachment
attach_btn = ttk.Button(frame, text="Attach File", command=attach_file)
attach_btn.pack(pady=5)

file_label = ttk.Label(frame, text="No file attached", foreground="gray")
file_label.pack()

# Send Button
send_btn = ttk.Button(frame, text="Send Email", command=send_email)
send_btn.pack(pady=15)

root.mainloop()
