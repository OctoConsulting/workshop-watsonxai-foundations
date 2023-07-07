# Product Lab 1 - Watson Code Assistant and Ansible Lightspeed

### Introduction
In this lab, you will become familiar with the capabilities of IBM's new AI-assisted IT Automation technology pattern: Watson Code Assistant (WCA). WCA is built on Watsonx.ai and uses a Foundation Model managed by IBM Research.  This model is capable of generating Ansible YAML playbooks from natural Language and is made available as a VSCode extension called "Ansible Lightspeed with IBM Watson Code Assistant".

Future capabilities will be released (target 4Q 2023) with Watson Code Assistant; including ability to generate RH Deployment YAMLs from Natural Language, and the ability to customize the model for your environment. In the future it will also be possible to install Watson Code Assistant on-prem. Next year (target 1Q 2024), Watson Code Assistant will be able to help modernize applications with COBOL-to-Java conversion capability.

Demo playbacks and additional information can be found on the [AI Assisted IT Automation technology pattern pages](https://ai-assisted-it-automation.tech-patterns.techzone.ibm.com/lightspeed-code-assistant)

### What is Watson Code Assistant?
Watch the [WCA product demo](https://www.ibm.com/products/watson-code-assistant)

## Continue this lab or stop?  Depends on your role...
If you're a data scientist then WCA may be less useful for you at-the-moment. However if you're a data engineer or technology engineer working with RedHat OpenShift, you'll be eager to learn about Ansible Lightspeed with IBM Watson Code Assistant.

### What is Ansible Lightspeed with IBM Watson Code Assistant?
Go to this [Keynote address during the AnsibleFest at Red Hat Summit](https://www.youtube.com/watch?v=Ot7JTBwYFk8)
   - Skip to 24:40 to see WCA in practice
   - Stop at 42:20 which ends the WCA session but feel free to keep watching.

### Hands-On with Ansible Lightspeed with IBM Watson Code Assistant?
1. [Install Visual Studio Code (VS Code)](https://code.visualstudio.com/download) if you don't already have it.
2. [Install the WCA extension for VS Code](https://docs.ai.ansible.redhat.com/vscode_guide/installing_vs)
6. Visit the [WCA Tech Preview launch blog post](https://www.ansible.com/blog/welcome-to-the-ansible-lightspeed-technical-preview) and complete any of the exercises at bottom of the blog post.

### Confused, stuck and looking for an Ansible Playbook example?
Unfamiliar with Ansible? Follow these steps to create a Ansible Playbook example of using WCA:
1. Create hybrid_azure.yml in VSCode
2. Copy and paste this yaml from the demo video: https://www.youtube.com/watch?v=Ot7JTBwYFk8 24:40
3. Reproduce steps from this video
   - Go to this [Keynote address during the AnsibleFest at Red Hat Summit](https://www.youtube.com/watch?v=Ot7JTBwYFk8)
   - Skip to 26:00
   - Use the configuration below
   
### Ansible Playbook Example
```
- name: Azure Hybrid Cloud Connectivity Data Lake on Azure
 hosts: localhost
 connection: local
 gather_facts: false
 vars:
  vm_config:
  vm_size: Standard_DS2_v2
  name: ansibull-01
  network_interfaces:
   - name: data-lake831
 tasks:
  # in this prompt, azure is detected from context & fully qualified collection name is used (best practice)
  # data is annonymized; update username and path to "rhel"
  # - name: Create VM using vm_config vars
   
- name: Configure Hybrid cloud instance
 hosts: rhel
 become: true
 tasks:
  # - name: Wait 30 secs for port 22 on current hosts
  # setup vpn software
  # - name: Install libreswan package
  # add mode: "644", using builtin ansible docs
  # - name: Copy ipsec_files folder to /etc/ipsec.d
  # - name: Start and enable ipsec service
```
