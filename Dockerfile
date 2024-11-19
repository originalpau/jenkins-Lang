FROM jenkins/jenkins:lts
USER root

# Update and install necessary packages
RUN apt-get -y update && \
    apt-get install -y sudo git wget && \
    echo "Jenkins ALL=NOPASSWD: ALL" >> /etc/sudoers

# Install Docker
RUN wget http://get.docker.com/builds/Linux/x86_64/docker-latest.tgz && \
    tar -xvzf docker-latest.tgz && \
    mv docker/* /usr/bin/ && \
    rm -rf docker-latest.tgz docker

# Install Python pip
RUN apt-get install -y python3 python3-pip python3-venv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install AWS CLI and mal-toolbox in virtual environment
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install awscli mal-toolbox

# Add virtual environment to PATH
ENV PATH="/opt/venv/bin:$PATH"

# Define a working directory
WORKDIR /app

# Switch back to Jenkins user
USER jenkins

# Expose necessary ports
EXPOSE 8080 50000

# Define volume
VOLUME /var/jenkins_home

# Start Jenkins
CMD ["java", "-jar", "/usr/share/jenkins/jenkins.war"]