from datetime import datetime


# * Add Zero in front of single digit numbers
def addZero(num) -> str:
    if num < 10:
        return f"0{num}"
    return f"{num}"
# * By GitHub Copilot ✨


def getTime() -> str:
    now = datetime.now()
    return f"{addZero(now.hour)}:{addZero(now.minute)}:{addZero(now.second)}"
