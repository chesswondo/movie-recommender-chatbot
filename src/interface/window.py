import tkinter as tk
from typing import Callable

class ChatWindow:
    """Class for implementing window interface using tkinter."""

    def __init__(self,
                 root: tk.Tk,
                 generate_answer: Callable[[str], str]) -> None:
        """
        Initializes an instance of ChatWindow.

        : param root: (tk.Tk) - a main window.
        : param generate_answer: (Callable[[str], str]) - an answer generation function.

        : return: (None) - this function does not return any value.
        """
        self._root = root
        self._root.title("Movie recommendation agent")
        self._generate_answer = generate_answer
        
        # Create a frame for the text area and scrollbar
        self._text_frame = tk.Frame(root)
        self._text_frame.pack(padx=10, pady=10)

        # Create a text widget for displaying messages
        self._text_area = tk.Text(self._text_frame, wrap=tk.WORD, state=tk.DISABLED, height=20, width=50)
        self._text_area.pack(side=tk.LEFT, padx=(0, 10))

        # Add a scrollbar to the text widget
        self._scrollbar = tk.Scrollbar(self._text_frame, command=self._text_area.yview)
        self._scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self._text_area['yscrollcommand'] = self._scrollbar.set

        # Create a frame for the entry field and send button
        self._entry_frame = tk.Frame(root)
        self._entry_frame.pack(padx=10, pady=(0, 10))

        # Create an entry widget for user input
        self._entry_field = tk.Entry(self._entry_frame, width=40)
        self._entry_field.pack(side=tk.LEFT, padx=(0, 10))

        # Bind the Enter key to the send_message method
        self._entry_field.bind("<Return>", self._send_message)

        # Create a button to send the message
        self._send_button = tk.Button(self._entry_frame, text="Send", command=self._send_message)
        self._send_button.pack(side=tk.LEFT)

    def _send_message(self, event=None) -> None:
        """A function that sends a message."""

        # Get the text from the entry field
        message = self._entry_field.get()

        # If the message is not empty, display it in the text area
        if message.strip():
            self._text_area.config(state=tk.NORMAL)
            self._text_area.insert(tk.END, "User: " + message + "\n\n")
            self._text_area.config(state=tk.DISABLED)
            self._text_area.see(tk.END)

            # Clear the entry field
            self._entry_field.delete(0, tk.END)

            # Generate and display answer
            answer = self._generate_answer(message).strip()
            self._text_area.config(state=tk.NORMAL)
            self._text_area.insert(tk.END, "Agent: " + answer + "\n\n\n")
            self._text_area.config(state=tk.DISABLED)
            self._text_area.see(tk.END)