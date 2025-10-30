# Description: A simple dialog with rich.prompt and rich.table

# As generated,
# 1. there is no confirm method on the prompt object.
# Instead, the Confirm class should be used.

# Also, I added the error handling suggested in the second response, but it
# does not work as expected.  Github copilot had a better suggestion, which is incorporated below.

from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich.prompt import Confirm

console = Console()
prompt = Prompt()

# Define a list of actions
actions = [["Option 1"], ["Option 2"], ["Option 3"], ["Quit"]]

# Create table
table = Table(title="Available actions")
table.add_column("Actions")

for action in actions:
    table.add_row(*action)

# Ask the user to select an action
while True:
    console.print(table)
    selected_action = prompt.ask("Please select an action:")
    if selected_action == "Quit":
        confirm = Confirm.ask("Are you sure you want to quit?")
        if confirm:
            break
        else:
            continue
    elif selected_action not in [action[0] for action in actions]:
        console.print(f"Invalid action: {selected_action}", style="bold red")
    else:
        console.print(f"You selected: {selected_action}")
