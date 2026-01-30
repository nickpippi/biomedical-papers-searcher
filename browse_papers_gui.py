#!/usr/bin/env python3
"""
GUI for Biomedical Papers Searcher.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import threading
from pathlib import Path
from datetime import datetime
from browse_papers import BiomedicalSearcher, DocxExporter


class ModernDarkGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Biomedical Papers Searcher")

        # Window setup - largura padrão otimizada, mas expande ao maximizar
        window_width = 800
        window_height = 850
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.minsize(650, 700)

        # Variables
        self.keywords_list = []
        self.year_mode_var = tk.StringVar(value="days")
        self.days_var = tk.IntVar(value=30)
        self.years_back_var = tk.IntVar(value=1)
        self.start_year_var = tk.IntVar(value=datetime.now().year)
        self.end_year_var = tk.IntVar(value=datetime.now().year)
        self.save_var = tk.BooleanVar(value=False)
        self.export_path = tk.StringVar(value="")
        self.is_searching = False

        # Dark Mode Colors
        self.colors = {
            'bg_dark': '#1a1a2e',
            'bg_medium': '#16213e',
            'bg_card': '#0f3460',
            'accent': '#00adb5',
            'accent_hover': '#05c7cf',
            'text_primary': '#eaeaea',
            'text_secondary': '#a8b2d1',
            'success': '#06ffa5',
            'danger': '#ff006e',
            'warning': '#ffbe0b',
            'input_bg': '#16213e',
            'border': '#2a2a4a'
        }

        self.root.configure(bg=self.colors['bg_dark'])
        self.setup_ui()

    def setup_ui(self):
        """Setup the interface"""
        # Header
        header = tk.Frame(self.root, bg=self.colors['accent'], height=90)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(
            header,
            text="BIOMEDICAL PAPERS SEARCHER",
            font=("Segoe UI", 18, "bold"),
            bg=self.colors['accent'],
            fg='white'
        ).pack(pady=(20, 3))

        tk.Label(
            header,
            text="Search across PubMed, bioRxiv, and Europe PMC",
            font=("Segoe UI", 9),
            bg=self.colors['accent'],
            fg='white'
        ).pack()

        # Main content with scrollbar
        main_frame = tk.Frame(self.root, bg=self.colors['bg_dark'])
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas and scrollbar - agora expande horizontalmente
        canvas = tk.Canvas(main_frame, bg=self.colors['bg_dark'], highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview, bg=self.colors['bg_medium'])

        # Container que irá expandir
        scrollable = tk.Frame(canvas, bg=self.colors['bg_dark'])

        def on_canvas_configure(event):
            # Atualiza a largura do frame interno para preencher o canvas
            canvas_width = event.width
            canvas.itemconfig(canvas_window, width=canvas_width)
            canvas.configure(scrollregion=canvas.bbox("all"))

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        # Mouse wheel scroll support
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind("<Configure>", on_canvas_configure)
        scrollable.bind("<Configure>", on_frame_configure)
        canvas.bind_all("<MouseWheel>", on_mousewheel)

        canvas_window = canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Sections
        self.create_keywords_section(scrollable)
        self.create_date_section(scrollable)
        self.create_export_section(scrollable)
        self.create_search_button(scrollable)
        self.create_results_section(scrollable)

    def create_card(self, parent, title):
        """Create a card container"""
        # Card frame
        card = tk.Frame(parent, bg=self.colors['bg_card'], highlightbackground=self.colors['border'],
                        highlightthickness=1)
        card.pack(fill=tk.X, pady=(0, 12), ipady=5, ipadx=5)

        # Title
        title_bar = tk.Frame(card, bg=self.colors['bg_medium'])
        title_bar.pack(fill=tk.X)

        tk.Label(
            title_bar,
            text=title,
            font=("Segoe UI", 10, "bold"),
            bg=self.colors['bg_medium'],
            fg=self.colors['text_primary'],
            anchor=tk.W
        ).pack(fill=tk.X, padx=12, pady=8)

        # Content frame
        content = tk.Frame(card, bg=self.colors['bg_card'])
        content.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        return content

    def create_keywords_section(self, parent):
        """Keywords section"""
        content = self.create_card(parent, "KEYWORDS")

        # Input
        input_frame = tk.Frame(content, bg=self.colors['bg_card'])
        input_frame.pack(fill=tk.X, pady=(0, 8))

        self.keyword_entry = tk.Entry(
            input_frame,
            font=("Segoe UI", 10),
            bg=self.colors['input_bg'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['accent'],
            relief=tk.FLAT,
            bd=0
        )
        self.keyword_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 8))
        self.keyword_entry.bind('<Return>', lambda e: self.add_keyword())

        tk.Button(
            input_frame,
            text="+ Add",
            font=("Segoe UI", 9, "bold"),
            bg=self.colors['accent'],
            fg='white',
            activebackground=self.colors['accent_hover'],
            activeforeground='white',
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            command=self.add_keyword,
            padx=18,
            pady=8
        ).pack(side=tk.LEFT)

        # Listbox
        list_frame = tk.Frame(content, bg=self.colors['input_bg'])
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 8))

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.keywords_listbox = tk.Listbox(
            list_frame,
            font=("Segoe UI", 9),
            bg=self.colors['input_bg'],
            fg=self.colors['text_primary'],
            selectbackground=self.colors['accent'],
            selectforeground='white',
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0,
            yscrollcommand=scrollbar.set,
            height=5
        )
        self.keywords_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=3, pady=3)
        scrollbar.config(command=self.keywords_listbox.yview)

        # Remove button
        tk.Button(
            content,
            text="- Remove Selected",
            font=("Segoe UI", 8),
            bg=self.colors['danger'],
            fg='white',
            activebackground='#cc0055',
            activeforeground='white',
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            command=self.remove_keyword,
            padx=12,
            pady=5
        ).pack()

    def create_date_section(self, parent):
        """Date selection section"""
        content = self.create_card(parent, "TIME RANGE")

        # Mode selection
        modes = [
            ("Last N Days", "days"),
            ("Years Back", "years"),
            ("Specific Year Range", "specific")
        ]

        for text, mode in modes:
            tk.Radiobutton(
                content,
                text=text,
                variable=self.year_mode_var,
                value=mode,
                font=("Segoe UI", 9),
                bg=self.colors['bg_card'],
                fg=self.colors['text_primary'],
                selectcolor=self.colors['bg_card'],
                activebackground=self.colors['bg_card'],
                activeforeground=self.colors['accent'],
                command=self.update_date_controls,
                cursor="hand2"
            ).pack(anchor=tk.W, pady=3)

        # Days frame
        self.days_frame = tk.Frame(content, bg=self.colors['bg_card'])
        self.days_frame.pack(fill=tk.X, pady=(8, 0))

        tk.Label(
            self.days_frame,
            text="Number of days:",
            font=("Segoe UI", 9),
            bg=self.colors['bg_card'],
            fg=self.colors['text_secondary']
        ).pack(anchor=tk.W, pady=(0, 5))

        btn_frame = tk.Frame(self.days_frame, bg=self.colors['bg_card'])
        btn_frame.pack(fill=tk.X)

        for days in [7, 14, 30, 60, 90, 180, 365]:
            tk.Button(
                btn_frame,
                text=f"{days}d",
                font=("Segoe UI", 8, "bold"),
                bg=self.colors['input_bg'],
                fg=self.colors['accent'],
                activebackground=self.colors['accent'],
                activeforeground='white',
                relief=tk.FLAT,
                bd=0,
                cursor="hand2",
                command=lambda d=days: self.set_days(d),
                padx=10,
                pady=5
            ).pack(side=tk.LEFT, padx=(0, 4))

        # Custom entry
        custom_frame = tk.Frame(self.days_frame, bg=self.colors['bg_card'])
        custom_frame.pack(fill=tk.X, pady=(8, 0))

        tk.Label(
            custom_frame,
            text="Custom:",
            font=("Segoe UI", 8),
            bg=self.colors['bg_card'],
            fg=self.colors['text_secondary']
        ).pack(side=tk.LEFT, padx=(0, 8))

        tk.Entry(
            custom_frame,
            textvariable=self.days_var,
            font=("Segoe UI", 9),
            width=8,
            bg=self.colors['input_bg'],
            fg=self.colors['text_primary'],
            relief=tk.FLAT,
            bd=0
        ).pack(side=tk.LEFT, ipady=4)

        # Years frame
        self.years_frame = tk.Frame(content, bg=self.colors['bg_card'])

        tk.Label(
            self.years_frame,
            text="Years back:",
            font=("Segoe UI", 9),
            bg=self.colors['bg_card'],
            fg=self.colors['text_secondary']
        ).pack(anchor=tk.W, pady=(0, 5))

        years_btn_frame = tk.Frame(self.years_frame, bg=self.colors['bg_card'])
        years_btn_frame.pack(fill=tk.X)

        for years in [1, 2, 3, 5, 10, 20, 30]:
            tk.Button(
                years_btn_frame,
                text=f"{years}y",
                font=("Segoe UI", 8, "bold"),
                bg=self.colors['input_bg'],
                fg='#7209b7',
                activebackground='#7209b7',
                activeforeground='white',
                relief=tk.FLAT,
                bd=0,
                cursor="hand2",
                command=lambda y=years: self.set_years(y),
                padx=10,
                pady=5
            ).pack(side=tk.LEFT, padx=(0, 4))

        # Specific years frame
        self.specific_frame = tk.Frame(content, bg=self.colors['bg_card'])

        # Start year
        start_frame = tk.Frame(self.specific_frame, bg=self.colors['bg_card'])
        start_frame.pack(fill=tk.X, pady=(0, 8))

        tk.Label(
            start_frame,
            text="Start Year:",
            font=("Segoe UI", 9),
            bg=self.colors['bg_card'],
            fg=self.colors['text_secondary']
        ).pack(side=tk.LEFT, padx=(0, 8))

        current_year = datetime.now().year
        tk.Spinbox(
            start_frame,
            from_=current_year - 30,
            to=current_year,
            textvariable=self.start_year_var,
            font=("Segoe UI", 9),
            width=8,
            bg=self.colors['input_bg'],
            fg=self.colors['text_primary'],
            relief=tk.FLAT,
            bd=0
        ).pack(side=tk.LEFT)

        # End year
        end_frame = tk.Frame(self.specific_frame, bg=self.colors['bg_card'])
        end_frame.pack(fill=tk.X)

        tk.Label(
            end_frame,
            text="End Year:",
            font=("Segoe UI", 9),
            bg=self.colors['bg_card'],
            fg=self.colors['text_secondary']
        ).pack(side=tk.LEFT, padx=(0, 8))

        tk.Spinbox(
            end_frame,
            from_=current_year - 30,
            to=current_year,
            textvariable=self.end_year_var,
            font=("Segoe UI", 9),
            width=8,
            bg=self.colors['input_bg'],
            fg=self.colors['text_primary'],
            relief=tk.FLAT,
            bd=0
        ).pack(side=tk.LEFT)

        self.update_date_controls()

    def create_export_section(self, parent):
        """Export options section"""
        content = self.create_card(parent, "EXPORT OPTIONS")

        # Checkbox
        tk.Checkbutton(
            content,
            text="Save results to DOCX document",
            variable=self.save_var,
            font=("Segoe UI", 9, "bold"),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            selectcolor=self.colors['bg_card'],
            activebackground=self.colors['bg_card'],
            activeforeground=self.colors['accent'],
            command=self.toggle_export,
            cursor="hand2"
        ).pack(anchor=tk.W, pady=(0, 10))

        # Path selection
        self.path_frame = tk.Frame(content, bg=self.colors['bg_card'])
        self.path_frame.pack(fill=tk.X)

        tk.Label(
            self.path_frame,
            text="Export folder:",
            font=("Segoe UI", 8),
            bg=self.colors['bg_card'],
            fg=self.colors['text_secondary']
        ).pack(anchor=tk.W, pady=(0, 5))

        path_input = tk.Frame(self.path_frame, bg=self.colors['bg_card'])
        path_input.pack(fill=tk.X)

        self.path_entry = tk.Entry(
            path_input,
            textvariable=self.export_path,
            font=("Segoe UI", 9),
            bg=self.colors['input_bg'],
            fg=self.colors['text_secondary'],
            relief=tk.FLAT,
            bd=0,
            state='disabled'
        )
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6, padx=(0, 8))

        self.browse_button = tk.Button(
            path_input,
            text="Browse...",
            font=("Segoe UI", 8),
            bg=self.colors['input_bg'],
            fg=self.colors['accent'],
            activebackground=self.colors['accent'],
            activeforeground='white',
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            command=self.browse_folder,
            state='disabled',
            padx=12,
            pady=6
        )
        self.browse_button.pack(side=tk.LEFT)

    def create_search_button(self, parent):
        """Search button section"""
        button_frame = tk.Frame(parent, bg=self.colors['bg_dark'])
        button_frame.pack(pady=15)

        self.search_button = tk.Button(
            button_frame,
            text="SEARCH PAPERS",
            font=("Segoe UI", 11, "bold"),
            bg=self.colors['success'],
            fg='black',
            activebackground='#04cc87',
            activeforeground='black',
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            command=self.start_search,
            padx=35,
            pady=10
        )
        self.search_button.pack(side=tk.LEFT, padx=4)

        self.cancel_button = tk.Button(
            button_frame,
            text="CANCEL",
            font=("Segoe UI", 10),
            bg=self.colors['danger'],
            fg='white',
            activebackground='#cc0055',
            activeforeground='white',
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            command=self.cancel_search,
            state='disabled',
            padx=25,
            pady=10
        )
        self.cancel_button.pack(side=tk.LEFT, padx=4)

    def create_results_section(self, parent):
        """Results display section"""
        content = self.create_card(parent, "PROGRESS & RESULTS")

        # Progress bar (using canvas for custom color)
        self.progress_canvas = tk.Canvas(
            content,
            height=4,
            bg=self.colors['input_bg'],
            highlightthickness=0
        )
        self.progress_canvas.pack(fill=tk.X, pady=(0, 10))

        # Progress indicator
        self.progress_bar = self.progress_canvas.create_rectangle(
            0, 0, 0, 4,
            fill=self.colors['accent'],
            outline=''
        )
        self.progress_active = False

        # Results text
        self.results_text = scrolledtext.ScrolledText(
            content,
            height=10,
            font=("Consolas", 9),
            bg='#0a0a12',
            fg='#00ff88',
            insertbackground=self.colors['accent'],
            relief=tk.FLAT,
            bd=0,
            wrap=tk.WORD,
            padx=8,
            pady=8
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)

    # Event handlers
    def set_days(self, days):
        self.days_var.set(days)

    def set_years(self, years):
        self.years_back_var.set(years)

    def update_date_controls(self):
        """Update date control visibility"""
        mode = self.year_mode_var.get()

        self.days_frame.pack_forget()
        self.years_frame.pack_forget()
        self.specific_frame.pack_forget()

        if mode == "days":
            self.days_frame.pack(fill=tk.X, pady=(8, 0))
        elif mode == "years":
            self.years_frame.pack(fill=tk.X, pady=(8, 0))
        elif mode == "specific":
            self.specific_frame.pack(fill=tk.X, pady=(8, 0))

    def toggle_export(self):
        """Toggle export options"""
        if self.save_var.get():
            self.path_entry.config(state='normal', fg=self.colors['text_primary'])
            self.browse_button.config(state='normal')
        else:
            self.path_entry.config(state='disabled', fg=self.colors['text_secondary'])
            self.browse_button.config(state='disabled')

    def browse_folder(self):
        """Browse for folder"""
        folder = filedialog.askdirectory(title="Select Export Folder")
        if folder:
            self.export_path.set(folder)
            self.log_message(f"[+] Export folder: {folder}")

    def add_keyword(self):
        """Add keyword"""
        keyword = self.keyword_entry.get().strip()
        if keyword and keyword not in self.keywords_list:
            self.keywords_list.append(keyword)
            self.keywords_listbox.insert(tk.END, keyword)
            self.keyword_entry.delete(0, tk.END)
            self.log_message(f"[+] Added: {keyword}")
        elif keyword in self.keywords_list:
            messagebox.showwarning("Duplicate", "Keyword already exists!")

    def remove_keyword(self):
        """Remove keyword"""
        selection = self.keywords_listbox.curselection()
        if selection:
            index = selection[0]
            keyword = self.keywords_list[index]
            del self.keywords_list[index]
            self.keywords_listbox.delete(index)
            self.log_message(f"[-] Removed: {keyword}")

    def log_message(self, message):
        """Log message"""
        self.results_text.insert(tk.END, message + "\n")
        self.results_text.see(tk.END)
        self.root.update_idletasks()

    def clear_results(self):
        """Clear results"""
        self.results_text.delete(1.0, tk.END)

    def animate_progress(self):
        """Animate progress bar"""
        if self.progress_active:
            current_width = self.progress_canvas.coords(self.progress_bar)[2]
            canvas_width = self.progress_canvas.winfo_width()

            if current_width >= canvas_width:
                self.progress_canvas.coords(self.progress_bar, 0, 0, 0, 4)
            else:
                new_width = current_width + 10
                self.progress_canvas.coords(self.progress_bar, 0, 0, new_width, 4)

            self.root.after(20, self.animate_progress)

    def calculate_days(self):
        """Calculate days based on mode"""
        mode = self.year_mode_var.get()

        if mode == "days":
            return self.days_var.get()
        elif mode == "years":
            return self.years_back_var.get() * 365
        elif mode == "specific":
            start = self.start_year_var.get()
            end = self.end_year_var.get()

            if start > end:
                raise ValueError("Start year must be <= end year!")

            current_year = datetime.now().year
            return (current_year - start) * 365 + 30

        return 30

    def validate_inputs(self):
        """Validate inputs"""
        if not self.keywords_list:
            messagebox.showerror("Error", "Add at least one keyword!")
            return False

        mode = self.year_mode_var.get()
        if mode == "specific":
            if self.start_year_var.get() > self.end_year_var.get():
                messagebox.showerror("Error", "Start year must be <= end year!")
                return False

        if self.save_var.get() and not self.export_path.get():
            messagebox.showerror("Error", "Select an export folder!")
            return False

        return True

    def start_search(self):
        """Start search"""
        if not self.validate_inputs():
            return

        self.search_button.config(state='disabled')
        self.cancel_button.config(state='normal')
        self.progress_active = True
        self.animate_progress()
        self.clear_results()
        self.is_searching = True

        threading.Thread(target=self.perform_search, daemon=True).start()

    def cancel_search(self):
        """Cancel search"""
        self.is_searching = False
        self.log_message("\n[!] Cancelled by user.\n")

    def perform_search(self):
        """Perform search"""
        try:
            days = self.calculate_days()
            mode = self.year_mode_var.get()

            if mode == "days":
                self.log_message(f"[*] Searching last {days} days...\n")
            elif mode == "years":
                self.log_message(f"[*] Searching last {self.years_back_var.get()} years...\n")
            elif mode == "specific":
                self.log_message(f"[*] From {self.start_year_var.get()} to {self.end_year_var.get()}...\n")

            self.log_message(f"[*] Keywords: {', '.join(self.keywords_list)}\n")

            searcher = BiomedicalSearcher(keywords=self.keywords_list, days=days)
            articles = searcher.search_all()

            if not self.is_searching:
                return

            ranked = searcher.rank_articles(articles)

            self.log_message("\n" + "=" * 60)
            self.log_message("RESULTS")
            self.log_message("=" * 60 + "\n")

            total = sum(len(articles) for articles in ranked.values())
            self.log_message(f"Total: {total} articles\n")

            for score in sorted(ranked.keys(), reverse=True):
                articles = ranked[score]
                self.log_message(f"\n{'=' * 60}")
                self.log_message(f"{score} MATCH{'ES' if score > 1 else ''} ({len(articles)} articles)")
                self.log_message('=' * 60)

                for idx, article in enumerate(articles[:3], 1):
                    self.log_message(f"\n[{idx}] {article.get('title', 'N/A')}")
                    self.log_message(f"    Source: {article.get('source', 'N/A')}")
                    self.log_message(f"    Date: {article['published'].strftime('%Y-%m-%d')}")
                    self.log_message(f"    Matches: {', '.join(article['matched_keywords'])}")

                if len(articles) > 3:
                    self.log_message(f"\n    ... +{len(articles) - 3} more")

            if self.save_var.get() and self.export_path.get():
                self.log_message("\n[*] Exporting...")
                exporter = DocxExporter(
                    keywords=self.keywords_list,
                    days=days,
                    output_path=self.export_path.get()
                )
                filepath = exporter.export(ranked)

                if filepath:
                    self.log_message(f"[+] Saved: {filepath}")
                else:
                    self.log_message("[-] Export failed")

            self.log_message("\n[+] Search completed!\n")

        except Exception as e:
            self.log_message(f"\n[!] Error: {str(e)}\n")

        finally:
            self.root.after(0, self.search_complete)

    def search_complete(self):
        """Search complete"""
        self.progress_active = False
        self.progress_canvas.coords(self.progress_bar, 0, 0, 0, 4)
        self.search_button.config(state='normal')
        self.cancel_button.config(state='disabled')
        self.is_searching = False


def main():
    root = tk.Tk()
    app = ModernDarkGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()