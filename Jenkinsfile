pipeline {
     agent { 
        docker {
            image 'originalpau07/custom-jenkins:v1'
        }
     }

    options {
        skipDefaultCheckout(true)
    }
    
    environment {
        AWS_ACCESS_KEY_ID = credentials('b2fc1a6c-1a3c-42cb-87b5-23a205486b43')
        AWS_SECRET_ACCESS_KEY = credentials('b2fc1a6c-1a3c-42cb-87b5-23a205486b43')
        AWS_REGION = 'eu-north-1'
    }
    
    stages {
        stage('Clean up workspace') {
            steps {
                cleanWs()
                checkout scm
            }
        }
        stage('Login to AWS') {
            steps {
                script {
                    echo 'Logging in to AWS...'
                    sh 'aws sts get-caller-identity'
                }
            }
        }
        
        stage('Trigger Parallel Jobs for networks') {
            steps {
                script {
                    def networks = ['Jenkins', 'Jenkins2']
                    def parallelJobs = [:]

                    networks.each { project -> parallelJobs[project] = {
                        node(master) {
                            stage('Fetch EC2 Instances') {
                                steps {
                                    script {
                                        echo "Listing EC2 Instances in ${project}"
                                        sh """
                                            aws ec2 describe-instances \
                                                --region eu-north-1 \
                                                --query 'Reservations[*].Instances[*].{Name:Tags[?Key==`Name`]|[0].Value,Instance:InstanceId,VPC:VpcId,Subnet:SubnetId,PublicIp:PublicIpAddress}' \
                                                --filters "Name=instance-state-name,Values=running" "Name=tag:Project,Values=${project}" \
                                                --output json > ${project}_instances.json
                                        """
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
                                        sh "python3 \$WORKSPACE/jenkinsLang_gen.py ${project}_instances.json"
                                    }
                                }
                            }

                            stage('Save output to S3 Bucket') {
                                steps {
                                    script {
                                        echo 'Saving output files to AWS storage'
                                        sh """
                                            TIMESTAMP=\$(date +"%Y-%m-%d_%H:%M")
                                            aws s3 cp aws_model.json s3://neo4j-attackgraph/\$TIMESTAMP-${project}/aws_model.json
                                            aws s3 cp attack_graph.json s3://neo4j-attackgraph/\$TIMESTAMP-${project}/attack_graph.json
                                            aws s3 cp ${project}_instances.json s3://neo4j-attackgraph/\$TIMESTAMP-${project}/${project}_instances.json
                                        """
                                    }
                                }
                            }
                        }
                    }}
                    parallel parallelJobs
                }
            }
        }
    }


    post {
    // Clean after build
    always {
        cleanWs(cleanWhenNotBuilt: false,
                deleteDirs: true,
                disableDeferredWipeout: true,
                notFailBuild: true,
                patterns: [[pattern: '.gitignore', type: 'INCLUDE'],
                            [pattern: '.propsfile', type: 'EXCLUDE']])
    }}
}
