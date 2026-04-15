FROM jenkins/jenkins:lts

USER root

# 1. Install Docker CLI (So Jenkins can run docker commands)
RUN apt-get update && apt-get install -y lsb-release ca-certificates curl gnupg && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list && \
    apt-get update && apt-get install -y docker-ce-cli

# 2. Fix Permissions: Add jenkins user to root group 
RUN usermod -aG root jenkins

# 3. Fix Git "Not a safe directory" error permanently
RUN git config --global --add safe.directory "*"

USER jenkins