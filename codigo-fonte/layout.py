# coding=utf-8
__author__ = 'JPINHEIRO'
from fpdf import FPDF
import datetime

def gerarPDF(qtd_img, Tamanho, qtd_Arq, diretorio):

	pdf = FPDF(orientation='P', format='A4', unit=u'mm')


	pdf.set_font(u'Arial', size=18)
	pdf.set_line_width(0.1)
	#   evita quebra automatica da pagina, ao chegar perto da borda inferior
	pdf.set_auto_page_break(False)

	pdf.set_margins(8, 8)
	pdf.add_page()

	pdf.text(60, 50, txt=u'Relatório de Contagem de Imagens')
	pdf.ln("")
	pdf.set_font_size(size=10)
	pdf.text(10, 60, txt=u'Total de Imagens = %s' %qtd_img)
	pdf.text(80, 60, txt=u'Espaço Ocupado = %s' %Tamanho)
	pdf.text(150, 60, txt=u'Total de Arquivos = %s' %qtd_Arq)

	pdf.text(10, 70, txt=u'Data = %s às %s' %(datetime.datetime.now().date().__format__(u'%d/%m/%Y'), datetime.datetime.now().time().__format__(u'%H:%M:%S')))
	pdf.ln("")
	pdf.text(10, 80, txt=u'Diretório Raiz= %s' %diretorio)

	pdf.output(u'./relatório.pdf', u'F')

# gerarPDF(0,0,0,0)