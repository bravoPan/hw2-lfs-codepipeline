# hw2-lfs-codepipeline
code pipelines for lfs.

### The pipelines for deploying lambda funciton
- Source stage: AWS Wekhook will pull all the updates from this repo to the S3 bucket `hw2-cp-lfs`.
- Build stage: Codebuild will run `buildspec.yml`, this file has `aws cloudformation` CLI command, which will extract the sample Cloudformation template `sampleTemplate.yaml`(In this template, we used CF created 2 Lambda Function resources, with the `CodeUri` which will import the file in )
