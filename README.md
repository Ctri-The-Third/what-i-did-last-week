
# What-I-Did-Last-Week

A script that checks against various services to automatically generate a weeklog for you.

[![PyTest](https://github.com/Ctri-The-Third/PythonTemplate/actions/workflows/main.yml/badge.svg)](https://github.com/Ctri-The-Third/PythonTemplate/actions/workflows/main.yml)

- [Overview](#Overview)
- [Environment setup](#Setup)
- [Deployment](#Deploy)


# Overview

This script checks through configured Zendesk, Freshdesk, and Jira instances and compares ticket assignees with the specified email address of a user, updated in the last week.
On finding a matching a ticket, it identifies time logged against the ticket from the last week and compiles a list for each of the services.

# Environment setup

the following environment variables are needed. 

| variable name | sample value | 
| --- | --- | 
| FRESHDESK_HOST | sample.freshdesk.com | 
| FRESHDESK_KEY | AlPh4NuM3r1cStR1Ng | 
| JIRA_HOST_1 | jira.domain.com | 
| JIRA_KEY_1 | YSBzaG9ydGVyIGJhc2UgNjQgZW5jb2RlZCBhcGkga2V5Lg== | 
| ZENDESK_HOST | subdomain.zendesk.com | 
| ZENDESK_KEY | SGVsbG8gd29ybGQhIFRoaXMgaXMgYSBsb25nIGJhc2UgNjQgZW5jb2RlZCBhcGkga2V5Lg==  | 

Additionally, [version 2.2+ of the HexHelpers](https://github.com/ctri-the-third/servicehelpers) are to be installed alongside the modules listed in the `requirements.txt` file

# Deployment

```
git clone git@github.com:Ctri-The-Third/what-i-did-last-week.git

wget https://github.com/Ctri-The-Third/ServiceHelpers/releases/download/v2.2.0/hex_helpers-2.2.0-py3-none-any.whl -O hex_helpers-2.2.0-py3-none-any.whl

pip install ./hex_helpers-2.2.0-py3-none-any.whl

pip install -r requirements.txt
```

# Execution

From the installed directory:
```
python3 ./main.py
```