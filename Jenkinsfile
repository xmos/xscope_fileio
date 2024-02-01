@Library('xmos_jenkins_shared_library@v0.24.0') _

def buildApps(appList) {
  appList.each { app ->
    sh "cmake -G 'Unix Makefiles' -S ${app} -B ${app}/build"
    sh "xmake -C ${app}/build -j\$(nproc)"
  }
}

getApproval()

pipeline {
  agent none
  parameters {
    string(
      name: 'TOOLS_VERSION',
      defaultValue: '15.2.1',
      description: 'The tools version to build with (check /projects/tools/ReleasesTools/)'
    )
  }
  options {
    skipDefaultCheckout()
    buildDiscarder(logRotator(
        numToKeepStr:         env.BRANCH_NAME ==~ /develop/ ? '50' : '',
        artifactNumToKeepStr: env.BRANCH_NAME ==~ /develop/ ? '50' : ''
    ))
  }
  stages {
    stage('xcore.ai') {
      agent {
        label 'xcore.ai' // xcore.ai nodes have 2 devices atatched, allowing parallel HW test
      }
      stages {
        stage('Checkout') {
          steps {
            dir('xscope_fileio') {
              checkout scm
              sh "git clone git@github0.xmos.com:xmos-int/xtagctl.git"
            }
          }
        }
        stage('Install Dependencies') {
          steps {
            dir('xscope_fileio') {
              withTools(params.TOOLS_VERSION) {
                installDependencies()
              }
            }
          }
        }
        stage('Static analysis') {
          steps {
            dir('xscope_fileio') {
              withVenv() {
                warnError("Flake") {
                  sh "flake8 --exit-zero --output-file=flake8.xml xscope_fileio"
                  recordIssues enabledForFailure: true, tool: flake8(pattern: 'flake8.xml')
                }
              }
            }
          }
        }
        stage('Build') {
          steps {
            sh "git clone -b develop git@github.com:xmos/xcommon_cmake ${WORKSPACE}/xcommon_cmake"
            dir('xscope_fileio') {
              withTools(params.TOOLS_VERSION) {
                withEnv(["XMOS_CMAKE_PATH=${WORKSPACE}/xcommon_cmake"]) {
                  buildApps([
                    "examples/fileio_features_xc",
                    "examples/throughput_c",
                    "tests/no_hang",
                    "tests/close_files",
                  ]) // buildApps
                } // withEnv
              } // withTools
            } // dir
          } // steps
        } // stage 'Build'
        stage('Cleanup xtagctl'){
          steps {
            dir('xscope_fileio') {
              withVenv() {
                withTools(params.TOOLS_VERSION) {
                  // sh 'rm -f ~/.xtag/status.lock ~/.xtag/acquired' // not needed
                  sh 'xtagctl reset_all XCORE-AI-EXPLORER'
                }
              }
            }
          }
        }
        stage('Tests'){
          failFast false
          parallel {

            stage('Hardware tests #1 (in parallel)') {
              stages{
                stage('Transfer test single large'){
                  steps {
                    dir('xscope_fileio/tests') {
                      withVenv() {
                        withTools(params.TOOLS_VERSION) {
                          sh 'pytest -c pytest.ini -k test_throughput.1'
                        } // withTools
                      } // withVenv
                    } // dir
                  } // steps
                } // stage
              }// stages
            } // Hardware tests #1
            
            stage('Hardware tests #2 (in parallel)') {
              stages{
                stage('Perform pytest tests'){
                  steps { dir('xscope_fileio/tests') {
                    withVenv() {
                      withTools(params.TOOLS_VERSION) {
                        sh 'pytest -c pytest.ini -k test_throughput.2'
                        sh 'pytest -c pytest.ini -k test_throughput.3'
                        sh 'pytest -c pytest.ini -k test_throughput.4'
                        sh 'pytest -c pytest.ini -k test_throughput.5'
                        sh 'pytest -c pytest.ini -k test_close_files'
                        sh 'pytest -c pytest.ini -k test_no_hang'
                      }
                    }
                  }}
                }
              } // stages
            } // Hardware tests #2

            stage('xsim tests (in parallel)'){
              stages{
                stage('feature test'){
                  steps {
                    dir('xscope_fileio') {
                      withVenv() {
                        withTools(params.TOOLS_VERSION) {
                          sh 'python tests/test_features.py'
                        } // withTools
                      } // withVenv
                    } // dir
                  } // steps
                } // stage
              } // stages
            } // stage xsim tests
          } // parallel
        } // Tests
      } // stages
      post {
        always {
          archiveArtifacts artifacts: "**/*.bin", fingerprint: true, allowEmptyArchive: true
        }
        cleanup {
          xcoreCleanSandbox()
        }
      }
    } // stage: xcore.ai
    stage('Windows build') {
      agent {
        label 'x86_64&&windows'
      }
      steps {
        checkout scm

        withTools(params.TOOLS_VERSION) {
          dir('host') {
            withVS("vcvars32.bat") {
              sh 'cmake -G "Ninja" .'
              sh 'ninja'
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
    } // stage: Windows build
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
    } // stage: Update view files
  } // stages
}
