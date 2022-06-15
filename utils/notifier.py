import subprocess

COMMAND = '''
on run argv
display notification (item 2 of argv) with title (item 1 of argv)
end run
'''

def send(title, text):
    subprocess.call(['osascript', '-e', COMMAND, title, text])