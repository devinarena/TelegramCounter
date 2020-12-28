from bs4 import BeautifulSoup
import matplotlib.pyplot as plot
import numpy as np
import os.path
import re

# Global variables used in functions
num_messages = {}
years = []

# Opens a directory specified by the user then loops through all messages.html files
# using BeautifulSoup to parse each one and get the number of messages per month.
# Adds these messages to our num_messages dictionary to be used when displaying the barplot.
def find_messages():
    # ask for a directory until a valid one is provided
    directory = input("Directory to analyze (CTRL+C to cancel): ")
    while not os.path.isdir(directory):
        print("Directory does not exist!")
        directory = input("Directory to analyze (CTRL+C to cancel): ")
    today = ""  # the day we are currently analyzing
    index = 1   # the index of the file, when messages{index}.html is not found, the loop terminates
    while os.path.exists(f"{directory}/messages{index}.html"):
        # open the html document and parse it with BeautifulSoup
        html_doc = open(f"{directory}/messages{index}.html", encoding="utf-8") 
        soup = BeautifulSoup(html_doc, "html.parser")

        # find every div tag with the CSS class message (these are our messages) 
        for tag in soup.select("div.message"):
            # ensure the class attribute of the tag exists
            if "class" in tag.attrs:
                # find the class attribute
                class_ = tag.attrs["class"]
                # if the class contains service, its either the date or a pinned message
                if "service" in class_:
                    # contents of the inner tag are located on the second line
                    message = str(tag.contents[1]).split("\n")[1]
                    # the year is the third token of the date, if it exists
                    if not " " in message or len(message.split(" ")) < 3:
                        continue
                    possible_year = message.split(" ")[2]
                    # ensure the date we located is a proper year using regex
                    if re.match(r'.*([1-3][0-9]{3})', possible_year) is not None:
                        # set today to the month and year
                        today = message.split(" ")[1] + message.split(" ")[2]
                        if not possible_year in years:
                            # append the year all years if its not currently there
                            years.append(possible_year) 
                # proper messages contain the css class clearfix
                elif "clearfix" in class_:
                    # if today is in messages increment the counter
                    if str(today) in num_messages:
                        num_messages[str(today)] += 1
                    #otherwise intialize the counter to 1
                    else:
                        num_messages[str(today)] = 1
        index += 1  # increment the index (move on to the next file if it exists)

# Plots the data using matplotlib on a bar chart. Plots every year as a different color.
# Each month is on the x axis and number of messages is on the y axis.
def plot_data():
    # Every month of the year as the x-axis labels
    labels = [ "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December" ]
    # Values we pull from the num_messages dictionary
    values = []
    # loop over every year and pull the messages per month adding them to an array in order
    index = 0
    for year in years:
        values.append([])
        for month in labels:
            # if the month and year combo exists in the dictionary we add it to the array
            if (month + year) in num_messages:
                values[index].append(num_messages[month + year])
            # otherwise default the value to 0
            else:
                values[index].append(0)
        index += 1 # next year

    # the number of bars is equal to the length of the values 2D array (also the number of years)
    num_bars = len(values)
    # generate x positions for the bars
    x = np.arange(len(labels))
    # calculate the width of the bars
    width = 0.40 - (num_bars * 0.04)

    # generate a subplot
    fig, ax = plot.subplots()
    # initialzie the size of the figure
    fig.set_size_inches(11 + num_bars, 6)
    # create a bar located around the x point, one bar per each year
    # the spacing of the bar is dependent on whether theres an even or odd number of years
    # the label is just the year, for the legend
    for i in range(num_bars):
        ax.bar(x + ((1 - num_bars) / 2 + i) * width, values[i], width, label=years[i])

    # init the axis labels
    ax.set_ylabel("Messages")
    ax.set_xlabel("Month")
    # init the title
    ax.set_title("Telegram Messages")
    # set the x tick marks
    ax.set_xticks(x)
    # set the labels for the x tick marks to the months
    ax.set_xticklabels(labels)
    # show a legend for each year
    ax.legend()

    # display the plot
    plot.show()

# Main entry point for the program
if __name__ == "__main__":
    # find the messages from the html files
    find_messages()
    # plot them on a barplot
    plot_data()