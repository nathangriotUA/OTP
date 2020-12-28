import argparse
import subprocess
import os


random_dev = open("/dev/urandom", "rb")

parser = argparse.ArgumentParser()
parser.add_argument("directory", help = "directory name", type = str )
parser.add_argument("-g", help = "generate pad files", action = "store_true")
parser.add_argument("-r", help = "send a message", action = "store_true")
parser.add_argument("-s", help = "receive a message", action = "store_true")
parser.add_argument("-f", help = "read message from file", type = str)
parser.add_argument("-t", help = "read message from text", type = str)


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
        

def main():
    ''' Main function '''
    args = parser.parse_args()
    if args.g:
        generate_files(args.directory)


if __name__ == '__main__':
    main()
