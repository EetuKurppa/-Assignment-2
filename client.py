#Eetu Kurppa
#Declaration of AI usage:I used ChatGPT to fix my code after I included threading for the code to handle multiple client requests at once.

import xmlrpc.client
import datetime

proxy = xmlrpc.client.ServerProxy("http://localhost:5000/")

def add_note():
    topic = input("Enter topic name: ")
    text = input("Write your note: ")
    timestamp = datetime.datetime.now().isoformat()

    try:
        response = proxy.add_note(topic, text, timestamp)
        if response["is_new_topic"]:
            print("Note added successfully!")
        else:
            print("Note added to an existing topic.")
    except xmlrpc.client.Fault as err:
        print("Server error: " + str(err))
    except xmlrpc.client.ProtocolError as err:
        print("Protocol error: " + str(err))
    except Exception as e:
        print("An unexpected error occurred: " + str(e))

def get_notes():
    topic = input("Enter topic name to retrieve notes: ")
    
    try:
        notes = proxy.get_notes(topic)
        if isinstance(notes, list):
            print("\nNotes for topic: " + topic)
            for note in notes:
                print("- " + note)
        else:
            print(notes)
    except xmlrpc.client.Fault as err:
        print("Server error: " + str(err))
    except xmlrpc.client.ProtocolError as err:
        print("Protocol error: " + str(err))
    except Exception as e:
        print("An unexpected error occurred: " + str(e))

while True:
    print("\nChoose an action:")
    print("1 - Add a note")
    print("2 - Retrieve notes")
    print("3 - Exit")

    choice = input("Selection: ")

    if choice == "1":
        add_note()
    elif choice == "2":
        get_notes()
    elif choice == "3":
        break
    else:
        print("Invalid choice, please try again.")

