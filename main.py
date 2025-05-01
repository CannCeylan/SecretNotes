from tkinter import *
from tkinter import messagebox
from cryptography.fernet import Fernet
import base64
import hashlib
import os

window = Tk()
window.title("Secret Notes")
window.minsize(300, 300)

def generate_key(password):
    key = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(key)

def encrypt():
    try:
        title = entry_title.get().strip()
        note = text_secret.get("1.0", END).strip()
        password = entry_key.get().strip()

        if not title or not password or not note:
            raise ValueError("Başlık, içerik ve anahtar boş olamaz.")

        key = generate_key(password)
        fernet = Fernet(key)
        encrypted = fernet.encrypt(note.encode()).decode()

        text_secret.delete("1.0", END)
        text_secret.insert("1.0", encrypted)


        desktop = os.path.expanduser("~/Desktop")
        folder = os.path.join(desktop, "Secret Notes")
        os.makedirs(folder, exist_ok=True)


        filepath = os.path.join(folder, f"{title}.txt")
        with open(filepath, "w") as file:
            file.write(encrypted)

        messagebox.showinfo("Başarılı", f"Not şifrelendi ve '{filepath}' konumuna kaydedildi!")

    except Exception as e:
        messagebox.showerror("Hata", f"Şifreleme hatası: {str(e)}")

def decrypt():
    try:
        encrypted_note = text_secret.get("1.0", END).strip()
        password = entry_key.get().strip()

        if not encrypted_note or not password:
            raise ValueError("Şifreli metin ve anahtar boş olamaz.")

        key = generate_key(password)
        fernet = Fernet(key)
        decrypted = fernet.decrypt(encrypted_note.encode()).decode()

        text_secret.delete("1.0", END)
        text_secret.insert("1.0", decrypted)
        messagebox.showinfo("Başarılı", "Not başarıyla çözüldü!")

    except Exception as e:
        messagebox.showerror("Hata", f"Çözme hatası: {str(e)}")


Label(window, text="Enter your title").pack()
entry_title = Entry(window)
entry_title.pack()

Label(window, text="Enter your secret / encrypted message").pack()
text_secret = Text(window, height=6)
text_secret.pack()

Label(window, text="Enter your key").pack()
entry_key = Entry(window, show="*")
entry_key.pack()

Button(window, text="Save & Encrypt", command=encrypt).pack(pady=5)
Button(window, text="Decrypt", command=decrypt).pack(pady=5)

window.mainloop()


