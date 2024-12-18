
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
from stegano import lsb
from stegano import exifHeader as aaa
from PIL import ImageTk, Image
import pyperclip

# Global variables
fileopen = None
imagee = None

def update_image_display():
    """Update the displayed image in the encoding window."""
    if fileopen:
        img = Image.open(fileopen)
        img.thumbnail((300, 300))  # Resize image to fit in the GUI
        global imagee
        imagee = ImageTk.PhotoImage(img)
        Labelimg.config(image=imagee)
        Labelimg.image = imagee  # Keep a reference to avoid garbage collection

def encode_message():
    """Encode a message in the selected image."""
    if not fileopen:
        messagebox.showwarning("Warning", "Please select an image first.")
        return

    if secimg.get() == "jpeg":
        response = messagebox.askyesno("Confirm", "Do you want to encode this message?")
        if response:
            try:
                encoded_image = aaa.hide(fileopen, entrysecmes.get())
                save_path = asksaveasfilename(defaultextension=".jpg", title="Save Encoded Image",
                                               filetypes=(("JPEG files", "*.jpg"), ("All files", "*.*")))
                if save_path:
                    encoded_image.save(save_path)
                    messagebox.showinfo("Success", f"Message successfully encoded in {save_path}!")
                else:
                    messagebox.showwarning("Warning", "Save operation was cancelled.")
            except Exception as e:
                messagebox.showerror("Error", f"Encoding failed: {str(e)}")

    elif secimg.get() == "png":
        response = messagebox.askyesno("Confirm", "Do you want to encode this message?")
        if response:
            try:
                encoded_image = lsb.hide(fileopen, message=entrysecmes.get())
                save_path = asksaveasfilename(defaultextension=".png", title="Save Encoded Image",
                                               filetypes=(("PNG files", "*.png"), ("All files", "*.*")))
                if save_path:
                    encoded_image.save(save_path)
                    messagebox.showinfo("Success", f"Message successfully encoded in {save_path}!")
                else:
                    messagebox.showwarning("Warning", "Save operation was cancelled.")
            except Exception as e:
                messagebox.showerror("Error", f"Encoding failed: {str(e)}")

def decode_message():
    """Decode a message from the selected image."""
    if not fileopen:
        messagebox.showwarning("Warning", "Please select an image first.")
        return

    try:
        if secimg.get() == "png":
            message = lsb.reveal(fileopen)
        elif secimg.get() == "jpeg":
            message = aaa.reveal(fileopen)
        else:
            message = "Please select an image format."
        
        if message:
            Label2.config(text=message)  # Display the decoded message
            pyperclip.copy(message)  # Copy decoded message to clipboard
            messagebox.showinfo("Copied", "Decoded message copied to clipboard.")
        else:
            Label2.config(text="No message found.")

    except Exception as e:
        messagebox.showerror("Error", f"Decoding failed: {str(e)}")

def open_file():
    """Open a file dialog to select an image file."""
    global fileopen
    fileopen = askopenfilename(title="Select image", filetypes=(("Image files", "*.jpg *.png"), ("All files", "*.*")))
    if fileopen:
        Labelpath.config(text=fileopen)
        update_image_display()

def create_encode_window():
    """Create a new window for encoding a message."""
    enc = Toplevel(main)
    enc.title("Encode Message")
    enc.geometry("700x500")  # Increased size for encoding window
    enc.configure(bg="#f2f2f2")
    
    LabelTitle = Label(enc, text="ENCODE", bg="red", fg="white", font=('Algerian', 32))
    LabelTitle.pack(pady=10)

    # Open file button
    Button(enc, text="Open File", command=open_file, font=('Helvetica', 14), bg="#2196F3", fg="white").pack(pady=10)

    # Radiobuttons for image type
    global secimg
    secimg = StringVar()
    Radiobutton(enc, text='JPEG', variable=secimg, value='jpeg', font=('Helvetica', 12), bg="#f2f2f2").pack()
    Radiobutton(enc, text='PNG', variable=secimg, value='png', font=('Helvetica', 12), bg="#f2f2f2").pack()

    # Entry for secret message
    global entrysecmes
    Label(enc, text="Enter message:", font=('Helvetica', 12), bg="#f2f2f2").pack()
    entrysecmes = Entry(enc, font=('Helvetica', 12), width=50)
    entrysecmes.pack(pady=5)

    # Label for the selected file path
    global Labelpath
    Labelpath = Label(enc, text="", font=('Helvetica', 12), bg="#f2f2f2")
    Labelpath.pack(pady=5)

    # Image preview
    global Labelimg
    Labelimg = Label(enc, bg="#f2f2f2")
    Labelimg.pack(pady=5)

    # Encode button
    Button(enc, text="ENCODE", command=encode_message, font=('Helvetica', 14), bg="#4CAF50", fg="white").pack(pady=20)
    
    # Back button
    Button(enc, text="Back", command=enc.destroy, font=('Helvetica', 12), bg="#f44336", fg="white").pack()

def create_decode_window():
    """Create a new window for decoding a message."""
    dec = Toplevel(main)
    dec.title("Decode Message")
    dec.geometry("700x500")  # Increased size for decoding window
    dec.configure(bg="#f2f2f2")
    
    LabelTitle = Label(dec, text="DECODE", bg="blue", fg="white", font=('Algerian', 32))
    LabelTitle.pack(pady=10)

    # Open file button
    Button(dec, text="Open File", command=open_file, font=('Helvetica', 14), bg="#2196F3", fg="white").pack(pady=10)

    # Radiobuttons for image type
    global secimg
    secimg = StringVar()
    Radiobutton(dec, text='JPEG', variable=secimg, value='jpeg', font=('Helvetica', 12), bg="#f2f2f2").pack()
    Radiobutton(dec, text='PNG', variable=secimg, value='png', font=('Helvetica', 12), bg="#f2f2f2").pack()

    # Decode button
    Button(dec, text="DECODE", command=decode_message, font=('Helvetica', 14), bg="#4CAF50", fg="white").pack(pady=20)

    # Label to display the decoded message
    global Label2
    Label2 = Label(dec, text="", font=('Helvetica', 12), wraplength=500, bg="#f2f2f2")
    Label2.pack(pady=10)

    # Back button
    Button(dec, text="Back", command=dec.destroy, font=('Helvetica', 12), bg="#f44336", fg="white").pack()

def encrypt(text, shift):
    """Encrypt the text using a simple Caesar cipher."""
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            shift_amount = shift % 26
            if char.islower():
                encrypted_text += chr((ord(char) + shift_amount - 97) % 26 + 97)
            else:
                encrypted_text += chr((ord(char) + shift_amount - 65) % 26 + 65)
        else:
            encrypted_text += char
    return encrypted_text

def decrypt(text, shift):
    """Decrypt the text using a simple Caesar cipher."""
    decrypted_text = ""
    for char in text:
        if char.isalpha():
            shift_amount = shift % 26
            if char.islower():
                decrypted_text += chr((ord(char) - shift_amount - 97) % 26 + 97)
            else:
                decrypted_text += chr((ord(char) - shift_amount - 65) % 26 + 65)
        else:
            decrypted_text += char
    return decrypted_text

def create_encryption_window():
    """Create a new window for encrypting and decrypting text."""
    enc_win = Toplevel(main)
    enc_win.title("Encrypt/Decrypt Text")
    enc_win.geometry("500x400")  # Adjusted size for encryption window
    enc_win.configure(bg="#f2f2f2")

    Label(enc_win, text="Encrypt/Decrypt Text", font=('Algerian', 20), bg="#f2f2f2").pack(pady=10)

    Label(enc_win, text="Enter text:", font=('Helvetica', 12), bg="#f2f2f2").pack(pady=5)
    text_entry = Entry(enc_win, width=40, font=('Helvetica', 12))
    text_entry.pack(pady=5)

    #Label(enc_win, text="Enter shift (1-100):", font=('Helvetica', 12), bg="#f2f2f2").pack(pady=5)
    Label(enc_win, text="Enter code (1-100):", font=('Helvetica', 12), bg="#f2f2f2").pack(pady=5)

    _shift = Entry(enc_win, width=5, font=('Helvetica', 12))
    _shift.pack(pady=5)

    def encrypt_text():
        """Handle text encryption."""
        text = text_entry.get()
        shift = int(_shift.get())
        encrypted = encrypt(text, shift)
        result_label.config(text=encrypted)
        pyperclip.copy(encrypted)
        messagebox.showinfo("Copied", "Encrypted message copied to clipboard.")

    def decrypt_text():
        """Handle text decryption."""
        text = text_entry.get()
        shift = int(_shift.get())
        decrypted = decrypt(text, shift)
        result_label.config(text=decrypted)
        pyperclip.copy(decrypted)
        messagebox.showinfo("Copied", "Decrypted message copied to clipboard.")

    Button(enc_win, text="Encrypt", command=encrypt_text, font=('Helvetica', 14), bg="#4CAF50", fg="white").pack(pady=10)
    Button(enc_win, text="Decrypt", command=decrypt_text, font=('Helvetica', 14), bg="#f44336", fg="white").pack(pady=10)

    result_label = Label(enc_win, text="", font=('Helvetica', 12), wraplength=500, bg="#f2f2f2")
    result_label.pack(pady=10)

    Button(enc_win, text="Back", command=enc_win.destroy, font=('Helvetica', 12), bg="#008CBA", fg="white").pack(pady=10)

# Main window setup
main = Tk()
main.title("Image Steganography Application")
main.geometry("600x400")  # Increased height for the main window
main.configure(bg="#f2f2f2")

Label(main, text="Steganography and Encryption, Decryption Application", font=('Algerian', 22), bg="#f2f2f2").pack(pady=20)

Button(main, text="  Encode Message  ", command=create_encode_window, font=('Helvetica', 14), bg="#4CAF50", fg="white").pack(pady=10)
Button(main, text="  Decode Message  ", command=create_decode_window, font=('Helvetica', 14), bg="#f44336", fg="white").pack(pady=10)
Button(main, text="Encrypt/Decrypt Text", command=create_encryption_window, font=('Helvetica', 14), bg="#008CBA", fg="white").pack(pady=10)

# Exit button
Button(main, text="Exit", command=main.destroy, font=('Helvetica', 14), bg="#f44336", fg="white").pack(pady=20)

main.mainloop()
