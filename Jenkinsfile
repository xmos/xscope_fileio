@Library('xmos_jenkins_shared_library@v0.28.0')

def runningOn(machine) {
  println "Stage running on:"
  println machine
}

def buildApps(appList) {
  appList.each { app ->
    sh "cmake -G 'Unix Makefiles' -S ${app} -B ${app}/build"
    sh "xmake -C ${app}/build -j\$(nproc)"
  }
}

def buildDocs(){
  sh 'pip install git+ssh://git@github.com/xmos/xmosdoc'
  sh 'xmosdoc html latex'
  script {
    def doc_version = sh(script: "cat settings.yml | awk '/version:/ {print \$2}'", returnStdout: true).trim()
    def zipFileName = "docs_xscope_fileio_v${doc_version}.zip"
    zip zipFile: zipFileName, archive: true, dir: "doc/_build"
  } // script
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
  } // parameters
  options {
    skipDefaultCheckout()
    timestamps()
    buildDiscarder(xmosDiscardBuildSettings(onlyArtifacts=false))
  } // options
  stages {
    stage('xcore.ai') {
      agent {
        label 'xcore.ai' // xcore.ai nodes have 2 devices atatched, allowing parallel HW test
      }

      stages {

        stage('Checkout') {
          steps {
            runningOn(env.NODE_NAME)
            dir('xscope_fileio') {
                checkout scm
                sh "git clone git@github0.xmos.com:xmos-int/xtagctl.git"
            } // dir
          } // steps
        } // stage 'Checkout'

        stage('Install Dependencies') {
          steps {
            dir('xscope_fileio') {
              withTools(params.TOOLS_VERSION) {
                createVenv("requirements.txt")
                withVenv {
                  sh "pip install -r requirements.txt"
                 }
              }
            }
          }
        }
        stage('Static analysis') {
          steps {
            dir('xscope_fileio') {
              withVenv {
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
              withVenv {
                withTools(params.TOOLS_VERSION) {
                  sh 'rm -f ~/.xtag/status.lock ~/.xtag/acquired'
                  sh 'xtagctl reset_all XCORE-AI-EXPLORER'
                }
              }
            }
          }
        }
        stage('Tests') {
          steps { 
            dir('xscope_fileio/tests') {
              withVenv {
                withTools(params.TOOLS_VERSION) {
                  sh 'pytest' // info: configuration opts in pytest.ini
                } // withTools
              } // withVenv
            } // dir
          } // steps
        } // Tests
      } // stages
      post {
        always {
          archiveArtifacts artifacts: "**/*.bin", fingerprint: true, allowEmptyArchive: true
          junit '**/reports/*.xml'
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
    }

    stage('Docs') {
      agent {
        label 'documentation'
      }
      steps {
        runningOn(env.NODE_NAME)
        dir('xscope_fileio') {
          checkout scm
          createVenv("requirements.txt")
          withTools(params.TOOLS_VERSION) {
            withVenv {
              buildDocs()  
            }
          }
        }
      }
      post {
        cleanup {
          cleanWs()
        }
      }
    } // stage: Docs

  } // stages
} // pipeline
