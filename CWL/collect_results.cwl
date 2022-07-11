#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: python3

hints:
  DockerRequirement:
    dockerPull: akazakovic/python3-ann
inputs:
  app_collect:
    type: File
    inputBinding:
      position: 1
  metrics:
    type: string[]
    inputBinding:
      position: 2
outputs:
  output_final:
    type: stdout
stdout: rezultati.txt


