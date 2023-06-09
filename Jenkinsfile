@Library('xmos_jenkins_shared_library@v0.24.0') _

getApproval()

pipeline {
  agent none
  parameters {
    string(
      name: 'TOOLS_VERSION',
      defaultValue: '15.1.4',
      description: 'The tools version to build with (check /projects/tools/ReleasesTools/)'
    )
  }
  options {
    skipDefaultCheckout()
  }
  stages {
    stage('xcore.ai') {
      agent {
        label 'xcore.ai'
      }
      stages {
        stage('Checkout') {
          steps {
            checkout scm
            sh "git clone git@github0.xmos.com:xmos-int/xtagctl.git"
          }
        }
        stage('Install Dependencies') {
          steps {
            withTools(params.TOOLS_VERSION) {
              installDependencies()
            }
          }
        }
        stage('Static analysis') {
          steps {
            withVenv() {
              warnError("Flake") {
                sh "flake8 --exit-zero --output-file=flake8.xml xscope_fileio"
                recordIssues enabledForFailure: true, tool: flake8(pattern: 'flake8.xml')
              }
            }
          }
        }
        stage('Build') {
          steps {
            withTools(params.TOOLS_VERSION) {
              sh 'tree'
              sh 'cd examples/throughput_c && make'
              withEnv(["XMOS_MODULE_PATH=${WORKSPACE}", "XCOMMON_DISABLE_AUTO_MODULE_SEARCH=1"]) {
                sh 'cd examples/fileio_features_xc && xmake'
              }
            }
          }
        }
        stage('Cleanup xtagctl'){
          steps {
            withVenv() {
              withTools(params.TOOLS_VERSION) {
                sh 'xtagctl reset_all XCORE-AI-EXPLORER'
                sh 'rm -f ~/.xtag/status.lock ~/.xtag/acquired'
              }
            }
          }
        }
        stage('Tests'){
          failFast false
          parallel {
            stage('Hardware tests') {
              stages{
                stage('Transfer test single large'){
                  steps {
                    withVenv() {
                      withTools(params.TOOLS_VERSION) {
                        sh 'python tests/test_throughput.py 64' //Pass size in MB
                      }
                    }
                  }
                }
              }
            }
            stage('Hardware tests #2 (in parallel)') {
              stages{
                stage('Transfer test multiple small'){
                  steps {
                    withVenv() {
                      withTools(params.TOOLS_VERSION) {
                        sh 'python tests/test_throughput.py 5' //Pass size in MB
                        sh 'python tests/test_throughput.py 5' //Pass size in MB
                        sh 'python tests/test_throughput.py 5' //Pass size in MB
                        sh 'python tests/test_throughput.py 5' //Pass size in MB
                      }
                    }
                  }
                }
              }
            }
            stage('xsim tests'){
              stages{
                stage('feature test'){
                  steps {
                    withVenv() {
                      withTools(params.TOOLS_VERSION) {
                        sh 'python tests/test_features.py'
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
      post {
        always {
          archiveArtifacts artifacts: "**/*.bin", fingerprint: true, allowEmptyArchive: true
        }
        cleanup {
          xcoreCleanSandbox()
        }
      }
    }
    stage('Windows build') {
      agent {
        label 'x86_64&&windows'
      }
      steps {
        checkout scm

        withTools(params.TOOLS_VERSION) {
          dir('host') {
            withVS("vcvars32.bat") {
              sh 'cmake -G"NMake Makefiles" -DCMAKE_BUILD_TYPE=Release .'
              sh 'nmake'
            }

            archiveArtifacts artifacts: "xscope_host_endpoint.exe", fingerprint: true
          }
        }
      }
      post {
        cleanup {
          xcoreCleanSandbox()
        }
      }
    }
    stage('Update view files') {
      agent {
        label 'x86_64 && linux'
      }
      when {
        expression { return currentBuild.currentResult == "SUCCESS" }
      }
      steps {
        script {
          current_scm = checkout scm
          env.SAVED_GIT_URL = current_scm.GIT_URL
          env.SAVED_GIT_COMMIT = current_scm.GIT_COMMIT
        }
        updateViewfiles()
      }
      post {
        cleanup {
          cleanWs()
        }
      }
    }
  }
}
