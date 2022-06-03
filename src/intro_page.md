# What I Did Last Week

Welcome! This service builds a weeklog of all the different activities you spent time on in the last 7 days.  


We access

* Jira (server)
* Zendesk
* Freshdesk (ddna ticketing system)

using the email supplied when you log into Google. We then look at all the tickets _assigned to you_ that have been updated in the last 7 days. (> current_date - 7 days)  
Then we go through all the recorded time entries (from the last 7 days) on those tickets and total it all up. This helps distinguish from tickets that have just been updated by the system (e.g. auto-close) and ones we've actually worked on. And also helps identify if I've forgotten to log time on any.

Additionally, if you provide consent:

* Google calendar meetings.

Any meetings with matching names have their time smooshed into a single entry.
We don't store any of this, so you'll need to log in again each time you visit the service.

To emphasise, this is not a reporting tool - it's entirely possible that between time logged in GCal, Jira, and FD/ZD that I can record time the same piece of work in 3 different places.  
It is purely intended to help remind you "What I Did Last Week". 

[Source code](https://github.com/ctri-the-third/what-i-did-last-week)


## Get started

Press the link below to begin.
Note, after logging in the service may take ~2-3 minutes to build the report. It's a raspberry pi and I've not implemented async web requests yet.

**[Click me to login & execute]({url})**

{envs}