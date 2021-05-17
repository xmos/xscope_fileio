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
    TOOLS_PATH = "/XMOS/tools/${params.TOOLS_VERSION}/XMOS/xTIMEcomposer/${params.TOOLS_VERSION}"
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
        installDependencies()
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
          // sh 'cd tests/test_callback && make'
          // sh 'cd tests/test_timing && make'
          // //sh 'cd tests/test_end_to_end && make' - This is built by the test and will fail otherwise
          // sh 'cd tests/test_tools/xscope_file_io_host && make'
          // sh 'export VOICE_FRONT_END_PATH=`pwd` && cd examples/app_vu && ls && cmake . -B build && cd build && make'
          // if you want to build once and distribute to multiple later stages
          // use "stash/unstash"
        }
      }
    }
    stage('Tests'){
      failFast false
      parallel {
        stage('Hardware tests') {
          stages{
            stage('Cleanup xtagctl'){
              steps {
                sh 'rm -f ~/.xtag/status.lock ~/.xtag/acquired'
              }
            }
            stage('Basic tests'){
              steps {
                dir('tests') {
                  withVenv() {
                    toolsEnv(TOOLS_PATH) {
                      sh 'python -m pytest test_end_to_end.py --junitxml=pytest_result.xml -s'
                      junit 'pytest_result.xml'
                    }
                  }
                }
              }
            }
          }
        }
        stage('xsim tests'){
          stages{
            stage('callback test'){
              steps {
                dir('tests/test_callback') {
                  withVenv() {
                    toolsEnv(TOOLS_PATH) {
                      // sh 'xsim test_isr.xe'
                    }          
                  }
                }
              }
            }
            stage('timing test'){
              steps {
                dir('tests/test_timing') {
                  withVenv() {
                    toolsEnv(TOOLS_PATH) {
                      // sh 'xsim test_timing.xe'
                    }
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
      // archiveArtifacts artifacts: "tests/pipelines/sensory_input/*.wav", fingerprint: true, allowEmptyArchive: true
      // archiveArtifacts artifacts: "tests/pipelines/configs/*.cfg", fingerprint: true, allowEmptyArchive: true
      // archiveArtifacts artifacts: "tests/pipelines/*.png", fingerprint: true, allowEmptyArchive: true
    }
    cleanup {
      cleanWs()
    }
  }
}