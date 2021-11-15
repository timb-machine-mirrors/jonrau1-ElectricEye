#This file is part of ElectricEye.
#SPDX-License-Identifier: Apache-2.0

#Licensed to the Apache Software Foundation (ASF) under one
#or more contributor license agreements.  See the NOTICE file
#distributed with this work for additional information
#regarding copyright ownership.  The ASF licenses this file
#to you under the Apache License, Version 2.0 (the
#"License"); you may not use this file except in compliance
#with the License.  You may obtain a copy of the License at

#http://www.apache.org/licenses/LICENSE-2.0

#Unless required by applicable law or agreed to in writing,
#software distributed under the License is distributed on an
#"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#KIND, either express or implied.  See the License for the
#specific language governing permissions and limitations
#under the License.
import json
from processor.outputs.output_base import ElectricEyeOutput

@ElectricEyeOutput
class JsonProvider(object):
    __provider__ = "json_normalized"

    def write_findings(self, findings: list, output_file: str, **kwargs):
        # create a new empty list to store flattened findings
        newFindings = []
        print(f"Writing {len(findings)} findings to JSON file")
        # create output file based on inputs
        jsonfile = f"{output_file}-normalized.json"

        print(f"Your filename is called {jsonfile}")

        # loop the findings and create a flatter structure - better for indexing without the nested lists
        for fi in findings:
            # create the new dict which will receive parsed values
            fDict = {
                "SchemaVersion": str(fi["SchemaVersion"]),
                "Id": str(fi["Id"]),
                "ProductArn": str(fi["ProductArn"]),
                "GeneratorId": str(fi["GeneratorId"]),
                "AwsAccountId": str(fi["AwsAccountId"]),
                "Types": str(fi["Types"]),
                "FirstObservedAt": str(fi["FirstObservedAt"]),
                "CreatedAt": str(fi["CreatedAt"]),
                "UpdatedAt": str(fi["UpdatedAt"]),
                "SeverityLabel": str(fi["Severity"]["Label"]),
                "Confidence": str(fi["Confidence"]),
                "Title": str(fi["Title"]),
                "Description": str(fi["Description"]),
                "RecommendationText": str(fi["Remediation"]["Recommendation"]["Text"]),
                "RecommendationUrl": str(fi["Remediation"]["Recommendation"]["Url"]),
                "ProductName": "ElectricEye",
                "ResourceType": str(fi["Resources"][0]["Type"]),
                "ResourceId": str(fi["Resources"][0]["Id"]),
                "ResourcePartition": str(fi["Resources"][0]["Partition"]),
                "ResourceRegion": str(fi["Resources"][0]["Region"]),
                "ResourceDetails": str(fi["Resources"][0]["Details"]),
                "ComplianceStatus": str(fi["Compliance"]["Status"]),
                "ComplianceRelatedRequirements": str(fi["Compliance"]["RelatedRequirements"]),
                "WorkflowStatus": str(fi["Workflow"]["Status"]),
                "RecordState": str(fi["RecordState"])
            }
            # append new dict to list
            newFindings.append(fDict)
        # once complete with parsing findings - write to file and purge findings from memory
        del findings

        with open(jsonfile, "w") as jsonfile:
            json.dump(newFindings, jsonfile, indent=4, default=str)

        return True