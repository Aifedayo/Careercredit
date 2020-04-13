pipeline {
  agent any
   options {
        disableConcurrentBuilds()
        // skipDefaultCheckout(true)
    }
  stages {
    stage('Copying the file from Jenkins Folder') {
      steps {
        script {
          sh 'sudo rm -rf /linuxjobber/www/*'
          sh 'sudo cp -rf /var/lib/jenkins/workspace/linuxjobber_sample_' + env.GIT_BRANCH + '/* /linuxjobber/www/'
          echo '${env.GIT_COMMITTER_EMAIL}'
          echo 'Stage 1'
        }
      }
    }
    stage('list credentials ids') {
      steps {
        script {
          sh 'cat $JENKINS_HOME/credentials.xml | grep "<id>"'
        }
      }
    }

    stage('usernamePassword') {
      steps {
        script {
          withCredentials([
            usernamePassword(credentialsId: 'root_est',
              usernameVariable: 'username',
              passwordVariable: 'password')
          ]) {
            def pass = "'${password}'"
            //sh "echo the word: ${pass}"
            sh 'sshpass -p '+"${pass}"+''' ssh -o StrictHostKeyChecking=no jerry@test.linuxjobber.com 'cd /;ls;'
            '''

           
          }
        }
      }
    }

    stage('Build Docker Image ') {
      steps {
        script {
          echo 'Stage 2'
          // sh "sleep 20"
        }
      }
    }
    stage('Deploy: int') {
      steps {
        script {
          echo 'Stage 3'
           // sh "sleep 60"
        }
      }
    }
    stage('Unit Test') {
      steps {
        script {
          echo 'Stage 3'
        }
      }
    }
  }
  post {
        always {
            echo 'This will always run'
        }
        success {
            echo 'This will run only if successful'
        }
        failure {
            echo 'This will run only if failed'
        }
        unstable {
            echo 'This will run only if the run was marked as unstable'
        }
        changed {
            echo 'This will run only if the state of the Pipeline has changed'
            echo 'For example, if the Pipeline was previously failing but is now successful'
            echo 'For example, if the Pipeline was previously failing but is now successful'
            echo 'For example, if the Pipeline was previously failing but is now successful'
        }
    }
}
