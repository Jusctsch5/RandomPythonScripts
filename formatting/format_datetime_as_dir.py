from datetime import datetime
import os

now = str(datetime.now())
now = now.replace(" ", "_")

user_path = os.path.expanduser('~')
print(user_path)
upgrade_dir = f"{user_path}/helm_upgrade_history/namespace/{now}"
if not os.path.exists(upgrade_dir):
    os.makedirs(upgrade_dir)
