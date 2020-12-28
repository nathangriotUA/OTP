import argparse
import subprocess
import os


random_dev = open("/dev/urandom", "rb")

parser = argparse.ArgumentParser()
parser.add_argument("directory", help = "directory name", type = str )
parser.add_argument("-g", help = "generate pad files", action = "store_true")
parser.add_argument("-s", help = "send a message", action = "store_true")
parser.add_argument("-r", help = "receive a message", action = "store_true")
parser.add_argument("-f", help = "read message from file", type = str)
parser.add_argument("-t", help = "read message from text", type = str)

def text_to_bin(text):
    ''' convert text into arrays of bins:
        Input:
            - text (str)
        Ouput:
            - Binary arrays
    '''
    chars = bytearray(text, "utf8")
    bins = []

    for char in chars:
        bin_char = bin(char)[2:].zfill(8)
        bin_char = list(bin_char)
        bins += bin_char

    return bins

def generate_files(directory_name):
    ''' generate key files:
        input:
            - directory name
        output:
            - none '''

    i = 0
    dir_name = ""

    while i <= 9999:
        dir_name = str(i).zfill(4)
        try:
            os.mkdir(directory_name+"/"+dir_name)
        except OSError:
            print (dir_name+" not available")
        else:
            break
        i += 1

    for i in range(100):        
        data_p = [bin(int.from_bytes(random_dev.read(1), 'big'))[2:].zfill(8) for i in range(48)]
        data_s = [bin(int.from_bytes(random_dev.read(1), 'big'))[2:].zfill(8) for i in range(48)]
        data_c = [bin(int.from_bytes(random_dev.read(1), 'big'))[2:].zfill(8) for i in range(2000)]

        cur_file = str(i).zfill(2)
        with open(directory_name+'/'+dir_name+"/"+cur_file+"p", 'w') as f:
            for random_bits in data_p:
                f.write(str(random_bits))
        with open(directory_name+'/'+dir_name+"/"+cur_file+"s", 'w') as f:
            for random_bits in data_s:
                f.write(str(random_bits))
        with open(directory_name+'/'+dir_name+"/"+cur_file+"c", 'w') as f:
            for random_bits in data_c:
                f.write(str(random_bits))
    random_dev.close()
        

def transmission(message,directory_name):
    ''' transmission it will take a message and encrypt it
    input:
        - message (str)
        - directory name 
    output:
        - none
    '''
    i= 0
    dir_used = ""
    file_used = ""
    found = False
    while i <= 9999 and found == False :
        j = 0
        while j <= 99 and found == False : 
            dir = str(i).zfill(4)
            filename = str(j).zfill(2)
            if os.path.isfile(directory_name+'/'+dir+'/'+filename+"c"):
                dir_used = dir
                file_used = filename
                found = True
    
    if len(message) > 2000:
        SystemError("Message is too long")

    f = open(directory_name+'/'+dir_used+"/"+file_used+"p", "r")
    datap = f.read()
    datap = [datap[i : i + 8] for i in range(0, len(datap), 8)]
    f.close()
    f = open(directory_name+'/'+dir_used+"/"+file_used+"s", "r")
    datas = f.read()
    datas = [datas[i : i + 8] for i in range(0, len(datas), 8)]
    f.close()
    f = open(directory_name+'/'+dir_used+"/"+file_used+"c", "r")
    datac = f.read()
    datac = [datac[i : i + 8] for i in range(0, len(datac), 8)]
    f.close()

    with open(directory_name+'/'+dir_used+"/"+file_used+"t", 'a') as f:
        for data in datap:
            f.write(str(data))
        
        for i, data in enumerate(message):
            data = str(bin(int(data, 2) + int(datac[i] , 2))[2:]).zfill(9)
            f.write(data)
        
        for data in datas:
            f.write(str(data))

    return 0





def receive(file,directory_name):
    ''' read file
        input:
            - file name
            - directory name
        output:
            - message 
     '''
    return 0

def main():
    ''' Main function '''
    args = parser.parse_args()
    if args.g:
        generate_files(args.directory)
    if args.s:
        if args.t:
            message = args.t
        elif args.f:
            message = readFromFile(args.f)
        else:
            message = input('Please write your message: ')

        bins = text_to_bin(message)
        transmission(bins,args.directory)
    if args.r:
        get_message(args.directory,filename)


if __name__ == '__main__':
    main()
