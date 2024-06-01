#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import argparse
import os
import sys

try:
    import tkinter as tk
    import tkinter.filedialog as filedialog

    TKINTER = True
except ImportError:
    TKINTER = False

import json
import shlex

from chgksuite.common import (
    DefaultNamespace,
    ensure_utf8,
    get_lastdir,
    get_source_dirs,
)
from chgksuite.version import __version__
from chgksuite.cli import ArgparseBuilder, single_action


class VarWrapper(object):
    def __init__(self, name, var):
        self.name = name
        self.var = var


class OpenFileDialog(object):
    def __init__(self, label, var, folder=False, lastdir=None, filetypes=None):
        self.label = label
        self.var = var
        self.folder = folder
        self.lastdir = lastdir
        self.filetypes = filetypes

    def __call__(self):
        function = (
            filedialog.askdirectory if self.folder else filedialog.askopenfilename
        )
        kwargs = {}
        if self.lastdir:
            kwargs["initialdir"] = self.lastdir
        if self.filetypes:
            kwargs["filetypes"] = self.filetypes
        output = function(**kwargs)
        if isinstance(output, bytes):
            output = output.decode("utf8")
        self.var.set(output or "")
        self.label.config(text=(output or "").split(ensure_utf8(os.sep))[-1])


class ParserWrapper(object):
    def __init__(self, parser, parent=None, lastdir=None):
        self.parent = parent
        if self.parent and not lastdir:
            self.lastdir = self.parent.lastdir
        else:
            self.lastdir = lastdir
        if self.parent:
            self.parent.children.append(self)
            self.frame = tk.Frame(self.parent.frame)
            self.frame.pack()
            self.frame.pack_forget()
            self.advanced_frame = tk.Frame(self.parent.advanced_frame)
            self.advanced_frame.pack()
            self.advanced_frame.pack_forget()
        else:
            self.init_tk()
        self.parser = parser
        self.subparsers_var = None
        self.cmdline_call = None
        self.children = []
        self.vars = []

    def _list_vars(self):
        result = []
        for var in self.vars:
            result.append((var.name, var.var.get()))
        if self.subparsers_var:
            chosen_parser_name = self.subparsers_var.get()
            chosen_parser = [
                x
                for x in self.subparsers.parsers
                if x.parser.prog.split()[-1] == chosen_parser_name
            ][0]
            result.append(("", chosen_parser_name))
            result.extend(chosen_parser._list_vars())
        return result

    def build_command_line_call(self):
        result = []
        result_to_print = []
        for tup in self._list_vars():
            to_append = None
            if tup[0].startswith("--"):
                if tup[1] == "true":
                    to_append = tup[0]
                elif not tup[1] or tup[1] == "false":
                    continue
                else:
                    to_append = [tup[0], tup[1]]
            else:
                to_append = tup[1]
            if isinstance(to_append, list):
                result.extend(to_append)
                if "password" in tup[0]:
                    result_to_print.append(tup[0])
                    result_to_print.append("********")
                else:
                    result_to_print.extend(to_append)
            else:
                result.append(to_append)
                result_to_print.append(to_append)
        print("Command line call: {}".format(shlex.join(result_to_print)))
        return result

    def ok_button_press(self):
        self.cmdline_call = self.build_command_line_call()
        self.tk.quit()
        self.tk.destroy()

    def toggle_advanced_frame(self):
        value = self.advanced_checkbox_var.get()
        if value == "true":
            self.advanced_frame.pack()
        else:
            self.advanced_frame.pack_forget()

    def init_tk(self):
        self.tk = tk.Tk()
        self.tk.title("chgksuite v{}".format(__version__))
        self.tk.minsize(600, 300)
        self.tk.eval("tk::PlaceWindow . center")
        self.mainframe = tk.Frame(self.tk)
        self.mainframe.pack(side="top")
        self.frame = tk.Frame(self.mainframe)
        self.frame.pack(side="top")
        self.button_frame = tk.Frame(self.mainframe)
        self.button_frame.pack(side="top")
        self.ok_button = tk.Button(
            self.button_frame,
            text="Запустить",
            command=self.ok_button_press,
            width=15,
            height=2,
        )
        self.ok_button.pack(side="top")
        self.advanced_checkbox_var = tk.StringVar()
        self.toggle_advanced_checkbox = tk.Checkbutton(
            self.button_frame,
            text="Показать дополнительные настройки",
            onvalue="true",
            offvalue="false",
            variable=self.advanced_checkbox_var,
            command=self.toggle_advanced_frame,
        )
        self.toggle_advanced_checkbox.pack(side="top")
        self.advanced_frame = tk.Frame(self.mainframe)
        self.advanced_frame.pack(side="top")
        self.advanced_frame.pack_forget()

    def add_argument(self, *args, **kwargs):
        if kwargs.pop("advanced", False):
            frame = self.advanced_frame
        else:
            frame = self.frame
        if kwargs.pop("hide", False):
            self.parser.add_argument(*args, **kwargs)
            return
        caption = kwargs.pop("caption", None) or args[0]
        argtype = kwargs.pop("argtype", None)
        filetypes = kwargs.pop("filetypes", None)
        if not argtype:
            if kwargs.get("action") == "store_true":
                argtype = "checkbutton"
            elif args[0] in {"filename", "folder"}:
                argtype = args[0]
            else:
                argtype = "entry"
        if argtype == "checkbutton":
            var = tk.StringVar()
            var.set("false")
            innerframe = tk.Frame(frame)
            innerframe.pack(side="top")
            checkbutton = tk.Checkbutton(
                innerframe, text=caption, variable=var, onvalue="true", offvalue="false"
            )
            checkbutton.pack(side="left")
            self.vars.append(VarWrapper(name=args[0], var=var))
        elif argtype == "radiobutton":
            var = tk.StringVar()
            var.set(kwargs["default"])
            innerframe = tk.Frame(frame)
            innerframe.pack(side="top")
            label = tk.Label(innerframe, text=caption)
            label.pack(side="left")
            for ch in kwargs["choices"]:
                radio = tk.Radiobutton(
                    innerframe,
                    text=ch,
                    variable=var,
                    value=ch,
                )
                radio.pack(side="left")
            self.vars.append(VarWrapper(name=args[0], var=var))
        elif argtype in {"filename", "folder"}:
            text = "(имя файла)" if argtype == "filename" else "(имя папки)"
            button_text = "Открыть файл" if argtype == "filename" else "Открыть папку"
            var = tk.StringVar()
            innerframe = tk.Frame(frame)
            innerframe.pack(side="top")
            label = tk.Label(innerframe, text=caption)
            label.pack(side="left")
            label = tk.Label(innerframe, text=text)
            ofd_kwargs = dict(folder=argtype == "folder", lastdir=self.lastdir)
            if filetypes:
                ofd_kwargs["filetypes"] = filetypes
            button = tk.Button(
                innerframe,
                text=button_text,
                command=OpenFileDialog(label, var, **ofd_kwargs),
            )
            button.pack(side="left")
            label.pack(side="left")
            self.vars.append(VarWrapper(name=args[0], var=var))
        elif argtype == "entry":
            var = tk.StringVar()
            var.set(kwargs.get("default") or "")
            innerframe = tk.Frame(frame)
            innerframe.pack(side="top")
            tk.Label(innerframe, text=caption).pack(side="left")
            entry_show = "*" if "password" in args[0] else ""
            entry = tk.Entry(innerframe, textvariable=var, show=entry_show)
            entry.pack(side="left")
            self.vars.append(VarWrapper(name=args[0], var=var))
        self.parser.add_argument(*args, **kwargs)

    def add_subparsers(self, *args, **kwargs):
        subparsers = self.parser.add_subparsers(*args, **kwargs)
        self.subparsers_var = tk.StringVar()
        self.subparsers = SubparsersWrapper(subparsers, parent=self)
        return self.subparsers

    def show_frame(self):
        for child in self.parent.children:
            child.frame.pack_forget()
            child.advanced_frame.pack_forget()
        self.frame.pack(side="top")
        self.advanced_frame.pack(side="top")

    def parse_args(self, *args, **kwargs):
        argv = sys.argv[1:]
        if not argv:
            self.tk.mainloop()
            if self.cmdline_call:
                return self.parser.parse_args(self.cmdline_call)
            else:
                sys.exit(0)
        return self.parser.parse_args(*args, **kwargs)


class SubparsersWrapper(object):
    def __init__(self, subparsers, parent):
        self.subparsers = subparsers
        self.parent = parent
        self.frame = tk.Frame(self.parent.frame)
        self.frame.pack(side="top")
        self.parsers = []

    def add_parser(self, *args, **kwargs):
        caption = kwargs.pop("caption", None) or args[0]
        parser = self.subparsers.add_parser(*args, **kwargs)
        pw = ParserWrapper(parser=parser, parent=self.parent)
        self.parsers.append(pw)
        radio = tk.Radiobutton(
            self.frame,
            text=caption,
            variable=self.parent.subparsers_var,
            value=args[0],
            command=pw.show_frame,
        )
        radio.pack(side="left")
        return pw


def app():
    _, resourcedir = get_source_dirs()
    ld = get_lastdir()
    use_wrapper = len(sys.argv) == 1 and TKINTER
    if use_wrapper:
        while True:
            parser = argparse.ArgumentParser(prog="chgksuite")
            parser = ParserWrapper(parser, lastdir=ld)
            ArgparseBuilder(parser, use_wrapper).build()
            args = DefaultNamespace(parser.parse_args())
            single_action(args, False, resourcedir)
    else:
        parser = argparse.ArgumentParser(prog="chgksuite")
        ArgparseBuilder(parser, use_wrapper).build()
        args = DefaultNamespace(parser.parse_args())
        single_action(args, False, resourcedir)
