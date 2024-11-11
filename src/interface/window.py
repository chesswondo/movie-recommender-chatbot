import tkinter as tk
from typing import Callable

class ChatWindow:
    def __init__(self, root, generate_answer: Callable[[str], str]):
        self.root = root
        self.root.title("Movie recommendation chatbot")
        self.generate_answer = generate_answer
        
        # Create a frame for the text area and scrollbar
        self.text_frame = tk.Frame(root)
        self.text_frame.pack(padx=10, pady=10)

        # Create a text widget for displaying messages
        self.text_area = tk.Text(self.text_frame, wrap=tk.WORD, state=tk.DISABLED, height=20, width=50)
        self.text_area.pack(side=tk.LEFT, padx=(0, 10))

        # Add a scrollbar to the text widget
        self.scrollbar = tk.Scrollbar(self.text_frame, command=self.text_area.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area['yscrollcommand'] = self.scrollbar.set

        # Create a frame for the entry field and send button
        self.entry_frame = tk.Frame(root)
        self.entry_frame.pack(padx=10, pady=(0, 10))

        # Create an entry widget for user input
        self.entry_field = tk.Entry(self.entry_frame, width=40)
        self.entry_field.pack(side=tk.LEFT, padx=(0, 10))

        # Bind the Enter key to the send_message method
        self.entry_field.bind("<Return>", self.send_message)

        # Create a button to send the message
        self.send_button = tk.Button(self.entry_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT)

    def send_message(self, event=None):
        
        # Get the text from the entry field
        message = self.entry_field.get()

        # If the message is not empty, display it in the text area
        if message.strip():
            self.text_area.config(state=tk.NORMAL)
            self.text_area.insert(tk.END, "User: " + message + "\n\n")
            self.text_area.config(state=tk.DISABLED)
            self.text_area.see(tk.END)

            # Clear the entry field
            self.entry_field.delete(0, tk.END)

            # Generate and display answer
            answer = self.generate_answer(message).strip()
            self.text_area.config(state=tk.NORMAL)
            self.text_area.insert(tk.END, "Bot: " + answer + "\n\n\n")
            self.text_area.config(state=tk.DISABLED)
            self.text_area.see(tk.END)