## Semantic Search over Research Corpus
(Project_22)
<!--
Discuss: Value proposition: Your will propose a machine learning system that can be
used in an existing business or service. (You should not propose a system in which
a new business or service would be developed around the machine learning system.)
Describe the value proposition for the machine learning system. What’s the (non-ML)
status quo used in the business or service? What business metric are you going to be
judged on? (Note that the “service” does not have to be for general users; you can
propose a system for a science problem, for example.)
-->

1. Our business or service is to provide an easier way for users to find relevant research papers from a vast corpus using semantic search.
2. The existing Non-ML status quo is arXiv's keywords based search over title, author names and abstract.
3. Business metric would be to Minimize the click through rate over entries from search results, click through rate through to the paper text from these results. Overall, improving search efficiency that is to reduc the time spent on search and serve highly relevant papers based on the search query.


### Contributors

| Name                            | Responsible for | Link to team members' commits in this repo |
|---------------------------------|-----------------|------------------------------------|
| Preetham Rakshith Prakash | Continuous X | https://github.com/Yugesh1620/Neura-Scholar/commits/main/?author=th-blitz |
| Riya Garg | Data pipeline | https://github.com/Yugesh1620/Neura-Scholar/commits/main/?author=riyagarg30 |
| Pranav Bhatt | Model serving and monitoring platforms | https://github.com/Yugesh1620/Neura-Scholar/commits/main/?author=pranav-bhatt |
| Yugesh Panta | Model training and training platforms | https://github.com/Yugesh1620/Neura-Scholar/commits/main/?author=Yugesh1620 |



### System diagram

<!-- Overall digram of system. Doesn't need polish, does need to show all the pieces.
Must include: all the hardware, all the containers/software platforms, all the models,
all the data. -->

![System Diagram](System%20Diagram.png)

### Summary of outside materials

<!-- In a table, a row for each dataset, foundation model.
Name of data/model, conditions under which it was created (ideally with links/references),
conditions under which it may be used. -->

|              | How it was created | Conditions of use |
|--------------|--------------------|-------------------|
| arXiv Dataset (PDFs) | [From arXiv's bulk access API](https://info.arxiv.org/help/bulk_data/index.html) | [arxiv's nonexclusive-distrib/1.0 license](https://arxiv.org/licenses/nonexclusive-distrib/1.0/license.html) for most individual papers, unknown for the rest
| arXiv Dataset (Metadata) | [From arXiv's kaggle dataset](https://www.kaggle.com/datasets/Cornell-University/arxiv) | [Creative Commons CC0 1.0 Universal Public Domain Dedication](https://creativecommons.org/publicdomain/zero/1.0) for the metadata only
| Script to pull in arXiv PDFs in bulk | A third party script called [mattbierbaum/arxiv-public-datasets](https://github.com/mattbierbaum/arxiv-public-datasets) to pull in arXiv Dataset in bulk from arXiv's bulk access API or Google bucket or AWS bucket and to generate plain text | [MIT License](https://github.com/mattbierbaum/arxiv-public-datasets/blob/master/LICENSE) |
| Base Embed Model | [Linq-AI-Research/Linq-Embed-Mistral](https://huggingface.co/Linq-AI-Research/Linq-Embed-Mistral) | Creative Commons Attribution Non Commercial 4.0 |
| BART (facebook/bart-large-cnn or philschmid/bart-large-cnn-samsum) | Pretrained by Facebook on CNN/DailyMail and/or SAMSum datasets, a Large language model with encoder-decoder structure. Hosted on [huggingface](https://huggingface.co/facebook/bart-large). | MIT License (Samsum variant) or Fairseq license for BART. Free for research use. |
| etc          | | |


### Summary of infrastructure requirements

<!-- Itemize all your anticipated requirements: What (`m1.medium` VM, `gpu_mi100`),
how much/when, justification. Include compute, floating IPs, persistent storage.
The table below shows an example, it is not a recommendation. -->

| Requirement     | How many/when                                     | Justification |
|-----------------|---------------------------------------------------|---------------|
| `m1.medium` VMs | 1 for the entire project duration, 2 more during final setup | For hosting a 1 conventional DB, 1 for a vector DB and 1 as a proxy |
| `compute_liqid` node with 2 GPUs OR `gpu_mi100` node with 2 GPUs | 1 node with 2 a100s for 20 hours a week ( 2x 4 hour blocks and 2x 6 hour blocks a week ) | Hosting a Ray cluster for training and serving models |
| `compute_liqid` or `gpu_mi100` or `rtx8000` node with 1 GPU | For the entire project duration | For training and serving models under development |
| Persistent Storage | 120 GB for entire project duration | Needed to persist models, database, training datasets, metrics etc |
| Floating IPs | 1 for entire project duration | 1 for everything ( gateway, dashboards etc ) |

<!--
| `m1.medium` VMs | 3 for entire project duration                     | ...           |
| `gpu_mi100` GPUs | 4 hour block four times a week |               |
| Persistent Storage | 120 GB for project duration | Needed to persist datasets, models, metrics, etc. |
| Floating IPs    | 1 for entire project duration, 1 for sporadic use |               |
| etc             |                                                   |               |
-->

### Detailed design plan

<!-- In each section, you should describe (1) your strategy, (2) the relevant parts of the
diagram, (3) justification for your strategy, (4) relate back to lecture material,
(5) include specific numbers. -->



#### Model training and training platforms

<!-- Make sure to clarify how you will satisfy the Unit 4 and Unit 5 requirements,
and which optional "difficulty" points you are attempting. -->

Our project focuses on information retrival based on semantic search. In this case retrival of relevant research papers from queries from a corpus and summarizing them to save time or click-throughs within search results.

For this we finetune 2 types of models for this project:
1. An Embed Model to generate embeddings of the corpus. The embeds are indexed and hosted on a vector DB. Whenever users submit thier search queries, the queires are embedded with this model and looked up in the vector DB to retrieve relevant papers.
2. A Summarizer Model to summarize the top K papers from the search results.

We plan to choose pre-trained models such as (mxbai, BART etc), then quantize & optimize the models for inference performance, and fine-tune them using our corpus dataset against a gold standard model, for example : Linq-Embed-Mistral and BART as a gold standard embed & summarizer models.

Platforms using for training jobs:
1. Ray to partition GPU compute resources and submit jobs.
2. MLflow & wandb to track or log training sessions and versioning models.  


#### Model serving and monitoring platforms

<!-- Make sure to clarify how you will satisfy the Unit 6 and Unit 7 requirements,
and which optional "difficulty" points you are attempting. -->

The embed and summarizer models are served as an API endpoint within a internal network running on GPU nodes ( or CPU nodes ) with a Triton backend. This endpoint is only accessible internally.

Both conventional DB ( i.e. SQL ) and Vector DB ( i.e. Faiss ) are served on CPU nodes as an API endpoint within the network.

These internal endpoints can be used to handle the system flow such as generating embeddings, vector DB lookups, SQL queries, and generating summaries.

A gateway node exposed to the public is used to handle requests to and from within the system.

Platforms used:
1. Docker to containerize software (i.e. DBs, models, monitoring platforms etc)
2. Triton backend for serving both models seperately in onnx format.
3. FastAPI to implement a gateway that interacts with serving models, and databases.

#### Data pipeline

<!-- Make sure to clarify how you will satisfy the Unit 8 requirements,  and which
optional "difficulty" points you are attempting. -->

A datapipeline that handles requests and transfer of information between Model endpoints, and the databases with low latency.

1. A persistent storage of 120 GB for the complete project.
2. A conventional DB ( i.e. SQL ) running on a m1.medium sharing a partition with the persistent storage of around 40GB ( Offline data ).
3. This conventional DB will house all of our dataset that is (a) the corpus of research papers in pdfs, and (b) it's metadata in text.
4. A Vector DB with it's partition of 30 GB to store embeddings of the corpus metadata. ( Offline data )
5. A second partition in our Vector DB of around 20 GB for gradual replacement of embeddings from a new model. ( Offline data )
6. Dataset for re-training ( Offline data ) will be used from the conventional DB itself.
7. The only Online data in our pipeline would be the user quries coming in as requests from the gateway, and the summaries generated by our summarizer model.

#### Continuous X

<!-- Make sure to clarify how you will satisfy the Unit 3 requirements,  and which
optional "difficulty" points you are attempting. -->

We plan to use PythonCHI for installation, configuration and deployment of our infrastructure, versioned as Git.

Implementation of a CI/CD pipeline to re-train, run tests and deploy our models.

Finally, setting up staging environment for the model deployment.



