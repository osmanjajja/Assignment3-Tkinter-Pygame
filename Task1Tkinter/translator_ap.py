import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import threading
import os
import webbrowser
import pyttsx3
from PIL import Image, ImageTk
from googletrans import Translator
from gtts import gTTS
from playsound import playsound
import tempfile

# multiple inheritance: Create a Mixin class for utility methods


class UtilityMixin:
    """Mixin for utility methods like tooltips."""

    def create_tooltip(self, widget, text):
        """Creates a tooltip for a given widget."""
        tooltip = tk.Toplevel(widget)
        tooltip.wm_overrideredirect(True)
        tooltip_label = ttkb.Label(tooltip, text=text, bootstyle="info")
        tooltip_label.pack()
        tooltip.withdraw()

        def enter(event):
            x = event.x_root + 20
            y = event.y_root + 20
            tooltip.wm_geometry(f"+{x}+{y}")
            tooltip.deiconify()

        def leave(event):
            tooltip.withdraw()

        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)

# The main class with multiple inheritance


class TranslatorApp(ttkb.Window, UtilityMixin):  # Multiple inheritance
    def __init__(self):
        super().__init__(title="Translation Application", themename="superhero")
        self.geometry("1200x800")
        self.resizable(True, True)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Encapsulation example: engine, voices, history, and favorites are private properties
        self.__engine = pyttsx3.init()
        self.__voices = self.__engine.getProperty('voices')
        self.__load_icons()
        self.__setup_ui()
        self.__history = []  # Private (Encapsulated) history
        self.__favorites = []  # Private (Encapsulated) favorites
        self.translator = Translator()

    def __load_icons(self):
        """Loads icons for the buttons (private method)."""
        self.icons = {}
        icon_names = ['translate', 'speak', 'copy', 'save',
                      'share', 'open_file', 'exit', 'about', 'favorite']
        for name in icon_names:
            try:
                image = Image.open(f'icons/{name}.png').resize((24, 24))
                self.icons[name] = ImageTk.PhotoImage(image)
            except FileNotFoundError:
                # Use a default or empty image if the icon is not found
                self.icons[name] = None
                print(f"Icon not found: {name}.png")

    def __setup_ui(self):
        """Sets up the UI components (comboboxes, text areas, buttons)."""
        self.languages = {
            'Auto-Detect': 'auto',
            'Afrikaans': 'af',
            'Arabic': 'ar',
            'Chinese (Simplified)': 'zh-cn',
            'Chinese (Traditional)': 'zh-tw',
            'English': 'en',
            'French': 'fr',
            'German': 'de',
            'Hindi': 'hi',
            'Japanese': 'ja',
            'Portuguese': 'pt',
            'Russian': 'ru',
            'Spanish': 'es',
            'Urdu': 'ur',

        }

        # Configure grid weights for responsiveness
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        # Source Language Combobox
        self.source_lang_var = tk.StringVar(value='Auto-Detect')
        self.source_lang_cb = ttkb.Combobox(self, textvariable=self.source_lang_var,
                                            values=list(self.languages.keys()), state='readonly', width=30)
        self.source_lang_cb.grid(
            row=0, column=0, padx=10, pady=10, sticky='ew')

        # Target Language Combobox
        self.target_lang_var = tk.StringVar(value='English')
        self.target_lang_cb = ttkb.Combobox(self, textvariable=self.target_lang_var,
                                            values=list(self.languages.keys())[1:], state='readonly', width=30)
        self.target_lang_cb.grid(
            row=0, column=1, padx=10, pady=10, sticky='ew')

        # Source Text
        self.source_text = tk.Text(
            self, height=15, wrap=WORD, font=('Helvetica', 12))
        self.source_text.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        # Translated Text
        self.translated_text = tk.Text(
            self, height=15, wrap=WORD, font=('Helvetica', 12))
        self.translated_text.grid(
            row=1, column=1, padx=10, pady=10, sticky='nsew')

        # Buttons Frame
        self.button_frame = ttkb.Frame(self)
        self.button_frame.grid(row=2, column=0, columnspan=2, pady=10)

        # Translate Button
        icon_translate = self.icons.get('translate')
        self.translate_btn = ttkb.Button(
            self.button_frame, text="Translate", command=self.translate_text, bootstyle="primary",
            image=icon_translate, compound=LEFT)
        self.translate_btn.grid(row=0, column=0, padx=5)
        self.create_tooltip(self.translate_btn, "Click to translate the text")

        # Text-to-Speech Buttons
        icon_speak = self.icons.get('speak')
        self.tts_source_btn = ttkb.Button(
            self.button_frame, text="Speak Source", command=self.speak_source_text, bootstyle="info",
            image=icon_speak, compound=LEFT)
        self.tts_source_btn.grid(row=0, column=1, padx=5)
        self.create_tooltip(self.tts_source_btn, "Speak the source text")

        self.tts_translated_btn = ttkb.Button(
            self.button_frame, text="Speak Translated", command=self.speak_translated_text, bootstyle="info",
            image=icon_speak, compound=LEFT)
        self.tts_translated_btn.grid(row=0, column=2, padx=5)
        self.create_tooltip(self.tts_translated_btn,
                            "Speak the translated text")

        # Copy, Save, and Share Buttons
        icon_copy = self.icons.get('copy')
        self.copy_btn = ttkb.Button(
            self.button_frame, text="Copy", command=self.copy_text, bootstyle="secondary",
            image=icon_copy, compound=LEFT)
        self.copy_btn.grid(row=0, column=3, padx=5)
        self.create_tooltip(self.copy_btn, "Copy the translated text")

        icon_save = self.icons.get('save')
        self.save_btn = ttkb.Button(
            self.button_frame, text="Save", command=self.save_translation, bootstyle="success",
            image=icon_save, compound=LEFT)
        self.save_btn.grid(row=0, column=4, padx=5)
        self.create_tooltip(self.save_btn, "Save the translation to a file")

        icon_share = self.icons.get('share')
        self.share_btn = ttkb.Button(
            self.button_frame, text="Share", command=self.share_translation, bootstyle="warning",
            image=icon_share, compound=LEFT)
        self.share_btn.grid(row=0, column=5, padx=5)
        self.create_tooltip(self.share_btn, "Share the translation via email")

        icon_favorite = self.icons.get('favorite')
        self.favorite_btn = ttkb.Button(
            self.button_frame, text="Add to Favorites", command=self.add_to_favorites, bootstyle="danger",
            image=icon_favorite, compound=LEFT)
        self.favorite_btn.grid(row=0, column=6, padx=5)
        self.create_tooltip(self.favorite_btn,
                            "Add the translation to favorites")

        # Menu Bar
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        # File Menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        icon_open_file = self.icons.get('open_file')
        file_menu.add_command(
            label="Open File", command=self.upload_file, image=icon_open_file, compound=LEFT)
        file_menu.add_separator()
        icon_exit = self.icons.get('exit')
        file_menu.add_command(
            label="Exit", command=self.on_closing, image=icon_exit, compound=LEFT)

        # History Menu
        history_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="History", menu=history_menu)
        history_menu.add_command(label="View History",
                                 command=self.view_history)
        history_menu.add_command(
            label="Clear History", command=self.clear_history)

        # Favorites Menu
        favorites_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Favorites", menu=favorites_menu)
        favorites_menu.add_command(
            label="View Favorites", command=self.view_favorites)
        favorites_menu.add_command(
            label="Clear Favorites", command=self.clear_favorites)

        # Help Menu
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)
        icon_about = self.icons.get('about')
        help_menu.add_command(
            label="About", command=self.show_about, image=icon_about, compound=LEFT)

    # Overriding the method to change its behavior
    def translate_text(self):
        """Translates text from source to target language."""
        src_lang = self.languages[self.source_lang_var.get()]
        dest_lang = self.languages[self.target_lang_var.get()]
        text = self.source_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning(
                "Input Error", "Please enter text to translate.")
            return

        # Disable the translate button to prevent multiple clicks
        self.translate_btn.config(state=DISABLED)

        # Use threading to prevent the GUI from freezing
        threading.Thread(target=self.__translate_thread,
                         args=(text, src_lang, dest_lang)).start()

    def __translate_thread(self, text, src_lang, dest_lang):
        """Handles translation in a separate thread (Encapsulated)."""
        try:
            # Call the translation API
            translated_text = self.call_translation_api(
                text, src_lang, dest_lang)
            self.translated_text.delete("1.0", tk.END)
            self.translated_text.insert(tk.END, translated_text)

            # Save to history
            self.__history.append({
                'source_text': text,
                'translated_text': translated_text,
                'source_lang': self.source_lang_var.get(),
                'target_lang': self.target_lang_var.get()
            })

            # Re-enable the translate button
            self.translate_btn.config(state=NORMAL)
        except Exception as e:
            self.translate_btn.config(state=NORMAL)
            messagebox.showerror("Translation Error", str(e))

    #  static method and multiple decorators
    @staticmethod
    def call_translation_api(text, src_lang, dest_lang):
        """Calls the translation API."""
        translator = Translator()
        result = translator.translate(text, src=src_lang, dest=dest_lang)
        return result.text

    # Polymorphism: Methods to speak different texts (source and translated)
    def speak_source_text(self):
        """Speaks the source text."""
        text = self.source_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Text-to-Speech", "No text to speak.")
            return
        threading.Thread(target=self.__speak_thread, args=(text,)).start()

    def speak_translated_text(self):
        """Speaks the translated text."""
        text = self.translated_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Text-to-Speech", "No text to speak.")
            return
        threading.Thread(target=self.__speak_thread, args=(text,)).start()

    def __speak_thread(self, text):
        """Thread to handle speaking text."""
        try:
            # Set the selected voice
            selected_voice_name = self.voice_var.get()
            for voice in self.__voices:
                if voice.name == selected_voice_name:
                    self.__engine.setProperty('voice', voice.id)
                    break
            # Speak the text
            self.__engine.say(text)
            self.__engine.runAndWait()
        except Exception as e:
            messagebox.showerror("Text-to-Speech Error", str(e))

    def copy_text(self):
        """Copies the translated text to the clipboard."""
        translated_text = self.translated_text.get("1.0", tk.END).strip()
        if not translated_text:
            messagebox.showwarning("Copy", "No translated text to copy.")
            return
        self.clipboard_clear()
        self.clipboard_append(translated_text)
        messagebox.showinfo("Copy", "Translated text copied to clipboard.")

    def save_translation(self):
        """Saves the translated text to a file."""
        translated_text = self.translated_text.get("1.0", tk.END).strip()
        if not translated_text:
            messagebox.showwarning("Save Error", "No translated text to save.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[
                                                     ("Text Files", "*.txt")],
                                                 title="Save Translation")
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write("Source Language: " +
                               self.source_lang_var.get() + "\n")
                    file.write("Target Language: " +
                               self.target_lang_var.get() + "\n\n")
                    file.write(
                        "Source Text:\n" + self.source_text.get("1.0", tk.END).strip() + "\n\n")
                    file.write("Translated Text:\n" + translated_text)
                messagebox.showinfo("Save", "Translation saved successfully.")
            except Exception as e:
                messagebox.showerror("Save Error", str(e))

    def share_translation(self):
        """Shares the translated text via email."""
        translated_text = self.translated_text.get("1.0", tk.END).strip()
        if not translated_text:
            messagebox.showwarning(
                "Share Error", "No translated text to share.")
            return
        subject = "Translated Text"
        body = translated_text
        url = f"mailto:?subject={subject}&body={body}"
        webbrowser.open(url)

    def add_to_favorites(self):
        """Adds the translation to favorites."""
        source_text = self.source_text.get("1.0", tk.END).strip()
        translated_text = self.translated_text.get("1.0", tk.END).strip()
        if not translated_text:
            messagebox.showwarning(
                "Favorites", "No translated text to add to favorites.")
            return
        self.__favorites.append({
            'source_text': source_text,
            'translated_text': translated_text,
            'source_lang': self.source_lang_var.get(),
            'target_lang': self.target_lang_var.get()
        })
        messagebox.showinfo("Favorites", "Translation added to favorites.")

    def upload_file(self):
        """Uploads a text file for translation."""
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")],
                                               title="Open Text File")
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    self.source_text.delete("1.0", tk.END)
                    self.source_text.insert(tk.END, content)
            except Exception as e:
                messagebox.showerror("File Error", str(e))

    def view_history(self):
        """Displays the translation history."""
        if not self.__history:
            messagebox.showinfo("History", "No history available.")
            return
        self.__display_records(self.__history, "Translation History")

    def clear_history(self):
        """Clears the translation history."""
        if messagebox.askyesno("Clear History", "Are you sure you want to clear the history?"):
            self.__history.clear()
            messagebox.showinfo("History", "History cleared.")

    def view_favorites(self):
        """Displays the favorites list."""
        if not self.__favorites:
            messagebox.showinfo("Favorites", "No favorites available.")
            return
        self.__display_records(self.__favorites, "Favorites")

    def clear_favorites(self):
        """Clears the favorites list."""
        if messagebox.askyesno("Clear Favorites", "Are you sure you want to clear the favorites?"):
            self.__favorites.clear()
            messagebox.showinfo("Favorites", "Favorites cleared.")

    def __display_records(self, records, title):
        """Displays the records in a table."""
        window = ttkb.Toplevel(self)
        window.title(title)
        window.geometry("800x400")
        window.resizable(False, False)

        columns = ('Source Language', 'Target Language',
                   'Source Text', 'Translated Text')
        tree = ttkb.Treeview(window, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150 if col !=
                        'Source Text' and col != 'Translated Text' else 250)

        tree.pack(fill=BOTH, expand=True)

        for item in records:
            tree.insert('', END, values=(
                item['source_lang'], item['target_lang'], item['source_text'], item['translated_text']))

    def show_about(self):
        """Displays the 'About' information."""
        messagebox.showinfo(
            "About", "Translation Application\nVersion 1.0")

    def on_closing(self):
        """Handles the closing event."""
        self.__engine.stop()
        self.destroy()


if __name__ == "__main__":
    app = TranslatorApp()
    app.mainloop()
