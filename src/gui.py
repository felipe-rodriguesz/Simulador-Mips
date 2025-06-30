import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

from mips_state import REGISTER_NAMES, NUM_REGISTERS

class SimulatorGUI:
    def __init__(self, simulator):
        self.simulator = simulator
        self.state = simulator.state

        # --- Configuração da Janela Principal ---
        self.window = Gtk.Window(title="Simulador MIPS em Python")
        self.window.set_default_size(1000, 700)
        self.window.connect("destroy", Gtk.main_quit) # Garante que o programa feche corretamente

        # --- Layout Principal (Painel Dividido Horizontalmente) ---
        paned = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        self.window.add(paned)

        # --- Painel Esquerdo (Registradores) ---
        left_panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5, margin=5)
        paned.add1(left_panel)
        
        reg_frame = Gtk.Frame(label="Registradores")
        scrolled_reg = Gtk.ScrolledWindow()
        scrolled_reg.set_hexpand(True)
        scrolled_reg.set_vexpand(True)
        self.registers_view = Gtk.TextView()
        self.registers_view.set_editable(False) # O usuário não pode editar os registradores diretamente
        self.registers_buffer = self.registers_view.get_buffer()
        scrolled_reg.add(self.registers_view)
        reg_frame.add(scrolled_reg)
        left_panel.pack_start(reg_frame, True, True, 0)

        # --- Painel Direito ---
        right_panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10, margin=5)
        paned.add2(right_panel)

        # Painel para Instruções Executadas
        inst_frame = Gtk.Frame(label="Instruções Executadas")
        scrolled_inst = Gtk.ScrolledWindow()
        scrolled_inst.set_hexpand(True)
        scrolled_inst.set_vexpand(True)
        self.instructions_view = Gtk.TextView()
        self.instructions_view.set_editable(False)
        self.instructions_buffer = self.instructions_view.get_buffer()
        scrolled_inst.add(self.instructions_view)
        inst_frame.add(scrolled_inst)
        right_panel.pack_start(inst_frame, True, True, 0)
        
        # Label para Código Binário
        self.binary_label = Gtk.Label(label="Binário: (ainda não executado)")
        self.binary_label.set_halign(Gtk.Align.START)
        right_panel.pack_start(self.binary_label, False, False, 0)

        # Painel para Saída de Syscalls
        output_frame = Gtk.Frame(label="Saída do Programa (Syscall)")
        scrolled_output = Gtk.ScrolledWindow()
        scrolled_output.set_hexpand(True)
        scrolled_output.set_vexpand(True)
        self.output_view = Gtk.TextView()
        self.output_view.set_editable(False)
        self.output_buffer = self.output_view.get_buffer()
        scrolled_output.add(self.output_view)
        output_frame.add(scrolled_output)
        right_panel.pack_start(output_frame, True, True, 0)

        # --- Botões de Controle ---
        button_box = Gtk.ButtonBox(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        button_box.set_layout(Gtk.ButtonBoxStyle.EXPAND)
        right_panel.pack_start(button_box, False, False, 0)
        
        btn_next = Gtk.Button(label="Próxima Instrução")
        btn_next.connect("clicked", self.on_next_clicked)
        button_box.pack_start(btn_next, True, True, 0)
        
        btn_run = Gtk.Button(label="Executar Tudo")
        btn_run.connect("clicked", self.on_run_all_clicked)
        button_box.pack_start(btn_run, True, True, 0)

        btn_exit = Gtk.Button(label="Sair")
        btn_exit.connect("clicked", Gtk.main_quit)
        button_box.pack_start(btn_exit, True, True, 0)
        
        # Atualiza a UI para o estado inicial antes de mostrar a janela.
        self.update_ui()

    def run(self):
        """Inicia a GUI e o loop principal de eventos do GTK."""
        self.window.show_all()
        Gtk.main()

    def update_ui(self, executed_pc=None):
        """Atualiza todos os componentes visuais com os dados do MIPSState."""
        # Atualiza o painel de registradores
        self.registers_buffer.set_text("")
        for i in range(NUM_REGISTERS):
            val = self.state.registers[i]
            line = f"{REGISTER_NAMES[i]:<6}: 0x{val:08X} ({val})\n"
            self.registers_buffer.insert_at_cursor(line)
        
        # Atualiza os painéis da direita (apenas se uma instrução foi executada)
        if executed_pc is not None:
            info = self.state.instruction_info.get(executed_pc)
            if not info: return # Proteção caso não haja info para o PC

            # Atualiza o label do código binário
            binary_val = info.get('binary', 0)
            self.binary_label.set_text(f"Binário: {binary_val:032b}")
            
            # Adiciona a instrução à lista de executadas
            inst_text = info.get('text', 'Instrução desconhecida')
            line = f"PC {executed_pc}: {inst_text}\n" # Usa o PC correto que foi passado
            
            # Insere a nova linha sempre no final do buffer de texto
            end_iter = self.instructions_buffer.get_end_iter()
            self.instructions_buffer.insert(end_iter, line)

            # Adiciona a saída de uma syscall, se houver
            output_text = info.get('output', '')
            if output_text:
                output_end_iter = self.output_buffer.get_end_iter()
                self.output_buffer.insert(output_end_iter, output_text)

    def on_next_clicked(self, widget):
        """Callback para o botão 'Próxima Instrução' (execução passo a passo)"""
        executed_pc = self.simulator.execute_instruction()
        if executed_pc is not None:
            self.update_ui(executed_pc) # Passa o PC que foi executado para a UI
        else:
            self.binary_label.set_text("Fim da execução.")

    def on_run_all_clicked(self, widget):
        """Callback para o botão 'Executar Tudo' (execução automática)"""
        # Usa GLib.idle_add para não congelar a interface durante a execução do loop
        def run_step():
            executed_pc = self.simulator.execute_instruction()
            if executed_pc is not None:
                self.update_ui(executed_pc)
                return True # Diz ao GLib para chamar esta função novamente
            else:
                self.binary_label.set_text("Fim da execução.")
                return False # Diz ao GLib para parar de chamar a função
        
        GLib.idle_add(run_step)