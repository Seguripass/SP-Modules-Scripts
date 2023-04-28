##!/usr/bin/python
import sys
from escpos.printer import usb
from escpos import  printer
from datetime import datetime
import string
import qrcode
import time



#////////////////////////////////////////////////////////
#Seleccionar Impresora

brand = "Marca patito"
model = "Modelo pato"
dir_logo = " "
#termal_printer = printer.Usb(0x0519, 0x003D)
#termal_printer = printer.Usb(0x0483, 0x5743, in_ep=0x81, out_ep=0x01)
#termal_printer = printer.Usb(0x0dd4, 0x01ad, in_ep=0x81, out_ep=0x02)
#termal_printer = printer.Usb(0x0483, 0x5743, in_ep=0x81, out_ep=0x01)
#////////////////////////////////////////////////////////

def check_cmd(line,termal_printer,argv):
    if line.find('-') == 0:
        line = line.strip('-')
        semistatic_line(line,termal_printer,argv)
    
    elif line.find('*') == 0:
        line = line.strip('*')
        dynamic_line(line,termal_printer)
        
    elif line.find('#') == 0:
        line = line.strip('#')
        print_logo(line,termal_printer)
    
    elif line.find('$') == 0:
        line = line.strip('$')
        bank_logo(line,termal_printer)
    
    elif line.find('^!') == 0:
        line = line.strip('^!')
        info_line(line,termal_printer)



def printQR(termal_printer):
    global dir_logo
    termal_printer.set (align='center', font='a', bold=False, underline=0, width=1, height=1)
    # Version 2.0 termal_printer.set("center", "B", 'normal', 1, 1)
    termal_printer.image('QRTicket.png')
    
def semistatic_line(line,termal_printer,argv):
    #termal_printer.set("left", "B", 'normal',1, 1)
    #termal_printer.set("center", "B", 'B', 2, 2)
    #or line.find('Importe') == 0 or line.find('Cambio') == 0
    data = ''
    if line.find('Total') == 0 :
        termal_printer.set (align='left', font='b', bold=False, underline=0, width=2, height=2)
        # Versio 2.0 termal_printer.set("left", "B", 'B',2, 2)
    else:
        termal_printer.set (align='left', font='b', bold=False, underline=0, width=1, height=1)
        # Versio 2.0 termal_printer.set("left", "B", 'normal',1, 1)
    
    if line.find('Barcode') == 0 :
        data = argv[0+2]
        #termal_printer.text(line+data+'\n')
    elif line.find('Entrada') == 0 :
        data = argv[1+2] +' '+ argv[2+2]
        #termal_printer.text(line+data+'\n')
    elif line.find('Salida') == 0 :
        data = argv[3+2] +' '+ argv[4+2]
        #termal_printer.text(line+data+'\n')
    elif line.find('Estancia') == 0 :
        #entrada = '27/02/2015 13:33:26'
        #salida = '28/02/2019 15:38:29' # for example
        entrada = argv[1+2] +' '+ argv[2+2]
        salida = argv[3+2] +' '+ argv[4+2]
        FMT = '%d/%m/%Y %H:%M:%S'
        tdelta = datetime.strptime(salida, FMT) - datetime.strptime(entrada, FMT)
        data = str(tdelta)
        if data.find('days') > 0:
            data = string.replace(data, 'days', 'dias')
        elif data.find('day') > 0:
            data = string.replace(data, 'day', 'dia')
        #termal_printer.text(line+data+'\n')
    elif line.find('Total') == 0 :
        data = argv[5+2]
        #termal_printer.text(line+data+'\n')
    elif line.find('Importe') == 0 :
        data = argv[6+2]
        #termal_printer.text(line+data+'\n')
    elif line.find('Cambio') == 0 :
        #data = str(float(argv[6]) - float(argv[5]))
        data = argv[7+2]
        #termal_printer.text(line+data+'\n')
    elif line.find('Tolerancia Salida') == 0 :
        #data = str(float(argv[6]) - float(argv[5]))
        data = argv[8+2]+"min"
    elif line.find('Modulo y Folio') == 0 :
        #data = str(float(argv[6]) - float(argv[5]))
        data = (argv[0+2][18:21]) +', '+ (argv[0+2][21:29])
    elif line.find('TiT, RTE y OPB') == 0 :
    #data = str(float(argv[6]) - float(argv[5]))
        data = (argv[9+2])+', '+ (argv[10+2])+', '+ (argv[11+2])
    #elif line.find('Folio') == 0 :
        #data = str(float(argv[6]) - float(argv[5]))
     #   data = (argv[0][21:29])
    elif line.find('Modulo') == 0 :
        data = argv[1+1]
    elif line.find('TiT') == 0 :
        data = argv[2+1] 
    elif line.find('RTE') == 0 :
        data = argv[3+1] 
    elif line.find('OPB') == 0 :
        data = argv[4+1] 
        
   
    
    if line.find('Barcode') == 0 :
        #termal_printer.barcode("{B012ABCDabcd", "CODE128", 64,3,'BELOW','A',function_type='B')
        #termal_printer.barcode(argv[0], 'CODE128', 64, 3, 'BELOW', 'A')#,True,'B',True)
        #termal_printer.barcode("{B01221105144526123400606A98F8612345678901A00040000", "CODE128", 64,3,'BELOW','A',function_type='B')
         termal_printer.barcode("{B01221105144526123400606", "CODE128", 64,2,'BELOW','B',function_type='B')

    elif line.find ('QR') == 0:
        printQR(termal_printer)
    else:
        termal_printer.text(line+' '+data+'\n')
    print (line)
    
    
def dynamic_line(line,termal_printer):
    termal_printer.set (align='center', font='b', bold=False, underline=0, width=1, height=1)
    # Versio 2.0 termal_printer.set("center", "B", 'normal', 1, 1)
    termal_printer.text(line+'\n')
    print (line)
    
def print_logo(logo_name,termal_printer):
    global dir_logo
    termal_printer.set (align='center', font='b', bold=False, underline=0, width=1, height=1)
    # Versio 2.0 termal_printer.set("center", "B", 'normal', 1, 1)
    termal_printer.image(dir_logo + logo_name)

def bank_logo(bank,termal_printer):
    termal_printer.bank_logo(int(bank))

def info_line(line,termal_printer):
    termal_printer.set (align='center', font='a', bold=False, underline=0, width=1, height=1)
    # Versio 2.0 termal_printer.set("center", "A", 'normal', 1, 1)
    termal_printer.text(line+'\n')
    print (line)

def main(argv):
    
    if argv[0] == "0":
        #Ticket de Entrada
        fo = open('/home/pi/En_ticket.txt', 'r')
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=8,
            border=4,
        )
        qr.add_data(argv[0+2])
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        #img = qrcode.make (argv[0])
        type(img)
        img.save('QRTicket.png')
        
    elif argv[0] == "1":
        #Ticket de EStadisticas
        fo = open('/home/pi/EM_Statistics.txt', 'r')
        
    if argv[1] == "1":
        #Impresora TS-80
        termal_printer = printer.Usb(0x0483, 0x5743, in_ep=0x81, out_ep=0x01)
        
    elif argv[1] == "2":
        #Impresora TS-80F
        termal_printer = printer.Usb(0x0483,0x5743, in_ep = 0x082, out_ep = 0x01);
    
    try:
        # Open a file
#         if termal_printer.paper_status():
        if argv[1] != "1" and argv[1] != "2":
            print('Error')
        elif argv[0] == "2":
            status = termal_printer.paper_status()
            if status == 2:
                print('IM OK')
            elif status == 1:
                print('Paper NearEnd')
            elif status == 0:
                print('Paper NOK')
        else:
            #fo = open('/home/pi/En_ticket.txt', 'r')
            lines = fo.readlines()
            list_lines = [i.strip() for i in lines]
            for x in range(0,len(list_lines)):
                check_cmd(list_lines[x],termal_printer,argv)
            # Close opend file
            fo.close()
            termal_printer.cut()
            time.sleep(1)
            status = termal_printer.paper_status()
            if status == 2:
                print('Print OK')
            elif status == 1:
                print('Paper NearEnd')
            elif status == 0:
                print('Paper NOK')
        #else:
            #print('Paper NOK')
    except Exception as e:
        print('Exception!')
        print(e)

#Funcion principal
if __name__ == "__main__":
    main(sys.argv[1:])

