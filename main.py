#!/bin/env python3
from subprocess import PIPE, run, Popen
from threading import Thread, Event
from sys import argv
import http.server

killer = Event()

class DirHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Idc some dumb server shit does not work if it is directly in the
        # doc folder
        super().__init__(*args, directory="./target", **kwargs)


def get_project_name():
    with open("Cargo.toml") as f:
        for line in f:
            if line.startswith("name"):
                name = line.split("=")[1].strip()[1:-1]
                name = name.replace("-", "_")
                return name
    return None


def main():
    port = int(argv[1]) if len(argv) > 1 else 2048
    handler = DirHandler
    httpd = http.server.HTTPServer(("", port), handler)
    server = Thread(target=httpd.serve_forever)
    server.start()

    project_name = get_project_name()
    color = "\033[92m"
    no_color = "\033[0m"
    print(f"Server running at {color}http://localhost:{port}{no_color}")
    if project_name:
        print(f"Project docs at {color}http://localhost:{port}/doc/{project_name}{no_color}\n")
    
    c = ""
    while c != "q":
        run(["cargo", "doc"])
        c = input("Reload? (q to quit) ").strip()
    print("Shutting down...")
    httpd.shutdown()
    server.join()
 

if __name__ == "__main__":
    main()
