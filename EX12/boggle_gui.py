import tkinter as tki
from tkinter.constants import BOTH, END, LEFT, RIGHT, Y
from typing import Any, Callable, List
# from PIL import Image
# try:  # if ImageTk is not on the aquarium server.
#     from PIL import ImageTk
# except ImportError:
#     import ImageTk

# from itertools import count, cycle


class Boogle_UI :

    BOARD_VALUE = 4

    def __init__(self, root) -> None:
        self.root = root
        self.root.title('The boggle game')
        self.button_text = [["?" for _ in range(self.BOARD_VALUE)] for _ in range(self.BOARD_VALUE)]
        self.found_words_list = []

    def started_menu(self, start_game: Callable) -> None:
        """Its the function that create the start menu

        Args:
            start_game (Callable): The function that active the main menu
        """

        #The main frame of the windows
        self.main_frame = tki.Frame(self.root, height=400, width=500, bg='RoyalBlue3')
        self.main_frame.pack()

        # the game title label
        # title_img = tki.PhotoImage(file='resources/boggle.gif')
        # title_label = tki.Label(self.main_frame,height=40, width=100, image=title_img)
        # self._create_gif_label(title_label, 'resources/boggle.gif')

        # title_label.place(x = 150, y = 10)
        #The start button himself

        start_button = tki.Button(self.main_frame, text= 'Lets Boggle!',font='Helvetica 15 bold', command = start_game)
        start_button.configure(width=40, height=7, bg='tomato3', font= ('helvetica'), border=2, borderwidth=5)
        start_button.place(x=65, y= 100)

        credit_button = tki.Button(self.main_frame, text='Credits', command= self._show_credits())
        credit_button.configure(width=10, height=2, border=9, background='Chartreuse', activebackground='HotPink1')
        credit_button.place(x=370,y=340)
    
    def _show_credits(self)-> Callable :
        """This function hails the two all-mighty creators of this game

        Returns:
            Callable: A callback function who activate when the credit button is pushed
        """

        # def credit_callback():
        #     messagebox.showinfo(title='Credits', message='This program has been created by Samuel Goash and Yotam Hayat')
            
        return self._open_credits

    def _open_credits(self):
        """Its a helper function that will create a new window and charge a gif 
        to it 
        """
        credits_win = tki.Toplevel(self.root)
        credits_win.title("CREDITS")
        credits_win.resizable(width=False, height= False)
        tki.Label(master=credits_win, bg='hot pink', fg='black', text= "ALL HAIL THE MIGHTY CREATORS - SAMUEL AND YOTAM", font= ('Helvetica 15 bold')).pack()
        creators_image = tki.PhotoImage(file="resources/creators.gif")
        gif_label = tki.Label(master=credits_win, bg='hot pink', image=creators_image)
        gif_label.pack()
        gif_label.load("resources/creators.gif")

    def actual_game(self, board: List[List[str]], score: int, timer: int, 
    create_button_callback : Callable, reset_button_callback : Callable, 
    send_button_callback : Callable, game_over_callback : Callable) -> None: 
        """ Its the function that create the ui of the main interface of the game

        Args:
            board (List[List[str]]): A list of list that will contains a letter that we gonna display in the buttons
            score (int): An initial score
            timer (int): The initial timer
            create_button_callback (Callable): A callback function that will be called when a button is pushed
            reset_button_callback (Callable): A callback function that will be called when the user want to reset a word
            send_button_callback (Callable): A callback function that will be called when the user want to check a word
            game_over_callback (Callable): A callback function that will be called when the timer fall to 0
        """
        
        # Destroy the previous display
        self.main_frame.destroy()

        #Create a new one
        self.main_frame = tki.Frame(self.root, height=900, width=900, bg='DodgerBlue4')
        self.main_frame.pack()

        #Create the interface frame which contains the score, the timer and the current word
        interface_frame = tki.Frame(self.main_frame, height=300, width=150, background='DarkGoldenrod3', relief='ridge',padx=5, pady=5)
        # interface_frame.configure(highlightbackground='Black', highlightthickness=2)

        interface_frame.grid(row=0, column=0, pady=(0, 20))
        self._create_interface(interface_frame, score, timer)
        
        #Create the interface that will display the found words list
        words_list_frame = tki.Frame(self.main_frame)
        words_list_frame.grid(row=0, column=1, rowspan=2, columnspan=1)
        self._create_words_list(words_list_frame)

        #Create the button container which contains the buttons
        button_frame = tki.Frame(self.main_frame, height=100, width= 100)
        button_frame.grid(row=1, column=0, rowspan=2)
        button_list = self._create_board_buttons(button_frame, board, create_button_callback)

        #Create the input frame 
        input_frame = tki.Frame(self.main_frame, height=100, width=350, bg='DodgerBlue4')
        input_frame.grid(row=3, column=0)
        self._create_command_buttons(input_frame, button_list, send_button_callback, reset_button_callback)#, words_list_frame)

        #The iteration of the countdown timer
        self._countdown_timer(timer, game_over_callback)

        # gif_frame = tki.Frame(self.main_frame)
        # gif_frame.grid(row=3, column=1)
        # self._create_dino_gif(gif_frame)

    def _create_interface(self, root, score : int, timer : int):
        """Thats an helper function that will receive a frame and will create the interface of the ui 

        Args:
            root ([type]): The master frame
            score (int): The original score
            timer (int): The original timer ( in seconds )
        """

        #Create the score 
        self.score_label = tki.Label(root, text = f'SCORE\n{str(score)}')
        self.score_label.configure(font='Helvetica 15 bold', height=3, width=10, padx=1, pady=1, bg='gray90', relief='ridge', borderwidth=3)
        self.score_label.grid(row=0, column=0)

        #Create the timer
        time_str = 'TIME RIGHT\n{:02d}:{:02d}'.format((timer // 60),(timer % 60))
        self.timer_label = tki.Label(root, text= time_str)
        self.timer_label.configure(font='Helvetica 15 bold', height=3, width=10, padx=1, pady=1, bg='gray90', relief='ridge', borderwidth=3)
        self.timer_label.grid(row=0, column=1)

        #Create the current word
        self.current_word_label = tki.Label(root, text='')
        self.current_word_label.configure(height=5, width=50, background='goldenrod', relief='sunken', borderwidth=3)
        self.current_word_label.grid(row=1, columnspan=2)

    def _create_words_list(self, root) -> None:
        """Its an helper function that will build the ui of the list of guessed well words

        Args:
            root ([type]): The master frame
        """

        root.configure(background= 'DodgerBlue4')

        word_list_presentation_label = tki.Label(root, text= 'Guessed words :', font=('Helvetica', 20), bg= "goldenrod2", width=15, borderwidth=3, relief='groove')
        word_list_presentation_label.pack(side=tki.TOP, pady=(100, 50))

        words_scrollbar = tki.Scrollbar(root)
        words_scrollbar.configure(orient= 'vertical')
        words_scrollbar.pack(side=RIGHT, fill=Y)

        self.wrd_list = tki.Listbox(root, yscrollcommand=words_scrollbar.set)
        self.wrd_list.configure(height=20, width= 40)
        # self.wrd_list.insert(END, word)      
        self.wrd_list.pack(side=LEFT, fill=BOTH)

        words_scrollbar.config(command=self.wrd_list.yview)

    def _create_board_buttons(self, root, board : List[List[str]], create_button_callback: Callable) -> List[Any]:
        """Its a function that will create the board with all his buttons

        Args:
            root ([type]): The master frame
            board (List[List[str]]): A list of list that will contains all the randomized letters
            create_button_callback (Callable): A callback that will be used to active an event when a button is clicked

        Returns:
            List[Any]: A list of all the buttons ( for futur changes )
        """
        button_list = []
        for i in range(len(board)):

            col_list = []

            for j in range(len(board[0])):
                
                actual_value = board[i][j]
                coordinate_tuple = (i,j)

                button = tki.Button(root, text=board[i][j], font=('helvetica 10 bold') ,  width=8, height=4, border=4)
                self.DEFAULT_BUTTON_COLOR = button['bg']
                button.configure(command= self._on_click_letter_button(create_button_callback, actual_value, button_list, coordinate_tuple))
                button.grid(row=i, column=j)

                col_list.append(button)

            button_list.append(col_list)
        
        return button_list

    def _create_command_buttons(self, root, button_list : List[Any], 
    send_button_callback :Callable, reset_button_callback: Callable) -> None:
        """Its an helper function that creates the send button and the reset button

        Args:
            root ([type]): The master frame
            button_list (List[Any]): A list of all the buttons of the board
            send_button_callback (Callable): A callback function that will be connected to the send button
            reset_button_callback (Callable): A callback function that will be connected to the reset button
        """
    
        reset_button = tki.Button(root, text='RESET', font='Helvetica 12 bold')
        reset_button.configure(width=15, height=3, background='orange2', activebackground='orange', border=3)
        reset_button.configure(command= self._on_click_reset_button(reset_button_callback, button_list, self.DEFAULT_BUTTON_COLOR))
        reset_button.place(x=10, y=20)

        send_button = tki.Button(root, text='SEND WORD',font ='Helvetica 12 bold')#, width=150)
        send_button.configure(width=15, height=3 , background='green3', activebackground='green2', border=3)
        send_button.configure( command= self._on_click_send_button(send_button_callback, button_list, self.DEFAULT_BUTTON_COLOR, self.wrd_list))
        send_button.place(x=180, y=20)
    
    def _create_dino_gif(self, root):
        """A function that will help us to build the cute tiny dino that run after the boggle

        Args:
            root ([type]): The master frame
        """
        dino_image = tki.PhotoImage(file = 'resources/dino.gif')
        dino_canvas = tki.Label(root, bg='Dodgerblue', height=100, width=130, image= dino_image)
        dino_canvas.pack(side=LEFT)
        # dino_gif = ImageLabel(master=dino_canvas)
        # dino_gif.pack()
        # dino_gif.load('resources/dino.gif')

        boggle_image = tki.PhotoImage(file='resources/boggle.gif')
        word_canvas = tki.Label(root,  height=100, width=150, relief='ridge', image=boggle_image)
        word_canvas.pack(side=LEFT)
        # boggle_img = ImageLabel(master=word_canvas)
        # boggle_img.pack()
        # boggle_img.load('resources/boggle.gif')

    def _countdown_timer(self, current_time : int, game_over_function  : Callable):
        """This function controls the time (Like Thanos) of the game and is creating an loop out the universe
        when the current time falls to 0 calls a function that ends the game

        Args:
            current_time (int): The current time 
            game_over_function (Callable): The function that destroy the universe
        """
        if current_time > 0:
            current_time -= 1
            time_str = 'TIME LEFT\n{:02d}:{:02d}'.format((current_time // 60),(current_time % 60))
            self.timer_label.configure(text=time_str,font=("Helvetica 15 bold"), justify="center",)

            # using after to update the clock every 1 second,
            self.root.after(1000, lambda: self._countdown_timer(current_time, game_over_function))

        else:
            game_over_function()


    def _on_click_letter_button(self, callback, letter, button_list, cords):
        def f1():
            valid_button = callback(letter, cords)
            if valid_button:
                button_list[cords[0]][cords[1]].configure(bg='cyan2')
            
        return f1
    
    def _on_click_reset_button(self, callback, button_list, default_color):
        def f2():
            callback(button_list, default_color)
        return f2
    
    def _on_click_send_button(self, callback, button_list, default_color, wrd_list):
        def f3():
            callback(button_list, default_color, wrd_list)
        return f3

    def add_to_found_words(self, root, current_word):

        self.found_words_list.append(current_word)

        # new_word = tki.Label(root, text=current_word)
        # new_word.pack()
        root.insert(END, current_word)


    def final_screen(self, score : int, words_list : List[str], play_again_callback, give_up_callback):
        """Its the function that launch the end game screen where we can see the score 
        the list of the words we found and have a chance to be better at life

        Args:
            score (int): The score of game
            words_list (List[str]): The list of valid guessed words
            play_again_callback ([type]): A callback function that will relaunch the game
            give_up_callback ([type]): A callback function that will end the game and close the window
        """
        self.main_frame.destroy()

        self.main_frame = tki.Frame(self.root)
        self.main_frame.configure(height=300, width=450, bg='dodgerblue4')
        self.main_frame.pack()

        #Create the score frame
        score_frame = tki.Frame(self.main_frame)
        score_frame.configure(bg='goldenrod2', height= 50, width= 300, relief='ridge', borderwidth=3)
        score_frame.place(x=80, y=20)

        self._create_score_label(score_frame, score)

        presentation_label = tki.Label(self.main_frame, text= 'You found these words:',font='helvetica', relief='ridge', borderwidth=2)
        presentation_label.configure(bg='goldenrod2', width=42)
        presentation_label.place(x=50, y=90)

        #Creating the list of word frame
        words_frame = tki.Frame(self.main_frame)
        words_frame.configure(bg='cadet blue', height=110, width=300)
        words_frame.place(x=50, y=120)

        self._create_words_guessed(words_frame, words_list)

        #Creating the button play again and give up
        continue_game_frame = tki.Frame(self.main_frame)
        continue_game_frame.configure(bg='gray70', height=50, width=300)
        continue_game_frame.place(x=80, y=235)

        self._create_play_and_give_up_button(continue_game_frame, play_again_callback, give_up_callback)

    def _create_score_label(self, root, score : int) -> None :
        score_label = tki.Label(root, text= f'Your score is : {score}')
        score_label.configure(bg='goldenrod2', font=('helvetica', 25))
        score_label.place(x=20, y=5)
    
    def _create_words_guessed(self,root, words_list : List[str]) -> None :
        words_scrollbar = tki.Scrollbar(root)
        words_scrollbar.configure(orient= 'vertical')
        words_scrollbar.pack(side=RIGHT, fill=Y)

        wrd_list = tki.Listbox(root, yscrollcommand=words_scrollbar.set)
        wrd_list.configure(height=6, width= 47)

        for word in words_list:
            wrd_list.insert(END, word)
        
        wrd_list.pack(side=LEFT, fill=BOTH)

        words_scrollbar.config(command=wrd_list.yview)

    # def _create_gif_label(self, root, file):
    #     gif_label = ImageLabel(master=root)
    #     gif_label.pack()
    #     gif_label.load(file)


    def _create_play_and_give_up_button(self, root, play_again_callback, give_up_callback) -> None :

        play_again_button = tki.Button(root, text='Play again ?')
        play_again_button.configure(bg='CadetBlue1',height=3, width=20)
        play_again_button.configure(command= play_again_callback())
        play_again_button.place(x=0)

        give_up_button = tki.Button(root, text='Give up')
        give_up_button.configure(bg='red3', height=3, width=20)
        give_up_button.configure(command=give_up_callback())
        give_up_button.place(x=150)

""" gif label creator from https://pythonprogramming.altervista.org/"""

#
# class ImageLabel(tki.Label):
#     """
#     A Label that displays images, and plays them if they are gifs
#     :im: A PIL Image instance or a string filename
#     """
#
#     def load(self, im):
#         if isinstance(im, str):
#             im = Image.open(im)
#         frames = []
#
#         try:
#             for i in count(1):
#                 frames.append(tki.PhotoImage(file = im.copy()))
#                 im.seek(i)
#         except EOFError:
#             pass
#         self.frames = cycle(frames)
#
#         try:
#             self.delay = im.info['duration']
#         except:
#             self.delay = 100
#
#         if len(frames) == 1:
#             self.config(image=next(self.frames))
#         else:
#             self.next_frame()
#
#     def unload(self):
#         self.config(image=None)
#         self.frames = None
#
#     def next_frame(self):
#         if self.frames:
#             self.config(image=next(self.frames))
#             self.after(self.delay, self.next_frame)



# if __name__ == "__main__":

#     root = tki.Tk()
#     waw = Boogle_UI(root)
#     mlst = list(range(30))
#     waw.final_screen(999, mlst, print, print)
#     root.mainloop()