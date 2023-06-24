#!/bin/env python3
from subprocess import PIPE, run, Popen
from threading import Thread, Event
from sys import argv

event = Event()

def run_server(port):
    cmd = ["npx", "serve", "-n", "-p", str(port), "./target/doc"]
    server = Popen(cmd, stdout=PIPE, universal_newlines=True)
    event.wait()
    server.kill()
    
    


def get_project_name():
    with open("Cargo.toml") as f:
        for line in f:
            if line.startswith("name"):
                name = line.split("=")[1].strip()[1:-1]
                name = name.replace("-", "_")
                return name
    return None


def main():
    port = argv[1] if len(argv) > 1 else 2048
    server = Thread(target=run_server, args=(port,))
    server.start()

    project_name = get_project_name()
    color = "\033[92m"
    no_color = "\033[0m"
    print(f"Server running at {color}http://localhost:{port}{no_color}")
    if project_name:
        print(f"Project docs at {color}http://localhost:{port}/{project_name}{no_color}\n")
    
    c = ""
    while c != "q":
        run(["cargo", "doc"])
        c = input("Reload? (q to quit) ").strip()
    print("Shutting down...")
    event.set()
    server.join()
    

 
if __name__ == "__main__":
    main()
