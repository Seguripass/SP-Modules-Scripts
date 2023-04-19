##!/usr/bin/python
import sys
from escpos.printer import usb
from escpos import  printer
from datetime import datetime
import string
import qrcode



#////////////////////////////////////////////////////////
#Seleccionar Impresora

brand = "Marca patito"
model = "Modelo pato"
dir_logo = " "
#termal_printer = printer.Usb(0x0519, 0x003D)
termal_printer = printer.Usb(0x0483, 0x5743)

#////////////////////////////////////////////////////////
termal_printer.text("\n")

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



def printQR():
    global dir_logo
    termal_printer.set("center", "B", 'normal', 1, 1)
    #termal_printer.image(dir_logo + 'QRTicket.png')
    termal_printer.image('QRTicket.png')
    
def semistatic_line(line,termal_printer,argv):
    #termal_printer.set("left", "B", 'normal',1, 1)
    #termal_printer.set("center", "B", 'B', 2, 2)
    #or line.find('Importe') == 0 or line.find('Cambio') == 0
    data = ''
    if line.find('Total') == 0 :
        termal_printer.set("left", "B", 'B',2, 2)
    else:
        termal_printer.set("left", "B", 'normal',1, 1)
    
    if line.find('Folio') == 0 :
        data = argv[0]
        #termal_printer.text(line+data+'\n')
    elif line.find('Entrada') == 0 :
        data = argv[1] +' '+ argv[2]
        #termal_printer.text(line+data+'\n')
    elif line.find('Salida') == 0 :
        data = argv[3] +' '+ argv[4]
        #termal_printer.text(line+data+'\n')
    elif line.find('Estancia') == 0 :
        #entrada = '27/02/2015 13:33:26'
        #salida = '28/02/2019 15:38:29' # for example
        entrada = argv[1] +' '+ argv[2]
        salida = argv[3] +' '+ argv[4]
        FMT = '%d/%m/%Y %H:%M:%S'
        tdelta = datetime.strptime(salida, FMT) - datetime.strptime(entrada, FMT)
        data = str(tdelta)
        if data.find('days') > 0:
            data = string.replace(data, 'days', 'dias')
        elif data.find('day') > 0:
            data = string.replace(data, 'day', 'dia')
        #termal_printer.text(line+data+'\n')
    elif line.find('Total') == 0 :
        data = argv[5]
        #termal_printer.text(line+data+'\n')
    elif line.find('Importe') == 0 :
        data = argv[6]
        #termal_printer.text(line+data+'\n')
    elif line.find('Cambio') == 0 :
        #data = str(float(argv[6]) - float(argv[5]))
        data = argv[7]
        #termal_printer.text(line+data+'\n')
    elif line.find('Tolerancia Salida') == 0 :
        #data = str(float(argv[6]) - float(argv[5]))
        data = argv[8]+"min"

    
    if line.find('Folio') == 0 :
        #termal_printer.barcode('1324354657687', 'EAN13', 64, 2, '', '')
        #Escpos.barcode(code, bc, height=64, width=3, pos='BELOW', font='A', align_ct=True, function_type=None, check=True
        termal_printer.barcode(argv[0], 'EAN13', 64, 3, 'BELOW', 'A')#,True,'B',True)
        #termal_printer.barcode("{B012ABCDabcd", "CODE128", 64,3,'BELOW','A',function_type='B')
        termal_printer.text ('\n')
        printQR()
    else:
        termal_printer.text(line+' '+data+'\n')
    
    print line
    
    
def dynamic_line(line,termal_printer):
    termal_printer.set("center", "B", 'normal', 1, 1)
    termal_printer.text(line+'\n')
    print line
    
def print_logo(logo_name,termal_printer):
    global dir_logo
    termal_printer.set("center", "B", 'normal', 1, 1)
    termal_printer.image(dir_logo + logo_name)

def bank_logo(bank,termal_printer):
    termal_printer.bank_logo(int(bank))

def info_line(line,termal_printer):
    termal_printer.set("center", "A", 'normal', 1, 1)
    termal_printer.text(line+'\n')
    print line

def main(argv):
    
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=7,
        border=4,
    )
    qr.add_data(argv[0])
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    #img = qrcode.make (argv[0])
    type(img)
    img.save('QRTicket.png')
    
    try:
        # Open a file
        fo = open('/home/pi/En_ticket.txt', 'r')
        lines = fo.readlines()
        list_lines = [i.strip() for i in lines]
        for x in range(0,len(list_lines)): 
            check_cmd(list_lines[x],termal_printer,argv)
        # Close opend file
        fo.close()
        termal_printer.cut()
	print('Impresion OK')
    except Exception, e:
        print('Exception!')
        print(e)

#Funcion principal
if __name__ == "__main__":
    main(sys.argv[1:])
