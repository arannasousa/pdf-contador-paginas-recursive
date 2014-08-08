# coding=utf-8
from traceback import format_exc
from pyPdf import PdfFileReader
import os, datetime, re, readline, glob
from geradorTarefa import geraTarefas
from layout import gerarPDF


def complete(text, state):
	return (glob.glob(text+'*')+[None])[state]

readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab: complete")
readline.set_completer(complete)

DIRETORIO = raw_input(u'Digite o caminho da pasta onde contem os arquivos (Ex.: c:\pdfs\)\n: ')
while not DIRETORIO:
	DIRETORIO = raw_input(u'Digite o caminho da pasta onde contem os arquivos (Ex.: c:\pdfs\)\n: ')

arquivos = [os.path.join(dp, f) for dp, dn, filenames in os.walk(DIRETORIO) for f in filenames if os.path.splitext(f)[1] == u'.pdf']

N_THREADS = 4
TOTAL_IMAGEM = 0
TOTAL_MB = 0
MARGEM_ESQUERDA = 8
MARGEM_SUPERIOR = 8

if not arquivos:
	print u'Nenhum arquivo PDF foi encontrado'
	raw_input(u'Pressione qualquer tecla para encerrar')
	exit(0)
	
if len(arquivos) < N_THREADS:
	N_THREADS = len(arquivos)

try:
	logArquivo = open(u'./logs.log', u'w')
	erroArquivo = open(u'./erros.log', u'w')
	erroPdfs = open(u'./pdfsErros.log', u'w')

	def log(texto):
		try:
			logArquivo.write(unicode(texto+ u'\n').encode(u'utf-8'))
		except:
			print format_exc()

	def contaPaginas(tarefa):
		while True:
			FILE_PDF = tarefa.get()
			if not FILE_PDF:
				break
			#---------------------------------------
			try:
				global TOTAL_IMAGEM
				global TOTAL_MB
				global log
				global erroArquivo

				with open(FILE_PDF, u'rb') as arquivo:
					print unicode(u"abrindo arquivo %s \n"%(b'%s'%FILE_PDF).decode(u"ascii", u"ignore")).encode(u'utf-8', u'ignore')
					pdf = PdfFileReader( arquivo )
					pagina = pdf.getNumPages()
					del pdf
					log('%s = %s'%(pagina, (b'%s'%FILE_PDF).decode(u"ascii", u"ignore") ) )

					TOTAL_IMAGEM += pagina
					TOTAL_MB += os.path.getsize(FILE_PDF)

			except:
				print format_exc()
				erroPdfs.write( unicode(u'%s\n'%FILE_PDF).encode(u'utf-8', u'ignore'))
				erroArquivo.write( format_exc() )

			tarefa.task_done()

	tarefas = geraTarefas(N_THREADS, contaPaginas)

	print u'Executando'
	for PDF in arquivos:
		tarefas.put(PDF)
	print u'Aguardando concluir...'
	#	aguarda todas as tarefas terminarem
	tarefas.join()       # block until all tasks are done
	print u'Concluído!'
	print u'Total de imagens: %s'%(TOTAL_IMAGEM)
	log(u'Total de imagens: %s'%(TOTAL_IMAGEM) )

	TOTAL_MB /= 1048576
	TOTAL_MB = u'%s MB' % TOTAL_MB

	print u'Tamanho Total em disco: %s'%(TOTAL_MB)
	log(u'Tamanho Total em disco: %s'%(TOTAL_MB))
	gerarPDF(TOTAL_IMAGEM, TOTAL_MB, len(arquivos), DIRETORIO)

	logArquivo.close()
	erroArquivo.close()
	erroPdfs.close()
	raw_input(u'Pressione qualquer tecla para encerrar')
except:
	print format_exc() 
	raw_input(u'Pressione qualquer tecla para encerrar')