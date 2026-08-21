import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk

#Here are some sites that could help you with the encoding/decoding:
#https://web.archive.org/web/20221107012747/https://sneekee.github.io/DLC4-Tools/tools.html
#https://rumkin.com/tools/cipher/vigenere#
#https://gc.de/gc/morse/
#https://morsecode.world/international/translator.html

MORSE_CODE = {
    ".-": "A",
    "-...": "B",
    "-.-.": "C",
    "-..": "D",
    ".": "E",
    "..-.": "F",
    "--.": "G",
    "....": "H",
    "..": "I",
    ".---": "J",
    "-.-": "K",
    ".-..": "L",
    "--": "M",
    "-.": "N",
    "---": "O",
    ".--.": "P",
    "--.-": "Q",
    ".-.": "R",
    "...": "S",
    "-": "T",
    "..-": "U",
    "...-": "V",
    ".--": "W",
    "-..-": "X",
    "-.--": "Y",
    "--..": "Z",

    "-----": "0",
    ".----": "1",
    "..---": "2",
    "...--": "3",
    "....-": "4",
    ".....": "5",
    "-....": "6",
    "--...": "7",
    "---..": "8",
    "----.": "9",

    ".-.-.-": ".",
    "--..--": ",",
    "..--..": "?",
    ".----.": "'",
    "-.-.--": "!",
    "-..-.": "/",
    "-.--.": "(",
    "-.--.-": ")",
    ".-...": "&",
    "---...": ":",
    "-.-.-.": ";",
    "-...-": "=",
    ".-.-.": "+",
    "-....-": "-",
    "..--.-": "_",
    ".-..-.": '"',
    "...-..-": "$",
    ".--.-.": "@"
}

# Reverse dictionary for converting letters into Morse code
TEXT_TO_MORSE = {
    character: morse
    for morse, character in MORSE_CODE.items()
}

def encode_morse(text: str) -> str:
    """
    Converts normal text into Morse code.

    Letters are separated by one space.
    Words are separated by a slash.
    """
    encoded_words = []

    for word in text.upper().split():
        encoded_letters = []

        for character in word:
            if character in TEXT_TO_MORSE:
                encoded_letters.append(TEXT_TO_MORSE[character])
            else:
                encoded_letters.append(character)

        encoded_words.append(" ".join(encoded_letters))

    return " / ".join(encoded_words)


def validate_key(key: str) -> str:
    """
    Validates the Vigenère cipher key.
    """
    cleaned_key = key.replace(" ", "")

    if not cleaned_key:
        raise ValueError("Please enter a cipher key.")

    if not cleaned_key.isascii() or not cleaned_key.isalpha():
        raise ValueError(
            "The cipher key may only contain letters from A to Z."
        )

    return cleaned_key.lower()


def decode_morse(morse_text: str, live_mode: bool = False) -> str:
    """
    Decodes Morse code.

    One space:
        Separates letters.

    A slash or at least two spaces:
        Separates words.
    """
    if not morse_text.strip():
        return ""

    normalized_text = morse_text

    # Normalize different dash characters
    normalized_text = normalized_text.replace("–", "-")
    normalized_text = normalized_text.replace("—", "-")
    normalized_text = normalized_text.replace("\t", " ")

    # Treat multiple spaces as word separators
    while "   " in normalized_text:
        normalized_text = normalized_text.replace("   ", " / ")

    normalized_text = normalized_text.replace("  ", " / ")

    words = normalized_text.split("/")
    decoded_words = []

    for word in words:
        symbols = word.strip().split()
        decoded_letters = []

        for symbol in symbols:
            if symbol in MORSE_CODE:
                decoded_letters.append(MORSE_CODE[symbol])
            elif live_mode:
                decoded_letters.append("?")
            else:
                raise ValueError(
                    f"Unknown Morse code sequence: {symbol}"
                )

        decoded_words.append("".join(decoded_letters))

    return " ".join(decoded_words)


def vigenere_decrypt(ciphertext: str, key: str) -> str:
    """
    Decrypts text using the classic Vigenère cipher.
    """
    key = validate_key(key)
    result = []
    key_index = 0

    for char in ciphertext:
        if char.isascii() and char.isalpha():
            base = ord("A") if char.isupper() else ord("a")

            cipher_value = ord(char) - base
            key_value = ord(key[key_index % len(key)]) - ord("a")

            decrypted_value = (cipher_value - key_value) % 26
            result.append(chr(base + decrypted_value))

            key_index += 1
        else:
            result.append(char)

    return "".join(result)


def vigenere_encrypt(plaintext: str, key: str) -> str:
    """
    Encrypts text using the classic Vigenère cipher.
    """
    key = validate_key(key)
    result = []
    key_index = 0

    for char in plaintext:
        if char.isascii() and char.isalpha():
            base = ord("A") if char.isupper() else ord("a")

            plain_value = ord(char) - base
            key_value = ord(key[key_index % len(key)]) - ord("a")

            encrypted_value = (plain_value + key_value) % 26
            result.append(chr(base + encrypted_value))

            key_index += 1
        else:
            result.append(char)

    return "".join(result)


def get_selected_key() -> str:
    """
    Returns the currently selected cipher key.
    """
    selected_key = key_selection.get()

    if selected_key == "Cross":
        return "Cross"

    if selected_key == "Archer":
        return "Archer"

    return custom_key_entry.get()


def update_key_selection(event=None) -> None:
    """
    Updates the key input field depending on the selected option.
    """
    selected_key = key_selection.get()

    custom_key_entry.config(state="normal")
    custom_key_entry.delete(0, tk.END)

    if selected_key == "Cross":
        custom_key_entry.insert(0, "Cross")
        custom_key_entry.config(state="disabled")

    elif selected_key == "Archer":
        custom_key_entry.insert(0, "Archer")
        custom_key_entry.config(state="disabled")

    else:
        custom_key_entry.config(state="normal")
        custom_key_entry.focus_set()

    update_final_result()


def update_live_morse(event=None) -> None:
    """
    Updates the Morse result after every keystroke.
    """
    morse_message = morse_input.get("1.0", "end-1c")

    decoded_message = decode_morse(
        morse_message,
        live_mode=True
    ).lower()

    morse_output.config(state="normal")
    morse_output.delete("1.0", tk.END)
    morse_output.insert("1.0", decoded_message)
    morse_output.config(state="disabled")

    vigenere_input.delete("1.0", tk.END)
    vigenere_input.insert("1.0", decoded_message)

    update_final_result()


def update_final_result(event=None) -> None:
    """
    Automatically decrypts the current message with Vigenère.
    """
    message = vigenere_input.get("1.0", "end-1c")
    key = get_selected_key()

    final_output.config(state="normal")
    final_output.delete("1.0", tk.END)

    if not message or not key.strip():
        final_output.config(state="disabled")
        return

    try:
        result = vigenere_decrypt(message, key)
        final_output.insert("1.0", result)

    except ValueError:
        final_output.insert(
            "1.0",
            "Please enter a valid cipher key."
        )

    final_output.config(state="disabled")


def encrypt_vigenere() -> None:
    """
    Encrypts the text inside the Vigenère message field.
    """
    try:
        message = vigenere_input.get("1.0", "end-1c")
        key = get_selected_key()

        if not message:
            raise ValueError("Please enter a message.")

        result = vigenere_encrypt(message, key)

        final_output.config(state="normal")
        final_output.delete("1.0", tk.END)
        final_output.insert("1.0", result)
        final_output.config(state="disabled")

    except ValueError as error:
        messagebox.showerror("Error", str(error))


def copy_result() -> None:
    """
    Copies the final result to the clipboard.
    """
    result = final_output.get("1.0", "end-1c").strip()

    if not result:
        messagebox.showinfo(
            "Information",
            "There is no final result yet."
        )
        return

    window.clipboard_clear()
    window.clipboard_append(result)
    window.update()

    messagebox.showinfo(
        "Copied",
        "The final result has been copied."
    )


def clear_all() -> None:
    """
    Clears all input and output fields.
    """
    morse_input.delete("1.0", tk.END)
    vigenere_input.delete("1.0", tk.END)

    morse_output.config(state="normal")
    morse_output.delete("1.0", tk.END)
    morse_output.config(state="disabled")

    final_output.config(state="normal")
    final_output.delete("1.0", tk.END)
    final_output.config(state="disabled")

    number_morse_output.config(state="normal")
    number_morse_output.delete("1.0", tk.END)
    number_morse_output.config(state="disabled")

    key_selection.set("Cross")
    update_key_selection()


def load_example() -> None:
    """
    Loads the example:
    Morse code -> mzzdgxvf -> killover
    """
    clear_all()

    morse_input.insert(
        "1.0",
        "-- --.. --.. -.. --. -..- ...- ..-."
    )

    key_selection.set("Cross")
    update_key_selection()
    update_live_morse()

def show_solution(solution: str, number: str) -> None:
    """
    Displays a predefined solution and automatically creates:
    - the matching Vigenère message
    - the matching Morse code
    - the selected number in Morse code
    """
    try:
        key = get_selected_key()

        # Encrypt the selected solution with the current cipher key
        encrypted_message = vigenere_encrypt(solution, key).lower()

        # Convert the encrypted message into Morse code
        message_morse_code = encode_morse(encrypted_message)

        # Convert the selected number into Morse code
        number_morse_code = encode_morse(number)

        # Display the generated Morse code
        morse_input.delete("1.0", tk.END)
        morse_input.insert("1.0", message_morse_code)

        # Display the decoded Morse result
        morse_output.config(state="normal")
        morse_output.delete("1.0", tk.END)
        morse_output.insert("1.0", encrypted_message)
        morse_output.config(state="disabled")

        # Display the encrypted Vigenère message
        vigenere_input.delete("1.0", tk.END)
        vigenere_input.insert("1.0", encrypted_message)

        # Display the final solution
        final_output.config(state="normal")
        final_output.delete("1.0", tk.END)
        final_output.insert("1.0", solution)
        final_output.config(state="disabled")

        # Display the selected number as Morse code
        number_morse_output.config(state="normal")
        number_morse_output.delete("1.0", tk.END)
        number_morse_output.insert("1.0", number_morse_code)
        number_morse_output.config(state="disabled")

    except ValueError as error:
        messagebox.showerror("Error", str(error))

# Main window
window = tk.Tk()
window.title("Morse and Vigenère Decoder")
window.geometry("800x780")
window.minsize(700, 650)

main_frame = tk.Frame(window, padx=20, pady=20)
main_frame.pack(fill=tk.BOTH, expand=True)

title_label = tk.Label(
    main_frame,
    text="Morse and Vigenère Decoder",
    font=("Arial", 20, "bold")
)
title_label.pack(pady=(0, 10))

description_label = tk.Label(
    main_frame,
    text=(
        "Morse code and Vigenère messages "
        "are decoded automatically."
    ),
    font=("Arial", 10),
    justify=tk.CENTER
)
description_label.pack(pady=(0, 20))


# Morse code section
morse_label = tk.Label(
    main_frame,
    text="1. Morse Code:",
    font=("Arial", 12, "bold")
)
morse_label.pack(anchor="w")

morse_hint = tk.Label(
    main_frame,
    text=(
        "Separate letters with one space. "
        "Separate words with / or two spaces."
    ),
    font=("Arial", 9)
)
morse_hint.pack(anchor="w", pady=(2, 5))

morse_input = scrolledtext.ScrolledText(
    main_frame,
    height=3,
    wrap=tk.WORD,
    font=("Consolas", 12)
)
morse_input.pack(fill=tk.X, pady=(0, 10))
morse_input.bind("<KeyRelease>", update_live_morse)


morse_result_label = tk.Label(
    main_frame,
    text="Morse Result:",
    font=("Arial", 11, "bold")
)
morse_result_label.pack(anchor="w")

morse_output = scrolledtext.ScrolledText(
    main_frame,
    height=3,
    wrap=tk.WORD,
    font=("Arial", 12),
    state="disabled"
)
morse_output.pack(fill=tk.X, pady=(5, 20))


# Cipher key section
key_label = tk.Label(
    main_frame,
    text="2. Cipher Key:",
    font=("Arial", 12, "bold")
)
key_label.pack(anchor="w")

key_selection = ttk.Combobox(
    main_frame,
    values=["Cross", "Archer", "Custom"],
    state="readonly",
    font=("Arial", 11)
)
key_selection.pack(fill=tk.X, pady=(5, 8))
key_selection.set("Cross")
key_selection.bind("<<ComboboxSelected>>", update_key_selection)


custom_key_label = tk.Label(
    main_frame,
    text="Cipher Key Input:",
    font=("Arial", 10)
)
custom_key_label.pack(anchor="w")

custom_key_entry = tk.Entry(
    main_frame,
    font=("Arial", 12)
)
custom_key_entry.pack(fill=tk.X, pady=(5, 15))
custom_key_entry.bind("<KeyRelease>", update_final_result)


# Vigenère message section
vigenere_label = tk.Label(
    main_frame,
    text="Vigenère Message:",
    font=("Arial", 11, "bold")
)
vigenere_label.pack(anchor="w")

vigenere_input = scrolledtext.ScrolledText(
    main_frame,
    height=3,
    wrap=tk.WORD,
    font=("Arial", 12)
)
vigenere_input.pack(fill=tk.X, pady=(5, 10))
vigenere_input.bind("<KeyRelease>", update_final_result)


# Action buttons
action_button_frame = tk.Frame(main_frame)
action_button_frame.pack(fill=tk.X, pady=(0, 8))

encrypt_button = tk.Button(
    action_button_frame,
    text="Encrypt with Vigenère",
    command=encrypt_vigenere,
    font=("Arial", 10),
    padx=12,
    pady=8
)
encrypt_button.pack(side=tk.LEFT)


solution_label = tk.Label(
    main_frame,
    text="Show Solution:",
    font=("Arial", 10, "bold")
)
solution_label.pack(anchor="w", pady=(0, 5))


solution_button_frame = tk.Frame(main_frame)
solution_button_frame.pack(fill=tk.X, pady=(0, 20))


solutions = [
    ("15 Cryptids", "killoverfifteencryptids", "fifteen"),
    ("20 Cryptids", "killovertwentycryptids", "twenty"),
    ("30 Cryptids", "killoverthirtycryptids", "thirty"),
    ("18 Cryptids", "killovereighteencryptids", "eighteen"),
    ("25 Cryptids", "killovertwentyfivecryptids", "twentyfive")
]


for button_text, solution_text, number_text in solutions:
    button = tk.Button(
        solution_button_frame,
        text=button_text,
        command=lambda solution=solution_text, number=number_text:
            show_solution(solution, number),
        font=("Arial", 10),
        padx=10,
        pady=8
    )
    button.pack(side=tk.LEFT, padx=(0, 8))


# Final result section
final_label = tk.Label(
    main_frame,
    text="Final Result:",
    font=("Arial", 12, "bold")
)
final_label.pack(anchor="w")

final_output = scrolledtext.ScrolledText(
    main_frame,
    height=3,
    wrap=tk.WORD,
    font=("Arial", 13, "bold"),
    state="disabled"
)
final_output.pack(fill=tk.BOTH, expand=True, pady=(5, 10))

number_morse_label = tk.Label(
    main_frame,
    text="Terminal input:",
    font=("Arial", 11, "bold")
)
number_morse_label.pack(anchor="w")


number_morse_output = scrolledtext.ScrolledText(
    main_frame,
    height=2,
    wrap=tk.WORD,
    font=("Consolas", 13, "bold"),
    state="disabled"
)
number_morse_output.pack(fill=tk.X, pady=(5, 10))


bottom_button_frame = tk.Frame(main_frame)
bottom_button_frame.pack(fill=tk.X)

example_button = tk.Button(
    bottom_button_frame,
    text="Load Example",
    command=load_example,
    font=("Arial", 10),
    padx=12,
    pady=7
)
example_button.pack(side=tk.LEFT)

clear_button = tk.Button(
    bottom_button_frame,
    text="Clear All",
    command=clear_all,
    font=("Arial", 10),
    padx=12,
    pady=7
)
clear_button.pack(side=tk.LEFT, padx=8)

copy_button = tk.Button(
    bottom_button_frame,
    text="Copy Final Result",
    command=copy_result,
    font=("Arial", 10, "bold"),
    padx=12,
    pady=7
)
copy_button.pack(side=tk.RIGHT)


load_example()

window.mainloop()