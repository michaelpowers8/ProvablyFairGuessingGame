import os
import hmac
import json
import secrets
import string
import hashlib
from math import exp, floor
from time import sleep
from turtle import Turtle,Screen,_Screen, bgcolor, width
from tkinter import Tk,Label,Button,Entry,Canvas

def generate_server_seed():
    possible_characters:str = string.hexdigits
    seed:str = "".join([secrets.choice(possible_characters) for _ in range(64)])
    return seed

def generate_client_seed():
    possible_characters:str = string.hexdigits
    seed:str = "".join([secrets.choice(possible_characters) for _ in range(20)])
    return seed

def sha256_encrypt(input_string: str) -> str:
    # Create a sha256 hash object
    sha256_hash = hashlib.sha256()
    
    # Update the hash object with the bytes of the input string
    sha256_hash.update(input_string.encode('utf-8'))
    
    # Return the hexadecimal representation of the hash
    return sha256_hash.hexdigest()

def seeds_to_hexadecimals(server_seed:str,client_seed:str,nonce:int) -> list[str]:
    messages:list[str] = [f"{client_seed}:{nonce}:{x}" for x in range(1)]
    hmac_objs:list[hmac.HMAC] = [hmac.new(server_seed.encode(),message.encode(),hashlib.sha256) for message in messages]
    return [hmac_obj.hexdigest() for hmac_obj in hmac_objs]

def hexadecimal_to_bytes(hexadecimal:str) -> list[int]:
    return list(bytes.fromhex(hexadecimal))

def bytes_to_number(bytes_list: list[int],multiplier:int) -> int:
    # Calculate a weighted index based on the first four bytes
    number:float =  (
                        (float(bytes_list[0]) / float(256**1)) +
                        (float(bytes_list[1]) / float(256**2)) +
                        (float(bytes_list[2]) / float(256**3)) +
                        (float(bytes_list[3]) / float(256**4))
                    )
    number = number*multiplier
    return floor(number)+1 

def seeds_to_results(server_seed:str,client_seed:str,nonce:int) -> str:
    hexs = seeds_to_hexadecimals(server_seed=server_seed,client_seed=client_seed,nonce=nonce)
    bytes_lists:list[list[int]] = [hexadecimal_to_bytes(current_hex) for current_hex in hexs]
    row:list[list[int]] = []
    for bytes_list in bytes_lists:
        for index in range(0,len(bytes_list),4):
            row.append(bytes_to_number(bytes_list[index:index+4],100))
            if(len(row)==1):
                return row[0]

def write_seeds_to_screen(server_hashed:str, client:str, nonce:int, writer:Turtle, screen:_Screen,font:tuple[str,int,str]):
    screen.tracer(False)
    writer.penup()
    writer.goto(0,(screen.window_height()//3))
    writer.write(f"Server (Hashed): {server_hashed}\nClient Seed: {client}\nNonce: {str(nonce)}",font=font,align="center")
    screen.update()

def clear_seeds_from_screen(writer:Turtle, screen:_Screen):
    screen.tracer(False)
    writer.clear()
    screen.update()

def destroy_difficulty_buttons(easy:Button,medium:Button,hard:Button,expert:Button):
    easy.destroy()
    medium.destroy()
    hard.destroy()
    expert.destroy()

def create_play_button(canvas: Canvas, font: tuple[str, int, str], nonce: int, 
                      screen: _Screen, seed_writer_turtle: Turtle, 
                      server_hashed: str, client: str, server: str,
                      feedback_label: Label, guess_label: Label):
    play_button = Button(canvas.master, text="PLAY", font=("Arial",60,"bold"), bg="green", fg="white")
    play_button.place(relx=0.45, rely=0.5, anchor="center")
    
    def play_again():
        # Clear previous game's UI elements
        play_button.destroy()
        feedback_label.config(text="")
        guess_label.config(text="")
        clear_seeds_from_screen(seed_writer_turtle, screen)
        
        # Start new game with incremented nonce
        new_nonce = nonce + 1
        write_seeds_to_screen(server_hashed, client, new_nonce, seed_writer_turtle, screen, font)
        make_difficulty_buttons(
            canvas, font, seeds_to_results(server, client, new_nonce),
            new_nonce, screen, seed_writer_turtle, server_hashed, client, server)
    
    play_button.configure(command=play_again)

def check_guess(button: Button, buttons: list[Button], number: int, answer: int, 
                remaining_guesses: list[int], guess_label: Label, feedback_label: Label,
                canvas: Canvas, font: tuple[str, int, str], nonce: int, screen: _Screen,
                seed_writer_turtle: Turtle, server_hashed: str, client: str, server: str):
    remaining_guesses[0] -= 1
    guess_label.config(text=f"Guesses left: {remaining_guesses[0]}")

    # Provide high/low feedback
    if number < answer:
        feedback_label.config(text=f"{number} is Too Low!", fg="red")
    elif number > answer:
        feedback_label.config(text=f"{number} is Too High!", fg="red")
    
    if number == answer:
        for inner_button in buttons:
            inner_button.destroy()
        feedback_label.config(text=f"You Win! The number was {answer}.", fg="green")
        create_play_button(canvas, font, nonce, screen, seed_writer_turtle, 
                         server_hashed, client, server, feedback_label, guess_label)
        return True
    elif remaining_guesses[0] <= 0:
        for inner_button in buttons:
            inner_button.destroy()
        feedback_label.config(text=f"You Lose! The number was {answer}.", fg="red")
        create_play_button(canvas, font, nonce, screen, seed_writer_turtle, 
                         server_hashed, client, server, feedback_label, guess_label)
        return False
    button.destroy()

def write_guess_numbers(canvas: Canvas, font: tuple[str, int, str], answer: int, guesses: int,
                       nonce: int, screen: _Screen, seed_writer_turtle: Turtle,
                       server_hashed: str, client: str, server: str):
    number: int = 1
    buttons: list[Button] = []
    remaining_guesses = [guesses]  # Track guesses as a mutable list

    # Create labels for feedback and guesses
    feedback_label = Label(canvas.master, text="", font=font, bg="white", fg="white")
    feedback_label.place(relx=0.45, rely=0.85, anchor="center")
    
    guess_label = Label(canvas.master, text=f"Guesses left: {remaining_guesses[0]}", font=font, fg="black", bg="white")
    guess_label.place(relx=0.45, rely=0.8, anchor="center")

    for row in range(10):
        for col in range(10):
            button: Button = Button(canvas.master, text=number, font=font, width=3, height=1, padx=1, pady=1)
            button.place(relx=(col/20)+0.25, rely=(row/20)+0.25)
            buttons.append(button)
            number += 1
    number:int = 1
    for inner_button in buttons:
        inner_button.configure(
            command=lambda btn=inner_button, num=number, lbl=guess_label, fb=feedback_label: 
                check_guess(btn, buttons, num, answer, remaining_guesses, lbl, fb,
                          canvas, font, nonce, screen, seed_writer_turtle, server_hashed, client, server)
        )
        number += 1

    return buttons, guess_label, feedback_label

def set_number_guesses(difficulty: str, easy: Button, medium: Button, hard: Button, expert: Button, 
                      canvas: Canvas, font: tuple[str, int, str], answer: int,
                      nonce: int, screen: _Screen, seed_writer_turtle: Turtle,
                      server_hashed: str, client: str, server: str):
    guesses: int = 1  # Expert default
    if difficulty.lower() == 'easy':
        guesses = 6
    elif difficulty.lower() == 'medium':
        guesses = 4
    elif difficulty.lower() == 'hard':
        guesses = 2

    guess_numbers, guess_label, feedback_label = write_guess_numbers(
        canvas, font, answer, guesses, nonce, screen, seed_writer_turtle, server_hashed, client, server)
    return guesses, guess_numbers

def make_difficulty_buttons(canvas: Canvas, font: tuple[str, int, str], answer: int,
                           nonce: int, screen: _Screen, seed_writer_turtle: Turtle,
                           server_hashed: str, client: str, server: str) -> tuple[Button, Button, Button, Button]:
    # Create difficulty buttons
    easy: Button = Button(canvas.master, text="Easy", font=font)
    easy.place(relx=0.2, rely=0.7)
    medium: Button = Button(canvas.master, text="Medium", font=font)
    medium.place(relx=0.4, rely=0.7)
    hard: Button = Button(canvas.master, text="Hard", font=font)
    hard.place(relx=0.6, rely=0.7)
    expert: Button = Button(canvas.master, text="Expert", font=font)
    expert.place(relx=0.8, rely=0.7)

    # Create Rotate Seeds button
    rotate_button = Button(canvas.master, text="Rotate Seeds", font=font, bg="orange")
    rotate_button.place(relx=0.5, rely=0.8, anchor="center")

    def rotate_seeds():
        # Create a new popup window
        popup = Tk()
        popup.title("Rotate Seeds")
        popup.attributes('-fullscreen', True)
        
        # Generate new seeds
        new_server = generate_server_seed()
        new_client = generate_client_seed()

        # Server seed display (read-only)
        Label(popup, text="Previous Server Seed:", font=font,pady=20,padx=20).pack()
        server_entry = Entry(popup, font=font, width=100, justify='center')
        server_entry.insert(0, sha256_encrypt(server))
        server_entry.config(state='readonly')
        server_entry.pack()

        # Server seed display (read-only)
        Label(popup, text="Previous Server Seed (Hashed):", font=font,pady=20,padx=20).pack()
        server_entry = Entry(popup, font=font, width=100, justify='center')
        server_entry.insert(0, sha256_encrypt(server_hashed))
        server_entry.config(state='readonly')
        server_entry.pack()

        # Server seed display (read-only)
        Label(popup, text="", font=font,pady=60,padx=20).pack()

        # Server seed display (read-only)
        Label(popup, text="Previous Client Seed:", font=font,pady=20,padx=20).pack()
        server_entry = Entry(popup, font=font, width=100, justify='center')
        server_entry.insert(0, sha256_encrypt(client))
        server_entry.config(state='readonly')
        server_entry.pack()
        
        # Server seed display (read-only)
        Label(popup, text="New Server Seed (Hashed):", font=font,pady=20,padx=20).pack()
        server_entry = Entry(popup, font=font, width=100, justify='center')
        server_entry.insert(0, sha256_encrypt(new_server))
        server_entry.config(state='readonly')
        server_entry.pack()
        
        # Client seed entry (editable)
        Label(popup, text="Client Seed (edit if desired):", font=font,pady=20,padx=20).pack()
        client_entry = Entry(popup, font=font, width=100, justify='center')
        client_entry.insert(0, new_client)
        client_entry.pack()
        
        def apply_changes():
            nonlocal server, server_hashed, client
            # Update seeds with user's input
            server = new_server
            server_hashed = sha256_encrypt(server)
            client = client_entry.get()
            nonce = 1
            
            # Clear and redraw screen with new seeds
            clear_seeds_from_screen(seed_writer_turtle, screen)
            write_seeds_to_screen(server_hashed, client, nonce, seed_writer_turtle, screen, font)
            popup.destroy()
        
        # Apply button
        apply_button = Button(popup, text="Apply", font=font, command=apply_changes)
        apply_button.pack(pady=10)
        
        popup.mainloop()

    rotate_button.configure(command=rotate_seeds)

    def destroy_all_buttons():
        destroy_difficulty_buttons(easy, medium, hard, expert)
        rotate_button.destroy()

    # Configure difficulty buttons to destroy all buttons when clicked
    easy.configure(command=lambda: [destroy_all_buttons(), set_number_guesses(
        "easy", easy, medium, hard, expert, canvas, font, answer,
        nonce, screen, seed_writer_turtle, server_hashed, client, server)])
    medium.configure(command=lambda: [destroy_all_buttons(), set_number_guesses(
        "medium", easy, medium, hard, expert, canvas, font, answer,
        nonce, screen, seed_writer_turtle, server_hashed, client, server)])
    hard.configure(command=lambda: [destroy_all_buttons(), set_number_guesses(
        "hard", easy, medium, hard, expert, canvas, font, answer,
        nonce, screen, seed_writer_turtle, server_hashed, client, server)])
    expert.configure(command=lambda: [destroy_all_buttons(), set_number_guesses(
        "expert", easy, medium, hard, expert, canvas, font, answer,
        nonce, screen, seed_writer_turtle, server_hashed, client, server)])

    return easy, medium, hard, expert, rotate_button

def main():
    # Get the path to the folder this script is in
    BASE_DIR:str = os.path.dirname(os.path.abspath(__file__))

    # Safely construct the full path to Configuration.json
    config_path:str = os.path.join(BASE_DIR, "Configuration.json")
    with open(config_path,"rb") as file:
        configuration:dict[str,str|int] = json.load(file)

    server:str = generate_server_seed()
    server_hashed:str = sha256_encrypt(server)
    client:str = generate_client_seed()
    nonces:range = range(configuration["MinimumNonce"],configuration["MaximumNonce"]+1)

    screen = Screen()
    screen.setup(width=1.0,height=1.0,startx=None,starty=None)
    screen.cv._rootwindow.resizable(False, False)  # Prevent resizing
    screen.cv._rootwindow.wm_attributes("-fullscreen", True)  # Force fullscreen
    screen.cv._rootwindow.protocol("WM_DELETE_WINDOW", lambda: None)  # Disable close button
    canvas:Canvas = screen.getcanvas()
    seed_writer_turtle:Turtle = Turtle(visible=False)

    for nonce in nonces[:1]:
        clear_seeds_from_screen(seed_writer_turtle,screen)
        write_seeds_to_screen(server_hashed,client,nonce,seed_writer_turtle,screen,("Arial",20,"bold"))
        make_difficulty_buttons(
            canvas,("Arial",20,"bold"),seeds_to_results(server,client,nonce),
            nonce, screen, seed_writer_turtle, server_hashed, client, server)

    screen.mainloop()

if __name__ == "__main__":
    main()