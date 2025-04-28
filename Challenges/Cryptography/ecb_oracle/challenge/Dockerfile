#in case the task requeries python to be installed:
    FROM python:3.9-slim-buster
    #else if its just a system : 
    #FROM ubuntu:22.04
    
    # Install some libs
    RUN apt-get update && apt-get -y upgrade
    
    # create ctf-user
    RUN groupadd -r ctf && useradd -r -g ctf ctf
    COPY task.py /home/ctf/
    COPY launch.sh /home/ctf/
    COPY ynetd /home/ctf/
    COPY secret.py /home/ctf
    
    
    #install some python libs
    RUN pip install pycryptodome
    
    #set some proper permissions
    RUN chown -R root:ctf /home/
    RUN chmod 750 /home/ctf/task.py
    RUN chmod 750 /home/ctf/ynetd
    RUN chmod 750 /home/ctf/launch.sh
    RUN chmod 750 /home/ctf/secret.py