# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

class Plan:
    key =''
    def __init__(self, shardId, planId, name, description,  duration, avgRequestsPerUser, totalUsers):
        
        self.shardId = shardId
        self.planId = planId
        self.key = shardId + ':' +  planId
        self.name = name
        self.description = description
        self.duration = duration
        self.avgRequestsPerUser = avgRequestsPerUser
        self.totalUsers = totalUsers
        

                

        

               

        
