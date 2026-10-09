import sys
sys.dont_write_bytecode = True

import webbrowser
from datetime import datetime
from urllib.parse import quote


def execute_command(command):

    command = command.lower().strip()

    # EXIT
    if any(word in command for word in ["exit", "quit", "goodbye", "stop", "bye"]):
        return "Goodbye! Have a great day.", True

    # HELP
    if command == "help":

        print("\n======================================")
        print("          AVAILABLE COMMANDS")
        print("======================================")

        print("\nGreetings:")
        print("  • hi / hello / hey")
        print("  • how are you?")
        print("  • who are you?")
        print("  • what can you do?")
        print("  • thank you")

        print("\nInformation:")
        print("  • what is the time?")
        print("  • what is today's date?")

        print("\nWebsites:")
        print("  • open Google")
        print("  • open YouTube")

        print("\nApplications:")
        print("  • open Calculator")
        print("  • open Notepad")
        print("  • open Word / PowerPoint / Excel")

        print("\nSearch:")
        print("  • search for <topic>")

        print("\nSystem:")
        print("  • help")
        print("  • exit / quit / bye / goodbye")

        print("======================================")

        return "I have displayed the available commands.", False

        return "I have displayed the available commands.", False

    # GREETINGS
    if command in ["hi", "hello", "hey", "hy"]:
        return (
            "Hello! I'm Nexa, your AI personal assistant. "
            "How can I help you?",
            False
        )

    # THANK YOU / APPRECIATION
    if any(
        phrase in command
        for phrase in ["thank you", "thanks", "thank u", "thx"]
    ):
        return (
            "You're welcome! I'm happy to help you.",
            False
        )

    # HOW ARE YOU
    if "how are you" in command or "how ru" in command:
        return (
            "I'm doing great! What can I do for you?",
            False
        )

    # WHO ARE YOU
    if "who are you" in command or "what are you" in command:
        return (
            "I'm NEXA, your AI personal assistant, "
            "created as part of the AI Capstone.",
            False
        )

    # WHAT CAN YOU DO
    if "what can you do" in command:
        return (
            "I can open websites and applications, "
            "tell you the time and date, search the web, "
            "and respond to basic commands. "
            "Say help to see the full command list.",
            False
        )

    # TIME
    if "time" in command:

        current_time = datetime.now().strftime("%I:%M %p")

        return (
            f"The current time is {current_time}.",
            False
        )

    # DATE
    if "date" in command or "today" in command:

        current_date = datetime.now().strftime("%d %B %Y")

        return (
            f"Today's date is {current_date}.",
            False
        )
        
    # WORD
    if "open word" in command or command == "word":

        try:
            import os
            os.system("start winword")

            return "Opening Microsoft Word.", False

        except Exception:
            return "I could not open Microsoft Word.", False

    # POWERPOINT
    if (
        "open powerpoint" in command
        or "open power point" in command
        or command == "powerpoint"
    ):

        try:
            import os
            os.system("start powerpnt")

            return "Opening Microsoft PowerPoint.", False

        except Exception:
            return "I could not open Microsoft PowerPoint.", False

    # EXCEL
    if "open excel" in command or command == "excel":

        try:
            import os
            os.system("start excel")

            return "Opening Microsoft Excel.", False

        except Exception:
            return "I could not open Microsoft Excel.", False

    # GOOGLE
    if "open google" in command:

        webbrowser.open("https://www.google.com")

        return "Opening Google.", False

    # YOUTUBE
    if "open youtube" in command:

        webbrowser.open("https://www.youtube.com")

        return "Opening YouTube.", False

    # CALCULATOR
    if "open calculator" in command or command == "calculator":

        try:
            import os
            os.system("start calc")

            return "Opening Calculator.", False

        except Exception:
            return "I could not open Calculator.", False

    # NOTEPAD
    if "open notepad" in command or command == "notepad":

        try:
            import os
            os.system("start notepad")

            return "Opening Notepad.", False

        except Exception:
            return "I could not open Notepad.", False

    # SEARCH
    if command.startswith("search for "):

        search_query = command.replace(
            "search for ",
            "",
            1
        ).strip()

        if search_query:

            url = (
                "https://www.google.com/search?q="
                + quote(search_query)
            )

            webbrowser.open(url)

            return (
                f"Searching Google for {search_query}.",
                False
            )

    # UNKNOWN COMMAND
    return (
        "I'm sorry, I don't understand the command yet. "
        "Please say help to see what I can do.",
        False
    )


if __name__ == "__main__":

    print("\n======================================")
    print("         COMMAND SYSTEM TEST")
    print("======================================")

    while True:

        command = input("\nEnter a command: ").strip()

        response, should_exit = execute_command(command)

        print("AI:", response)

        if should_exit:
            break