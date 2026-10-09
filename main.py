import sys
sys.dont_write_bytecode = True

from face_auth import authenticate_face
from dialog import get_command, speak
from commands import execute_command


def show_banner():

    print("\n==============================================")
    print("                    NEXA AI")
    print("==============================================")
    print("             AI PERSONAL ASSISTANT")
    print("==============================================")


def main():

    show_banner()

    print("\nStarting NEXA AI...")
    print("Initializing security system...")

    # ==========================================
    # STEP 1 — FACE AUTHENTICATION
    # ==========================================

    authenticated = authenticate_face()

    if not authenticated:

        print("\n==============================================")
        print("                 ACCESS DENIED")
        print("==============================================")
        print("Face authentication was not completed.")
        return

    # ==========================================
    # STEP 2 — ACCESS GRANTED
    # ==========================================

    print("\n==============================================")
    print("                 ACCESS GRANTED")
    print("==============================================")
    print("Authentication successful.")
    print("NEXA AI is ready.")
    print("==============================================")

    speak(
        "Authentication successful.\n "
        "   Welcome to Nexa AI. How can I help you?\n"
        "   Type or say HELP to see available commands and EXIT to quit"
    )

    # ==========================================
    # STEP 3 — COMMAND LOOP
    # ==========================================

    while True:

        command = get_command()

        if not command:

            print("\nNo command received.")
            continue

        # ======================================
        # STEP 4 — COMMAND PROCESSING
        # ======================================

        print("\nProcessing command...")

        response, should_exit = execute_command(
            command
        )

        # ======================================
        # STEP 5 — AI RESPONSE
        # ======================================

        speak(response)

        # ======================================
        # STEP 6 — EXIT
        # ======================================

        if should_exit:
            break

    # ==========================================
    # APPLICATION CLOSED
    # ==========================================

    print("\n==============================================")
    print("                 NEXA AI CLOSED")
    print("==============================================")
    print("Thank you for using NEXA AI.")


if __name__ == "__main__":
    main()