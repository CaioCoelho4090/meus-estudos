class GerenciadorDeTarefas:
    def __init__(self):
        self.tarefas = []
        print("Gerenciador de Tarefas iniciado")
        
    def adicionar_tarefas(self, descricao):
        nova_tarefa = {
            "Descrição": descricao,
            "Concluida": False
        }
        self.tarefas.append(nova_tarefa)
        print(f"Tarefa '{descricao}' adicionada!")
    
    def listar_tarefas(self):
        print("\n--- Lista de Tarefas ---")
        if not self.tarefas:
            print("Nenhuma tarefa encontrada")
            return
        for i, tarefa in enumerate(self.tarefas):
            status = "[X]" if tarefa["Concluida"] else "[ ]"
            print(f"{i + 1}. {status} {tarefa['Descrição']}")
    
    def marcar_como_concluida(self, descricao):
        for tarefa in self.tarefas:
            if tarefa["Descrição"] == descricao:
                tarefa["Concluida"] = True
                print(f"Tarefa '{descricao}' marcada como concluida")
                return
        print(f"Erro: Tarefa '{descricao}' não encontrada!")
        
    def remover_tarefa(self, descricao):
        for tarefa in self.tarefas:
            if tarefa["Descrição"] == descricao:
                self.tarefas.remove(tarefa)
                print(f"Tarefa '{descricao}' removida")
                return
            
        print(f"Erro: Tarefa '{descricao}' não encontrada!")

print("Criando um novo gerenciador de tarefas...")
gerenciador = GerenciadorDeTarefas()

gerenciador.adicionar_tarefas("Estudar Python")
gerenciador.adicionar_tarefas("Ir à academia")
gerenciador.adicionar_tarefas("Ir à faculdade")
gerenciador.adicionar_tarefas("Fazer o trabalho")

gerenciador.listar_tarefas()
gerenciador.marcar_como_concluida("Estudar Python")
gerenciador.listar_tarefas()