#Eetu Kurppa
#Declaration of AI usage: I used ChatGPT to fix my code after I included threading for the code to handle multiple client requests at once.

from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn
import xml.etree.ElementTree as ET
import threading
import datetime

XML_FILE = "notes.xml"

def initialize_xml():
    try:
        tree = ET.parse(XML_FILE)
    except FileNotFoundError:
        root = ET.Element("notes")
        tree = ET.ElementTree(root)
        tree.write(XML_FILE)
    return ET.parse(XML_FILE)

def add_note(topic, text, timestamp):
    tree = initialize_xml()
    root = tree.getroot()

    timestamp_obj = datetime.datetime.fromisoformat(timestamp)
    formatted_timestamp = timestamp_obj.strftime("%m/%d/%y - %H:%M:%S")

    topic_element = root.find("./topic[@name='" + topic + "']")
    if topic_element is None:
        topic_element = ET.SubElement(root, "topic", name=topic)
        is_new_topic = True
    else:
        is_new_topic = False

    note_text = text

    note = ET.SubElement(topic_element, "note")
    note.set("timestamp", formatted_timestamp)
    note.text = note_text 

    tree.write(XML_FILE)

    return {
        "message": "Note added under the topic '" + topic + "'.",
        "is_new_topic": is_new_topic
    }


def get_notes(topic):
    tree = initialize_xml()
    root = tree.getroot()

    topic_element = root.find("./topic[@name='" + topic + "']")
    if topic_element is None:
        return ["No notes found for topic '" + topic + "'."]
    
    notes = []
    for note in topic_element.findall("note"):
        note_text = note.text
        timestamp = note.get("timestamp")
        notes.append(f"{note_text} {timestamp}")
    
    return notes if notes else ["No notes."]

class ThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

def run_server():
    server = ThreadedXMLRPCServer(("localhost", 5000), allow_none=True)
    print("Serving XML-RPC on localhost port 5000")
    server.register_function(add_note, "add_note")
    server.register_function(get_notes, "get_notes")
    server.serve_forever()

if __name__ == "__main__":
    server_thread = threading.Thread(target=run_server)
    server_thread.start()



