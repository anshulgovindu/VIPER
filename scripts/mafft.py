import subprocess

def mafft_local(input, output, gap_open_penalty = None, offset = None , gap_extend_penalty = None):
    starter = ["wsl", "mafft", "--auto", "--localpair"]
    "" if gap_open_penalty == None else starter.extend(["--lop", str(gap_open_penalty)])
    "" if gap_open_penalty == None else starter.extend(["--lep", str(offset)])
    "" if gap_open_penalty == None else starter.extend(["--lexp", str(gap_extend_penalty)])
    starter.extend([input, ">", output])
    subprocess.run(starter, shell = True)