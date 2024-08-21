import subprocess

command = ['which', 'foo_echo.sh']
p = subprocess.run(command, capture_output=True, text=True)
print(p.stdout)

p = subprocess.run(command, capture_output=True, text=True, env=None)
print(p.stdout)

env = {'Bongo': 'Bongo'}
p = subprocess.run(command, capture_output=True, text=True, env=env)
print(p.stdout)

# Launch the command using subprocess.Popen
command = ['foo_echo.sh', '10']
process = subprocess.Popen(command)

# Wait for the process to finish
process.wait()
print("Output for foo_echo.sh")
print(process)


# PATH=$PATH:/work/z2/johns/source/repos/RandomPythonScripts/subprocess/path python3 subprocess_path.py
# python3 subprocess_path.py