#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow

requirements:
  ScatterFeatureRequirement: {}
  SubworkflowFeatureRequirement: {}

inputs:
  folds: int[]
  app_name: File
  input_file: File
  k: int
  app_collect: File

steps:
  app:
    run: app.cwl
    scatter: current_fold
    in:
      current_fold: folds
      app_name: app_name
      input_file: input_file
      k: k
    out: [out_data]
  collect:
    run: collect_results.cwl
    in:
      metrics: app/out_data
      app_collect: app_collect  
    out: [output_final]
outputs:
  output_final:
    type: File
    outputSource: collect/output_final
