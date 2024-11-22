pipeline {
     agent { 
        docker {
            image 'originalpau07/custom-jenkins:v1'
        }
     }
    
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

        stage('Verify AWS Output') {
            steps {
                script {
                    echo 'Listing workspace files...'
                    sh 'ls -la $WORKSPACE'
                }
            }
        }
        
        stage('List EC2 Instances') {
            steps {
                script {
                    def networks = ["Jenkins", "Jenkins2"]

                    networks.each { p -> 
                        echo "Listing EC2 Instances in ${networks} as ${p}"
                        sh """
                            aws ec2 describe-instances \
                                --region eu-north-1 \
                                --query 'Reservations[*].Instances[*].{Name:Tags[?Key==`Name`]|[0].Value,Instance:InstanceId,VPC:VpcId,Subnet:SubnetId,PublicIp:PublicIpAddress}' \
                                --filters "Name=instance-state-name,Values=running" "Name=tag:Project,Values=${p}" \
                                --output json > ${p}.json
                        """
                    }
                }
            }
        }

        stage('Verify AWS Output') {
            steps {
                script {
                    echo 'Listing workspace files...'
                    sh 'ls -la $WORKSPACE'
                }
            }
        }

        stage('Create attack graph') {
            steps {
                script {
                    echo 'Creating attack graph with python script'
                    sh "python3 \$WORKSPACE/jenkinsLang_gen.py ${Jenkins.json}"
                }
            }
        }

        stage('Save output to S3 Bucket') {
            steps {
                script {
                    echo 'Saving output files to AWS storage'
                    sh '''
                        TIMESTAMP=$(date +"%Y-%m-%d_%H:%M")
                        aws s3 cp aws_model.json s3://neo4j-attackgraph/$TIMESTAMP/aws_model.json
                        aws s3 cp attack_graph.json s3://neo4j-attackgraph/$TIMESTAMP/attack_graph.json
                        aws s3 cp Jenkins.json s3://neo4j-attackgraph/$TIMESTAMP/Jenkins.json
                    '''
                }
            }
        }
    }
}

