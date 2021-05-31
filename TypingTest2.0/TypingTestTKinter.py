from tkinter import *
import tkinter.font as tkFont
import random, time

#Colours
#dark_blue = (4, 0, 94)
dark_blue = '#04005E'
#light_blue = (68, 11, 212)
light_blue = '#440BD4'
#neon_pink = (255, 32, 121)
neon_pink = '#FF2079'
#magenta = (233, 46, 251)
magenta = '#E92EFB'
#white = (255, 255, 255)
white  = '#FFFFFF'
text_collection = ["hello how are you doing this fine evening", "good morning how was your day in the sun", "the morning is early so start your day right", "black ink is the best type of ink", "always make sure to water your plants or else they will wilt"]

#Used for comparing users answer to the actual words
user_answer = []
words = []
points = 0

#timer
start_time = 0
end_time = 0

start_limit = 0 #So it can start timer automatically if you press any key
space_bar_limit = 0 #So it can end instead of pressing enter all the time

#needed for other functions
accuracy = 0
wpm = 0
accuracy_onscreen = 0
wpm_onscreen = 0
highscore = False

#Recent score variables
with open("recentscores.txt", 'r') as a:
    recentscore_text = a.readlines()[-1]    #finds the last element in array without using a while loop
with open("highscore.txt", 'r') as b:
    highscore_text =  b.readline()

def timer(*args):
    global start_time, start_limit
    print("time started")
    start_time = time.time()
    start_limit += 1
    if start_limit == 1:
        root.bind("<Key>", unbind)

#Changing to a new text
def new_sample():    
    text_sample = text_collection[random.randint(0, len(text_collection) - 1)]
    return text_sample

def add_word(*args):
    global user_answer, space_bar_limit
    #use n to get rid of the space
    n = len(type_box.get()) - 1
    user_word = type_box.get()[:len(type_box.get()) - 1]
    user_answer.append(user_word)
    type_box.delete(0, len(type_box.get()))
    print(user_answer)
    print(words)
    space_bar_limit += 1
    if space_bar_limit == len(words):
        check_result()
        show_result()
        update_score()

def check_result(*args):
    global user_answer, words, start_time, end_time, points
    end_time = time.time()
    if len(user_answer) == len(words):
        for i in range(len(words)):
            if user_answer[i] == words[i]:
                points += 1

def show_result():
    global accuracy_onscreen, wpm_onscreen, points, end_time, start_time, wpm, accuracy
    #Calculating Accuracy
    accuracy = str("{:.2%}".format(points/len(words)))
    print(accuracy)
    #Show on screen
    accuracy_onscreen = Label(root, text = "Your accuracy is " + accuracy, font = med_font, bg = dark_blue, fg = magenta)
    accuracy_onscreen.grid(column = 1, row = 2)

    #Calculating WPM
    duration = end_time - start_time
    wpm = "{:.1f}".format((points/duration) * 60)
    print(wpm)
    #Show on screen
    wpm_onscreen = Label(root, text = "Your speed is " + wpm + " WPM", font = med_font, bg = dark_blue, fg = magenta)
    wpm_onscreen.grid(column = 1, row = 1)

def reset(*args):
    global words, text_onscreen, user_answer, wpm_onscreen, accuracy_onscreen, points, space_bar_limit, start_limit, recentscore_text, highscore_text, recentscore_onscreen, highscore_onscreen, highscore
    points = 0
    user_answer = []
    start_limit = 0
    space_bar_limit = 0
    
    #update with a new text sample
    words = new_sample().split(" ")
    text_onscreen.destroy()
    text_onscreen = Label(root, text = words, font = med_font, bg = dark_blue, fg = neon_pink)
    text_onscreen.grid(columnspan = 3, column = 0, row = 0)

    #rebinding keys
    root.bind("<Key>", timer)

    #if the show result is not empty, destory
    if wpm_onscreen != 0:
        wpm_onscreen.destroy()
        accuracy_onscreen.destroy()

    #Updating recentscore
    with open("recentscores.txt", 'r') as c:
        new_score = c.readlines()[-1]
        if new_score != recentscore_text:
            recentscore_text = new_score
            recentscore_onscreen.destroy()
            recentscore_onscreen = Label(root, text = "Recent score:" + recentscore_text + "WPM", font = small_font, bg = dark_blue, fg = neon_pink)
            recentscore_onscreen.place(x = 20, y = 100)

    #If boolean of highscore set to true
    if highscore:
        with open("highscore.txt", 'r') as d:
                new_highscore = d.readline()
                highscore_text = new_highscore
                highscore_onscreen.destroy()
                highscore_onscreen = Label(root, text = "Highscore:" + highscore_text + "WPM", font = small_font, bg = dark_blue, fg = neon_pink)
                highscore_onscreen.place(x = 20, y = 20)
        
def unbind(*args):
    y = "x"
    #supposed to be a useless function since I can't unbind the key

def update_score():
    global wpm, accuracy, highscore
    highscore = False
    #Used for finding average typing speed from previous scores and current score
    #updating text file only
    with open("recentscores.txt", 'a') as e:
        e.write(str(wpm) + '\n')
    #Finding average WPM
    with open("recentscores.txt", 'r') as f:
        scores = f.readlines()
        total = 0 
        count = 0
        for score in scores:
            total += float(score)
            count += 1
        avg_wpm = "{:.1f}".format(total/count)
        print("\nYour average speed is", avg_wpm, "WPM")

    #Replacing highscore (if needed)
    with open("highscore.txt", 'r') as g:
        if float(wpm) > float(g.readline()):
            print("\nYou got a new highscore!")
            highscore = True
            with open("highscore.txt", 'w') as new_score:
                new_score.write(str(wpm))

#Main Loop
root = Tk()
root.title("Speed Typing Test")

#Screen Settings
screen = Canvas(root, width = 1280, height = 720, bg = dark_blue)
screen.grid(columnspan = 3, rowspan = 3)

#Font variable
small_font = tkFont.Font(family = 'Corbel', size = 16)
med_font = tkFont.Font(family = 'Corbel', size = 22)
big_font = tkFont.Font(family = 'Corbel', size = 30)

#Input box
type_box_label = Label(root, text = "Type in here to start", font = med_font, bg = dark_blue, fg = magenta)
type_box_label.grid(column = 1, row = 2)
type_box = Entry(root, width = 40, font = med_font, bg = white, fg = neon_pink)
type_box.grid(column = 1, row = 3, padx = 0, pady = 20, ipady = 10)

#Scores showing on screen
recentscore_onscreen = Label(root, text = "Recent score:" + recentscore_text + "WPM", font = small_font, bg = dark_blue, fg = neon_pink)
recentscore_onscreen.place(x = 20, y = 100)

highscore_onscreen =  Label(root, text = "High score:" + highscore_text + "WPM", font = small_font, bg = dark_blue, fg = neon_pink)
highscore_onscreen.place(x = 20, y = 20)

#The text showing on screen
words = new_sample().split(" ")
text_onscreen = Label(root, text = words, font = med_font, bg = dark_blue, fg = neon_pink)
text_onscreen.grid(columnspan = 3, column = 0, row = 0)

#Submit Button
submit_text = StringVar()
submit_button = Button(root, textvariable = submit_text, font = med_font, bg = light_blue, fg = neon_pink, command = check_result)
submit_text.set("Submit")
submit_button.grid(column = 2, row = 3)

#Restart Button
restart_text = StringVar()
restart_button = Button(root, textvariable = restart_text, font = med_font, bg = light_blue, fg = neon_pink, command = reset)
restart_text.set("Restart")
restart_button.grid(column = 3, row = 3)

#When pressing any key, the timer starts
root.bind("<Key>", timer)

#Binding space and enter to get the word that was in the box
root.bind("<space>", add_word)
root.bind("<Return>", add_word)

#End of loop
root.mainloop()