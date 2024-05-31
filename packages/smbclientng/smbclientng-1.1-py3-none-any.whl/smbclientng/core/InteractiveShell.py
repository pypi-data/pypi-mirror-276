#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : InteractiveShell.py
# Author             : Podalirius (@podalirius_)
# Date created       : 23 may 2024


import datetime
import impacket
from importlib import import_module
import ntpath
import os
import readline
import shutil
import sys
import traceback
from rich.console import Console
from rich.table import Table
from smbclientng.core.CommandCompleter import CommandCompleter
from smbclientng.core.utils import b_filesize, unix_permissions, windows_ls_entry


## Decorators

def command_arguments_required(func):
    def wrapper(*args, **kwargs):
        self, arguments,command  = args[0], args[1], args[2]
        if len(arguments) != 0:
            return func(*args, **kwargs)
        else:
            self.commandCompleterObject.print_help(command=command)
            return None
    return wrapper

def active_smb_connection_needed(func):
    def wrapper(*args, **kwargs):
        self, arguments,command  = args[0], args[1], args[2]
        #
        self.smbSession.ping_smb_session()
        if self.smbSession.connected:
            return func(*args, **kwargs)
        else:
            print("[!] SMB Session is disconnected.")
            return None
    return wrapper

def smb_share_is_set(func):
    def wrapper(*args, **kwargs):
        self, arguments,command  = args[0], args[1], args[2]
        if self.smbSession.smb_share is not None:
            return func(*args, **kwargs)
        else:
            print("[!] You must open a share first, try the 'use <share>' command.")
            return None
    return wrapper


class InteractiveShell(object):
    """
    Class InteractiveShell is designed to manage the interactive command line interface for smbclient-ng.
    
    This class handles user input, executes commands, and manages the state of the SMB session. It provides
    a command line interface for users to interact with SMB shares, execute commands like directory listing,
    file transfer, and more.

    Attributes:
        smbSession (SMBConnection): The active SMB connection session.
        debug (bool): Flag to enable or disable debug mode.
        smb_share (str): The current SMB share in use.
        smb_path (str): The current path within the SMB share.
        commandCompleterObject (CommandCompleter): Object to handle command completion and help generation.

    Methods:
        __init__(self, smbSession, debug=False): Initializes the InteractiveShell with the given SMB session and debug mode.
        run(self): Starts the command line interface loop, processing user input until exit.
    """
    
    def __init__(self, smbSession, debug=False):
        self.smbSession = smbSession
        self.debug = debug

        self.smb_share = None
        self.smb_cwd = ""

        self.modules = {}

        self.commandCompleterObject = CommandCompleter(smbSession=self.smbSession)
        readline.set_completer(self.commandCompleterObject.complete)
        readline.parse_and_bind("tab: complete")
        readline.set_completer_delims("\n")

        self.__load_modules()

    def run(self):
        running = True
        while running:
            try:
                user_input = input(self.__prompt()).strip().split(" ")
                command, arguments = user_input[0].lower(), user_input[1:]
                
                # Exit the command line
                if command == "exit":
                    running = False

                elif command in self.commandCompleterObject.commands.keys():
                    self.process_command(
                        command=command, 
                        arguments=arguments
                    )

                elif command.strip() == "":
                    pass

                # Fallback to unknown command
                else:
                    print("Unknown command. Type \"help\" for help.")

            except KeyboardInterrupt as e:
                print()

            except EOFError as e:
                print()
                running = False

            except Exception as e:
                if self.debug:
                    traceback.print_exc()
                print("[!] Error: %s" % str(e))

    def process_command(self, command, arguments=[]):
        # Skip
        if command.strip() == "":
            pass
        
        # Display help
        elif command == "help":
            self.command_help(arguments, command)

        # Closes the current SMB session
        elif command == "close":
            self.command_close(arguments, command)
               
        # Change directory in the current share
        elif command == "cd":
            self.command_cd(arguments, command)

        # Get a file
        elif command == "get":
            self.command_get(arguments, command)

        # SMB server info
        elif command == "info":
            self.command_info(arguments, command)

        # List directory contents in a share
        elif command in ["ls", "dir"]:
            self.command_ls(arguments, command)

        # Creates a new remote directory
        elif command == "mkdir":
            self.command_mkdir(arguments, command)

        # Put a file
        elif command == "put":
            self.command_put(arguments, command)

        # Changes the current local directory
        elif command == "lcd":
            self.command_lcd(arguments, command)

        # Lists the contents of the current local directory
        elif command == "lls":
            self.command_lls(arguments, command)

        # Creates a new local directory
        elif command == "lmkdir":
            self.command_lmkdir(arguments, command)

        # Removes a local file
        elif command == "lrm":
            self.command_lrm(arguments, command)

        # Removes a local directory
        elif command == "lrmdir":
            self.command_lrmdir(arguments, command)

        # Shows the current local directory
        elif command == "lpwd":
            self.command_lpwd(arguments, command)

        # 
        elif command == "module":
            self.command_module(arguments, command)

        # Reconnects the current SMB session
        elif command in ["connect", "reconnect"]:
            self.command_reconnect(arguments, command)

        # Reset the TTY output
        elif command == "reset":
            self.command_reset(arguments, command)

        # Removes a remote file
        elif command == "rm":
            self.command_rm(arguments, command)
            
        # Removes a remote directory
        elif command == "rmdir":
            self.command_rmdir(arguments, command)

        # List shares
        elif command == "shares":
            self.command_shares(arguments, command)
        
        # Displays a tree view of the CWD
        elif command == "tree":
            self.command_tree(arguments, command)
        
        # Use a share
        elif command == "use":
            self.command_use(arguments, command)

    # Commands ================================================================

    @command_arguments_required
    @active_smb_connection_needed
    @smb_share_is_set
    def command_cd(self, arguments, command):
        # Command arguments required   : Yes
        # Active SMB connection needed : Yes
        # SMB share needed             : Yes

        path = ' '.join(arguments)
        try:
            self.smbSession.set_cwd(path=path)
        except impacket.smbconnection.SessionError as e:
            print("[!] SMB Error: %s" % e)

    def command_close(self, arguments, command):
        # Command arguments required   : No
        # Active SMB connection needed : No
        # SMB share needed             : No

        self.smbSession.ping_smb_session()
        if self.smbSession.connected:
            self.smbSession.close_smb_session()

    @command_arguments_required
    @active_smb_connection_needed
    @smb_share_is_set
    def command_get(self, arguments, command):
        # Command arguments required   : Yes
        # Active SMB connection needed : Yes
        # SMB share needed             : Yes

        # Get files recursively
        if arguments[0] == "-r":
            path = ' '.join(arguments[1:]).replace('/', ntpath.sep)
            try:
                self.smbSession.get_file_recursively(path=path)
            except impacket.smbconnection.SessionError as e:
                print("[!] SMB Error: %s" % e)
        # Get a single file
        else:
            path = ' '.join(arguments).replace('/', ntpath.sep)
            try:
                self.smbSession.get_file(path=path)
            except impacket.smbconnection.SessionError as e:
                print("[!] SMB Error: %s" % e)

    def command_help(self, arguments, command):
        # Command arguments required   : No
        # Active SMB connection needed : No
        # SMB share needed             : No

        if len(arguments) != 0:
            self.commandCompleterObject.print_help(command=arguments[0])
        else:
            self.commandCompleterObject.print_help(command=None)

    @active_smb_connection_needed
    def command_info(self, arguments, command):
        # Command arguments required   : No
        # Active SMB connection needed : Yes
        # SMB share needed             : No

        print_server_info = False
        print_share_info = False
        if len(arguments) != 0:
            print_server_info = (arguments[0].lower() == "server")
            print_share_info = (arguments[0].lower() == "share")
        else:
            print_server_info = True
            print_share_info = True

        try:
            self.smbSession.info(
                share=print_share_info,
                server=print_server_info
            )
        except impacket.smbconnection.SessionError as e:
            print("[!] SMB Error: %s" % e)

    @command_arguments_required
    def command_lcd(self, arguments, command):
        # Command arguments required   : Yes
        # Active SMB connection needed : No
        # SMB share needed             : No

        path = ' '.join(arguments)
        if os.path.exists(path=path):
            if os.path.isdir(s=path):
                os.chdir(path=path)
            else:
                print("[!] Path '%s' is not a directory." % path)
        else:
            print("[!] Directory '%s' does not exists." % path)

    def command_lls(self, arguments, command):
        # Command arguments required   : No
        # Active SMB connection needed : No
        # SMB share needed             : No

        if len(arguments) == 0:
            directory_contents = os.listdir(path='.')
        else:
            directory_contents = os.listdir(path=' '.join(arguments))

        for entryname in sorted(directory_contents):
            rights_str = unix_permissions(entryname)
            size_str = b_filesize(os.path.getsize(filename=entryname))
            date_str = datetime.datetime.fromtimestamp(os.path.getmtime(filename=entryname)).strftime("%Y-%m-%d %H:%M")

            if os.path.isdir(s=entryname):
                print("%s %10s  %s  \x1b[1;96m%s\x1b[0m%s" % (rights_str, size_str, date_str, entryname, os.path.sep))
            else:
                print("%s %10s  %s  \x1b[1m%s\x1b[0m" % (rights_str, size_str, date_str, entryname))
    
    @command_arguments_required
    def command_lmkdir(self, arguments, command):
        # Command arguments required   : Yes
        # Active SMB connection needed : No
        # SMB share needed             : No

        path = ' '.join(arguments)

        # Split each dir
        if os.path.sep in path:
            path = path.strip(os.path.sep).split(os.path.sep)
        else:
            path = [path]

        # Create each dir in the path
        for depth in range(1, len(path)+1):
            tmp_path = os.path.sep.join(path[:depth])
            if not os.path.exists(tmp_path):
                os.mkdir(path=tmp_path)

    @command_arguments_required
    def command_lrm(self, arguments, command):
        # Command arguments required   : Yes
        # Active SMB connection needed : No
        # SMB share needed             : No

        path = ' '.join(arguments)
        if os.path.exists(path):
            if not os.path.isdir(s=path):
                try:
                    os.remove(path=path)
                except Exception as e:
                    print("[!] Error removing file '%s' : %s" % path)
            else:
                print("[!] Cannot delete '%s'. It is a directory, use 'lrmdir <directory>' instead." % path)
        else:
            print("[!] Path '%s' does not exist." % path)

    @command_arguments_required
    def command_lrmdir(self, arguments, command):
        # Command arguments required   : Yes
        # Active SMB connection needed : No
        # SMB share needed             : No

        path = ' '.join(arguments)
        if os.path.exists(path):
            if os.path.isdir(s=path):
                try:
                    shutil.rmtree(path=path)
                except Exception as e:
                    print("[!] Error removing directory '%s' : %s" % path)
            else:
                print("[!] Cannot delete '%s'. It is a file, use 'lrm <file>' instead." % path)
        else:
            print("[!] Path '%s' does not exist." % path)

    def command_lpwd(self, arguments, command):
        # Command arguments required   : No
        # Active SMB connection needed : No
        # SMB share needed             : No

        print(os.getcwd())

    @active_smb_connection_needed
    @smb_share_is_set
    def command_ls(self, arguments, command):
        # Command arguments required   : No
        # Active SMB connection needed : Yes
        # SMB share needed             : Yes

        # Read the files
        directory_contents = self.smbSession.list_contents(path=' '.join(arguments))

        for longname in sorted(directory_contents.keys(), key=lambda x:x.lower()):
            windows_ls_entry(directory_contents[longname])
            
    @command_arguments_required
    @active_smb_connection_needed
    @smb_share_is_set
    def command_mkdir(self, arguments, command):
        # Command arguments required   : Yes
        # Active SMB connection needed : Yes
        # SMB share needed             : Yes

        path = ' '.join(arguments)
        self.smbSession.mkdir(path=path)

    @command_arguments_required
    @active_smb_connection_needed
    @smb_share_is_set
    def command_module(self, arguments, command):
        module_name = arguments[0]

        if module_name in self.modules.keys():
            module = self.modules[module_name](self.smbSession)
            module.run(' '.join(arguments[1:]))
        else:
            print("[!] Module '%s' does not exist." % module_name)

    @command_arguments_required
    @active_smb_connection_needed
    @smb_share_is_set
    def command_put(self, arguments, command):
        # Command arguments required   : Yes
        # Active SMB connection needed : Yes
        # SMB share needed             : Yes

        # Put files recursively
        if arguments[0] == "-r":
            localpath = ' '.join(arguments[1:])
            try:
                self.smbSession.put_file_recursively(localpath=localpath)
            except impacket.smbconnection.SessionError as e:
                print("[!] SMB Error: %s" % e)

        # Put a single file
        else:
            localpath = ' '.join(arguments)
            try:
                self.smbSession.put_file(localpath=localpath)
            except impacket.smbconnection.SessionError as e:
                print("[!] SMB Error: %s" % e)

    def command_reconnect(self, arguments, command):
        # Command arguments required   : No
        # Active SMB connection needed : No
        # SMB share needed             : No

        self.smbSession.ping_smb_session()
        if self.smbSession.connected:
            self.smbSession.close_smb_session()
            self.smbSession.init_smb_session()
        else:
            self.smbSession.init_smb_session()

    def command_reset(self, arguments, command):
        # Command arguments required   : No
        # Active SMB connection needed : No
        # SMB share needed             : No
        sys.stdout.write('\x1b[?25h') # Sets the cursor to on
        sys.stdout.write('\x1b[v')  
        sys.stdout.write('\x1b[o') # Reset
        sys.stdout.flush()

    @command_arguments_required
    @active_smb_connection_needed
    @smb_share_is_set
    def command_rm(self, arguments, command):
        # Command arguments required   : Yes
        # Active SMB connection needed : Yes
        # SMB share needed             : Yes

        path = ' '.join(arguments)
        if self.smbSession.path_exists(path):
            if self.smbSession.path_isfile(path):
                try:
                    self.smbSession.rm(path=path)
                except Exception as e:
                    print("[!] Error removing file '%s' : %s" % path)
            else:
                print("[!] Cannot delete '%s': This is a directory, use 'rmdir <directory>' instead." % path)
        else:
            print("[!] Remote file '%s' does not exist." % path)

    @command_arguments_required
    @active_smb_connection_needed
    @smb_share_is_set
    def command_rmdir(self, arguments, command):
        # Command arguments required   : Yes
        # Active SMB connection needed : Yes
        # SMB share needed             : Yes

        path = ' '.join(arguments)
        if self.smbSession.path_exists(path):
            if self.smbSession.path_isdir(path):
                try:
                    self.smbSession.rmdir(path=path)
                except Exception as e:
                    print("[!] Error removing directory '%s' : %s" % path)
            else:
                print("[!] Cannot delete '%s': This is a file, use 'rm <file>' instead." % path)
        else:
            print("[!] Remote directory '%s' does not exist." % path)

    @active_smb_connection_needed
    def command_shares(self, arguments, command):
        # Command arguments required   : No
        # Active SMB connection needed : Yes
        # SMB share needed             : No

        shares = self.smbSession.list_shares()
        if len(shares.keys()) != 0:
            table = Table(title=None)
            table.add_column("Share")
            table.add_column("Hidden")
            table.add_column("Type")
            table.add_column("Description", justify="left")

            for sharename in sorted(shares.keys()):
                is_hidden = bool(sharename.endswith('$'))
                types = ', '.join([s.replace("STYPE_","") for s in shares[sharename]["type"]])
                if is_hidden:
                    table.add_row(sharename, str(is_hidden), types, shares[sharename]["comment"])
                else:
                    table.add_row(sharename, str(is_hidden), types, shares[sharename]["comment"])

            Console().print(table)
        else:
            print("[!] No share served on '%s'" % self.smbSession.address)

    @active_smb_connection_needed
    @smb_share_is_set
    def command_tree(self, arguments, command):
        # Command arguments required   : No
        # Active SMB connection needed : Yes
        # SMB share needed             : Yes

        if len(arguments) == 0:
            self.smbSession.tree(path='.')
        else:
            self.smbSession.tree(path=' '.join(arguments))

    @command_arguments_required
    @active_smb_connection_needed
    def command_use(self, arguments, command):
        # Command arguments required   : Yes
        # Active SMB connection needed : Yes
        # SMB share needed             : No

        sharename = ' '.join(arguments)
        # Reload the list of shares
        shares = self.smbSession.list_shares()
        shares = [s.lower() for s in shares.keys()]
        if sharename.lower() in shares:
            self.smbSession.set_share(sharename)
        else:
            print("[!] No share named '%s' on '%s'" % (sharename, self.smbSession.address))

    # Private functions =======================================================

    def __load_modules(self):
        self.modules.clear()

        modules_dir = os.path.normpath(os.path.dirname(__file__) + os.path.sep + ".." + os.path.sep + "modules")
        if self.debug:
            print("[debug] Loading modules from %s ..." % modules_dir)
        sys.path.extend([modules_dir])

        for file in os.listdir(modules_dir):
            filepath = os.path.normpath(modules_dir + os.path.sep + file)
            if file.endswith('.py'):
                if os.path.isfile(filepath) and file not in ["__init__.py"]:
                    try:
                        module_file = import_module('smbclientng.modules.%s' % (file[:-3]))
                        module = module_file.__getattribute__(file[:-3])
                        self.modules[module.name.lower()] = module
                    except AttributeError as e:
                        pass

        if self.debug:
            print("[debug] modules:", self.modules)
        
        if self.commandCompleterObject is not None:
            self.commandCompleterObject.commands["module"]["subcommands"] = list(self.modules.keys())

    def __prompt(self):
        self.smbSession.ping_smb_session()
        if self.smbSession.connected:
            connected_dot = "\x1b[1;92m⏺ \x1b[0m"
        else:
            connected_dot = "\x1b[1;91m⏺ \x1b[0m"
        if self.smbSession.smb_share is None:
            str_prompt = "%s[\x1b[1;94m\\\\%s\\\x1b[0m]> " % (connected_dot, self.smbSession.address)
        else:
            str_path = "\\\\%s\\%s\\%s" % (self.smbSession.address, self.smbSession.smb_share, self.smbSession.smb_cwd.lstrip(ntpath.sep))
            str_prompt = "%s[\x1b[1;94m%s\x1b[0m]> " % (connected_dot, str_path)
        return str_prompt
