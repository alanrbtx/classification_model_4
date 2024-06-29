pipeline {
  agent none
  stages {
    stage('Docker Build') {
      agent any
      steps {
        sh 'docker build -t alan1402/bigdata:0.4 .'
      }
    }
    stage('Docker push') {
      agent any
      steps {
        sh 'docker push alan1402/bigdata:0.4'
      }
    }
    stage('Deployment: test stage 1') {
      agent any
      steps {
        sh 'docker compose up --build -d'
        sh 'python3 init_vault.py --vault_addr "http://127.0.0.1:8200" --port 6379 --token "hvsvio2dl8SxHJU83uFk8O8JGGE" --prod_host 9092' 
      }
    }
    stage('Deployment: test stage 2') {
      agent any
      steps {
        sh 'python3 -m pytest service/app.py'
        sh 'python3 tests/test_api.py'
        sh 'docker stop $(docker ps -a -q)'
      }
    }
  }
}