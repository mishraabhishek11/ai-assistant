from openai import OpenAI
from dotenv import load_dotenv
import os
from assistant_role import get_role_prompt
from tools import get_current_time, roll_dice, generate_password


# Load configuration
load_dotenv()

# Create AI client
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

print("=" * 40)
print("      My AI Assistant")
print("=" * 40)


print("""Choose Your Assistant

1. Friendly School Teacher
2. Senior Python Developer
3. Experienced Travel Guide
4. Motivational Coach
5. Professional Interviewer 
""")

choice = input("\nEnter your choice : ")

system_message = get_role_prompt(choice)

print("\nYou have selected:", system_message)


messages = [{"role": "system",
             "content": system_message}]

while True:

    user_input = input("\nYou : ")
    messages.append({"role": "user", "content": user_input})

    if user_input.lower() == "quit":
        messages.append(
            {"role": "assistant", "content": "Goodbye! Have a great day."})
        print("\nAI  : Goodbye! Have a great day.")
        break

    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=messages
    )

    response_message = response.choices[0].message.content
    messages.append({"role": "assistant", "content": response_message})

    print("\nAI :", response_message)
