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

# Switch back to Jenkins user
USER jenkins

# Expose necessary ports
EXPOSE 8080 50000

# Define volume
VOLUME /var/jenkins_home

# Start Jenkins
CMD ["java", "-jar", "/usr/share/jenkins/jenkins.war"]