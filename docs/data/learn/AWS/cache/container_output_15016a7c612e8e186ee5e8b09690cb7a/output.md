<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The lists above for instance families, additional capabilities, etc.. are non-exhaustive. Two particular classes of compute resource that are important to enterprise but not listed above are ...

 1. dedicated instances: Your EC2 instances are guaranteed to run on physical machines exclusive to you, meaning no other AWS customer will have an EC2 instances on those physical machines. However, there may be multiple physical machines running your EC2 instances. For example, if you were to ask for 2 large and 6 small m6in instance types, one of the large instances could be on physical machine A while the other large and small instances could be on physical machine B. AWS decides which physical machine runs what and instances can hop between physical machines on restart, but all physical machines are guaranteed to only be running your instances (no other AWS customer will be running instances on those phsyical machines).

 2. dedicated hosts: Your EC2 instances are guaranteed to *always run on the same* physical machine, which is exclusive to you. That is, you rent the machine and decide how you want it split up into instances.
</div>

