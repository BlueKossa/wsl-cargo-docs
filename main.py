#!/bin/python3
from subprocess import PIPE, run
from threading import Thread
from sys import argv


def run_server(port):
    cmd = ["npx", "serve", "-n", "-p", str(port), "./target/doc"]
    run(cmd, stdout=PIPE, universal_newlines=True)


def main():
    port = argv[1] if len(argv) > 1 else 2048
    Thread(target=run_server, args=(port,)).start()
    color = "\033[92m"
    print(f"Server running at {color}http://localhost:{port}\n")
    c = ""
    while c != "q":
        run(["cargo", "doc"])
        c = input("Reload? (q to quit) ")

 
if __name__ == "__main__":
    main()
