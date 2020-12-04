FROM fedora:33

RUN dnf update -y && dnf install -y \
  yum-utils coreutils python3

RUN sed -i 's/^metalink/#metalink/g' /etc/yum.repos.d/fedora*.repo \
    && sed -i 's/^#baseurl/baseurl/g' /etc/yum.repos.d/fedora*.repo \
    && sed -i 's/download\.example/download\.fedoraproject\.org/g' /etc/yum.repos.d/fedora*.repo

RUN dnf update -y

COPY ./fetch-repo-workspace.py /fetch/fetch-repo-workspace.py
WORKDIR /fetch
