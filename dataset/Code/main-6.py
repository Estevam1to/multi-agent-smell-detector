#!/usr/bin/env python3
"""
    pyed - a simple 1 line based text editor

    Manual: readme.txt
    Copyright 2021 Ian Hiew

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""


import os

def write(filename,contents):
    f = open(filename,"a")
    f.write(contents)
    if f:
        print(f'*{filename}: {os.path.getsize(filename)}')
        f.close()
    else:
        print("!")

def read(filename,mode):
    f = open(filename,"r")
    if mode == "p":
        print(f.read())
        print(f'{filename}: {os.path.getsize(filename)}')
        print("*")
        f.close()
    elif mode == "n":
        # github copilot made this. nice.
        # print every line of filename with line number in front
        li = f.readlines()
        for i in range(len(li)):
            print(f'{i+1} {li[i]}')
        print(f'{filename}: {os.path.getsize(filename)}')
        f.close()
    else:
        print("?")

def removeLine(filename,line):
    f = open(filename,"r")
    # catch if line numbers is larger than file's line numbers
    li = f.readlines()
    if line > int(li):
        print("?")
    else:
        print(li[line])
        with open(filename,"a") as fi:
            li[line] = "\n"
            if li:
                print("*")
            else:
                print("!")

def sizeof(filename):
    if os.path.getsize(filename):
        return os.path.getsize(filename)
    else:
        return "!"

def main():
    running = True
    while running:
        k = input()
        
        if k == "q":
            quit()

        else:
            sk = k.split(" ")
            try:
                if sk[0] == "w":
                    getInput = True

                    while getInput:
                        wInput = input()
                        if wInput != ".":
                            write(sk[1],f'\n{wInput}')
                        else:
                            getInput = False
                            print("*")
                
                elif sk[0] == "p":
                    read(sk[1],"p")
                
                elif sk[0] == "n":
                    read(sk[1],"n")
                
                #elif sk[0] == "r":
                    #if sk[2]:
                        #removeLine(sk[1],int(sk[2]))
                    #else:
                        #print("!")
                
                elif sk[0] == "s":
                    print(sizeof(sk[1]))
            
            except Exception as e:
                print(e)

if __name__ == "__main__":
    print("*")
    main()