@Library('xmos_jenkins_shared_library@v0.24.0') _

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
            dir('xscope_fileio') {
              withTools(params.TOOLS_VERSION) {
                sh 'tree'
                sh 'cd examples/throughput_c && make'
                sh 'cd tests/no_hang && . make.sh'
                withEnv(["XMOS_MODULE_PATH=${WORKSPACE}", "XCOMMON_DISABLE_AUTO_MODULE_SEARCH=1"]) {
                  sh 'cd examples/fileio_features_xc && xmake'
                }
                // xcommon cmake
                sh "git clone -b develop git@github.com:xmos/xcommon_cmake ${WORKSPACE}/xcommon_cmake"
                withEnv(["XMOS_CMAKE_PATH=${WORKSPACE}/xcommon_cmake"]) {
                  // build close files test
                  sh 'cmake -G "Unix Makefiles" -S tests/close_files -B tests/close_files/build'
                  sh 'xmake -C tests/close_files/build -j4'
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
            stage('Hardware tests') {
              stages{
                stage('Transfer test single large'){
                  steps {
                    dir('xscope_fileio') {
                      withVenv() {
                        withTools(params.TOOLS_VERSION) {
                          sh 'python tests/test_throughput.py 64' //Pass size in MB
                        }
                      }
                    }
                  }
                }
              }
            }
            stage('Hardware tests #2 (in parallel)') {
              stages{
                stage('Transfer test multiple small'){
                  steps { dir('xscope_fileio') {
                    withVenv() {
                      withTools(params.TOOLS_VERSION) {
                        sh 'python tests/test_throughput.py 5' //Pass size in MB
                        sh 'python tests/test_throughput.py 5' //Pass size in MB
                        sh 'python tests/test_throughput.py 5' //Pass size in MB
                        sh 'python tests/test_throughput.py 5' //Pass size in MB
                      }
                    }
                  }}
                }
                stage('Test closing files'){
                  steps { dir('xscope_fileio') {
                    withVenv() {
                      withTools(params.TOOLS_VERSION) {
                        sh 'python tests/test_close_files.py'
                      }
                    } // withVenv
                  }} // steps
                } // stage 'Test closing files'

                stage('Test for no hanging on missing read file'){
                  steps { dir('xscope_fileio') {
                    withVenv() {
                      withTools(params.TOOLS_VERSION) {
                        sh 'python tests/test_no_hang.py'
                      }
                    }}
                  }
                } // stage 'Test for no hanging on missing read file'
              } // stages
            } // Hardware tests #2

            stage('xsim tests'){
              stages{
                stage('feature test'){
                  steps {
                    dir('xscope_fileio') {
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
