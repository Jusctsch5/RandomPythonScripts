import subprocess

output = subprocess.run(["pgrep", "^myriad_masterd"], stdout=subprocess.PIPE, text=True)
print(output.stdout)

output = subprocess.run(["pgrep", "^myriad_targetd"], stdout=subprocess.PIPE, text=True)
print(output.stdout)


output = subprocess.run(["pgrep", "^bash"], stdout=subprocess.PIPE, text=True)
print(output.stdout)
pid_list = output.stdout.split('\n')
print(pid_list)


print("ps myriad_masted")
cmd = ["ps", "-aux", "|", "grep", "-i", "^myriad_masterd"]
print(" ".join(cmd))
output = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
print(output.stdout)
pid_list = output.stdout.split('\n')
print(pid_list)
