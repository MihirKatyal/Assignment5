import pathlib
import tkinter as tk
from tkinter import ttk, filedialog
from Profile import Profile, Post
import ds_client
from ds_messenger import DirectMessenger


class Body(tk.Frame):
    def __init__(self, root, recipient_selected_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = [str]
        self._select_callback = recipient_selected_callback
        self._draw()

    def node_select(self, event):
        if len(self.posts_tree.selection()) == 0:
            return None
        index = int(self.posts_tree.selection()[0])
        entry = self._contacts[index]
        if self._select_callback is not None:
            self._select_callback(entry)

    def insert_contact(self, contact: str):
        self._contacts.append(contact)
        index = len(self._contacts) - 1
        self._insert_contact_tree(index, contact)

    def _insert_contact_tree(self, idx, contact: str):
        if idx % 2 == 1:
            idx = self.posts_tree.insert('', idx, idx,
                                         text=contact, tags='oddrow')
        else:
            idx = self.posts_tree.insert('', idx, idx,
                                         text=contact, tags='evenrow')

    def insert_user_message(self, message: str):
        self.entry_editor.configure(state='normal')
        self.entry_editor.insert(tk.END, message + '\n', 'entry-right')
        self.entry_editor.configure(state='disabled')

    def insert_contact_message(self, message: str):
        self.entry_editor.configure(state='normal')
        self.entry_editor.insert(tk.END, message + '\n', 'entry-left')
        self.entry_editor.configure(state='disabled')

    def get_text_entry(self) -> str:
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text: str):
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)

    def clear_contacts(self):
        self._contacts = [str]
        for contact in self.posts_tree.get_children():
            self.posts_tree.delete(contact)

    def get_contacts(self):
        return self._contacts

    def _draw(self):
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.tag_configure('oddrow', background='cyan')
        self.posts_tree.tag_configure('evenrow', background='magenta')
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP,
                             expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        message_frame = tk.Frame(master=self, bg="yellow")
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)

        self.message_editor = tk.Text(message_frame, width=0, height=5)
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                                 expand=True, padx=0, pady=0)

        self.entry_editor = tk.Text(editor_frame, width=0, height=5)
        self.entry_editor.tag_configure('entry-right', justify='right')
        self.entry_editor.tag_configure('entry-left', justify='left')
        self.entry_editor.configure(state='disabled')
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                               expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame,
                                              command=lambda:
                                              self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT,
                                    expand=False, padx=0, pady=0)


class Footer(tk.Frame):
    def __init__(self, root, send_callback=None, publish_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._publish_callback = publish_callback
        self._draw()

    def send_click(self):
        if self._send_callback is not None:
            self._send_callback()

    def pub_click(self):
        if self._publish_callback is not None:
            self._publish_callback()

    def _draw(self):
        save_button = tk.Button(master=self, text="Send", width=20,
                                command=lambda: self.send_click())
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        pub_button = tk.Button(master=self, text="Publish", width=20,
                               command=lambda: self.pub_click())
        pub_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


class NewContactDialog(tk.simpledialog.Dialog):
    def __init__(self, root, title=None, user=None, pwd=None, server=None):
        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        self.applied = False
        super().__init__(root, title)

    def body(self, frame):
        self.server_label = tk.Label(frame, width=30, text="DS Server Address")
        self.server_label.pack()
        self.server_entry = tk.Entry(frame, width=30)
        self.server_entry.pack()

        self.username_label = tk.Label(frame, width=30, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.pack()

        self.password_label = tk.Label(frame, width=30, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(frame, width=30)
        self.password_entry['show'] = '*'
        self.password_entry.pack()

    def apply(self):
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.server = self.server_entry.get()


class MainApp(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.username = None
        self.password = None
        self.server = None
        self.recipient = None
        self.online = False
        self.usedopen = False
        self.profile = None
        self.direct_messenger = None
        self.notonline_label = None
        self.userlabel = None
        self.path = None
        self.api = False
        self.openweather = None
        self.lastfm = None
        self.typ = None
        self.popup = None
        self.messagedict = {}
        self._draw()
        self.configure_server()

    def send_message(self):
        if self.online:
            message = self.body.get_text_entry()
            if len(message) == 0 or self.recipient is None:
                return None
            if self.api:
                message = self.openweather.transclude(message)
                message = self.lastfm.transclude(message)
            sent = self.direct_messenger.send(message, self.recipient)
            if sent:
                typ = "send:"
                self._savemessage(message, typ, self.recipient)
                self.profile.save_profile(self.path)
                self.body.insert_user_message(message)
            else:
                self.popup = tk.Toplevel(self.root)
                self.popup.geometry("300x150")
                self.popup.title("ERROR")
                tk.Label(self.popup,
                         text="Error, faulty message").place(x=100, y=50)
            self.body.message_editor.delete(1.0, tk.END)
        else:
            self.popup = tk.Toplevel(self.root)
            self.popup.geometry("300x150")
            self.popup.title("ERROR")
            tk.Label(self.popup, text="You are not shown as online").place(x=100, y=50)

    def add_contact(self):
        newcontact = tk.simpledialog.askstring(title="",
                                               prompt="Please add a Contact")
        if newcontact is None:
            return None
        newcontact = newcontact.strip()
        if newcontact == self.username:
            newcontact = ""
        if len(newcontact) != 0 and newcontact not in self.body._contacts:
            self.body.insert_contact(newcontact)
            self.messagedict[newcontact] = []
            if self.profile is not None and self.path is not None:
                self.profile.save_profile(self.path)
        else:
            self.popup = tk.Toplevel(self.root)
            self.popup.geometry("300x150")
            self.popup.title("ERROR")
            tk.Label(self.popup,
                     text="Error when adding contact!").place(x=90, y=50)

    def recipient_selected(self, recipient):
        self.body.entry_editor.configure(state="normal")
        self.body.entry_editor.delete(1.0, tk.END)
        self.body.entry_editor.configure(state="disabled")
        self.recipient = recipient
        self._loadmessages()

    def configure_server(self):
        if not self.usedopen:
            ud = NewContactDialog(self.root, "Configure Account",
                                  self.username, self.password, self.server)
            self.username = ud.user
            self.password = ud.pwd
            self.server = ud.server
        self.body.clear_contacts()
        try:
            self.body.entry_editor.delete(1.0, tk.END)
            self.direct_messenger = DirectMessenger(self.server,
                                                    self.username,
                                                    self.password)
            self.online = self.direct_messenger.connected
        except:
            self.online = False
        if not self.online:
            if self.notonline_label is None:
                self.notonline_label = tk.Label(self.root, width=200,
                                                text="not online",
                                                background="black",
                                                foreground="white")
                self.notonline_label.pack()
            if self.username and self.password:
                self._loadprofile()
            else:
                self.popup = tk.Toplevel(self.root)
                self.popup.geometry("300x150")
                self.popup.title("ERROR")
                tk.Label(self.popup,
                         text="WARNING: No profile has been loaded").place(x=75, y=40)
                tk.Label(self.popup,
                         text=("Click on Settings > Configure "
                               "DS Server to get profile")).place(x=10, y=65)
        else:
            # Destroys label if exists
            if self.notonline_label is not None:
                self.notonline_label.destroy()
                self.notonline_label = None
            self._loadprofile()
        self.usedopen = False

    def _loadprofile(self):
        # Checks if dsu exists in cwd
        cwd = pathlib.Path.cwd()
        filelist = []
        dsu_files = []
        extensions = [".dsu"]
        files = cwd.iterdir()
        for file in files:
            if file.is_file():
                filelist.append(file.name)
        for idx, ext in enumerate(extensions):
            if ext == ".dsu":
                dsu_files.append(filelist[idx])
        # Loads json and checks if self.username == fileusername
        foundprof = False
        obj = Profile()
        for dsu in dsu_files:
            temppath = cwd / dsu
            obj.load_profile(temppath)
            if obj.username == self.username and obj.password == self.password:
                if self.server is not None:
                    obj.dsuserver = self.server
                obj.save_profile(temppath)
                self.profile = obj
                self.path = temppath
                self.messagedict = self.profile.get_messages()
                friends = self.messagedict.keys()
                for friend in friends:
                    if friend not in self.body._contacts:
                        self.body.insert_contact(friend)
                foundprof = True
                break
        # Creates profile if not found
        if not foundprof:
            dsuname = tk.simpledialog.askstring(title="",
                                                prompt="Please enter a profile name:")
            if dsuname is None:
                self.popup = tk.Toplevel(self.root)
                self.popup.geometry("300x150")
                self.popup.title("ERROR")
                tk.Label(self.popup,
                         text="A profile has not created").place(x=100, y=50)
                return None
            dsuname += ".dsu"
            temppath = cwd / dsuname
            temppath.touch()
            obj.username = self.username
            obj.password = self.password
            obj.dsuserver = self.server
            obj.save_profile(temppath)
            self.profile = obj
            self.path = temppath

    def _loadmessages(self):
        if self.recipient in self.messagedict.keys():
            self.body.entry_editor.configure(state="normal")
            self.body.entry_editor.delete(1.0, tk.END)
            self.body.entry_editor.configure(state="disabled")
            messages = self.messagedict[self.recipient]
            for message in messages:
                typ = message[0:5]
                if typ == "recv:":
                    self.body.insert_contact_message(message[6:])
                else:
                    self.body.insert_user_message(message[6:])

    def _biocallback(self):
        self.typ = "bio"
        self.popup.destroy()

    def _postcallback(self):
        self.typ = "post"
        self.popup.destroy()

    def publish(self):
        if self.online:
            message = self.body.get_text_entry()
            if len(message) == 0:
                return None

            self.popup = tk.Toplevel(self.root)
            self.popup.geometry("300x150")
            self.popup.title("CHOOSE TYPE")

            biobutton = tk.Button(master=self.popup,
                                  text="update bio", width=20,
                                  command=lambda: self._biocallback())
            biobutton.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

            postbutton = tk.Button(master=self.popup, text="make post",
                                   width=20, command=lambda:
                                   self._postcallback())
            postbutton.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)
            self.root.wait_window(self.popup)

            if self.typ is None:
                return None

            if self.api:
                message = self.openweather.transclude(message)
                message = self.lastfm.transclude(message)

            if self.typ == "bio":
                sent = ds_client.send(self.server, 3021, self.profile.username,
                                      self.profile.password, bio=message)
            else:
                sent = ds_client.send(self.server, 3021, self.profile.username,
                                      self.profile.password, message)

            if sent:
                if self.typ == "bio":
                    self.profile.bio = message
                else:
                    post = Post()
                    post.set_entry(message)
                    self.profile.add_post(post)
                self.profile.save_profile(self.path)
            else:
                self.popup = tk.Toplevel(self.root)
                self.popup.geometry("300x150")
                self.popup.title("ERROR")
                tk.Label(self.popup,
                         text="Error, faulty message").place(x=100, y=50)
            self.typ = None
            self.body.message_editor.delete(1.0, tk.END)
        else:
            self.popup = tk.Toplevel(self.root)
            self.popup.geometry("300x150")
            self.popup.title("ERROR")
            tk.Label(self.popup,
                     text="You are not shown as online").place(x=100, y=50)

    def check_new(self):
        if self.online:
            lst_new = self.direct_messenger.retrieve_new()
            for obj in lst_new:
                message = obj.message
                sender = obj.recipient
                contacts = self.body.get_contacts()
                if sender not in contacts:
                    self.body.insert_contact(sender)
                if self.profile is not None:
                    typ = "recv:"
                    self._savemessage(message, typ, sender)
            if self.profile is not None:
                self.profile.save_message(self.messagedict)
                self.profile.save_profile(self.path)
            self._loadmessages()
        self.root.after(5000, lambda: self.check_new())

    def _savemessage(self, message, typ, username):
        if username not in self.messagedict.keys():
            self.messagedict[username] = []
        self.messagedict[username].append(f"{typ} {message}")

    def _opendsu(self):
        file_path = filedialog.askopenfilename(title="Select a File",
                                               filetypes=[("Text files",
                                                           "*.dsu"),
                                                          ("All files",
                                                           "*.*")])
        if file_path:
            if file_path == self.path:
                return None
            if self.profile is not None:
                self._close()
            self.usedopen = True
            self.path = file_path
            self.profile = Profile()
            self.profile.load_profile(self.path)
            self.username = self.profile.username
            self.password = self.profile.password
            self.server = self.profile.dsuserver
            self.configure_server()
            if self.userlabel is not None:
                self.userlabel.destroy()
            self.userlabel = tk.Label(self.root,
                                      text=(f"Username: {self.username} "
                                            f"| Server: {self.server}"))
            self.userlabel.pack()

    def _close(self):
        if self.path is not None:
            if self.notonline_label is None:
                self.notonline_label = tk.Label(self.root, width=200,
                                                text="not online",
                                                background="black",
                                                foreground="white")
                self.notonline_label.pack()
            if self.userlabel is not None:
                self.userlabel.destroy()
                self.userlabel = None
            self.username = None
            self.password = None
            self.server = None
            self.recipient = None
            self.online = False
            self.profile = None
            self.direct_messenger = None
            self.path = None
            self.messagedict = {}
            self.body.clear_contacts()
            self.body.entry_editor.configure(state="normal")
            self.body.entry_editor.delete(1.0, tk.END)
            self.body.entry_editor.configure(state="disabled")

    def _change_server(self):
        if self.profile is not None:
            dsuserver = tk.simpledialog.askstring(title="",
                                                  prompt="Enter a dsuserver:")
            if dsuserver is not None:
                self.server = dsuserver
                self.profile.dsuserver = dsuserver
                self.profile.save_profile(self.path)
                self.usedopen = True
                self.configure_server()

    def check_changes(self):
        if self.profile is not None and self.path is not None:
            p = pathlib.Path(self.path)
            if not p.exists():
                self._close()
                return None
            check_prof = Profile()
            check_prof.load_profile(self.path)
            if self.username != check_prof.username:
                self._close()
                return None
            if self.password != check_prof.password:
                self._close()
                return None
        self.root.after(3000, lambda: self.check_changes())

    def _draw(self):
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)

        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New', command=lambda: self.configure_server())
        menu_file.add_command(label='Open...', command=lambda: self._opendsu())
        menu_file.add_command(label='Close', command=lambda: self._close())

        settings_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=settings_file, label='Settings')
        settings_file.add_command(label='Add Contact',
                                  command=self.add_contact)
        settings_file.add_command(label='Configure DS Server',
                                  command=lambda: self._change_server())

        self.body = Body(self.root,
                         recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message,
                             publish_callback=self.publish)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)

        style = ttk.Style(self.root)
        style.theme_use("classic")
        style.configure("Treeview", background="blue",
                        fieldbackground="green", foreground="white")
        self.body.set_text_entry("To begin, add a contact by "
                                 "clicking settings, "
                                 "or create\nand open a "
                                 "profile by clicking file.")


if __name__ == "__main__":
    main = tk.Tk()

    main.title("ICS 32 Distributed Social Messenger")

    main.geometry("720x480")

    main.option_add('*tearOff', False)

    app = MainApp(main)
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    idx = main.after(5000, app.check_new)
    print(idx)

    main.mainloop()
