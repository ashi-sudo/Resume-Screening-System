"""
Graphical User Interface for Resume Screening System
Run this file to open the GUI application
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
import pandas as pd
from threading import Thread

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import config
from src.extract_text import extract_text
from src.simple_preprocess import preprocess_text
from src.match_skills import load_skills, match_skills

class ResumeScreeningGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Resume Screening System")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # Set icon (optional)
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
        
        # Variables
        self.resume_files = []
        self.skills = []
        self.results = []
        
        # Create GUI
        self.create_widgets()
        
        # Load skills automatically
        self.load_skills()
        
        # Scan resumes folder
        self.scan_resumes_folder()
    
    def create_widgets(self):
        # Title Frame
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="🤖 AI Resume Screening System", 
                               font=('Arial', 24, 'bold'), bg='#2c3e50', fg='white')
        title_label.pack(pady=20)
        
        # Main Content Frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Left Panel - Controls
        left_panel = tk.Frame(main_frame, bg='#ffffff', relief='raised', bd=1)
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Right Panel - Results
        right_panel = tk.Frame(main_frame, bg='#ffffff', relief='raised', bd=1)
        right_panel.pack(side='right', fill='both', expand=True)
        
        # ========== LEFT PANEL CONTENT ==========
        # Skills Section
        skills_label = tk.Label(left_panel, text="📋 Required Skills", 
                                font=('Arial', 14, 'bold'), bg='#ffffff')
        skills_label.pack(pady=(15, 5), anchor='w', padx=15)
        
        # Skills Text Area
        self.skills_text = tk.Text(left_panel, height=8, width=35, font=('Arial', 10))
        self.skills_text.pack(padx=15, pady=5, fill='both')
        
        # Skills Buttons
        skills_btn_frame = tk.Frame(left_panel, bg='#ffffff')
        skills_btn_frame.pack(pady=5, padx=15)
        
        tk.Button(skills_btn_frame, text="📂 Load Skills File", command=self.load_skills_file,
                 bg='#3498db', fg='white', padx=10, pady=5).pack(side='left', padx=5)
        tk.Button(skills_btn_frame, text="💾 Save Skills", command=self.save_skills,
                 bg='#2ecc71', fg='white', padx=10, pady=5).pack(side='left', padx=5)
        
        # Resume Section
        resume_label = tk.Label(left_panel, text="📄 Resumes", 
                                font=('Arial', 14, 'bold'), bg='#ffffff')
        resume_label.pack(pady=(15, 5), anchor='w', padx=15)
        
        # Resume Listbox
        self.resume_listbox = tk.Listbox(left_panel, height=8, selectmode='extended',
                                          font=('Arial', 10))
        self.resume_listbox.pack(padx=15, pady=5, fill='both')
        
        # Resume Buttons
        resume_btn_frame = tk.Frame(left_panel, bg='#ffffff')
        resume_btn_frame.pack(pady=5, padx=15)
        
        tk.Button(resume_btn_frame, text="➕ Add Resume(s)", command=self.add_resumes,
                 bg='#3498db', fg='white', padx=10, pady=5).pack(side='left', padx=5)
        tk.Button(resume_btn_frame, text="🗑️ Remove Selected", command=self.remove_selected,
                 bg='#e74c3c', fg='white', padx=10, pady=5).pack(side='left', padx=5)
        
        # Progress Bar
        self.progress = ttk.Progressbar(left_panel, mode='indeterminate')
        self.progress.pack(pady=15, padx=15, fill='x')
        
        # Run Button
        self.run_button = tk.Button(left_panel, text="🚀 START SCREENING", 
                                    command=self.start_screening,
                                    bg='#e67e22', fg='white', font=('Arial', 12, 'bold'),
                                    padx=20, pady=10)
        self.run_button.pack(pady=15, padx=15, fill='x')
        
        # Status Label
        self.status_label = tk.Label(left_panel, text="✅ Ready", 
                                     font=('Arial', 10), bg='#ffffff', fg='green')
        self.status_label.pack(pady=5)
        
        # ========== RIGHT PANEL CONTENT ==========
        # Results Label
        results_label = tk.Label(right_panel, text="🏆 Ranked Candidates", 
                                 font=('Arial', 14, 'bold'), bg='#ffffff')
        results_label.pack(pady=(15, 5), anchor='w', padx=15)
        
        # Results Treeview
        columns = ('Rank', 'Resume', 'Score', 'Matched Skills')
        self.tree = ttk.Treeview(right_panel, columns=columns, show='headings', height=15)
        
        # Define headings
        self.tree.heading('Rank', text='Rank')
        self.tree.heading('Resume', text='Resume Name')
        self.tree.heading('Score', text='Score (%)')
        self.tree.heading('Matched Skills', text='Matched Skills')
        
        # Define column widths
        self.tree.column('Rank', width=50, anchor='center')
        self.tree.column('Resume', width=200)
        self.tree.column('Score', width=80, anchor='center')
        self.tree.column('Matched Skills', width=250)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(right_panel, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(padx=15, pady=5, fill='both', expand=True)
        scrollbar.pack(side='right', fill='y', pady=5)
        
        # Export Buttons
        export_frame = tk.Frame(right_panel, bg='#ffffff')
        export_frame.pack(pady=10, padx=15, fill='x')
        
        tk.Button(export_frame, text="📊 Export to CSV", command=self.export_csv,
                 bg='#27ae60', fg='white', padx=15, pady=5).pack(side='left', padx=5)
        tk.Button(export_frame, text="🖨️ Print Results", command=self.print_results,
                 bg='#2980b9', fg='white', padx=15, pady=5).pack(side='left', padx=5)
        tk.Button(export_frame, text="🗑️ Clear Results", command=self.clear_results,
                 bg='#95a5a6', fg='white', padx=15, pady=5).pack(side='left', padx=5)
        
        # Stats Frame
        stats_frame = tk.Frame(right_panel, bg='#ecf0f1', relief='sunken', bd=1)
        stats_frame.pack(pady=10, padx=15, fill='x')
        
        self.stats_label = tk.Label(stats_frame, text="📊 Statistics: Ready", 
                                    font=('Arial', 10), bg='#ecf0f1')
        self.stats_label.pack(pady=5)
    
    def load_skills(self):
        """Load skills from default file"""
        try:
            if os.path.exists(config.SKILLS_FILE):
                with open(config.SKILLS_FILE, 'r') as f:
                    skills = f.read()
                    self.skills_text.delete('1.0', tk.END)
                    self.skills_text.insert('1.0', skills)
                    self.status_label.config(text="✅ Skills loaded", fg='green')
            else:
                # Default skills
                default_skills = "python\nmachine learning\nnlp\nsql\ntensorflow\npytorch\ndata analysis\ncommunication"
                self.skills_text.insert('1.0', default_skills)
        except Exception as e:
            self.status_label.config(text=f"❌ Error: {e}", fg='red')
    
    def load_skills_file(self):
        """Load skills from selected file"""
        filepath = filedialog.askopenfilename(
            title="Select Skills File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filepath:
            try:
                with open(filepath, 'r') as f:
                    skills = f.read()
                    self.skills_text.delete('1.0', tk.END)
                    self.skills_text.insert('1.0', skills)
                    self.status_label.config(text="✅ Skills file loaded", fg='green')
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")
    
    def save_skills(self):
        """Save skills to file"""
        filepath = filedialog.asksaveasfilename(
            title="Save Skills File",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filepath:
            try:
                skills = self.skills_text.get('1.0', tk.END)
                with open(filepath, 'w') as f:
                    f.write(skills)
                self.status_label.config(text="✅ Skills saved", fg='green')
                messagebox.showinfo("Success", "Skills saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save: {e}")
    
    def scan_resumes_folder(self):
        """Scan resumes folder and populate listbox"""
        if os.path.exists(config.RESUME_DIR):
            for file in os.listdir(config.RESUME_DIR):
                if file.endswith(('.pdf', '.docx')):
                    self.resume_files.append(file)
                    self.resume_listbox.insert(tk.END, file)
            self.status_label.config(text=f"✅ Found {len(self.resume_files)} resumes", fg='green')
    
    def add_resumes(self):
        """Add resume files manually"""
        files = filedialog.askopenfilenames(
            title="Select Resume Files",
            filetypes=[("Resume files", "*.pdf *.docx"), ("PDF files", "*.pdf"), ("DOCX files", "*.docx")]
        )
        for file in files:
            filename = os.path.basename(file)
            if filename not in self.resume_files:
                # Copy to resumes folder
                import shutil
                dest = os.path.join(config.RESUME_DIR, filename)
                shutil.copy(file, dest)
                self.resume_files.append(filename)
                self.resume_listbox.insert(tk.END, filename)
        self.status_label.config(text=f"✅ Added {len(files)} resumes", fg='green')
    
    def remove_selected(self):
        """Remove selected resumes"""
        selected = self.resume_listbox.curselection()
        for i in reversed(selected):
            filename = self.resume_listbox.get(i)
            self.resume_files.remove(filename)
            self.resume_listbox.delete(i)
            # Delete file from folder
            filepath = os.path.join(config.RESUME_DIR, filename)
            if os.path.exists(filepath):
                os.remove(filepath)
        self.status_label.config(text=f"✅ Removed {len(selected)} resumes", fg='green')
    
    def start_screening(self):
        """Start the screening process"""
        if not self.resume_files:
            messagebox.showwarning("No Resumes", "Please add some resumes first!")
            return
        
        # Clear previous results
        self.clear_results()
        
        # Disable button during processing
        self.run_button.config(state='disabled', text="⏳ Processing...")
        self.progress.start()
        self.status_label.config(text="🔄 Processing resumes...", fg='blue')
        
        # Run in thread to keep GUI responsive
        thread = Thread(target=self.process_resumes)
        thread.start()
    
    def process_resumes(self):
        """Process all resumes (runs in background thread)"""
        try:
            # Load skills
            skills_text = self.skills_text.get('1.0', tk.END)
            skills = [s.strip().lower() for s in skills_text.split('\n') if s.strip()]
            
            results = []
            
            for filename in self.resume_files:
                filepath = os.path.join(config.RESUME_DIR, filename)
                
                # Extract text
                raw_text = extract_text(filepath)
                if not raw_text:
                    results.append((filename, 0, "Extraction failed"))
                    continue
                
                # Preprocess
                tokens = preprocess_text(raw_text, verbose=False)
                
                # Match skills
                matched = []
                for skill in skills:
                    skill_parts = skill.split()
                    if len(skill_parts) == 1:
                        if skill in tokens:
                            matched.append(skill)
                    else:
                        if all(part in tokens for part in skill_parts):
                            matched.append(skill)
                
                # Calculate score
                score = (len(matched) / len(skills)) * 100 if skills else 0
                results.append((filename, round(score, 2), ', '.join(matched[:5])))
            
            # Sort by score
            results.sort(key=lambda x: x[1], reverse=True)
            self.results = results
            
            # Update GUI (must be done in main thread)
            self.root.after(0, self.display_results, results, skills)
            
        except Exception as e:
            self.root.after(0, self.show_error, str(e))
    
    def display_results(self, results, skills):
        """Display results in treeview"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for rank, (filename, score, matched) in enumerate(results, 1):
            self.tree.insert('', 'end', values=(rank, filename, f"{score}%", matched))
        
        # Update statistics
        avg_score = sum(r[1] for r in results) / len(results) if results else 0
        stats_text = f"📊 Total: {len(results)} resumes | Avg Score: {avg_score:.2f}% | Skills: {len(skills)}"
        self.stats_label.config(text=stats_text)
        
        # Stop progress
        self.progress.stop()
        self.run_button.config(state='normal', text="🚀 START SCREENING")
        self.status_label.config(text="✅ Screening complete!", fg='green')
        
        # Show top candidate
        if results:
            top = results[0]
            messagebox.showinfo("Screening Complete", 
                               f"Top Candidate: {top[0]}\nScore: {top[1]}%\n\nResults saved in memory. Click Export to save CSV.")
    
    def show_error(self, error):
        """Show error message"""
        self.progress.stop()
        self.run_button.config(state='normal', text="🚀 START SCREENING")
        self.status_label.config(text=f"❌ Error: {error}", fg='red')
        messagebox.showerror("Processing Error", error)
    
    def export_csv(self):
        """Export results to CSV"""
        if not self.results:
            messagebox.showwarning("No Results", "No results to export. Run screening first!")
            return
        
        filepath = filedialog.asksaveasfilename(
            title="Save CSV File",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filepath:
            try:
                df = pd.DataFrame(self.results, columns=['Resume', 'Score (%)', 'Matched Skills'])
                df.insert(0, 'Rank', range(1, len(df) + 1))
                df.to_csv(filepath, index=False)
                messagebox.showinfo("Success", f"Results exported to:\n{filepath}")
                self.status_label.config(text="✅ Exported to CSV", fg='green')
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {e}")
    
    def print_results(self):
        """Print/save results as text"""
        if not self.results:
            messagebox.showwarning("No Results", "No results to print. Run screening first!")
            return
        
        output = "="*60 + "\n"
        output += "AI RESUME SCREENING SYSTEM - RESULTS\n"
        output += "="*60 + "\n\n"
        
        for rank, (filename, score, matched) in enumerate(self.results, 1):
            output += f"Rank #{rank}: {filename}\n"
            output += f"   Score: {score}%\n"
            output += f"   Matched: {matched}\n\n"
        
        output += "="*60 + "\n"
        
        # Save to file
        filepath = os.path.join(config.OUTPUT_DIR, "results_print.txt")
        with open(filepath, 'w') as f:
            f.write(output)
        
        messagebox.showinfo("Results Saved", f"Results saved to:\n{filepath}")
        self.status_label.config(text="✅ Results printed", fg='green')
    
    def clear_results(self):
        """Clear all results"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.results = []
        self.stats_label.config(text="📊 Statistics: Ready")
        self.status_label.config(text="✅ Results cleared", fg='green')


def main():
    root = tk.Tk()
    app = ResumeScreeningGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()