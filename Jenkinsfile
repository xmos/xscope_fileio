@Library('xmos_jenkins_shared_library@v0.16.2') _

getApproval()

pipeline {
  agent {
    label 'xcore.ai-explorer'
  }
  parameters {
    string(
      name: 'TOOLS_VERSION',
      defaultValue: '15.0.5',
      description: 'The tools version to build with (check /projects/tools/ReleasesTools/)'
    )
  }
  environment {
    // '/XMOS/tools' from get_tools.py and rest from tools installers
    TOOLS_PATH = "/XMOS/tools/${params.TOOLS_VERSION}/XMOS/XTC/${params.TOOLS_VERSION}"
  }
  options {
    skipDefaultCheckout()
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
        sh '/XMOS/get_tools.py ' + params.TOOLS_VERSION
        toolsEnv(TOOLS_PATH) {
          installDependencies()
        }
      }
    }
    stage('Static analysis') {
      steps {
        withVenv() {
          sh "flake8 --exit-zero --output-file=flake8.xml xscope_fileio"
          recordIssues enabledForFailure: true, tool: flake8(pattern: 'flake8.xml')
        }
      }
    }
    stage('Build') {
      steps {
        toolsEnv(TOOLS_PATH) {  // load xmos tools
          sh 'tree'
          sh 'cd examples/throughput_c && make'
          sh 'cd examples/fileio_features_xc && xmake'
        }
      }
    }
    stage('Cleanup xtagctl'){
      steps {
        withVenv() {
          toolsEnv(TOOLS_PATH) {
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
                  toolsEnv(TOOLS_PATH) {
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
                  toolsEnv(TOOLS_PATH) {
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
                  toolsEnv(TOOLS_PATH) {
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
    success {
      println "Do some sort of promotion: viewfiles/submodules/branches/tags"
    }
    always {
      archiveArtifacts artifacts: "**/*.bin", fingerprint: true, allowEmptyArchive: true
    }
    cleanup {
      cleanWs()
    }
  }
}