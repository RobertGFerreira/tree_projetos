import os
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from pathlib import Path
import re

class FileTreeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de Árvore de Arquivos")
        
        # Maximizar a janela
        self.root.state('zoomed')  # Para Windows
        try:
            self.root.attributes('-zoomed', True)  # Para Linux
        except:
            pass
        
        # Variáveis
        self.selected_dir = tk.StringVar()
        self.extensions = {}
        self.extension_vars = {}
        self.directory_structure = {}
        self.directory_vars = {}
        self.files_by_dir = {}
        self.preview_text = tk.StringVar()
        
        # Frame principal
        main_frame = ttk.Frame(root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Frame superior para seleção de diretório
        dir_frame = ttk.LabelFrame(main_frame, text="Selecionar Diretório")
        dir_frame.pack(fill="x", padx=5, pady=5)
        
        self.dir_entry = ttk.Entry(dir_frame, textvariable=self.selected_dir, width=50)
        self.dir_entry.pack(side="left", padx=5, pady=5, fill="x", expand=True)
        
        self.browse_button = ttk.Button(dir_frame, text="Procurar...", command=self.browse_directory)
        self.browse_button.pack(side="right", padx=5, pady=5)
        
        # Frame para conteúdo principal dividido em 3 partes
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill="both", expand=True, padx=5, pady=5)
        content_frame.columnconfigure(0, weight=2)  # Estrutura de pastas
        content_frame.columnconfigure(1, weight=1)  # Lista de extensões
        content_frame.columnconfigure(2, weight=3)  # Prévia
        content_frame.rowconfigure(0, weight=1)
        
        # 1. Frame para estrutura de pastas
        dirs_frame = ttk.LabelFrame(content_frame, text="Estrutura de Pastas")
        dirs_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        # Adicionar uma treeview para a estrutura de pastas
        self.dirs_tree = ttk.Treeview(dirs_frame)
        self.dirs_tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        dir_scrollbar = ttk.Scrollbar(self.dirs_tree, orient="vertical", command=self.dirs_tree.yview)
        self.dirs_tree.configure(yscrollcommand=dir_scrollbar.set)
        dir_scrollbar.pack(side="right", fill="y")
        
        # 2. Frame para extensões
        extensions_frame = ttk.LabelFrame(content_frame, text="Extensões")
        extensions_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        
        self.extensions_canvas = tk.Canvas(extensions_frame)
        self.extensions_canvas.pack(side="left", fill="both", expand=True)
        
        ext_scrollbar = ttk.Scrollbar(extensions_frame, orient="vertical", command=self.extensions_canvas.yview)
        ext_scrollbar.pack(side="right", fill="y")
        
        self.extensions_canvas.configure(yscrollcommand=ext_scrollbar.set)
        self.extensions_canvas.bind("<Configure>", lambda e: self.extensions_canvas.configure(scrollregion=self.extensions_canvas.bbox("all")))
        
        self.check_ext_frame = ttk.Frame(self.extensions_canvas)
        self.extensions_canvas.create_window((0, 0), window=self.check_ext_frame, anchor="nw")
        
        # 3. Frame para prévia
        preview_frame = ttk.LabelFrame(content_frame, text="Prévia da Árvore")
        preview_frame.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
        
        self.preview_text = tk.Text(preview_frame, wrap="none", font=("Courier", 10))
        self.preview_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        preview_y_scrollbar = ttk.Scrollbar(self.preview_text, orient="vertical", command=self.preview_text.yview)
        preview_y_scrollbar.pack(side="right", fill="y")
        
        preview_x_scrollbar = ttk.Scrollbar(preview_frame, orient="horizontal", command=self.preview_text.xview)
        preview_x_scrollbar.pack(side="bottom", fill="x")
        
        self.preview_text.configure(yscrollcommand=preview_y_scrollbar.set, xscrollcommand=preview_x_scrollbar.set)
        
        # Frame para ações
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill="x", padx=5, pady=5)
        
        # Checkboxes para selecionar todas as extensões
        self.select_all_ext_var = tk.BooleanVar()
        self.select_all_ext_check = ttk.Checkbutton(
            action_frame, 
            text="Selecionar Todas as Extensões", 
            variable=self.select_all_ext_var, 
            command=self.toggle_all_extensions
        )
        self.select_all_ext_check.pack(side="left", padx=5, pady=5)
        
        # Botão para atualizar prévia
        self.update_preview_button = ttk.Button(action_frame, text="Atualizar Prévia", command=self.update_preview)
        self.update_preview_button.pack(side="left", padx=5, pady=5)
        
        self.generate_button = ttk.Button(action_frame, text="Gerar TXT", command=self.generate_tree)
        self.generate_button.pack(side="right", padx=5, pady=5)
        
        # Botão para salvar como Markdown com ícones
        self.save_markdown_button = ttk.Button(action_frame, text="Gerar Markdown", command=self.generate_markdown)
        self.save_markdown_button.pack(side="right", padx=5, pady=5)
        
        # Configurar eventos para a árvore
        self.dirs_tree.bind("<ButtonRelease-1>", self.on_tree_click)
    
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.selected_dir.set(directory)
            self.scan_directory(directory)
    
    def scan_directory(self, directory):
        # Limpar variáveis anteriores
        self.extensions = {}
        self.extension_vars = {}
        self.directory_structure = {}
        self.directory_vars = {}
        self.files_by_dir = {}
        
        # Limpar a TreeView
        for item in self.dirs_tree.get_children():
            self.dirs_tree.delete(item)
        
        # Limpar checkboxes de extensões
        for widget in self.check_ext_frame.winfo_children():
            widget.destroy()
        
        # Configurar colunas da TreeView
        self.dirs_tree["columns"] = ("include")
        self.dirs_tree.column("#0", width=300, minwidth=250)
        self.dirs_tree.column("include", width=60, minwidth=60, anchor=tk.CENTER)
        self.dirs_tree.heading("#0", text="Diretório")
        self.dirs_tree.heading("include", text="Incluir")
        
        # Adicionar diretório raiz
        self.root_dir = directory
        root_node = self.dirs_tree.insert("", "end", text=os.path.basename(directory), values=("✓",), open=True)
        self.directory_vars[""] = tk.BooleanVar(value=True)
        
        # Escanear diretórios e arquivos
        for root, dirs, files in os.walk(directory):
            rel_path = os.path.relpath(root, directory)
            if rel_path == ".":
                rel_path = ""
                parent = root_node
            else:
                # Encontrar o ID do nó pai
                parent_path = os.path.dirname(rel_path)
                if parent_path == "":
                    parent = root_node
                else:
                    parent_candidates = self.dirs_tree.get_children(root_node)
                    parent = self._find_parent_node(parent_candidates, parent_path)
                
                # Inserir este diretório na árvore
                dir_node = self.dirs_tree.insert(parent, "end", text=os.path.basename(root), values=("✓",))
                self.directory_vars[rel_path] = tk.BooleanVar(value=True)
            
            # Registrar arquivos
            if rel_path not in self.files_by_dir:
                self.files_by_dir[rel_path] = []
            
            for file in files:
                ext = Path(file).suffix.lower()
                if ext not in self.extensions:
                    self.extensions[ext] = True
                
                self.files_by_dir[rel_path].append((file, ext))
        
        # Criar checkboxes para extensões - agora com múltiplos por linha
        extensions_list = sorted(self.extensions.keys())
        col, row = 0, 0
        max_cols = 3  # Número máximo de extensões por linha
        
        for ext in extensions_list:
            if ext:  # Ignorar arquivos sem extensão
                var = tk.BooleanVar(value=True)
                self.extension_vars[ext] = var
                cb = ttk.Checkbutton(
                    self.check_ext_frame, 
                    text=f"{ext} ({self.count_extensions(ext)})", 
                    variable=var,
                    command=self.update_preview
                )
                cb.grid(row=row, column=col, sticky="w", padx=15, pady=2)
                
                col += 1
                if col >= max_cols:
                    col = 0
                    row += 1
        
        # Gerar prévia inicial
        self.update_preview()
    
    def _find_parent_node(self, nodes, path):
        """Função recursiva para encontrar o nó pai na árvore"""
        for node in nodes:
            node_text = self.dirs_tree.item(node, "text")
            if os.path.basename(path) == node_text:
                return node
            
            # Verificar filhos
            children = self.dirs_tree.get_children(node)
            if children:
                result = self._find_parent_node(children, path)
                if result:
                    return result
        return None
    
    def count_extensions(self, ext):
        count = 0
        for files_in_dir in self.files_by_dir.values():
            for file, file_ext in files_in_dir:
                if file_ext == ext:
                    count += 1
        return count
    
    def toggle_all_extensions(self):
        value = self.select_all_ext_var.get()
        for var in self.extension_vars.values():
            var.set(value)
        self.update_preview()
    
    def on_tree_click(self, event):
        """Tratamento para cliques na árvore - verifica se clicou na coluna checkbox"""
        region = self.dirs_tree.identify("region", event.x, event.y)
        if region != "cell":  # Se não clicou na célula (checkbox), ignorar
            return
            
        column = self.dirs_tree.identify_column(event.x)
        if column != "#1":  # A coluna do checkbox é #1
            return
            
        item = self.dirs_tree.identify("item", event.x, event.y)
        if not item:
            return
            
        # Toggle o valor do checkbox
        current_values = self.dirs_tree.item(item, "values")
        new_value = "✓" if current_values[0] != "✓" else "□"
        self.dirs_tree.item(item, values=(new_value,))
        
        # Update directory_vars para refletir a seleção
        self._update_path_selection(item, new_value == "✓")
        
        # Atualizar prévia
        self.update_preview()
    
    def _update_path_selection(self, item, selected):
        """Atualiza a seleção de uma pasta e suas subpastas"""
        # Atualizar a pasta atual
        path = self._get_full_path(item)
        if path in self.directory_vars:
            self.directory_vars[path].set(selected)
        
        # Atualizar todas as subpastas
        for child in self.dirs_tree.get_children(item):
            self.dirs_tree.item(child, values=("✓" if selected else "□",))
            self._update_path_selection(child, selected)
    
    def _get_full_path(self, item):
        """Obtém o caminho completo de um item da árvore"""
        if item == self.dirs_tree.get_children()[0]:  # Root
            return ""
        
        path_parts = []
        current = item
        
        while current != self.dirs_tree.get_children()[0]:
            path_parts.insert(0, self.dirs_tree.item(current, "text"))
            parent = self.dirs_tree.parent(current)
            current = parent
        
        return os.path.join(*path_parts) if path_parts else ""
    
    def build_directory_tree(self, selected_directories, files_by_dir, selected_extensions):
        """Constrói uma estrutura hierárquica dos diretórios e arquivos selecionados"""
        tree = {}
        for path in selected_directories:
            if not path:
                continue
            parts = path.split(os.path.sep)
            current = tree
            for part in parts:
                if part not in current:
                    current[part] = {}
                current = current[part]
        
        # Adicionar arquivos aos diretórios
        for path in selected_directories:
            if not path:
                continue
            parts = path.split(os.path.sep)
            current = tree
            for part in parts:
                current = current[part]
            if path in files_by_dir:
                files = [file for file, ext in files_by_dir[path] if ext in selected_extensions]
                current['files'] = sorted(files)
        
        # Arquivos do diretório raiz
        if "" in selected_directories and "" in files_by_dir:
            root_files = [file for file, ext in files_by_dir[""] if ext in selected_extensions]
            tree['files'] = sorted(root_files)
        
        return tree
    
    def _build_tree_paths(self, nested_tree, prefix="", is_last=True):
        """Constrói as linhas da árvore de diretórios e arquivos com riscos completos"""
        lines = []
        
        # Primeiro, processar subdiretórios
        subdirs = {k: v for k, v in nested_tree.items() if k != 'files'}
        items = sorted(subdirs.items())
        for i, (name, subtree) in enumerate(items):
            has_files = 'files' in nested_tree
            is_last_item = i == len(items) - 1 and not has_files
            connector = "└── " if is_last_item else "├── "
            lines.append(prefix + connector + name + "/")
            if subtree:
                extension = "    " if is_last_item else "│   "
                lines.extend(self._build_tree_paths(subtree, prefix + extension, is_last_item))
        
        # Depois, processar arquivos
        if 'files' in nested_tree:
            files = nested_tree['files']
            for i, file in enumerate(files):
                is_last_file = i == len(files) - 1
                connector = "└── " if is_last_file else "├── "
                lines.append(prefix + connector + file)
        
        return lines
    
    def _build_markdown_tree(self, nested_tree, prefix="", is_last=True):
        """Constrói as linhas da árvore em formato Markdown com riscos e ícones"""
        lines = []
        
        # Primeiro, processar subdiretórios
        subdirs = {k: v for k, v in nested_tree.items() if k != 'files'}
        items = sorted(subdirs.items())
        for i, (name, subtree) in enumerate(items):
            has_files = 'files' in nested_tree
            is_last_item = i == len(items) - 1 and not has_files
            connector = "└── " if is_last_item else "├── "
            lines.append(prefix + connector + "📁 " + name + "/")
            if subtree:
                extension = "    " if is_last_item else "│   "
                lines.extend(self._build_markdown_tree(subtree, prefix + extension, is_last_item))
        
        # Depois, processar arquivos
        if 'files' in nested_tree:
            files = nested_tree['files']
            for i, file in enumerate(files):
                is_last_file = i == len(files) - 1
                connector = "└── " if is_last_file else "├── "
                lines.append(prefix + connector + "📄 " + file)
        
        return lines
    
    def update_preview(self):
        """Atualiza a prévia da árvore com base nas seleções atuais"""
        # Limpar prévia
        self.preview_text.delete(1.0, tk.END)
        
        # Filtrar apenas extensões selecionadas
        selected_extensions = [ext for ext, var in self.extension_vars.items() if var.get()]
        
        # Preparar lista de diretórios selecionados
        selected_directories = []
        for path, var in self.directory_vars.items():
            if var.get():
                selected_directories.append(path)
        
        # Construir estrutura hierárquica dos diretórios e arquivos
        directory_tree = self.build_directory_tree(selected_directories, self.files_by_dir, selected_extensions)
        
        # Gerar as linhas da árvore
        root_name = os.path.basename(self.root_dir)
        tree_lines = [root_name + "/"] + self._build_tree_paths(directory_tree)
        
        # Adicionar números de linha à esquerda
        line_numbered_tree = []
        for i, line in enumerate(tree_lines, 1):
            line_numbered_tree.append(f"{i:4d} {line}")
        
        # Atualizar a prévia
        self.preview_text.insert(tk.END, "\n".join(line_numbered_tree))
    
    def generate_tree(self):
        if not self.selected_dir.get() or not self.files_by_dir:
            messagebox.showerror("Erro", "Por favor, selecione um diretório válido primeiro.")
            return
        
        # Perguntar onde salvar o arquivo
        output_file = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")],
            initialdir=self.selected_dir.get(),
            initialfile="directory_tree.txt",
            title="Salvar árvore de diretórios como"
        )
        
        if not output_file:
            return  # Usuário cancelou
        
        # Obter o conteúdo da prévia (com números de linha)
        preview_content = self.preview_text.get(1.0, tk.END)
        
        # Salvar arquivo
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(preview_content)
        
        # Mostrar resultado
        messagebox.showinfo("Sucesso", f"Árvore de diretório gerada em:\n{output_file}")
        
        # Abrir o arquivo para visualização
        try:
            os.startfile(output_file)
        except AttributeError:
            # Para sistemas que não têm startfile (Linux, Mac)
            import subprocess
            subprocess.call(('xdg-open', output_file))
    
    def generate_markdown(self):
        if not self.selected_dir.get() or not self.files_by_dir:
            messagebox.showerror("Erro", "Por favor, selecione um diretório válido primeiro.")
            return
        
        # Perguntar onde salvar o arquivo
        output_file = filedialog.asksaveasfilename(
            defaultextension=".md",
            filetypes=[("Arquivos Markdown", "*.md"), ("Todos os arquivos", "*.*")],
            initialdir=self.selected_dir.get(),
            initialfile="directory_tree.md",
            title="Salvar árvore de diretórios como Markdown"
        )
        
        if not output_file:
            return  # Usuário cancelou
        
        # Filtrar apenas extensões selecionadas
        selected_extensions = [ext for ext, var in self.extension_vars.items() if var.get()]
        
        # Preparar lista de diretórios selecionados
        selected_directories = []
        for path, var in self.directory_vars.items():
            if var.get():
                selected_directories.append(path)
        
        # Construir estrutura hierárquica dos diretórios e arquivos
        directory_tree = self.build_directory_tree(selected_directories, self.files_by_dir, selected_extensions)
        
        # Gerar as linhas da árvore em formato Markdown
        root_name = os.path.basename(self.root_dir)
        tree_lines = [f"# 📁 {root_name}/"] + self._build_markdown_tree(directory_tree)
        
        # Criar conteúdo Markdown
        markdown_content = "# Árvore de Diretórios\n\n" + "\n".join(tree_lines) + "\n"
        
        # Salvar arquivo
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        # Mostrar resultado
        messagebox.showinfo("Sucesso", f"Árvore de diretório em Markdown gerada em:\n{output_file}")
        
        # Abrir o arquivo para visualização
        try:
            os.startfile(output_file)
        except AttributeError:
            # Para sistemas que não têm startfile (Linux, Mac)
            import subprocess
            subprocess.call(('xdg-open', output_file))

if __name__ == "__main__":
    root = tk.Tk()
    app = FileTreeGenerator(root)
    root.mainloop()