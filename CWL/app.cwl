#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: python3

hints:
  DockerRequirement:
    dockerPull: akazakovic/python3-ann
inputs:
  app_name:
    type: File
    inputBinding:
      position: 1
  input_file:
    type: File
    inputBinding:
      position: 2
  k:
    type: int
    inputBinding:
      position: 3
  current_fold:
    type: int
    inputBinding:
      position: 4

stdout: output.txt

outputs:
  out_data:
    type: string
    outputBinding:
      glob: output.txt
      loadContents: true
      outputEval: $(self[0].contents)



