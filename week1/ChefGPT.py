from openai import OpenAI

client = OpenAI()

model = "gpt-4-turbo-preview"

def handle_option(option, dish=None, ingredients=None, recipe=None):
    if option == 1:
        return f"Suggest dishes based on ingredients: {ingredients}\n"
    elif option == 2:
        return f"Give recipes to dish: {dish}\n"
    elif option == 3:
        return f"Criticize the recipe: {recipe}\n"
    else:
        return "Invalid option selected.\n"

def prompt_user():
    print("Select an option (1-3):")
    print("1. Suggest dishes based on ingredients")
    print("2. Give recipes to dishes")
    print("3. Criticize recipes")
    
    while True:
        option = input()
        if option.isdigit():
            option = int(option)
            if option in [1, 2, 3]:
                if option == 1:
                    ingredients = input("Enter ingredients:\n")
                    return option, ingredients
                elif option == 2:
                    dish = input("Type the name of the dish you want a recipe for:\n")
                    if not dish:
                        print("Please provide a dish name.")
                        continue
                    return option, dish
                elif option == 3:
                    recipe = input("Enter the recipe to criticize:\n")
                    return option, recipe
            else:
                print("Invalid option. Please select a number between 1 and 3.")
        else:
            print("Invalid input. Please enter a number.")

while True:
    messages = [
        {
            "role": "system",
            "content": (
                "You are an experienced Spanish chef, specialized in Mediterranean cuisine. "
                "You provide detailed cooking instructions, tips, and advice on selecting the best ingredients. "
                "If you receive a number '1:' and a list of ingredients, you only answer with the dish name of Mediterranean cuisine, if you find it. "
                "If you receive a number '2:' and a dish name, then you only answer with the detailed recipe and how to cook it and present it. "
                "If you receive a number '3:' and a recipe name or a dish name, then you answer criticizing that recipe, and suggesting at least one way to improve it, "
                "making it tastier and fresher. "
                "If you receive another number or another type of text that is not a list of food ingredients or a dish name, "
                "you only answer with 'wrong option, try again, please'."
            ),
        },
##        {
##            "role": "system",
##            "content": (
##                "Your client is going to ask for three different possible inputs: \n"
##                "1. Suggest dishes based on ingredients. \n"
##                "2. Give recipes to dishes. \n"
##                "3. Criticize recipes. Please, be kind and suggest at least one way to improve the recipe."
##            ),
##        }
    ]

    option, data = prompt_user()
    messages.append(
        {
            "role": "user",
            "content":  f"{option}: {data}"
        }
    )

    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
    )

    collected_messages = []
    for chunk in stream:
        chunk_message = chunk.choices[0].delta.content or ""
        print(chunk_message, end="")
        collected_messages.append(chunk_message)

    messages.append(
        {
            "role": "system",
            "content": "".join(collected_messages)
        }
    )

    choice = input("\nDo you want to continue? (yes/no): ").lower()
    if choice != 'yes':
        break



