import sys
sys.dont_write_bytecode = True

import speech_recognition as sr
import pyttsx3


# Confirmed working microphone
MICROPHONE_INDEX = 1


def speak(text):
    """
    Converts text response into speech.
    """

    print(f"\nAI: {text}")

    try:
        engine = pyttsx3.init()

        engine.setProperty("rate", 170)
        engine.setProperty("volume", 1.0)

        engine.say(text)
        engine.runAndWait()
        engine.stop()

    except Exception as error:
        print(f"Speech output error: {error}")


def get_voice_command():
    """
    Captures a voice command and converts it to text.
    """

    recognizer = sr.Recognizer()

    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 1.0
    recognizer.phrase_threshold = 0.3
    recognizer.non_speaking_duration = 0.5

    print("\n======================================")
    print("             VOICE INPUT")
    print("======================================")
    print("Microphone is ready.")
    print("Speak your command clearly.")

    try:

        with sr.Microphone(
                device_index=MICROPHONE_INDEX
        ) as source:

            print("\nAdjusting microphone...")
            recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            print("Listening...\n")

            audio = recognizer.listen(
                source,
                timeout=8,
                phrase_time_limit=12
            )

        print("Processing your command...")

        command = recognizer.recognize_google(
            audio,
            language="en-IN"
        )

        print(f"You: {command}")

        return command.lower().strip()

    except sr.WaitTimeoutError:

        print("No speech detected.")
        return ""

    except sr.UnknownValueError:

        print("Sorry, I could not understand the speech.")
        return ""

    except sr.RequestError as error:

        print(
            f"Speech recognition service error: {error}"
        )
        return ""

    except Exception as error:

        print(f"Microphone error: {error}")
        return ""


def get_text_command():
    """
    Gets a command using keyboard input.
    """

    print("\n======================================")
    print("              TEXT INPUT")
    print("======================================")

    command = input("You: ")

    return command.lower().strip()


def get_command():

    print("\n--------------------------------------")
    print("         CHOOSE INPUT METHOD")
    print("--------------------------------------")
    print("1. Voice")
    print("2. Text")
    print("--------------------------------------")

    choice = input("Enter your choice (1/2): ").strip()

    if choice == "1":

        command = get_voice_command()

        if not command:

            print("\nVoice input was not understood.")
            print("Switching to text input...")

            command = get_text_command()

        return command

    elif choice == "2":

        return get_text_command()

    else:

        print("\nInvalid choice. Please select 1 or 2.")
        return ""


if __name__ == "__main__":

    print("\n======================================")
    print("        DIALOG SYSTEM TEST")
    print("======================================")

    command = get_command()

    if command:
        print("\nCommand received:", command)
    else:
        print("\nNo command received.")