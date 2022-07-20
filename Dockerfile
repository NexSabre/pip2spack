FROM spack/ubuntu-jammy:latest

# add Spack bin to the bash
RUN echo 'alias spack=/opt/spack/bin/spack' >> /root/.bashrc

# install latest pip2spack
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install pip2spack

ENTRYPOINT ["/bin/bash", "--rcfile", "/etc/profile", "-l"]
