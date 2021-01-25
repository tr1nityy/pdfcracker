import PyPDF2 as pdf
import os
from time import sleep
from sys import exit


def parse_file(file):
    source_dir = os.path.dirname(__file__)

    try:
        if file.startswith('~'):
            file = os.path.expanduser(file)

        if file.endswith('.txt'):
            if source_dir == '':
                textfile = open(os.path.join(os.getcwd(), file), 'r')
            else:
                textfile = open(os.path.join(source_dir + '/passwords', file), 'r')

            print('[*] Selected ' + os.path.basename(file))

            return textfile

        elif file.endswith('.pdf'):
            pdf_file = pdf.PdfFileReader(open(os.path.join(source_dir, file), 'rb'))
            print('[!] Selected ' + os.path.basename(file))

            return pdf_file
        else:
            return None
    except FileNotFoundError:
        print('[!] File not found error.')
        exit(1)



def crackpdf(wordlist, pdf_file): 
    print('\n[*] Initializing the attack [*]')

    pdfWriter = pdf.PdfFileWriter()

    for password in wordlist.read().split():
        if pdf_file.decrypt(password) == 0:
            print('Tried: ' + password)

        elif pdf_file.decrypt(password) == 1:
            print('\n[!] PASSWORD FOUND: ' + password + ' [!]')
            autoDecryption = input('Decrypt the file? [Y/N]:').lower()

            if autoDecryption == 'y' or autoDecryption == 'yes':
                decrypted = open(os.path.join(os.path.expanduser('~'), 'decrypted.pdf'), 'wb')

                for pages in range(pdf_file.numPages):
                    pdfWriter.addPage(pdf_file.getPage(pages))
                    pdfWriter.write(decrypted)

                decrypted.close()
                print('[*] File decrypted successfully and saved as ~/decrypted.pdf [*]')
                exit()

            elif autoDecryption == 'n' or autoDecryption == 'no':
                exit()


    if pdf_file.isEncrypted:
        wordlist.close()
        print('\n[!] PASSWORD NOT FOUND [!]')
        exit()



def main():
    input_pass = input('Input path to wordlist: ')
    pass_txt = parse_file(input_pass)

    path_to_pdf = input('Input path to PDF: ')
    pdf_file = parse_file(path_to_pdf)

    crackpdf(pass_txt, pdf_file)


if __name__ == '__main__':
    main()
