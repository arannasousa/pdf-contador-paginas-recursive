# coding=utf-8
__author__ = 'Aranna'

def geraTarefas(numero_tarefas, funcao):
	"""
	Gera tasks para execucao de uma funcao
	"""
	#---------------------------------------------------------------
	#	cria Threads para executar a tarefa
	#---------------------------------------------------------------
	from threading import Thread
	from Queue import Queue

	class myThread (Thread):
		def __init__(self, tarefa, funcao):
			Thread.__init__(self)
			self.tarefa = tarefa
			self.funcao = funcao
		def run(self):
			self.funcao(self.tarefa)

	#	configura o numero de TAREFAS
	tarefas = Queue(numero_tarefas)
	for i in range(numero_tarefas):
		t = myThread(tarefas, funcao)
		#Thread(target=worker, name=i)
		t.daemon = True
		t.start()

	return tarefas