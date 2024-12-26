import keyboard

def on_key_event(event):
    print(f"Key {event.name} {event.event_type}")

keyboard.hook(on_key_event)
keyboard.wait('esc')  # Press 'esc' to exit