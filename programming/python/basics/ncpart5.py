#ask your customer what their name is with the input() function and store that in variable name.abs
name = input("What is your name?\n").lower()

if name == "ben":
    evil_status = input("Are you evil?\n").lower()
    if evil_status == "yes":
        print("You're not welcome here Ben!!!! fuck off!!!")
        exit()
    elif evil_status == "no":
        print("oh, so your one of those good Bens. come on in!!!")
    else:
        print("Why are you being weird?")
else:
    print("Hello " + name + ", thank you so much for coming in today.\n\n\n")

# Let's add a feature where we ask the user for their favorite color
favorite_color = input("What's your favorite color?\n").lower()

# We can use a dictionary to store some color meanings
color_meanings = {
    "red": "Red is the color of fire and blood, so it is associated with energy, war, danger, strength, power, determination as well as passion, desire, and love.",
    "blue": "Blue is the color of the sky and sea. It is often associated with depth and stability. It symbolizes trust, loyalty, wisdom, confidence, intelligence, faith, truth, and heaven.",
    "green": "Green is the color of nature. It symbolizes growth, harmony, freshness, and fertility. Green has strong emotional correspondence with safety.",
    # Add more colors and their meanings here
}

# Now we can tell the user what their favorite color means
if favorite_color in color_meanings:
    print("Your favorite color is " + favorite_color + ". Here's what it means: " + color_meanings[favorite_color])
else:
    print("I'm sorry, I don't know the meaning of that color.")