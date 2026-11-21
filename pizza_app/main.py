import os
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationSummaryBufferMemory

try:
    from pizza_app.chat_commands import is_quit_or_exit_command, is_summary_command
except ImportError:
    from chat_commands import is_quit_or_exit_command, is_summary_command

# --- 1. Load Environment and LLM ---
load_dotenv()

if os.getenv("GOOGLE_API_KEY") is None:
    print("Error: GOOGLE_API_KEY environment variable not set.")
    exit()

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)

# --- 2. Define the System Prompt ---
SYSTEM_PROMPT_TEMPLATE = """
You are an AI assistant for 'Nebula Pizza Store', a friendly and helpful virtual cashier.
Your goal is to provide an excellent customer experience by helping users order pizza.

---
**CRITICAL INSTRUCTION: You MUST conduct the entire conversation in the Georgian language (ქართული ენა).** 
All your greetings, questions, and responses to the user must be in Georgian.
---

Your capabilities (perform all these in Georgian):
- Greet the customer warmly.
- Present the menu and answer questions about it. You must translate the menu items and details into Georgian for the customer.
- Take the customer's order item by item.
- Suggest popular items or pairings if the customer is unsure.
- Handle order modifications (e.g., adding/removing toppings).
- Confirm the complete order with the customer before finalizing.
- Be conversational, polite, and a little bit fun. Use emojis where appropriate!

Our Menu (This is your source of truth data. Translate it for the user):
- Pizzas:
  - Margherita: Tomato, Mozzarella, Basil - $12
  - Pepperoni: Classic Pepperoni, Mozzarella - $14
  - Veggie Supreme: Bell Peppers, Onions, Olives, Mushrooms - $15
  - Meat Lover's: Pepperoni, Sausage, Bacon - $16
- Sides:
  - Garlic Knots (6 pcs) - $6
  - Caesar Salad - $8
- Drinks:
  - Soda (Coke, Sprite) - $2
  - Water - $1

Important Rules (follow these strictly):
1.  **Language:** Your primary and only language for user interaction is Georgian.
2.  **No Payments:** Do not take payment information.
3.  **Menu Adherence:** If asked about something not on the menu, politely state that it's not available (in Georgian).
4.  **Final Confirmation:** At the end of the conversation, summarize the final order and ask for confirmation (in Georgian).
"""

# --- 3. Create the Prompt Template and Memory ---
prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT_TEMPLATE),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
])

memory = ConversationSummaryBufferMemory(
    llm=llm,
    max_token_limit=800,
    memory_key="history",
    return_messages=True
)

# --- 4. Create the Modern LCEL Chain  ---
chain = (
    RunnablePassthrough.assign(
        history=lambda x: memory.load_memory_variables(x)["history"]
    )
    | prompt
    | llm
    | StrOutputParser()
)

# --- 5. Define the Main Chatbot Loop ---
def run_chatbot():
    """
    Runs the main loop for the Pizza AI Chatbot.
    """
    print("გამარჯობა, რით შემიძლია დაგეხმაროთ?")
    print("Type 'quit' to exit or '!summary' to see the conversation summary.\n")

    while True:
        try:
            user_input = input("You: ")

            if is_quit_or_exit_command(user_input):
                print("\nნახვამდის! 👋")
                break

            if is_summary_command(user_input):
                current_summary = memory.moving_summary_buffer
                if not current_summary:
                    print("\n[System: ჯერ საუბრის ისტორია არ არის.]")
                else:
                    print("\n--- მიმდინარე საუბრის ისტორია ---")
                    print(current_summary)
                continue

            inputs = {"input": user_input}
            response = chain.invoke(inputs)

            # Manually save the context to memory for the next turn
            memory.save_context(inputs, {"output": response})

            print(f"Gino: {response}")

        except Exception as e:
            print(f"\n[Error: An unexpected error occurred: {e}]")

if __name__ == "__main__":
    run_chatbot()
