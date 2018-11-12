import boto3
from collections import defaultdict

client = boto3.client('datapipeline')

pipelines_list = client.list_pipelines()['pipelineIdList']

pipeline_details = defaultdict(list)

for pipeline in pipelines_list:
    pipeline_details[pipeline['name']].append({'pipelineId' : pipeline['id']})
    pipeline_details[pipeline['name']].append({'pipelineName' : pipeline['name']})
    pipeline_description = client.describe_pipelines(pipelineIds=[str(pipeline['id'])])['pipelineDescriptionList'][0]['fields']
    pipeline_details[pipeline['name']].append({'healthStatus': 'PENDING'})

    for description in pipeline_description:
        if "'@healthStatus'" in str(description):
                pipeline_details[pipeline['name']].append({'healthStatus': description['stringValue']})
                if len(pipeline_details[pipeline['name']]) == 4 :
                    (pipeline_details['name']).pop(2)


