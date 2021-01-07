# OTP

This toolkit is used ton ecrypt messages.
It doesnt use any library so anyone can use it, you only need python 3.

In order to use it there are 3 modes:

    - generation : it is used to generate the files needed to encrypt your message
    - writing : uses the generated files to encrypt the message
    - reading  : reads the content of the message and create a new file where the message is stored


This toolkit checks if you are connected to the internet. If you are the toolkit wont work, this is made to protect the content of your message. 

Urandom was used instead of random because random takes way too much time to generate. Since there are a lot of data to generate urandom was necessary.

to start :

generation:

    python3 main.py -g [directorie]
    python3 main.py [directorie]

send:

    python3 main.py -s [directorie]
    python3 main.py -s -t [text message] [directorie]
    python3 main.py -s -f [filename] [directorie]

receive:

    python3 main.py -r [directorie] [filename]
    
  