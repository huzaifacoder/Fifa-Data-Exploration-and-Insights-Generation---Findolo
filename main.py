
import tkinter as tk
import time
import os
import pandas as pd
from scipy.stats import skew
import numpy as np
import threading

# read csv
cwd_join = os.getcwd() + "\\"

database_rel = os.path.relpath('DATABASE\\Career Mode player datasets - FIFA 15-22.csv')
icon_rel = os.path.relpath('ICONS\\')
background_rel = os.path.relpath('BACKGROUND\\')
icon_abs = cwd_join + icon_rel
database_abs = cwd_join + database_rel
background_abs_updt = cwd_join + background_rel
csv_data = pd.read_csv(database_abs, low_memory=False)
# csv_data = pd.read_csv()

# note : csv_data[""] = csv_data[""]

# storing
short_name = csv_data["short_name"]
long_name = csv_data["long_name"]
wage = csv_data["wage_eur"]
age = csv_data["age"]
potential = csv_data["potential"]
contract_valid_until = csv_data["club_contract_valid_until"]
players_url = csv_data["player_face_url"]
height_cm = csv_data["height_cm"]
height_meters = height_cm / 100
international_reputation = csv_data["international_reputation"]
preferred_foot = csv_data["preferred_foot"]
nationality_name = csv_data["nationality_name"]
nationality_name.sort_values(ascending=True)
player_face = csv_data["player_face_url"]

# lists
short_name_list = list(short_name)
short_name_fam = short_name_list[0: 20]
filter_list = ["No filter", "Top 20 players"]
long_name_list = list(long_name)
age_list = list(age)
wage_list = list(wage)
potential_list = list(potential)
international_reputation_list = list(international_reputation)
preferred_foot_list = list(preferred_foot)
height_meters_list = list(height_meters)

nationality_name_set = set(nationality_name.sort_values())
nationality_name_list = list(nationality_name_set)
nationality_name_list.sort()
nationality_name_length = len(nationality_name_set)
nationality_name_list_org = list(nationality_name)

"""
GUI
"""
root = tk.Tk()
root.title('FIFA Data Exploration and Insights Generation App (MAIN).')
root.geometry("800x500")
root.resizable(False, False)

root.configure(bg="lightblue")
# Import required libraries
from tkinter import *
from PIL import ImageTk, Image

# Create an instance of tkinter window

frame = Frame(root, width=800, height=500)
frame.pack()
frame.place(anchor='center', relx=0.5, rely=0.5)

# Create an object of tkinter ImageTk
img = ImageTk.PhotoImage(Image.open(background_abs_updt + "\\Background.jpg"))
# Create a Label Widget to display the text or Image
label = Label(frame, image=img)
label.pack()

p1 = PhotoImage(file=icon_abs + "\\fifa_logo2.png")
# Setting icon of the window
root.iconphoto(False, p1)

# Import required libraries
from tkinter import *
from PIL import ImageTk, Image


def extra_stats():
    global extra_stats_win
    extra_stats_win = Toplevel(root)
    extra_stats_win.geometry("800x500")
    extra_stats_win.title("Overall Statistics")
    img_e = ImageTk.PhotoImage(Image.open(background_abs_updt + "\\Background3.JPG"))

    frame_e = Frame(extra_stats_win, width=800, height=500)
    frame_e.pack()
    frame_e.place(anchor='center', relx=0.5, rely=0.5)

    labele = Label(frame_e, image=img_e)
    label.image = img_e
    labele.pack()

    p3 = PhotoImage(file=icon_abs + '\\plus_logo.png')
    extra_stats_win.iconphoto(False, p3)
    basic_info_overall = tk.Label(extra_stats_win, text=(
        f"{min(wage_list)} is the lowest WAGE.\n"
        f"{max(wage_list)} is the highest WAGE.\n"
        f"{int(np.mean(wage))} is the mean average WAGE.\n"
        f"{max(potential_list)} is the highest POTENTIAL.\n"
        f"{min(potential_list)} is the lowest POTENTIAL.\n"
        f"{int(np.mean(potential_list))} is the mean average POTENTIAL.\n"
        f"The {max(csv_data.preferred_foot)} foot is the most Preferred foot.\n"
        f"{nationality_name_length} countries participated in FIFA."))
    basic_info_overall.configure(bg="#AFEEEE", fg="black", highlightbackground="#C4A484", font=("PT Monoa", 13))
    basic_info_overall.pack(pady=4)

    threading.Thread(target=bar).start()

    ###
    list_wage_X1 = []
    list_wage_comp1 = [list_wage_X1.append(1) for wage1 in wage_list if wage1 > 50_000]
    int_wage_crazy_high = np.sum(list_wage_X1)

    list_wage_X2 = []
    list_wage_comp2 = [list_wage_X2.append(1) for wage2 in wage_list if wage2 < 1_000]
    int_wage_low = np.sum(list_wage_X2)

    list_wage_X3 = []
    list_wage_comp3 = [list_wage_X3.append(1) for wage3 in wage_list if wage3 > 1_000]
    int_wage_high = np.sum(list_wage_X3)

    list_pot_X1 = []
    list_pot_comp1 = [list_pot_X1.append(1) for potH in potential_list if potH > 85]
    int_pot_crazy_high = np.sum(list_pot_X1)

    list_pot_X2 = []
    list_pot_comp2 = [list_pot_X2.append(1) for potL in potential_list if potL < 65]
    int_pot_low = np.sum(list_pot_X2)

    list_pot_X3 = []
    list_pot_comp3 = [list_pot_X3.append(1) for potA in potential_list if potA == np.median(potential_list)]
    int_pot_average = np.sum(list_pot_X3)

    try:
        global larger_stats_overall
        larger_stats_overall = tk.Label(extra_stats_win, text=
        f"There are {int_wage_low} players that have wage below 1,000.\n"
        f"There are {int_wage_high} players that have wage above 1,000.\n"
        f"There are {int_wage_crazy_high} players that have wage above 50,000.\n"
        f"There are {int_pot_crazy_high} players that have potential above 85.\n"
        f"There are {int_pot_low} players that have potential below 65.\n"
        f"There are {int_pot_average} players that have average potential.")

    except RuntimeError:
        pass
    larger_stats_overall.configure(bg="#AFEEEE", fg="black", highlightbackground="#AFEEEE", font=("PT Monoa", 13))

    larger_stats_overall.pack(pady=5)

    # Check for the maximum player age group
    # 15-20
    # 21-25
    # 26-30
    # 31-35
    # 36-40
    int_age_group_1 = 0
    int_age_group_2 = 0
    int_age_group_3 = 0
    int_age_group_4 = 0
    int_age_group_5 = 0
    int_age_group_6 = 0
    list_age_X1 = []
    player_list_comp_A1 = [list_age_X1.append(1) for player_age1 in age_list if 17 <= player_age1 <= 20]
    int_age_group_1 = np.sum(list_age_X1)
    list_age_X2 = []
    player_list_comp_A2 = [list_age_X2.append(1) for player_age2 in age_list if 21 <= player_age2 <= 25]
    int_age_group_2 = np.sum(list_age_X2)
    list_age_X3 = []
    player_list_comp_A3 = [list_age_X3.append(1) for player_age3 in age_list if 26 <= player_age3 <= 30]
    int_age_group_3 = np.sum(list_age_X3)
    list_age_X4 = []
    player_list_comp_A4 = [list_age_X4.append(1) for player_age4 in age_list if 31 <= player_age4 <= 35]
    int_age_group_4 = np.sum(list_age_X4)
    list_age_X5 = []
    player_list_comp_A5 = [list_age_X5.append(1) for player_age5 in age_list if 36 <= player_age5 <= 40]
    int_age_group_5 = np.sum(list_age_X5)
    list_age_X6 = []
    player_list_comp_A6 = [list_age_X6.append(1) for player_age6 in age_list if 41 <= player_age6 <= 55]
    int_age_group_6 = np.sum(list_age_X6)

    age_group_stats = tk.Label(extra_stats_win, text=
    f"There are {int_age_group_1} Players in age group 15-20.\n"
    f"There are {int_age_group_2} Players in age group 21-25.\n"
    f"There are {int_age_group_3} Players in age group 26-30.\n"
    f"There are {int_age_group_4} Players in age group 31-35.\n"
    f"There are {int_age_group_5} Players in age group 36-40.\n"
    f"There are {int_age_group_6} Players in age group 41-55.")
    age_group_stats.configure(bg="#AFEEEE", fg="black", highlightbackground="#AFEEEE", font=("PT Monoa", 13))

    age_group_stats.pack(pady=5)

    # 15-20
    # 21-25
    # 26-30
    # 31-35
    # 36-40
    # age_group_dict = {"15-20" : int_age_group_1,
    #                            "21-25" : int_age_group_2,
    #                            "26-30" : int_age_group_3,
    #                            "31-35" : int_age_group_4,
    #                            "36-40" : int_age_group_5}

    age_group_list = [int_age_group_1, int_age_group_2, int_age_group_3, int_age_group_4]
    age_group_max = max(age_group_list)

    if age_group_max == int_age_group_1:
        age_group_max_stats_label = tk.Label(extra_stats_win, text="most common age group is 15-20 years.")
        age_group_max_stats_label.configure(bg="#AFEEEE", fg="black", font=("PT Monoa", 13))
        age_group_max_stats_label.pack(pady=4)
    if age_group_max == int_age_group_2:
        age_group_max_stats_label = tk.Label(extra_stats_win, text="most common group is 21-25 years.")
        age_group_max_stats_label.configure(bg="#AFEEEE", fg="black", font=("PT Monoa", 13))
        age_group_max_stats_label.pack(pady=4)

    if age_group_max == int_age_group_3:
        age_group_max_stats_label = tk.Label(extra_stats_win, text="most common group is 26-30 years.")
        age_group_max_stats_label.configure(bg="#AFEEEE", fg="black", font=("PT Monoa", 13))
        age_group_max_stats_label.pack(pady=4)

    if age_group_max == int_age_group_4:
        age_group_max_stats_label = tk.Label(extra_stats_win, text="Most common age group is 31-35 years.")
        age_group_max_stats_label.configure(bg="#AFEEEE", fg="black", highlightbackground="#C4A484",
                                            font=("PT Monoa", 13))

        age_group_max_stats_label.pack(pady=4)
    if age_group_max == int_age_group_5:
        age_group_max_stats_label = tk.Label(extra_stats_win, text="Most common age group is 36-40 years.")
        age_group_max_stats_label.configure(bg="#AFEEEE", fg="black", highlightbackground="#C4A484",
                                            font=("PT Monoa", 13))

        age_group_max_stats_label.pack(pady=4)


###################
from tkinter import ttk


def fn_get_player1(arg1):
    global int_first_player_label1
    global options_footballer

    intPlayerIndex1 = short_name_list.index(arg1)
    try:
        player_info = f"Long Name: {long_name.dropna()[intPlayerIndex1]}" \
                      f"\nShort Name: {short_name_list[intPlayerIndex1]}" \
                      f"\nAge: {str(age_list[intPlayerIndex1])}" \
                      f"\nWage: £{str(int(wage_list[intPlayerIndex1]))}" \
                      f"\nPotential: {str(potential_list[intPlayerIndex1])}" \
                      f"\nHeight: {str(height_meters[intPlayerIndex1])} meters" \
                      f"\nPreferred foot: {preferred_foot_list[intPlayerIndex1]}" \
                      f"\nInternational reputation: {str(international_reputation_list[intPlayerIndex1])}"
    except ValueError:
        player_info = f"Long Name: {long_name.dropna()[intPlayerIndex]}" \
                      f"\nShort Name: {short_name_list[intPlayerIndex1]}" \
                      f"\nAge: {str(age_list[intPlayerIndex1])}\nWage: £ 0" \
                      f"\nPotential: {str(potential_list[intPlayerIndex1])}" \
                      f"\nHeight: {str(height_meters[intPlayerIndex1])} meters" \
                      f"\nPreferred foot: {preferred_foot_list[intPlayerIndex1]}" \
                      f"\nInternational reputation: {str(international_reputation_list[intPlayerIndex1])}"

    global label_player_info_nationality_window

    if int_first_player_label1 != 0:
        label_player_info_nationality_window.destroy()
    int_first_player_label1 = 1
    label_player_info_nationality_window = Label(new_window, text=player_info)
    label_player_info_nationality_window.configure(bg="#4b322a", fg="white", font=("PT Monoa", 13))
    label_player_info_nationality_window.pack()


int_nationality_window_first_time_exec = 0


# def options_footballer_operations_dup(arg):
#    global int_first_player_label
#    global options_footballer
#    global int_first_player_label
#    int_first_player_label = 0
#    if int_first_player_label != 0:
#        options_footballer.destroy()
#    if int_first_player_label != 0:
#        label_player_info.destroy()
#    int_first_player_label = 1
#
#    if arg == filter_list[0]:
#        options_footballer.destroy()
#        options_footballer = tk.OptionMenu(root, clicked_players, *short_name_list, command=fn_get_player)
#    elif arg == filter_list[1]:
#        options_footballer.destroy()
#        options_footballer = tk.OptionMenu(root, clicked_players, *short_name_fam, command=fn_get_player)
#
#    options_footballer.configure(bg="#C4A484", highlightbackground="#C4A484")
#    options_footballer.pack()


def nationality_func_command1(arg):
    intNationalIndex1 = 0
    player_c = []

    for country_name in nationality_name_list_org:
        if country_name == arg:
            player_c.append(short_name_list[intNationalIndex1])
        intNationalIndex1 += 1

    clicked_nation1 = tk.StringVar()
    global nationality_player_option
    global nationality_player_label
    global int_nationality_window_first_time_exec
    if int_nationality_window_first_time_exec != 0:
        nationality_player_label.destroy()
        nationality_player_option.destroy()

    int_nationality_window_first_time_exec = 1
    # global nationality_option

    nationality_player_label = tk.Label(new_window, text="Pick a Footballer.")
    nationality_player_label.configure(bg="#D3D3D3", fg="black", highlightbackground="#D3D3D3", font=("PT Monoa", 13))
    nationality_player_label.pack()
    nationality_player_option = tk.OptionMenu(new_window, clicked_nation1, *player_c, command=fn_get_player1)
    nationality_player_option.configure(bg="#D3D3D3", fg="black", font=("PT Monoa", 13), highlightbackground="#D3D3D3")
    nationality_player_option.pack()


def nationality_func():
    global int_nationalityindex
    global int_first_player_label1
    global new_window
    int_first_player_label1 = 0
    new_window = Toplevel(root)
    p2 = PhotoImage(file=icon_abs + "\\location-map-logo-hd.png")
    new_window.iconphoto(False, p2)
    new_window.geometry("800x500")
    new_window.title("Nationality Analysis")
    new_window.resizable(False, False)
    img_n = ImageTk.PhotoImage(Image.open(background_abs_updt + "\\Background2.JPG"))
    frame_n = Frame(new_window, width=800, height=500)
    frame_n.pack()
    frame_n.place(anchor='center', relx=0.5, rely=0.5)

    labeln = Label(frame_n, image=img_n)
    label.image = img_n
    labeln.pack()

    nationality_label = Label(new_window, text="Pick a Nationality.")
    nationality_label.configure(bg="#CCC9C0", highlightbackground="#CCC9C0", font=("PT Monoa", 13))
    nationality_label.pack()
    global clicked_nation
    clicked_nation = tk.StringVar()
    nationality_option = tk.OptionMenu(new_window, clicked_nation,
                                       *nationality_name_list, command=nationality_func_command1)

    nationality_option.configure(bg="#CCC9C0", highlightbackground="#CCC9C0", font=("PT Monoa", 13))
    nationality_option.pack(padx=50, pady=3)


# progress bar int for completion -- 7.692307692307692


def bar_command1():
    global bar_real
    bar_real = ttk.Progressbar(extra_stats_win, orient=HORIZONTAL, length=250)
    tasks = 30
    x = 0
    while x < tasks:
        time.sleep(1)
        try:
            bar_real['value'] += 3.68
        except:
            pass
        x += 1
    try:
        bar_real.destroy()
    except RuntimeError:
        pass
    Label_bar.destroy()


def bar():
    global Label_bar
    Label_bar = tk.Label(extra_stats_win,
                         text="Please Wait...",
                         command=threading.Thread(target=bar_command1).start())
    Label_bar.pack()
    bar_real.pack()
    s = ttk.Style()
    s.theme_use('alt')

    # bar_real.configure("blue.Horizontal.TProgressbar", foreground='blue', BACKGROUND='blue')


def plot():
    import plotly.express as px
    #import matplotlib.pyplot as plt
    #fig, axs = plt.subplots(1, 2, tight_layout=False)
    hist_age = px.histogram(csv_data, x=age, nbins=20, title="Distribution of age.")
    hist_wage = px.histogram(csv_data, x=wage, nbins=20, title="Distribution of wage in pounds (£).")
    hist_height = px.histogram(csv_data, x=height_meters, nbins=20, title="Distribution of height in meters.")
    hist_country = px.histogram(csv_data, x=nationality_name, nbins=20, title="Distribution of nationality.")
    hist_prf_foot = px.histogram(csv_data, x=preferred_foot, nbins=20, title="Distribution of preferred foot.")

    hist_age.show()
    hist_wage.show()
    hist_height.show()
    hist_country.show()
    hist_prf_foot.show()


def check_skew():
    skew_win = Toplevel(root)
    skew_win.title("Check Skewness")

    age_skew = skew(csv_data.age)
    height_skew = skew(csv_data.height_cm)
    wage_skew = skew(csv_data.wage_eur)
    prf_foot_skew = skew(preferred_foot.map({"Right": 1, "Left": 0}))

    age_skew_label = tk.Label(skew_win, text="")
    height_skew_label = tk.Label(skew_win, text="")
    wage_skew_label = tk.Label(skew_win, text="")

    prf_foot_skew_label = tk.Label(skew_win, text="")

    # age
    if age_skew > 0:
        age_skew_label.configure(text="The distribution of age is right skewed.",
                                 font=("PT Monoa", 20))
        age_skew_label.pack(pady=3)
    elif age_skew < 0:
        age_skew_label.configure(text="The distribution of age is left skewed.",
                                 font=("PT Monoa", 20))
        age_skew_label.pack(pady=3)
    else:
        age_skew_label.configure(text="The distribution of age is centrally allocated.",
                                 font=("PT Monoa", 20))
        age_skew_label.pack(pady=3)

    # height
    if height_skew > 0:
        height_skew_label.configure(text="The distribution of height is right skewed.",
                                    font=("PT Monoa", 20))
        height_skew_label.pack(pady=3)
    elif height_skew < 0:
        height_skew_label.configure(text="The distribution of height is left skewed.",
                                    font=("PT Monoa", 20))
        height_skew_label.pack(pady=3)
    else:
        height_skew_label.configure(text="The distribution of height is centrally allocated.",
                                    font=("PT Monoa", 20))
        height_skew_label.pack(pady=3)

    # wage
    if wage_skew > 0:
        wage_skew_label.configure(text="The distribution of wage is right skewed.",
                                  font=("PT Monoa", 20))
        wage_skew_label.pack(pady=3)
    elif wage_skew < 0:
        wage_skew_label.configure(text="The distribution of wage is left skewed.",
                                  font=("PT Monoa", 20))
        wage_skew_label.pack(pady=3)
    else:
        wage_skew_label.configure(text="The distribution of wage is left skewed.",
                                  font=("PT Monoa", 20))
        wage_skew_label.pack(pady=3)
    # prf foot
    if prf_foot_skew > 0:
        prf_foot_skew_label.configure(text="The distribution of preferred foot is right skewed.",
                                      font=("PT Monoa", 20))
        prf_foot_skew_label.pack(pady=3)
    elif prf_foot_skew < 0:
        prf_foot_skew_label.configure(text="The distribution of preferred foot is left skewed.",
                                      font=("PT Monoa", 20))
        prf_foot_skew_label.pack(pady=3)
    else:
        prf_foot_skew_label.configure(text="The distribution of preferred foot is centrally allocated.",
                                      font=("PT Monoa", 20))
        prf_foot_skew_label.pack(pady=3)


int_first_player_label = 0
int_first_player_label1 = 0
if __name__ == "__main__":

    generate_skew_button = tk.Button(root, text="Check skewness", command=check_skew)
    generate_skew_button.configure(bg="#C4A484", font=("PT Monoa", 13))
    generate_skew_button.pack(pady=2, side=BOTTOM)

    generate_plot_button = tk.Button(root, text="Generate Plots", command=threading.Thread(target=plot).start)
    generate_plot_button.configure(bg="#C4A484", font=("PT Monoa", 13))
    generate_plot_button.pack(pady=2, side=BOTTOM)


def fn_get_player(arg):
    global label_player_info
    global int_first_player_label
    global options_footballer

    global intPlayerIndex
    intPlayerIndex = short_name_list.index(arg)

    try:
        player_info = f"Long Name: {long_name.dropna()[intPlayerIndex]}" \
                      f"\nShort Name: {short_name_list[intPlayerIndex]}" \
                      f"\nAge: {str(age_list[intPlayerIndex])}\nWage: £{str(int(wage_list[intPlayerIndex]))}" \
                      f"\nPotential: {str(potential_list[intPlayerIndex])}" \
                      f"\nHeight:{str(height_meters[intPlayerIndex])}meters" \
                      f"\nPreferred foot: {preferred_foot_list[intPlayerIndex]}" \
                      f"\nInternational reputation: {str(international_reputation_list[intPlayerIndex])}"

    except ValueError:
        player_info = f"Long Name: {long_name.dropna()[intPlayerIndex]}" \
                      f"\nShort Name: {short_name_list[intPlayerIndex]}" \
                      f"\nAge: {str(age_list[intPlayerIndex])}\nWage: £ 0" \
                      f"\nPotential: {str(potential_list[intPlayerIndex])}" \
                      f"\nHeight: {str(height_meters[intPlayerIndex])} meters" \
                      f"\nPreferred foot: {preferred_foot_list[intPlayerIndex]}" \
                      f"\nInternational reputation: {str(international_reputation_list[intPlayerIndex])}"

    if int_first_player_label != 0:
        label_player_info.destroy()
    int_first_player_label = 1
    label_player_info = Label(root, text=player_info)
    label_player_info.configure(bg="#4b322a", fg="white", font=("PT Monoa", 13))
    label_player_info.pack(pady=3)


nationality_func_btn = tk.Button(root, text="Nationality Analysis", command=nationality_func)
try:
    nationality_func_btn.configure(bg="#C4A484", highlightbackground="#C4A484", font=("PT Monoa", 13))

except:
    pass
nationality_func_btn.pack(pady=2, side=BOTTOM)
extra_stats_func_btn = tk.Button(root, text="Overall Statistics",
                                 command=threading.Thread(target=lambda: extra_stats()).start)
extra_stats_func_btn.configure(bg="#C4A484", highlightbackground="#C4A484", font=("PT Monoa", 13))
extra_stats_func_btn.pack(padx=2, pady=3, anchor=NW)

# map_img_org = (Image.open("location-map-logo_red.png"))
# map_img_resized = map_img_org.resize((50, 50), Image.ANTIALIAS)
# map_img_new = ImageTk.PhotoImage(map_img_resized)

# frame_img_map = Frame(root, width=50, height=50)

# map_img_label = tk.Label(frame_img_map, image = map_img_new)
# map_img_label.image = map_img_new
# map_img_label.pack(padx = 5)

int_first = 0


def options_footballer_operations(arg):
    global int_first
    global options_footballer
    # global int_first_player_label
    # int_first_player_label = 0
    if int_first != 0:
        options_footballer.destroy()
    # if int_first_player_label != 0:
    #    label_player_info.destroy()
    int_first = 1
    # int_first_player_label =1

    if arg == filter_list[0]:
        options_footballer = tk.OptionMenu(root, clicked_players, *short_name_list, command=fn_get_player)
    elif arg == filter_list[1]:
        options_footballer = tk.OptionMenu(root, clicked_players, *short_name_fam, command=fn_get_player)

    options_footballer.configure(bg="#C4A484", highlightbackground="#C4A484", font=("PT Monoa", 13))
    options_footballer.pack()


# options_filter_label
options_filter_label = Label(root, text="Pick a Filter")
options_filter_label.configure(bg="#FFE5B4", fg="black", font=("PT Monoa", 13))
clicked_filters = tk.StringVar()
options_filter_label.pack()

# options_filter
options_filter = tk.OptionMenu(root, clicked_filters, *filter_list, command=options_footballer_operations)
options_filter.configure(bg="#C4A484", highlightbackground="#C4A484", font=("PT Monoa", 13))
options_filter.pack()

clicked_players = tk.StringVar()

options_footballer_label = Label(root, text="Pick a Footballer")
options_footballer_label.configure(bg="#FFE5B4", fg="black", font=("PT Monoa", 13))
options_footballer_label.place(x=195, y=7)
options_footballer_label.pack()

root.mainloop()
try:
    root.destroy()

except:
    print("Program executed successfully.")
