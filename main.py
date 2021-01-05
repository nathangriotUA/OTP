import argparse
import subprocess
import os
import sys

random_dev = open("/dev/urandom", "rb")

parser = argparse.ArgumentParser()
parser.add_argument("directory", help = "directory name", type = str )
parser.add_argument("-filename", help = "file name", type = str )
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
        bins.append(bin_char)

    return bins

def readFromFile(filename):
    ''' allows to read the content of a file:
        input:
            - filename
        output:
            - file content (str)
    '''
    file = open(filename, "r")
    text = file.read()
    file.close()
    return text

def generate_files(directory_name):
    ''' generate key files:
        input:
            - directory name
        output:
            - none '''

    i = 0
    dir_name = ""
    try:
        os.mkdir(directory_name)
        os.mkdir(directory_name + "_receiver")
    except OSError:
            print ("unable to create directory")


    created = False
    while i <= 9999:
        dir_name = str(i).zfill(4)
        try:
            os.mkdir(directory_name + "/" + dir_name)
            created = True
        except OSError:
            print (dir_name + " not available")
        if created:
            break
        i += 1

    if created:
        for i in range(100):        
            data_p = [bin(int.from_bytes(random_dev.read(1), 'big'))[2:].zfill(8) for i in range(48)]
            data_s = [bin(int.from_bytes(random_dev.read(1), 'big'))[2:].zfill(8) for i in range(48)]
            data_c = [bin(int.from_bytes(random_dev.read(1), 'big'))[2:].zfill(8) for i in range(2000)]

            cur_file = str(i).zfill(2)
            with open(directory_name + '/' + dir_name + "/" + cur_file + "p", 'w') as f:
                for random_bits in data_p:
                    f.write(str(random_bits))
            with open(directory_name + '/' + dir_name + "/" + cur_file + "s", 'w') as f:
                for random_bits in data_s:
                    f.write(str(random_bits))
            with open(directory_name + '/' + dir_name + "/" + cur_file + "c", 'w') as f:
                for random_bits in data_c:
                    f.write(str(random_bits))

        subprocess.call('cp -r ./' + directory_name + '/* ./' + directory_name + '_receiver/', shell=True)
        random_dev.close()
        

def transmission(message, directory_name):
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
            if os.path.isfile(directory_name + '/' + dir + '/' + filename + "c"):
                dir_used = dir
                file_used = filename
                found = True
            j += 1
        i += 1
    
    # If not found then we return and print an error message
    if found == False:
        print("Sorry please generate files in order to do this task.")
        return 0

    if len(message) > 2000:
        sys.exit("Message is too long")

    f = open(directory_name + '/' + dir_used + "/" + file_used + "p", "r")
    datap = f.read()
    datap = [datap[i : i + 8] for i in range(0, len(datap), 8)]
    f.close()
    f = open(directory_name + '/' + dir_used + "/" + file_used + "s", "r")
    datas = f.read()
    datas = [datas[i : i + 8] for i in range(0, len(datas), 8)]
    f.close()
    f = open(directory_name + '/' + dir_used + "/" + file_used + "c", "r")
    datac = f.read()
    datac = [datac[i : i + 8] for i in range(0, len(datac), 8)]
    f.close()

    with open(directory_name+'-'+dir_used+"-"+file_used+"t", 'w') as f:
        for data in datap:
            f.write(str(data))
        
        for i, data in enumerate(message):
            print(data)
            a = int(data, 2)
            b = int(datac[i], 2)
            c = a + b
            data = bin(c)[2:].zfill(9)
            f.write(data)
        
        for data in datas:
            f.write(str(data))

    subprocess.call("shred --remove " + directory_name+'/'+dir_used+"/"+file_used+"c", shell = True)
    return 0





def receive(directory_name, file):
    ''' read file : this function writes a file with the message after processing
        input:
            - file name 
            - directory name
        output:
            - none 
     '''
    i = 0
    dir_used = ""
    file_used = ""
    found = False
    f = open(file, "r")
    datat = f.read()
    datat = datat[:384]
    f.close()
    while i <= 9999 and found == False :
        j = 0
        while j <= 99 and found == False : 
            dir = str(i).zfill(4)
            filename = str(j).zfill(2)
            if os.path.isfile(directory_name + '/' + dir + "/" + filename + "p"):
                f = open(directory_name + '/' + dir + "/" + filename + "p", "r")
                datap = f.read()
                f.close()
                if datat == datap:
                    # pad found so we delete it
                    subprocess.call("shred --remove " + directory_name + '/' + dir + "/" + filename + "p", shell = True)
                    f = open(directory_name + '/' + dir + "/"+ filename + "c", "r")
                    datac = f.read()
                    datac = [datac[i : i + 8] for i in range(0, len(datac), 8)]
                    dir_used = dir
                    file_used = filename
                    f.close()
                    # transimission recovered so we delete it
                    subprocess.call("shred --remove " + directory_name + '/' + dir + "/" + filename + "c", shell = True)
                    found = True
            j += 1
        i += 1

    if found == False :
        print("Impossible to find the right file for this message")
        return 0

    f = open(file, "r")
    datam = f.read()
    datam = datam[384 :- 384]
    datam = [datam[i : i + 9] for i in range(0, len(datam), 9)]

    with open(directory_name + '-' + dir_used + "-" + file_used + "m", 'w') as f:
        for i, data in enumerate(datam):
            a = int(data, 2)
            b = int(datac[i], 2)
            c = a - b
            print(a - b)
            data = chr(c)
            f.write(data)
    return 0

def main():
    ''' Main function '''
    
    #try :
    #    socket.create_connection(("1.1.1.1", 53))
    #    print("please disconnect from the internet")
    #    return 0
    #except :
    #    print("not connected to the internet, able to continue")
    
    # get interfaces 
    args = parser.parse_args()
    current_dir = "/sys/class/net/"
    sub_dirs = [x[1] for x in os.walk(current_dir)]

    for sub_dir in sub_dirs[0]:
        file = open(current_dir+sub_dir+"/operstate", "r")
        text = file.read()
        file.close()
        if "up" in text:
            print("connected to the internet. Please disconnect")
            return 0


    if (not args.s and not args.r) or args.g:
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
        receive(args.directory,args.filename)


if __name__ == '__main__':
    main()
