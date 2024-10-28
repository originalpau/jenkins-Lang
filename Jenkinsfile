pipeline {
    agent any
    
    environment {
        AWS_ACCESS_KEY_ID = credentials('b2fc1a6c-1a3c-42cb-87b5-23a205486b43')
        AWS_SECRET_ACCESS_KEY = credentials('b2fc1a6c-1a3c-42cb-87b5-23a205486b43')
        AWS_REGION = 'eu-north-1'
    }
    
    stages {
        stage('Login to AWS') {
            steps {
                script {
                    echo 'Logging in to AWS...'
                    sh 'aws sts get-caller-identity'
                }
            }
        }
        
        stage('List EC2 Instances') {
            steps {
                script {
                    echo 'Listing EC2 Instances...'
                    sh '''
                        aws ec2 describe-instances \
                            --query 'Reservations[*].Instances[*].{Name:Tags[?Key==`Name`]|[0].Value,Instance:InstanceId,VPC:VpcId,Subnet:SubnetId,PublicIp:PublicIpAddress}' \
                            --filters "Name=instance-state-name,Values=running" "Name=tag:Project,Values=Jenkins" \
                            --output json > aws_output.json
                    '''
                }
            }
        }
        
        stage('Create attack graph') {
            steps {
                script {
                    echo 'Creating attack graph with python script'
                    sh '''
                        sh 'python3 jenkinsLang_gen.py'
                    '''
                }
            }
        }
    }
}

