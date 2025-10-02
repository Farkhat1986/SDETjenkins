import jenkins.model.*
import org.jenkinsci.plugins.workflow.job.WorkflowJob
import org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition

def jenkins = Jenkins.instance
def jobName = "TestPipeline"

if (jenkins.getItem(jobName) == null) {
    def job = new WorkflowJob(jenkins, jobName)

    def pipelineScript = """
        pipeline {
            agent any
            stages {
                stage('Hello') {
                    steps {
                        echo 'Hello World'
                    }
                }
                stage('Email') {
                    steps {
                        emailext (
                            subject: 'Jenkins Test Email',
                            body: 'Pipeline executed successfully!',
                            to: 'farhatsdet@mail.ru'
                        )
                    }
                }
            }
        }
    """.stripIndent()

    job.definition = new CpsFlowDefinition(pipelineScript, true)
    job.save()
    println("Pipeline Job '${jobName}' создан успешно")
} else {
    println("Job '${jobName}' уже существует")
}
