import csv
import json
import boto3
import uuid
import sys
from datetime import datetime
import datetime as dt

# import awscli.customizations.datapipeline.translator as trans

json_file_path = sys.argv[3]  # "/Users/hmandadi/Desktop/abc3.json"

# client = boto3.client('datapipeline', region_name='us-west-2')
start_time = sys.argv[5]
start_time_list = []
time_delta = dt.timedelta(minutes=10)


def get_the_start_time_for_pipeline(i):
    if i == 0:
        start_time_list.append(start_time)
        return start_time_list[-1]
    a = datetime.strptime(start_time_list[-1], '%Y-%m-%dT%H:%M:%S')
    start_time1 = a + time_delta
    start_time_list.append(start_time1.strftime('%Y-%m-%dT%H:%M:%S'))
    return start_time_list[-1]


def create_the_datapipelines_template_and_return_json(group_name, time_for_group):
    data2 = data.replace("___GROUPNAME___", group_name).replace("___LONGTIME___", time_for_group)
    return data2


'''def create_the_pipeline(template_files_path, cluster_name):
    create = client.create_pipeline(name=cluster_name, uniqueId=str(uuid.uuid1()))
    definition = json.load(open(template_files_path + cluster_name + "_"+ "" +".json", 'r'))
    # definition = json.loads(create_the_datapipelines_template_and_return_json(group_name, time_for_group))
    pipelineObjects = trans.definition_to_api_objects(definition)
    parameterObjects = trans.definition_to_api_parameters(definition)
    parameterValues = trans.definition_to_parameter_values(definition)
    response = client.put_pipeline_definition(pipelineId=create['pipelineId'], pipelineObjects=pipelineObjects,
                                              parameterObjects=parameterObjects, parameterValues=parameterValues)

    client.activate_pipeline(
        pipelineId=create['pipelineId'],
        parameterValues=[{'id': 'string', 'stringValue': 'string'}])'''

with open(json_file_path, 'r') as f:
    data = f.read()


def create_the_datapipelines_template_for_camus(cluster_name, time_for_group, worker_group, pipeline_start_time):
    data2 = data.replace("___GROUPNAME___", cluster_name) \
        .replace("___LONGTIME___", time_for_group) \
        .replace("___WORKER_GROUP___", worker_group) \
        .replace("DataPipelineDefaultRole", "datapipeline-service-role-sched-data-lake-prd") \
        .replace("___START_TIME___", pipeline_start_time)
    with open(sys.argv[2] + cluster_name + "_" + "" + ".json", 'w+') as generated_template:
        generated_template.write(data2)


def create_the_datapipelines_template_for_reconciler(group_name, time_for_group, worker_group, parallelism,
                                                     number_of_executions, pipeline_start_time):
    data2 = data.replace("___GROUPNAME___", group_name) \
        .replace("___LONGTIME___", time_for_group) \
        .replace("___WORKER_GROUP___", worker_group) \
        .replace("___PARALLELISM___", parallelism) \
        .replace("___NUMBER_OF_EXEC___", number_of_executions) \
        .replace("___START_TIME___", pipeline_start_time)
    with open(sys.argv[2] + group_name + ".json", 'w+') as generated_template:
        generated_template.write(data2)


def read_csv(file_path):
    with open(file_path, 'r') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        if sys.argv[4] == "camus":
            i = 0
            for row in readCSV:
                worker_group = row[0]
                time_for_group = row[1]
                cluster_name = row[2]
                print(cluster_name)
                pipeline_start_time = get_the_start_time_for_pipeline(i)
                create_the_datapipelines_template_for_camus(cluster_name, time_for_group, worker_group,
                                                            pipeline_start_time)
                # create_the_pipeline(sys.argv[2], cluster_name)
                i += 1
        elif sys.argv[4] == "reconciler":
            i = 0
            for row in readCSV:
                group_name = row[0]
                time_for_group = row[1]
                worker_group = row[2]
                parallelism = row[3]
                number_of_executions = row[4]
                pipeline_start_time = get_the_start_time_for_pipeline(i)
                create_the_datapipelines_template_for_reconciler(group_name, time_for_group, worker_group, parallelism,
                                                                 number_of_executions, pipeline_start_time)
                # create_the_pipeline(sys.argv[2], group_name)
                i += 1


if __name__ == '__main__':
    csv_iterator = read_csv(sys.argv[1])

#python DataPipelines.py /Users/hmandadi/Desktop/template_csv /Users/hmandadi/Desktop/template_testing/template_camus_ /Users/hmandadi/Desktop/camus_json.json camus 2018-10-14T00:00:00
