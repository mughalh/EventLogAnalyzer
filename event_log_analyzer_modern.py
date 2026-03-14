import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import tkinter.font as tkFont
import xml.etree.ElementTree as ET
import re
from datetime import datetime
import threading
import os
import json

class ModernEventLogAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Windows Event Log Analyzer")
        self.root.geometry("1400x900")
        
        # Set modern theme and colors
        self.setup_styles()
        
        # Variables
        self.current_files = []
        self.events = []
        self.filtered_events = []
        self.bookmarks = []
        self.dark_mode = False
        
        # Setup UI
        self.setup_ui()
        self.setup_drag_drop()
        
    def setup_styles(self):
        """Configure modern styles and colors"""
        self.colors = {
            'bg': '#f5f5f5',
            'fg': '#333333',
            'accent': '#007acc',
            'accent_light': '#e1f0fa',
            'success': '#28a745',
            'warning': '#ffc107',
            'danger': '#dc3545',
            'card_bg': '#ffffff',
            'border': '#dee2e6',
            'critical': '#ffcccc',
            'error': '#fff3cd',
            'warning_bg': '#fff3cd',
            'info_bg': '#d1ecf1'
        }
        
        # Configure ttk styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors for different elements
        style.configure('Accent.TButton', 
                       background=self.colors['accent'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Segoe UI', 10))
        style.map('Accent.TButton',
                 background=[('active', '#005a9e')])
        
        style.configure('Card.TFrame',
                       background=self.colors['card_bg'],
                       relief='solid',
                       borderwidth=1)
        
        style.configure('Treeview',
                       background='white',
                       foreground=self.colors['fg'],
                       rowheight=25,
                       fieldbackground='white',
                       font=('Segoe UI', 10))
        style.map('Treeview',
                 background=[('selected', self.colors['accent_light'])],
                 foreground=[('selected', self.colors['fg'])])
        
        style.configure('Heading.TLabel',
                       font=('Segoe UI', 11, 'bold'),
                       foreground=self.colors['fg'])
        
        style.configure('Stats.TLabel',
                       font=('Segoe UI', 10),
                       background=self.colors['card_bg'])
        
    def setup_ui(self):
        """Create the modern UI"""
        # Configure root window
        self.root.configure(bg=self.colors['bg'])
        
        # Create menu bar
        self.create_menu()
        
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top toolbar
        self.create_toolbar(main_container)
        
        # Main content area with two columns
        content_frame = ttk.Frame(main_container)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Left panel - File info and controls
        left_panel = ttk.Frame(content_frame, width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Right panel - Event viewer
        right_panel = ttk.Frame(content_frame)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Build left panel sections
        self.create_file_section(left_panel)
        self.create_quick_analysis_section(left_panel)
        self.create_filter_section(left_panel)
        self.create_stats_section(left_panel)
        
        # Build right panel sections
        self.create_event_viewer(right_panel)
        self.create_details_view(right_panel)
        
        # Status bar
        self.create_status_bar()
        
    def create_menu(self):
        """Create modern menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open File(s)", command=self.open_files, accelerator="Ctrl+O")
        file_menu.add_command(label="Open Folder", command=self.open_folder)
        file_menu.add_separator()
        file_menu.add_command(label="Export Results", command=self.export_results, accelerator="Ctrl+E")
        file_menu.add_command(label="Export as JSON", command=self.export_json)
        file_menu.add_separator()
        file_menu.add_command(label="Clear All", command=self.clear_all)
        file_menu.add_command(label="Exit", command=self.root.quit, accelerator="Alt+F4")
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Toggle Dark Mode", command=self.toggle_dark_mode, accelerator="Ctrl+D")
        view_menu.add_separator()
        view_menu.add_command(label="Show Only Critical", command=lambda: self.quick_filter_level('Critical'))
        view_menu.add_command(label="Show Only Errors", command=lambda: self.quick_filter_level('Error'))
        view_menu.add_command(label="Show Only Warnings", command=lambda: self.quick_filter_level('Warning'))
        view_menu.add_separator()
        view_menu.add_command(label="Expand All Details", command=self.expand_all_details)
        view_menu.add_command(label="Collapse All Details", command=self.collapse_all_details)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Find in Events", command=self.show_search_dialog, accelerator="Ctrl+F")
        tools_menu.add_command(label="Bookmark Current Event", command=self.bookmark_event, accelerator="Ctrl+B")
        tools_menu.add_command(label="Show Bookmarks", command=self.show_bookmarks)
        tools_menu.add_separator()
        tools_menu.add_command(label="Generate Report", command=self.generate_report)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Documentation", command=self.show_documentation)
        help_menu.add_command(label="About", command=self.show_about)
        
        # Bind keyboard shortcuts
        self.root.bind('<Control-o>', lambda e: self.open_files())
        self.root.bind('<Control-e>', lambda e: self.export_results())
        self.root.bind('<Control-f>', lambda e: self.show_search_dialog())
        self.root.bind('<Control-b>', lambda e: self.bookmark_event())
        self.root.bind('<Control-d>', lambda e: self.toggle_dark_mode())
        
    def create_toolbar(self, parent):
        """Create modern toolbar with icons (using text for simplicity)"""
        toolbar = ttk.Frame(parent, style='Card.TFrame')
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        # Toolbar buttons with icons (using emoji as simple icons)
        buttons = [
            ('📂', 'Open Files', self.open_files),
            ('📁', 'Open Folder', self.open_folder),
            ('💾', 'Export', self.export_results),
            ('🔍', 'Search', self.show_search_dialog),
            ('⭐', 'Bookmark', self.bookmark_event),
            ('📊', 'Report', self.generate_report),
            ('🔄', 'Refresh', self.refresh_view),
            ('🗑️', 'Clear', self.clear_all)
        ]
        
        for i, (icon, text, command) in enumerate(buttons):
            btn = tk.Button(toolbar, text=f"{icon} {text}", 
                          bg=self.colors['accent'] if i == 0 else self.colors['card_bg'],
                          fg='white' if i == 0 else self.colors['fg'],
                          font=('Segoe UI', 10),
                          borderwidth=0,
                          padx=10,
                          pady=5,
                          cursor='hand2',
                          command=command)
            btn.pack(side=tk.LEFT, padx=2)
            
            # Hover effects
            btn.bind('<Enter>', lambda e, b=btn: b.configure(bg=self.colors['accent_light'] 
                    if b.cget('bg') != self.colors['accent'] else '#005a9e'))
            btn.bind('<Leave>', lambda e, b=btn: b.configure(bg=self.colors['accent'] 
                    if b.cget('text').startswith('📂') else self.colors['card_bg']))
        
        # File info label on the right
        self.toolbar_file_label = tk.Label(toolbar, text="No files loaded", 
                                          bg=self.colors['card_bg'],
                                          fg=self.colors['fg'],
                                          font=('Segoe UI', 10))
        self.toolbar_file_label.pack(side=tk.RIGHT, padx=10)
        
    def create_file_section(self, parent):
        """Create file information section"""
        section = ttk.LabelFrame(parent, text="📁 Files", padding=10)
        section.pack(fill=tk.X, pady=(0, 10))
        
        # Drag and drop area
        self.drop_area = tk.Frame(section, bg=self.colors['accent_light'], 
                                  height=80, relief='solid', bd=2)
        self.drop_area.pack(fill=tk.X, pady=(0, 10))
        self.drop_area.pack_propagate(False)
        
        drop_label = tk.Label(self.drop_area, 
                             text="⬇️ Drop .evtx files here\nor click to browse",
                             bg=self.colors['accent_light'],
                             fg=self.colors['fg'],
                             font=('Segoe UI', 10))
        drop_label.pack(expand=True)
        
        # Make drop area clickable
        self.drop_area.bind('<Button-1>', lambda e: self.open_files())
        drop_label.bind('<Button-1>', lambda e: self.open_files())
        
        # File list with scrollbar
        list_frame = ttk.Frame(section)
        list_frame.pack(fill=tk.X)
        
        self.file_listbox = tk.Listbox(list_frame, height=4,
                                       bg='white',
                                       fg=self.colors['fg'],
                                       selectbackground=self.colors['accent_light'],
                                       selectforeground=self.colors['fg'],
                                       font=('Segoe UI', 9))
        self.file_listbox.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, 
                                  command=self.file_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_listbox.config(yscrollcommand=scrollbar.set)
        
        # Bind double-click to remove file
        self.file_listbox.bind('<Double-Button-1>', self.remove_file)
        
    def create_quick_analysis_section(self, parent):
        """Create quick analysis buttons section"""
        section = ttk.LabelFrame(parent, text="⚡ Quick Analysis", padding=10)
        section.pack(fill=tk.X, pady=(0, 10))
        
        # Create grid of buttons
        buttons = [
            ('💥 Crashes', '1001', self.colors['danger']),
            ('🔌 Shutdowns', '41', self.colors['warning']),
            ('❌ Critical', 'critical', self.colors['danger']),
            ('⚠️ Errors', 'error', self.colors['warning']),
            ('💾 Disk', 'disk', self.colors['accent']),
            ('📊 Last 50', 'last50', self.colors['success'])
        ]
        
        row = 0
        col = 0
        for text, value, color in buttons:
            btn = tk.Button(section, text=text,
                          bg=color,
                          fg='white',
                          font=('Segoe UI', 10),
                          borderwidth=0,
                          padx=10,
                          pady=8,
                          cursor='hand2',
                          command=lambda v=value: self.quick_analysis_action(v))
            btn.grid(row=row, column=col, padx=2, pady=2, sticky='ew')
            
            # Configure grid weights
            section.grid_columnconfigure(col, weight=1)
            
            col += 1
            if col > 1:
                col = 0
                row += 1
        
        # Progress bar
        self.progress = ttk.Progressbar(section, mode='indeterminate')
        self.progress.grid(row=row+1, column=0, columnspan=2, sticky='ew', pady=(10, 0))
        
    def create_filter_section(self, parent):
        """Create advanced filter section"""
        section = ttk.LabelFrame(parent, text="🔍 Advanced Filters", padding=10)
        section.pack(fill=tk.X, pady=(0, 10))
        
        # Event ID filter
        filter_frame = ttk.Frame(section)
        filter_frame.pack(fill=tk.X, pady=2)
        ttk.Label(filter_frame, text="Event ID:", width=10).pack(side=tk.LEFT)
        self.event_id_entry = ttk.Entry(filter_frame)
        self.event_id_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        # Level filter
        filter_frame = ttk.Frame(section)
        filter_frame.pack(fill=tk.X, pady=2)
        ttk.Label(filter_frame, text="Level:", width=10).pack(side=tk.LEFT)
        self.level_combo = ttk.Combobox(filter_frame, 
                                       values=["All", "Critical", "Error", "Warning", "Information"],
                                       state='readonly')
        self.level_combo.set("All")
        self.level_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        # Provider filter
        filter_frame = ttk.Frame(section)
        filter_frame.pack(fill=tk.X, pady=2)
        ttk.Label(filter_frame, text="Provider:", width=10).pack(side=tk.LEFT)
        self.provider_entry = ttk.Entry(filter_frame)
        self.provider_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        # Search text
        filter_frame = ttk.Frame(section)
        filter_frame.pack(fill=tk.X, pady=2)
        ttk.Label(filter_frame, text="Search:", width=10).pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(filter_frame)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        # Filter buttons
        button_frame = ttk.Frame(section)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="Apply Filters", 
                  command=self.apply_filters,
                  style='Accent.TButton').pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        ttk.Button(button_frame, text="Clear", 
                  command=self.clear_filters).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
    def create_stats_section(self, parent):
        """Create statistics section"""
        section = ttk.LabelFrame(parent, text="📊 Statistics", padding=10)
        section.pack(fill=tk.X, pady=(0, 10))
        
        self.stats_vars = {
            'total': tk.StringVar(value="0"),
            'critical': tk.StringVar(value="0"),
            'error': tk.StringVar(value="0"),
            'warning': tk.StringVar(value="0"),
            'info': tk.StringVar(value="0"),
            'bookmarks': tk.StringVar(value="0")
        }
        
        # Create stats grid
        stats = [
            ('Total Events', 'total', self.colors['fg']),
            ('🔥 Critical', 'critical', self.colors['danger']),
            ('⚠️ Error', 'error', self.colors['warning']),
            ('📝 Warning', 'warning', self.colors['accent']),
            ('ℹ️ Info', 'info', self.colors['success']),
            ('⭐ Bookmarked', 'bookmarks', self.colors['accent'])
        ]
        
        row = 0
        col = 0
        for label, key, color in stats:
            frame = ttk.Frame(section)
            frame.grid(row=row, column=col, padx=5, pady=2, sticky='ew')
            
            ttk.Label(frame, text=label, font=('Segoe UI', 9)).pack(anchor='w')
            ttk.Label(frame, textvariable=self.stats_vars[key], 
                     font=('Segoe UI', 12, 'bold'),
                     foreground=color).pack(anchor='w')
            
            col += 1
            if col > 1:
                col = 0
                row += 1
            
            section.grid_columnconfigure(col, weight=1)
        
    def create_event_viewer(self, parent):
        """Create enhanced event viewer with treeview"""
        section = ttk.LabelFrame(parent, text="📋 Events", padding=10)
        section.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Create toolbar for event viewer
        toolbar = ttk.Frame(section)
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(toolbar, text=f"Showing: ", font=('Segoe UI', 10)).pack(side=tk.LEFT)
        self.showing_label = ttk.Label(toolbar, text="0 events", 
                                       font=('Segoe UI', 10, 'bold'))
        self.showing_label.pack(side=tk.LEFT)
        
        # View controls
        ttk.Button(toolbar, text="Expand All", 
                  command=self.expand_all).pack(side=tk.RIGHT, padx=2)
        ttk.Button(toolbar, text="Collapse All", 
                  command=self.collapse_all).pack(side=tk.RIGHT, padx=2)
        
        # Create Treeview with scrollbars
        tree_frame = ttk.Frame(section)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview with columns
        self.tree = ttk.Treeview(tree_frame, 
                                 columns=("Time", "Event ID", "Level", "Provider", "Computer"),
                                 show="tree headings",
                                 height=15)
        
        # Configure columns
        self.tree.heading("#0", text="Record")
        self.tree.heading("Time", text="Time")
        self.tree.heading("Event ID", text="ID")
        self.tree.heading("Level", text="Level")
        self.tree.heading("Provider", text="Provider")
        self.tree.heading("Computer", text="Computer")
        
        self.tree.column("#0", width=60, minwidth=60)
        self.tree.column("Time", width=150, minwidth=120)
        self.tree.column("Event ID", width=50, minwidth=50)
        self.tree.column("Level", width=80, minwidth=80)
        self.tree.column("Provider", width=200, minwidth=150)
        self.tree.column("Computer", width=150, minwidth=120)
        
        # Add scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Bind events
        self.tree.bind('<<TreeviewSelect>>', self.on_event_select)
        self.tree.bind('<Double-Button-1>', self.on_event_double_click)
        self.tree.bind('<Button-3>', self.show_context_menu)
        
        # Configure tags for coloring
        self.tree.tag_configure('critical', background=self.colors['critical'])
        self.tree.tag_configure('error', background=self.colors['error'])
        self.tree.tag_configure('warning', background=self.colors['warning_bg'])
        self.tree.tag_configure('info', background=self.colors['info_bg'])
        self.tree.tag_configure('bookmarked', font=('Segoe UI', 10, 'bold'))
        
    def create_details_view(self, parent):
        """Create enhanced details view with tabs"""
        section = ttk.LabelFrame(parent, text="📄 Event Details", padding=10)
        section.pack(fill=tk.BOTH, expand=True)
        
        # Create notebook for tabs
        self.details_notebook = ttk.Notebook(section)
        self.details_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Summary tab
        summary_frame = ttk.Frame(self.details_notebook)
        self.details_notebook.add(summary_frame, text="Summary")
        
        # Create summary text widget
        self.summary_text = tk.Text(summary_frame, wrap=tk.WORD,
                                   font=('Consolas', 10),
                                   bg='white',
                                   fg=self.colors['fg'],
                                   padx=10,
                                   pady=10)
        summary_scroll = ttk.Scrollbar(summary_frame, orient=tk.VERTICAL,
                                      command=self.summary_text.yview)
        self.summary_text.configure(yscrollcommand=summary_scroll.set)
        
        self.summary_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        summary_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Raw XML tab
        xml_frame = ttk.Frame(self.details_notebook)
        self.details_notebook.add(xml_frame, text="Raw XML")
        
        self.xml_text = tk.Text(xml_frame, wrap=tk.NONE,
                               font=('Consolas', 10),
                               bg='white',
                               fg=self.colors['fg'],
                               padx=10,
                               pady=10)
        xml_scroll_y = ttk.Scrollbar(xml_frame, orient=tk.VERTICAL,
                                    command=self.xml_text.yview)
        xml_scroll_x = ttk.Scrollbar(xml_frame, orient=tk.HORIZONTAL,
                                    command=self.xml_text.xview)
        self.xml_text.configure(yscrollcommand=xml_scroll_y.set,
                               xscrollcommand=xml_scroll_x.set)
        
        self.xml_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        xml_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        xml_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Data Fields tab
        fields_frame = ttk.Frame(self.details_notebook)
        self.details_notebook.add(fields_frame, text="Data Fields")
        
        # Create treeview for data fields
        self.fields_tree = ttk.Treeview(fields_frame, columns=("Value",),
                                        show="tree headings")
        self.fields_tree.heading("#0", text="Field Name")
        self.fields_tree.heading("Value", text="Value")
        
        fields_scroll = ttk.Scrollbar(fields_frame, orient=tk.VERTICAL,
                                     command=self.fields_tree.yview)
        self.fields_tree.configure(yscrollcommand=fields_scroll.set)
        
        self.fields_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        fields_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bookmarks tab
        bookmarks_frame = ttk.Frame(self.details_notebook)
        self.details_notebook.add(bookmarks_frame, text="Bookmarks")
        
        self.bookmarks_text = tk.Text(bookmarks_frame, wrap=tk.WORD,
                                     font=('Consolas', 10),
                                     bg='white',
                                     fg=self.colors['fg'])
        bookmarks_scroll = ttk.Scrollbar(bookmarks_frame, orient=tk.VERTICAL,
                                        command=self.bookmarks_text.yview)
        self.bookmarks_text.configure(yscrollcommand=bookmarks_scroll.set)
        
        self.bookmarks_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        bookmarks_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
    def create_status_bar(self):
        """Create status bar"""
        self.status_bar = ttk.Frame(self.root, relief='sunken')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_label = ttk.Label(self.status_bar, text="Ready", padding=(5, 2))
        self.status_label.pack(side=tk.LEFT)
        
        self.progress_status = ttk.Label(self.status_bar, text="", padding=(5, 2))
        self.progress_status.pack(side=tk.RIGHT)
        
    def setup_drag_drop(self):
        """Setup drag and drop support (simplified version)"""
        # Note: Full drag-drop requires additional libraries
        # This is a placeholder for the concept
        self.root.drop_target_register = lambda *args: None
        self.root.dnd_bind = lambda *args: None
        
    def open_files(self):
        """Open file(s) dialog"""
        files = filedialog.askopenfilenames(
            title="Select Event Log Files",
            filetypes=[("EVTX files", "*.evtx"), ("All files", "*.*")]
        )
        if files:
            self.load_files(files)
    
    def open_folder(self):
        """Open folder dialog"""
        folder = filedialog.askdirectory(title="Select Folder with EVTX files")
        if folder:
            evtx_files = []
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if file.lower().endswith('.evtx'):
                        evtx_files.append(os.path.join(root, file))
            
            if evtx_files:
                self.load_files(evtx_files)
            else:
                messagebox.showinfo("No Files", "No .evtx files found in the selected folder")
    
    def load_files(self, files):
        """Load multiple files"""
        self.current_files = list(files)
        self.update_file_list()
        
        self.status_label.config(text=f"Loading {len(files)} files...")
        self.progress.start()
        
        thread = threading.Thread(target=self._load_files_thread, args=(files,))
        thread.daemon = True
        thread.start()
    
    def _load_files_thread(self, files):
        """Load files in background thread"""
        try:
            from evtx import PyEvtxParser
            
            self.events = []
            for file in files:
                try:
                    parser = PyEvtxParser(file)
                    for record in parser.records():
                        info = self.extract_event_info(record['event_record_id'], record['data'])
                        self.events.append(info)
                except Exception as e:
                    print(f"Error loading {file}: {e}")
            
            # Sort events by timestamp
            self.events.sort(key=lambda x: x['timestamp'], reverse=True)
            
            self.root.after(0, self._load_complete)
            
        except Exception as e:
            self.root.after(0, lambda: self._load_error(str(e)))
    
    def _load_complete(self):
        """Handle load completion"""
        self.progress.stop()
        self.filtered_events = self.events.copy()
        self.update_tree()
        self.update_stats()
        self.toolbar_file_label.config(text=f"{len(self.current_files)} files loaded")
        self.status_label.config(text=f"Loaded {len(self.events)} events from {len(self.current_files)} files")
    
    def _load_error(self, error_msg):
        """Handle load error"""
        self.progress.stop()
        messagebox.showerror("Error", f"Failed to load files:\n{error_msg}")
        self.status_label.config(text="Error loading files")
    
    def extract_event_info(self, record_id, xml_data):
        """Extract key fields from event XML"""
        info = {
            'record_id': record_id,
            'event_id': 'N/A',
            'level': 'Information',
            'level_num': '4',
            'provider': 'N/A',
            'timestamp': 'N/A',
            'computer': 'N/A',
            'raw_data': xml_data,
            'data_fields': [],
            'bookmarked': False
        }
        
        try:
            # Extract EventID
            match = re.search(r'<EventID[^>]*>(\d+)</EventID>', xml_data)
            if match:
                info['event_id'] = match.group(1)
            
            # Extract Level
            match = re.search(r'<Level[^>]*>(\d+)</Level>', xml_data)
            if match:
                info['level_num'] = match.group(1)
                level_map = {'1': 'Critical', '2': 'Error', '3': 'Warning', '4': 'Information'}
                info['level'] = level_map.get(info['level_num'], 'Unknown')
            
            # Extract Provider
            match = re.search(r'<Provider Name=[\'"]([^\'"]+)[\'"]', xml_data)
            if match:
                info['provider'] = match.group(1)
            
            # Extract TimeCreated
            match = re.search(r'<TimeCreated SystemTime=[\'"]([^\'"]+)[\'"]', xml_data)
            if match:
                timestamp = match.group(1)
                try:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    info['timestamp'] = dt.strftime('%Y-%m-%d %H:%M:%S')
                except:
                    info['timestamp'] = timestamp
            
            # Extract Computer
            match = re.search(r'<Computer>([^<]+)</Computer>', xml_data)
            if match:
                info['computer'] = match.group(1)
            
            # Extract all Data fields
            data_matches = re.findall(r'<Data Name=[\'"]([^\'"]+)[\'"]>([^<]*)</Data>', xml_data)
            info['data_fields'] = data_matches
            
        except Exception as e:
            print(f"Error parsing record {record_id}: {e}")
        
        return info
    
    def update_file_list(self):
        """Update the file listbox"""
        self.file_listbox.delete(0, tk.END)
        for file in self.current_files:
            self.file_listbox.insert(tk.END, os.path.basename(file))
    
    def remove_file(self, event):
        """Remove selected file from list"""
        selection = self.file_listbox.curselection()
        if selection:
            index = selection[0]
            del self.current_files[index]
            self.file_listbox.delete(index)
            
            if not self.current_files:
                self.clear_all()
    
    def update_tree(self):
        """Update the treeview with filtered events"""
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add events
        for event in self.filtered_events:
            # Determine tags
            tags = []
            if event['level'] == 'Critical':
                tags.append('critical')
            elif event['level'] == 'Error':
                tags.append('error')
            elif event['level'] == 'Warning':
                tags.append('warning')
            elif event['level'] == 'Information':
                tags.append('info')
            
            if event.get('bookmarked', False):
                tags.append('bookmarked')
            
            # Insert item
            self.tree.insert('', 'end',
                           text=event['record_id'],
                           values=(event['timestamp'][:19],  # Trim seconds
                                  event['event_id'],
                                  event['level'],
                                  event['provider'][:50] + ('...' if len(event['provider']) > 50 else ''),
                                  event['computer'][:30]),
                           tags=tags)
        
        # Update showing label
        self.showing_label.config(text=f"{len(self.filtered_events)} events")
    
    def update_stats(self):
        """Update statistics display"""
        critical = sum(1 for e in self.events if e['level'] == 'Critical')
        error = sum(1 for e in self.events if e['level'] == 'Error')
        warning = sum(1 for e in self.events if e['level'] == 'Warning')
        info = sum(1 for e in self.events if e['level'] == 'Information')
        bookmarks = sum(1 for e in self.events if e.get('bookmarked', False))
        
        self.stats_vars['total'].set(str(len(self.events)))
        self.stats_vars['critical'].set(str(critical))
        self.stats_vars['error'].set(str(error))
        self.stats_vars['warning'].set(str(warning))
        self.stats_vars['info'].set(str(info))
        self.stats_vars['bookmarks'].set(str(bookmarks))
    
    def quick_analysis_action(self, value):
        """Handle quick analysis button clicks"""
        if not self.events:
            messagebox.showinfo("Info", "Please load files first")
            return
        
        if value == '1001':
            self.filtered_events = [e for e in self.events if e['event_id'] == '1001']
            msg = f"Found {len(self.filtered_events)} crash events"
        elif value == '41':
            self.filtered_events = [e for e in self.events if e['event_id'] == '41']
            msg = f"Found {len(self.filtered_events)} unexpected shutdown events"
        elif value == 'critical':
            self.filtered_events = [e for e in self.events if e['level'] == 'Critical']
            msg = f"Found {len(self.filtered_events)} critical events"
        elif value == 'error':
            self.filtered_events = [e for e in self.events if e['level'] in ['Critical', 'Error']]
            msg = f"Found {len(self.filtered_events)} error events"
        elif value == 'disk':
            self.filtered_events = self.filter_disk_errors()
            msg = f"Found {len(self.filtered_events)} disk-related errors"
        elif value == 'last50':
            self.filtered_events = self.events[:50]
            msg = "Showing last 50 events"
        
        self.update_tree()
        self.status_label.config(text=msg)
    
    def quick_filter_level(self, level):
        """Filter by level"""
        if not self.events:
            return
        self.filtered_events = [e for e in self.events if e['level'] == level]
        self.update_tree()
        self.status_label.config(text=f"Showing {level.lower()} events")
    
    def filter_disk_errors(self):
        """Filter disk-related errors"""
        disk_keywords = ['disk', 'volume', 'ntfs', 'harddisk', 'storahci', 'atapi']
        results = []
        
        for event in self.events:
            if event['level'] in ['Critical', 'Error']:
                data_text = ' '.join([f"{name}:{value}" for name, value in event['data_fields']])
                provider_lower = event['provider'].lower()
                
                if any(keyword in provider_lower or keyword in data_text.lower() 
                       for keyword in disk_keywords):
                    results.append(event)
        
        return results
    
    def apply_filters(self):
        """Apply custom filters"""
        if not self.events:
            return
        
        event_id = self.event_id_entry.get().strip()
        level = self.level_combo.get()
        provider = self.provider_entry.get().strip().lower()
        search_text = self.search_entry.get().strip().lower()
        
        self.filtered_events = []
        
        for event in self.events:
            # Filter by Event ID
            if event_id and event['event_id'] != event_id:
                continue
            
            # Filter by Level
            if level != "All" and event['level'] != level:
                continue
            
            # Filter by Provider
            if provider and provider not in event['provider'].lower():
                continue
            
            # Filter by search text
            if search_text:
                data_text = ' '.join([f"{name}:{value}" for name, value in event['data_fields']])
                if search_text not in data_text.lower() and search_text not in event['raw_data'].lower():
                    continue
            
            self.filtered_events.append(event)
        
        self.update_tree()
        self.status_label.config(text=f"Found {len(self.filtered_events)} matching events")
    
    def clear_filters(self):
        """Clear all filters"""
        self.event_id_entry.delete(0, tk.END)
        self.level_combo.set("All")
        self.provider_entry.delete(0, tk.END)
        self.search_entry.delete(0, tk.END)
        
        self.filtered_events = self.events.copy()
        self.update_tree()
        self.status_label.config(text="Filters cleared")
    
    def on_event_select(self, event):
        """Handle event selection"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = selection[0]
        record_id = self.tree.item(item, 'text')
        
        # Find the event
        for event in self.filtered_events:
            if str(event['record_id']) == str(record_id):
                self.show_event_details(event)
                break
    
    def on_event_double_click(self, event):
        """Handle double-click on event"""
        self.on_event_select(event)
        # Switch to summary tab
        self.details_notebook.select(0)
    
    def show_context_menu(self, event):
        """Show context menu for event"""
        # Get item at click position
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            
            # Create popup menu
            menu = tk.Menu(self.root, tearoff=0)
            menu.add_command(label="Bookmark Event", command=self.bookmark_event)
            menu.add_command(label="Copy Event ID", command=self.copy_event_id)
            menu.add_command(label="Copy Provider", command=self.copy_provider)
            menu.add_separator()
            menu.add_command(label="Export This Event", command=self.export_single_event)
            
            menu.post(event.x_root, event.y_root)
    
    def show_event_details(self, event):
        """Show detailed event information in tabs"""
        # Update summary tab
        self.summary_text.delete(1.0, tk.END)
        
        summary = f"""╔══════════════════════════════════════════════════════════╗
║                     EVENT DETAILS                          ║
╚══════════════════════════════════════════════════════════════╝

📋 BASIC INFORMATION
────────────────────────────────────────────────
Record ID:      {event['record_id']}
Timestamp:      {event['timestamp']}
Event ID:       {event['event_id']}
Level:          {event['level']}
Provider:       {event['provider']}
Computer:       {event['computer']}
Bookmarked:     {'✅ Yes' if event.get('bookmarked', False) else '❌ No'}

📊 DATA FIELDS
────────────────────────────────────────────────
"""
        
        for name, value in event['data_fields']:
            summary += f"{name}: {value}\n"
        
        if not event['data_fields']:
            summary += "No data fields available\n"
        
        self.summary_text.insert(1.0, summary)
        
        # Update XML tab
        self.xml_text.delete(1.0, tk.END)
        self.xml_text.insert(1.0, event['raw_data'])
        
        # Update fields tree
        for item in self.fields_tree.get_children():
            self.fields_tree.delete(item)
        
        for name, value in event['data_fields']:
            self.fields_tree.insert('', 'end', text=name, values=(value,))
    
    def bookmark_event(self):
        """Bookmark current event"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = selection[0]
        record_id = self.tree.item(item, 'text')
        
        # Find and toggle bookmark
        for event in self.filtered_events:
            if str(event['record_id']) == str(record_id):
                event['bookmarked'] = not event.get('bookmarked', False)
                
                # Update bookmarks list
                if event['bookmarked']:
                    self.bookmarks.append(event)
                    self.bookmarks_text.insert(tk.END, 
                        f"📌 Event {event['record_id']} - {event['timestamp']}\n"
                        f"   {event['provider']} - {event['event_id']}\n\n")
                else:
                    self.bookmarks = [b for b in self.bookmarks 
                                    if str(b['record_id']) != str(record_id)]
                    self.update_bookmarks_text()
                
                # Update tree
                self.update_tree()
                self.update_stats()
                
                status = "bookmarked" if event['bookmarked'] else "unbookmarked"
                self.status_label.config(text=f"Event {status}")
                break
    
    def update_bookmarks_text(self):
        """Update bookmarks text widget"""
        self.bookmarks_text.delete(1.0, tk.END)
        for bookmark in self.bookmarks:
            self.bookmarks_text.insert(tk.END,
                f"📌 Event {bookmark['record_id']} - {bookmark['timestamp']}\n"
                f"   {bookmark['provider']} - {bookmark['event_id']}\n\n")
    
    def show_bookmarks(self):
        """Switch to bookmarks tab"""
        self.details_notebook.select(3)  # Bookmarks tab
    
    def copy_event_id(self):
        """Copy event ID to clipboard"""
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            event_id = self.tree.item(item, 'values')[1]
            self.root.clipboard_clear()
            self.root.clipboard_append(event_id)
            self.status_label.config(text=f"Event ID {event_id} copied to clipboard")
    
    def copy_provider(self):
        """Copy provider to clipboard"""
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            provider = self.tree.item(item, 'values')[3]
            self.root.clipboard_clear()
            self.root.clipboard_append(provider)
            self.status_label.config(text=f"Provider copied to clipboard")
    
    def export_single_event(self):
        """Export currently selected event"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = selection[0]
        record_id = self.tree.item(item, 'text')
        
        for event in self.filtered_events:
            if str(event['record_id']) == str(record_id):
                filename = filedialog.asksaveasfilename(
                    title="Export Event",
                    defaultextension=".txt",
                    initialfile=f"event_{record_id}.txt",
                    filetypes=[("Text files", "*.txt"), ("XML files", "*.xml"), ("All files", "*.*")]
                )
                
                if filename:
                    try:
                        with open(filename, 'w') as f:
                            f.write(event['raw_data'])
                        messagebox.showinfo("Success", f"Event exported to {filename}")
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to export: {e}")
                break
    
    def expand_all(self):
        """Expand all tree items"""
        for item in self.tree.get_children():
            self.tree.item(item, open=True)
    
    def collapse_all(self):
        """Collapse all tree items"""
        for item in self.tree.get_children():
            self.tree.item(item, open=False)
    
    def expand_all_details(self):
        """Expand all details tabs"""
        # Implementation for expanding details
        pass
    
    def collapse_all_details(self):
        """Collapse all details tabs"""
        # Implementation for collapsing details
        pass
    
    def show_search_dialog(self):
        """Show search dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Search Events")
        dialog.geometry("400x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Search for:", font=('Segoe UI', 10)).pack(pady=10)
        
        search_entry = ttk.Entry(dialog, width=40, font=('Segoe UI', 10))
        search_entry.pack(pady=5)
        search_entry.focus()
        
        def do_search():
            text = search_entry.get().strip()
            if text:
                self.search_entry.delete(0, tk.END)
                self.search_entry.insert(0, text)
                self.apply_filters()
                dialog.destroy()
        
        ttk.Button(dialog, text="Search", command=do_search, 
                  style='Accent.TButton').pack(pady=10)
        
        search_entry.bind('<Return>', lambda e: do_search())
    
    def generate_report(self):
        """Generate summary report"""
        if not self.events:
            messagebox.showinfo("Info", "No events loaded")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Save Report",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write("=" * 80 + "\n")
                    f.write("WINDOWS EVENT LOG ANALYSIS REPORT\n")
                    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("=" * 80 + "\n\n")
                    
                    # Summary statistics
                    f.write("SUMMARY STATISTICS\n")
                    f.write("-" * 40 + "\n")
                    f.write(f"Total Events: {len(self.events)}\n")
                    f.write(f"Critical: {self.stats_vars['critical'].get()}\n")
                    f.write(f"Error: {self.stats_vars['error'].get()}\n")
                    f.write(f"Warning: {self.stats_vars['warning'].get()}\n")
                    f.write(f"Information: {self.stats_vars['info'].get()}\n")
                    f.write(f"Bookmarked: {self.stats_vars['bookmarks'].get()}\n\n")
                    
                    # Crash events
                    crashes = [e for e in self.events if e['event_id'] == '1001']
                    if crashes:
                        f.write("CRASH EVENTS (BugCheck)\n")
                        f.write("-" * 40 + "\n")
                        for crash in crashes[:10]:  # Show first 10
                            f.write(f"Time: {crash['timestamp']}\n")
                            f.write(f"Provider: {crash['provider']}\n")
                            f.write("-" * 20 + "\n")
                        if len(crashes) > 10:
                            f.write(f"... and {len(crashes) - 10} more\n\n")
                    
                    # Top providers
                    f.write("\nTOP EVENT PROVIDERS\n")
                    f.write("-" * 40 + "\n")
                    providers = {}
                    for event in self.events:
                        providers[event['provider']] = providers.get(event['provider'], 0) + 1
                    
                    for provider, count in sorted(providers.items(), key=lambda x: x[1], reverse=True)[:10]:
                        f.write(f"{provider}: {count} events\n")
                
                messagebox.showinfo("Success", f"Report saved to {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save report: {e}")
    
    def export_json(self):
        """Export events as JSON"""
        if not self.filtered_events:
            messagebox.showinfo("Info", "No events to export")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Export as JSON",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                # Prepare data for JSON
                export_data = []
                for event in self.filtered_events:
                    export_data.append({
                        'record_id': event['record_id'],
                        'timestamp': event['timestamp'],
                        'event_id': event['event_id'],
                        'level': event['level'],
                        'provider': event['provider'],
                        'computer': event['computer'],
                        'data_fields': dict(event['data_fields']),
                        'bookmarked': event.get('bookmarked', False)
                    })
                
                with open(filename, 'w') as f:
                    json.dump(export_data, f, indent=2)
                
                messagebox.showinfo("Success", f"Exported {len(export_data)} events to {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {e}")
    
    def export_results(self):
        """Export filtered results"""
        if not self.filtered_events:
            messagebox.showinfo("Info", "No results to export")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Export Results",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    if filename.endswith('.csv'):
                        # CSV format
                        f.write("Record ID,Time,Event ID,Level,Provider,Computer\n")
                        for event in self.filtered_events:
                            f.write(f"{event['record_id']},{event['timestamp']},"
                                   f"{event['event_id']},{event['level']},"
                                   f"{event['provider']},{event['computer']}\n")
                    else:
                        # Text format
                        for event in self.filtered_events:
                            f.write(f"--- Record {event['record_id']} ---\n")
                            f.write(f"Time: {event['timestamp']}\n")
                            f.write(f"Event ID: {event['event_id']}\n")
                            f.write(f"Level: {event['level']}\n")
                            f.write(f"Provider: {event['provider']}\n")
                            f.write(f"Computer: {event['computer']}\n")
                            f.write("-" * 60 + "\n\n")
                
                messagebox.showinfo("Success", f"Exported {len(self.filtered_events)} events to {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {e}")
    
    def refresh_view(self):
        """Refresh the current view"""
        self.update_tree()
        self.status_label.config(text="View refreshed")
    
    def clear_all(self):
        """Clear all loaded data"""
        self.current_files = []
        self.events = []
        self.filtered_events = []
        self.bookmarks = []
        
        self.file_listbox.delete(0, tk.END)
        self.toolbar_file_label.config(text="No files loaded")
        self.update_tree()
        self.update_stats()
        self.summary_text.delete(1.0, tk.END)
        self.xml_text.delete(1.0, tk.END)
        self.bookmarks_text.delete(1.0, tk.END)
        
        for item in self.fields_tree.get_children():
            self.fields_tree.delete(item)
        
        self.status_label.config(text="Cleared all data")
    
    def toggle_dark_mode(self):
        """Toggle dark/light mode"""
        self.dark_mode = not self.dark_mode
        
        if self.dark_mode:
            # Dark mode colors
            self.colors.update({
                'bg': '#1e1e1e',
                'fg': '#ffffff',
                'card_bg': '#2d2d2d',
                'border': '#404040',
                'accent_light': '#2d4d6e'
            })
        else:
            # Light mode colors
            self.colors.update({
                'bg': '#f5f5f5',
                'fg': '#333333',
                'card_bg': '#ffffff',
                'border': '#dee2e6',
                'accent_light': '#e1f0fa'
            })
        
        # Apply colors (simplified - would need to update all widgets)
        self.root.configure(bg=self.colors['bg'])
        self.status_label.config(text="Dark mode " + ("enabled" if self.dark_mode else "disabled"))
    
    def show_documentation(self):
        """Show documentation"""
        doc_text = """
Windows Event Log Analyzer
==========================

A powerful tool for analyzing Windows Event Log files (.evtx)

QUICK START:
1. Click 'Open Files' or drag & drop .evtx files
2. Use Quick Analysis buttons for common tasks
3. Click events to see details
4. Bookmark important events for later

FEATURES:
- View and filter event logs
- Quick crash analysis (Event ID 1001)
- Unexpected shutdown detection (Event ID 41)
- Disk error filtering
- Export to CSV, JSON, or text
- Bookmark important events
- Generate summary reports

For more help, visit the project website.
"""
        messagebox.showinfo("Documentation", doc_text)
    
    def show_about(self):
        """Show about dialog"""
        about_text = """
Windows Event Log Analyzer
Version 2.0

A modern tool for analyzing Windows event logs
to troubleshoot crashes and system issues.

Created with Python and Tkinter
Uses python-evtx for EVTX parsing

© 2024
"""
        messagebox.showinfo("About", about_text)

def main():
    root = tk.Tk()
    app = ModernEventLogAnalyzer(root)
    root.mainloop()

if __name__ == "__main__":
    main()