import time
import RNS
import LXMF
import os
import requests


def delivery_callback(message):
    print("\n--- New LXMF Message Received ---")


    gotify_token=os.environ.get('GOTIFY_TOKEN')

    sender_hash = RNS.prettyhexrep(message.source_hash)
    print(f"From (Sender Hash): {sender_hash}")

    # Extract timestamps and content
    print(f"Sent at           : {time.ctime(message.timestamp)}")
    print(f"Title/Subject     : {message.title}")
    content = message.content.decode('utf-8')
    print(f"Content           : {content}")

    #Send message to Gotify 'app'
    resp = requests.post('http://server.local:5555/message', headers={"X-Gotify-Key": gotify_token}, json={
        "message": content + '\n' + sender_hash,
        "priority": 2,
        "title": "From lxmf: " + sender_hash
    })

    print("---------------------------------\n")

def main():
    reticulum = RNS.Reticulum()
    router = LXMF.LXMRouter(storagepath="./lxmf_storage")
    KEY_PATH = "./identities/identity.gotify"

    if os.path.exists(KEY_PATH):
        my_identity = RNS.Identity.from_file(KEY_PATH)
        print("Loaded existing identity.")
    else:
        my_identity = RNS.Identity()
        my_identity.to_file(KEY_PATH)
        print("Created and saved a new identity.")

    my_lxmf_destination = router.register_delivery_identity(
        my_identity, 
        display_name="LXMF2Gotify Bridge Test"
    )

    router.register_delivery_callback(delivery_callback)

    my_address_hex = RNS.prettyhexrep(my_lxmf_destination.hash)
    print(f"[+] LXMF Receiver Ready.")
    print(f"[+] Your LXMF Address is: {my_address_hex}")
    print("[+] Listening for incoming messages... (Press Ctrl+C to exit)")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[-] Shutting down receiver.")

if __name__ == "__main__":
    main()

