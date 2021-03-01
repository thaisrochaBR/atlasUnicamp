#!/usr/bin/env python
# coding: utf-8
__file__
__version__ = '1.0'

import pandas as pd
import datetime
import os
import datetime  
from datetime import date 
import calendar 
import PIL
from PIL import Image
import glob


#rotina que redimensiona as imagens para 256x256 pixels
def redimensiona_images(diaini,diafim,ano):
    dia=diaini
    dia_fim=diafim
    ano = ano
    lstfiles=[]
    lstano=[]
    lstdia=[]
    lsthora=[]
    
    dirRaiz = 'imagesred'
    if not os.path.exists(dirRaiz):
        os.makedirs(dirRaiz)                 
        
    dirRaiz = 'imagesred/ch03'
    if not os.path.exists(dirRaiz):        
        os.makedirs(dirRaiz)     
        
    while dia<=dia_fim: 
        dia_pasta='%03d'%(dia)  
        for file in glob.glob("images/ch03/"+str(ano)+"/"+str(dia_pasta)+"/*.png"):
            if file.find(".png")>0:  
                dirRaiz = "imagesred/ch03/"+str(ano)
                if not os.path.exists(dirRaiz):
                    os.makedirs(dirRaiz)                 

                dirRaiz = "imagesred/ch03/"+str(ano)+"/"+str(dia_pasta)
                if not os.path.exists(dirRaiz):
                    os.makedirs(dirRaiz) 
                    
                filename = file
                try:
                    image = Image.open(filename)  
                    new_image = image.resize((255, 255), PIL.Image.ANTIALIAS)
                    newfilename=dirRaiz+'/'+(filename[-77:])                        
                    new_image.save(newfilename)
                    print('image save :'+newfilename) 
                except:
                    print('nao conseguiu abrir :'+filename)
                    pass
        dia+=1         
                
#rotina que carrega os dados do DAE, com vazao do rio e que le o valor da coluna "intervalo"
#depois criar:
# - duas novas colunas, com data e com hora da vazao medida
# - tres colunas, com categoria, faixa e diretorio
def format_dados_vazao_DAE(pArqCsv,agrup=10):
    
    data_dae=pd.read_csv(pArqCsv)
    data_dae=data_dae.dropna()
    
    #carrega a coluna intervalo, que tem data/hora da leitura da vazão. Ex: 2018-01-01 03:00:00 UTC
    lst_data=list(data_dae['intervalo'])
    lst_valor=list(data_dae['valor'])
    qtd = len(lst_data)
    num = 0
    lstdia=[]
    lsthora=[]
    lstano=[]
    lstdir=[]
    
    #faz um loop nos intervalos e separa o dia e a hora, e salva em uma lista
    while num<qtd:
        dia_ano = datetime.datetime(int(lst_data[num][:4]),int(lst_data[num][5:7]),int(lst_data[num][8:10])).strftime("%j")
        hora=lst_data[num][11:13]        
        ano=lst_data[num][0:4]
        lstano.append(str(ano))
        lstdia.append(str(dia_ano))
        lsthora.append(str(hora))
        valor = str(int(round(lst_valor[num],0)))        
        lstdir.append(int(valor))
        num+=1

    #com os dados carregados de data e hora, cria 2 colunas no dataframe do DAE    
    data_dae['ano']=lstano
    data_dae['dia_ano']=lstdia
    data_dae['hora']=lsthora    
    data_dae['categoria']=lstdir
    
    #verificar qual o diretorio que a imagem deve ser movida
    if agrup==10:
        vbins=list(range(0, 470, 10))
        vlabels=list(range(0, 460, 10))    
    elif agrup==5:
        vbins=list(range(0, 460, 5))
        vlabels=list(range(0, 455, 5))
        
    data_dae['diretorio'] = pd.cut(x=data_dae['categoria'],bins=vbins, labels=vlabels)
    data_dae['faixa'] = pd.cut(x=data_dae['categoria'], bins=vbins)    
    
    return data_dae

def gera_lista_arquivos_goes(ano1,dia1ini,dia1fim,ano2,dia2ini,dia2fim):
    dia=dia1ini
    dia_fim=dia1fim
    ano = ano1
    lstfiles=[]
    lstano=[]
    lstdia=[]
    lsthora=[]
    while dia<=dia_fim: 
        dia_pasta='%03d'%(dia)  
        
        #as imagens ja estao reduzidas de 2018 e 2019
        for file in glob.glob("imagesred/ch03/"+str(ano)+"/"+str(dia_pasta)+"/*.png"):
        #for file in glob.glob("images/ch03/"+str(ano)+"/"+str(dia_pasta)+"/*.png"):
            if file.find(".png")>0:  
                pos=file.find("s"+str(ano)+str(dia_pasta))            
                hora = file[int(pos)+8:int(pos)+8+2]            
                lstfiles.append(file) 
                lstano.append(str(ano))
                lstdia.append(str(dia_pasta))
                lsthora.append(str(hora))
        dia+=1    

    dia=dia2ini
    dia_fim=dia2fim
    ano = ano2
    while dia<=dia_fim:   
        dia_pasta='%03d'%(dia)        
        #as imagens ja estao reduzidas de 2018 e 2019
        for file in glob.glob("imagesred/ch03/"+str(ano)+"/"+str(dia_pasta)+"/*.png"):
            if file.find(".png")>0:
                pos=file.find("s"+str(ano)+str(dia_pasta))            
                hora = file[int(pos)+8:int(pos)+8+2]            
                lstfiles.append(file) 
                lstano.append(str(ano))
                lstdia.append(str(dia_pasta))
                lsthora.append(str(hora))
        dia+=1

    data_images=pd.DataFrame(data={'filename':lstfiles,'ano':lstano,'dia':lstdia,'hora':lsthora})
    return data_images

#une dados da lista de arquivos baixados do GOES com a lista de dados de vazao do DAE e gera um csv
def gera_csv_lista_dados_imagens_treinamento_rna(Dados_DAE_Posto, Dados_Imagens_GOES,SiglaPosto,tp_vazao,diamais=0,agrup=10):
    data_dae = Dados_DAE_Posto
    data_images = Dados_Imagens_GOES
    
    id_label=[]
    value_label=[]
    diretorio_img=[]
    faixa_img=[]

    for index, row in data_images.iterrows():
        dia = row['dia']        
        hora = row['hora']
        ano = row['ano']         
        
        if int(diamais)>=1:
            if int(dia)==365:
                dia = '001'
                ano = str(int(ano)+1)
            else:                
                dia=int(dia)+int(diamais)                
                dia='%03d'%(dia)
                dia=str(dia)
            
        #a imagem sera sempre das 12h
        if int(hora) == 12:
        
            if tp_vazao == '12':

                data_dae_1 = data_dae.loc[(data_dae['ano']==str(ano))&(data_dae['dia_ano']==str(dia))&(data_dae['hora']==str(hora))]
                found=int(data_dae_1['hora'].count())
                if found>0:  
                    valor = data_dae_1['valor'].values[0]
                    diretorio = data_dae_1['diretorio'].values[0]
                    faixa = data_dae_1['faixa'].values[0]

                    id_label.append(row['filename'])
                    value_label.append(str(valor))        
                    diretorio_img.append(str(diretorio))
                    faixa_img.append(str(faixa))
                else:
                    #se nao tiver vazao as 12, procurar as primeira vazao depois das 12 
                    data_dae_1 = data_dae.loc[(data_dae['ano']==str(ano))&(data_dae['dia_ano']==str(dia))&(data_dae['hora']>=str(hora))].sort_values('hora')
                    found=int(data_dae_1['hora'].count())
                    if found>0:                     
                        valor = data_dae_1['valor'].values[0]
                        diretorio = data_dae_1['diretorio'].values[0]
                        faixa = data_dae_1['faixa'].values[0]

                        id_label.append(row['filename'])
                        value_label.append(str(valor))        
                        diretorio_img.append(str(diretorio))
                        faixa_img.append(str(faixa))
                    else:
                        #se nao tiver vazao as 12, procurar as primeira vazao depois das 12 , senao achar, procurar a primeira vazao do dia
                        data_dae_1 = data_dae.loc[(data_dae['ano']==str(ano))&(data_dae['dia_ano']==str(dia))].sort_values('hora')
                        found=int(data_dae_1['hora'].count())
                        if found>0:                     
                            valor = data_dae_1['valor'].values[0]
                            diretorio = data_dae_1['diretorio'].values[0]
                            faixa = data_dae_1['faixa'].values[0]

                            id_label.append(row['filename'])
                            value_label.append(str(valor))        
                            diretorio_img.append(str(diretorio))
                            faixa_img.append(str(faixa))                    
                        

            elif tp_vazao == 'media':

                #nao filtra por hora, só por ano e dia

                data_dae_1 = data_dae.loc[(data_dae['ano']==str(ano))&(data_dae['dia_ano']==str(dia))]            
                found=int(data_dae_1['hora'].count())

                if found>0:  
                    #calcula a média
                    media_val=(data_dae_1['diretorio'].values.max()+data_dae_1['diretorio'].values.min())/2

                    if agrup==10:
                        vbins=list(range(0, 470, 10))
                        vlabels=list(range(0, 460, 10))    
                    elif agrup==5:
                        vbins=list(range(0, 460, 5))
                        vlabels=list(range(0, 455, 5))

                    vazao=[]
                    vazao.append(media_val)
                    diretorio=[]
                    diretorio = pd.cut(x=vazao,bins=vbins, labels=vlabels)                

                    valor = data_dae_1['valor'].values[0]
                    diretorio = diretorio[0]
                    faixa = data_dae_1['faixa'].values[0]

                    id_label.append(row['filename'])
                    value_label.append(str(valor))        
                    diretorio_img.append(str(diretorio))
                    faixa_img.append(str(faixa))

            

    data_labels=pd.DataFrame(data={'filename':id_label
                                   ,'valor_vazao':value_label
                                   ,'diretorio':diretorio_img
                                   ,'faixa':faixa_img
                                  })   
    data_labels.to_csv("data_train_rna_"+str(SiglaPosto)+".csv")
    print('gerado arquivo :'+ "data_train_rna_"+str(SiglaPosto)+".csv")
    return data_labels, "data_train_rna_"+str(SiglaPosto)+".csv"

#funcao para redimensionar arquivos para 255x255 pixels e 
#mover em diretorios conforme o valor de vazao
def redimensiona_images_move_diretorio_digits(Csv_Train_Rna,SiglaPosto):
    data_labels=pd.read_csv(Csv_Train_Rna)
    listafile=[]
    listvalue=[]
    listdirName=[]
    dirRaiz = SiglaPosto
    
    #criar diretorio Raiz caso nao exista
    if not os.path.exists(dirRaiz):
        os.makedirs(dirRaiz)  

    for index, row in data_labels.iterrows():
        
        filename=row['filename']
        valor=row['valor_vazao']     
        dirName=str(row['diretorio'])
        listdirName.append(dirName)
        if not os.path.exists(dirRaiz+"/"+dirName):        
            os.makedirs(dirRaiz+"/"+dirName)
            print(str(dirRaiz+"/"+dirName))

        image = Image.open(filename)  
        
        #as imagens ja foram redimensionadas, antes pela funcao ()
        #new_image = image.resize((255, 255), PIL.Image.ANTIALIAS)
        new_image = image
        
        newfilename=dirRaiz+"/"+dirName+'/'+(filename[-77:])        
        new_image.save(newfilename)
        print('image save :'+newfilename)
        listafile.append(newfilename)    
        listvalue.append(valor)

    data_labels=pd.DataFrame(data={'id':listafile,'label':listvalue})   
    data_labels.to_csv("data_label_train_resize_"+dirRaiz+".csv")
    print("gerado arquivo: data_label_train_resize_"+dirRaiz+".csv")
    #print("redimensionar/mover arquivos finalizado!!")
    print("mover arquivos finalizado!!")

          
def findDay(date): 
    day, month, year = (int(i) for i in date.split(' '))     
    born = datetime.date(year, month, day) 
    return born.strftime("%j") #day of year  

	
def main():

    parser = argparse.ArgumentParser(
        description='This is a Unicamp App Merge Img Inflow - Resize and Merge Inflow Values script by Thais Rocha. (Errors are not yet logged.)',
        prog='app-merge-img-inflow',
        formatter_class=SmartFormatter)

    parser.add_argument('-y','--year',                
        help='The year format(2020)',
		type=int)
    parser.add_argument('-c','--csv',                
        help='File name csv (name.csv)',
		type=int)		
    parser.add_argument('-a','--acronym',
        type=int,        
        help='name folder, acronym station (FSB_10_media_m1)')
    parser.add_argument('-g','--group',                
        help='media, 12h')

    args = parser.parse_args()

    if len(args) != 3:
        parser.error("error - not found arguments - [-y, -c, -g] abort run")
	else:
        getimage(args.year, args.startday, hour, args.outputpath, args.channel, args.crop)
			
		data_dae = format_dados_vazao_DAE(args.csv,5)
		data_images = gera_lista_arquivos_goes(args.year,1,2,args.year,3,365)
		data_train,nome_csv = gera_csv_lista_dados_imagens_treinamento_rna(data_dae, data_images,args.acronym,args.group,1,365)		
		
		#agrupar os diretorios 
		data_train['diretorio']=data_train['diretorio'].astype(int)
		
		data_train.to_csv(nome_csv)		
		redimensiona_images_move_diretorio_digits(nome_csv,args.acronym)		
		
        print("Done.")
		
main()		