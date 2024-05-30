'''
# Amazon Bedrock Construct Library

<!--BEGIN STABILITY BANNER-->---


![Stability: Experimental](https://img.shields.io/badge/stability-Experimental-important.svg?style=for-the-badge)

> All classes are under active development and subject to non-backward compatible changes or removal in any
> future version. These are not subject to the [Semantic Versioning](https://semver.org/) model.
> This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

| **Language**     | **Package**        |
|:-------------|-----------------|
|![Typescript Logo](https://docs.aws.amazon.com/cdk/api/latest/img/typescript32.png) TypeScript|`@cdklabs/generative-ai-cdk-constructs`|
|![Python Logo](https://docs.aws.amazon.com/cdk/api/latest/img/python32.png) Python|`cdklabs.generative_ai_cdk_constructs`|

[Amazon Bedrock](https://aws.amazon.com/bedrock/) is a fully managed service that offers a choice of foundation models (FMs) along with a broad set of capabilities for building generative AI applications.

This construct library includes CloudFormation L1 resources to deploy Bedrock features.

## Table of contents

* [API](#api)
* [Knowledge Bases](#knowledge-bases)
* [Agents](#agents)

## API

See the [API documentation](../../../apidocs/modules/bedrock.md).

## Knowledge Bases

With Knowledge Bases for Amazon Bedrock, you can give FMs and agents contextual information from your company’s private data sources for Retrieval Augmented Generation (RAG) to deliver more relevant, accurate, and customized responses.

### Create a Knowledge Base

A vector index on a vector store is required to create a Knowledge Base. This construct currently supports [Amazon OpenSearch Serverless](../opensearchserverless), [Amazon RDS Aurora PostgreSQL](../amazonaurora/), [Pinecone](../pinecone/) . By default, this resource will create an OpenSearch Serverless vector collection and index for each Knowledge Base you create, but you can provide an existing collection and/or index to have more control. For other resources you need to have the vector stores already created and credentials stored in AWS Secrets Manager. For Aurora, the construct provides an option to create a default `AmazonAuroraDefaultVectorStore` construct that will provision the vector store backed by Amazon Aurora for you. To learn more you can read [here](../amazonaurora/README.md).

The resource accepts an `instruction` prop that is provided to any Bedrock Agent it is associated with so the agent can decide when to query the Knowledge Base.

Amazon Bedrock Knowledge Bases currently only supports S3 as a data source. The `S3DataSource` resource is used to configure how the Knowledge Base handles the data source.

Example of `OpenSearch Serverless`:

TypeScript

```python
import * as s3 from 'aws-cdk-lib/aws-s3';
import { bedrock } from '@cdklabs/generative-ai-cdk-constructs';

const kb = new bedrock.KnowledgeBase(this, 'KnowledgeBase', {
  embeddingsModel: bedrock.BedrockFoundationModel.TITAN_EMBED_TEXT_V1,
  instruction: 'Use this knowledge base to answer questions about books. ' +
    'It contains the full text of novels.',
});

const docBucket = new s3.Bucket(this, 'DocBucket');

new bedrock.S3DataSource(this, 'DataSource', {
  bucket: docBucket,
  knowledgeBase: kb,
  dataSourceName: 'books',
  chunkingStrategy: bedrock.ChunkingStrategy.FIXED_SIZE,
  maxTokens: 500,
  overlapPercentage: 20,
});
```

Python

```python

from aws_cdk import (
    aws_s3 as s3,
)
from cdklabs.generative_ai_cdk_constructs import (
    bedrock
)

kb = bedrock.KnowledgeBase(self, 'KnowledgeBase',
            embeddings_model= bedrock.BedrockFoundationModel.TITAN_EMBED_TEXT_V1,
            instruction=  'Use this knowledge base to answer questions about books. ' +
    'It contains the full text of novels.'
        )

docBucket = s3.Bucket(self, 'DockBucket')

bedrock.S3DataSource(self, 'DataSource',
    bucket= docBucket,
    knowledge_base=kb,
    data_source_name='books',
    chunking_strategy= bedrock.ChunkingStrategy.FIXED_SIZE,
    max_tokens=500,
    overlap_percentage=20
)

```

Example of `Amazon RDS Aurora PostgreSQL` (manual, you must have Amazon RDS Aurora PostgreSQL already created):

TypeScript

```python
import * as s3 from 'aws-cdk-lib/aws-s3';
import { amazonaurora, bedrock } from '@cdklabs/generative-ai-cdk-constructs';

const auroraDbManual = new amazonaurora.AmazonAuroraVectorStore(
  {
    resourceArn: 'arn:aws:rds:your-region:123456789876:cluster:aurora-cluster-manual',
    databaseName: 'bedrock_vector_db',
    tableName: 'bedrock_integration.bedrock_kb',
    credentialsSecretArn: 'arn:aws:secretsmanager:your-region:123456789876:secret:your-key-name',
    primaryKeyField: 'id',
    vectorField: 'embedding',
    textField: 'chunks',
    metadataField: 'metadata',
  });

const kb = new bedrock.KnowledgeBase(this, 'KnowledgeBase', {
  vectorStore: auroraDbManual,
  embeddingsModel: bedrock.BedrockFoundationModel.COHERE_EMBED_ENGLISH_V3,
  instruction: 'Use this knowledge base to answer questions about books. ' +
    'It contains the full text of novels.',
});

const docBucket = new s3.Bucket(this, 'DocBucket');

new bedrock.S3DataSource(this, 'DataSource', {
  bucket: docBucket,
  knowledgeBase: kb,
  dataSourceName: 'books',
  chunkingStrategy: bedrock.ChunkingStrategy.FIXED_SIZE,
  maxTokens: 500,
  overlapPercentage: 20,
});
```

Python

```python

from aws_cdk import (
    aws_s3 as s3,
)
from cdklabs.generative_ai_cdk_constructs import (
    bedrock,
    amazonaurora
)

aurora = amazonaurora.AmazonAuroraVectorStore(
    credentials_secret_arn='arn:aws:secretsmanager:your-region:123456789876:secret:your-key-name',
    database_name='bedrock_vector_db',
    metadata_field='metadata',
    primary_key_field='id',
    resource_arn='arn:aws:rds:your-region:123456789876:cluster:aurora-cluster-manual',
    table_name='bedrock_integration.bedrock_kb',
    text_field='chunks',
    vector_field='embedding',
)

kb = bedrock.KnowledgeBase(self, 'KnowledgeBase',
            vector_store= aurora,
            embeddings_model= bedrock.BedrockFoundationModel.COHERE_EMBED_ENGLISH_V3,
            instruction=  'Use this knowledge base to answer questions about books. ' +
    'It contains the full text of novels.'
        )

docBucket = s3.Bucket(self, 'DockBucket')

bedrock.S3DataSource(self, 'DataSource',
    bucket= docBucket,
    knowledge_base=kb,
    data_source_name='books',
    chunking_strategy= bedrock.ChunkingStrategy.FIXED_SIZE,
    max_tokens=500,
    overlap_percentage=20
)

```

Example of `Amazon RDS Aurora PostgreSQL` (default):

TypeScript

```python
import * as s3 from 'aws-cdk-lib/aws-s3';
import { amazonaurora, bedrock } from '@cdklabs/generative-ai-cdk-constructs';

const auroraDb = new amazonaurora.AmazonAuroraDefaultVectorStore(this, 'AuroraDefaultVectorStore', {
  embeddingsModelVectorDimension: BedrockFoundationModel.COHERE_EMBED_ENGLISH_V3.vectorDimensions!,
});

const kb = new bedrock.KnowledgeBase(this, 'KnowledgeBase', {
  vectorStore: auroraDb,
  embeddingsModel: bedrock.BedrockFoundationModel.COHERE_EMBED_ENGLISH_V3,
  instruction: 'Use this knowledge base to answer questions about books. ' +
    'It contains the full text of novels.',
});

const docBucket = new s3.Bucket(this, 'DocBucket');

new bedrock.S3DataSource(this, 'DataSource', {
  bucket: docBucket,
  knowledgeBase: kb,
  dataSourceName: 'books',
  chunkingStrategy: bedrock.ChunkingStrategy.FIXED_SIZE,
  maxTokens: 500,
  overlapPercentage: 20,
});
```

Python

```python

from aws_cdk import (
    aws_s3 as s3,
)
from cdklabs.generative_ai_cdk_constructs import (
    bedrock,
    amazonaurora
)

dimension = bedrock.BedrockFoundationModel.COHERE_EMBED_ENGLISH_V3.vector_dimensions

aurora = amazonaurora.AmazonAuroraDefaultVectorStore(self, 'AuroraDefaultVectorStore',
    embeddings_model_vector_dimension=dimension
)

kb = bedrock.KnowledgeBase(self, 'KnowledgeBase',
            vector_store= aurora,
            embeddings_model= bedrock.BedrockFoundationModel.COHERE_EMBED_ENGLISH_V3,
            instruction=  'Use this knowledge base to answer questions about books. ' +
    'It contains the full text of novels.'
        )

docBucket = s3.Bucket(self, 'DockBucket')

bedrock.S3DataSource(self, 'DataSource',
    bucket= docBucket,
    knowledge_base=kb,
    data_source_name='books',
    chunking_strategy= bedrock.ChunkingStrategy.FIXED_SIZE,
    max_tokens=500,
    overlap_percentage=20
)
```

Example of `Pinecone` (manual, you must have Pinecone vector store created):

TypeScript

```python
import * as s3 from 'aws-cdk-lib/aws-s3';
import { pinecone, bedrock } from '@cdklabs/generative-ai-cdk-constructs';

const pineconeds = new pinecone.PineconeVectorStore({
  connectionString: 'https://your-index-1234567.svc.gcp-starter.pinecone.io',
  credentialsSecretArn: 'arn:aws:secretsmanager:your-region:123456789876:secret:your-key-name',
  textField: 'question',
  metadataField: 'metadata'
});

const kb = new bedrock.KnowledgeBase(this, 'KnowledgeBase', {
  vectorStore: pineconeds,
  embeddingsModel: bedrock.BedrockFoundationModel.TITAN_EMBED_TEXT_V1,
  instruction: 'Use this knowledge base to answer questions about books. ' +
    'It contains the full text of novels.',
});

const docBucket = new s3.Bucket(this, 'DocBucket');

new bedrock.S3DataSource(this, 'DataSource', {
  bucket: docBucket,
  knowledgeBase: kb,
  dataSourceName: 'books',
  chunkingStrategy: bedrock.ChunkingStrategy.FIXED_SIZE,
  maxTokens: 500,
  overlapPercentage: 20,
});
```

Python

```python

from aws_cdk import (
    aws_s3 as s3,
)
from cdklabs.generative_ai_cdk_constructs import (
    bedrock,
    pinecone
)

pineconevs = pinecone.PineconeVectorStore(
            connection_string='https://your-index-1234567.svc.gcp-starter.pinecone.io',
            credentials_secret_arn='arn:aws:secretsmanager:your-region:123456789876:secret:your-key-name',
            text_field='question',
            metadata_field='metadata'
        )

kb = bedrock.KnowledgeBase(self, 'KnowledgeBase',
            vector_store= pineconevs,
            embeddings_model= bedrock.BedrockFoundationModel.COHERE_EMBED_ENGLISH_V3,
            instruction=  'Use this knowledge base to answer questions about books. ' +
    'It contains the full text of novels.'
        )

docBucket = s3.Bucket(self, 'DockBucket')

bedrock.S3DataSource(self, 'DataSource',
    bucket= docBucket,
    knowledge_base=kb,
    data_source_name='books',
    chunking_strategy= bedrock.ChunkingStrategy.FIXED_SIZE,
    max_tokens=500,
    overlap_percentage=20
)
```

## Agents

Enable generative AI applications to execute multistep tasks across company systems and data sources.

### Create an Agent

The following example creates an Agent with a simple instruction and default prompts that consults a Knowledge Base.

TypeScript

```python
const agent = new bedrock.Agent(this, 'Agent', {
  foundationModel: bedrock.BedrockFoundationModel.ANTHROPIC_CLAUDE_V2_1,
  instruction: 'You are a helpful and friendly agent that answers questions about literature.',

});

agent.addKnowledgeBase([kb]);
```

Python

```python
agent = bedrock.Agent(
    self,
    "Agent",
    foundation_model=bedrock.BedrockFoundationModel.ANTHROPIC_CLAUDE_V2_1,
    instruction="You are a helpful and friendly agent that answers questions about insurance claims.",
)
  agent.add_knowledge_base(kb);
```

### Action Groups

An action group defines functions your agent can call. The functions are Lambda functions. The action group uses an OpenAPI schema to tell the agent what your functions do and how to call them.

```python
const actionGroupFunction = new lambda_python.PythonFunction(this, 'ActionGroupFunction', {
  runtime: lambda.Runtime.PYTHON_3_12,
  entry: path.join(__dirname, '../lambda/action-group'),
});

const actionGroup = new bedrock.AgentActionGroup(this,'MyActionGroup',{
  actionGroupName: 'query-library',
  description: 'Use these functions to get information about the books in the library.',
  actionGroupExecutor: actionGroupFunction,
  actionGroupState: "ENABLED",
  apiSchema: bedrock.ApiSchema.fromAsset(path.join(__dirname, 'action-group.yaml')),
});

agent.addActionGroup(actionGroup);
```

Python

```python

action_group_function = PythonFunction(
            self,
            "LambdaFunction",
            runtime=Runtime.PYTHON_3_12,
            entry="./lambda",
            index="app.py",
            handler="lambda_handler",
)

actionGroup = bedrock.AgentActionGroup(self,
    "MyActionGroup",
    action_group_name="query-library",
    description="Use these functions to get information about the books in the library.",
    action_group_executor=action_group_function,
    action_group_state="ENABLED",
    api_schema=bedrock.ApiSchema.from_asset("action-group.yaml"))

agent.add_action_group(actionGroup)
```

### Prepare the Agent

The `Agent`  constructs take an optional parameter `shouldPrepareAgent` to indicate that the Agent should be prepared after any updates to an agent, Knowledge Base association, or action group. This may increase the time to create and update those resources. By default, this value is false .

Creating an agent alias will not prepare the agent, so if you create an alias with `addAlias` or by providing an `aliasName` when creating the agent then you should set `shouldPrepareAgent` to ***true***.

#### Prompt Overrides

Bedrock Agents allows you to customize the prompts and LLM configuration for its different steps. You can disable steps or create a new prompt template. Prompt templates can be inserted from plain text files.

TypeScript

```python
import { readFileSync } from 'fs';

const orchestration = readFileSync('prompts/orchestration.txt', 'utf-8');
const agent = new bedrock.Agent(this, 'Agent', {
  foundationModel: bedrock.BedrockFoundationModel.ANTHROPIC_CLAUDE_V2_1,
  instruction: "You are a helpful and friendly agent that answers questions about literature.",
  promptOverrideConfiguration: {
    promptConfigurations: [
      {
        promptType: bedrock.PromptType.PRE_PROCESSING,
        promptState: bedrock.PromptState.DISABLED,
        promptCreationMode:  bedrock.PromptCreationMode.OVERRIDDEN,
        basePromptTemplate: "disabled",
        inferenceConfiguration: {
          temperature:  0.0,
          topP: 1,
          topK: 250,
          maximumLength: 1,
          stopSequences: ['\n\nHuman:'],
        }
      },
      {
        promptType: bedrock.PromptType.ORCHESTRATION,
        basePromptTemplate: orchestration,
        promptState: bedrock.PromptState.ENABLED,
        promptCreationMode:  bedrock.PromptCreationMode.OVERRIDDEN,
        inferenceConfiguration: {
          temperature:  0.0,
          topP: 1,
          topK: 250,
          maximumLength: 2048,
          stopSequences: ['</invoke>', '</answer>', '</error>'],
        },
      },
    ]
  }
});
```

Python

```python
orchestration = open('prompts/orchestration.txt', encoding="utf-8").read()
agent = bedrock.Agent(self, "Agent",
            foundation_model=bedrock.BedrockFoundationModel.ANTHROPIC_CLAUDE_V2_1,
            instruction="You are a helpful and friendly agent that answers questions about insurance claims.",
            prompt_override_configuration= bedrock.PromptOverrideConfiguration(
                prompt_configurations=[
                    bedrock.PromptConfiguration(
                        prompt_type=bedrock.PromptType.PRE_PROCESSING,
                        prompt_state=bedrock.PromptState.DISABLED,
                        prompt_creation_mode=bedrock.PromptCreationMode.OVERRIDDEN,
                        base_prompt_template="disabled",
                        inference_configuration=bedrock.InferenceConfiguration(
                            temperature=0.0,
                            top_k=250,
                            top_p=1,
                            maximum_length=1,
                            stop_sequences=['\n\nHuman:'],
                        )
                    ),
                    bedrock.PromptConfiguration(
                        prompt_type=bedrock.PromptType.ORCHESTRATION,
                        prompt_state=bedrock.PromptState.ENABLED,
                        prompt_creation_mode=bedrock.PromptCreationMode.OVERRIDDEN,
                        base_prompt_template=orchestration,
                        inference_configuration=bedrock.InferenceConfiguration(
                            temperature=0.0,
                            top_k=250,
                            top_p=1,
                            maximum_length=2048,
                            stop_sequences=['</invoke>', '</answer>', '</error>'],
                        )
                    )
                ]
            ),
        )
```

### Agent Alias

After you have sufficiently iterated on your working draft and are satisfied with the behavior of your agent, you can set it up for deployment and integration into your application by creating aliases of your agent.

To deploy your agent, you need to create an alias. During alias creation, Amazon Bedrock automatically creates a version of your agent. The alias points to this newly created version. You can point the alias to a previously created version if necessary. You then configure your application to make API calls to that alias.

By default, the `Agent` resource does not create any aliases, and you can use the 'DRAFT' version.

#### Tracking the latest version

The `Agent` resource optionally takes an `aliasName` property that, if defined, will create an Alias that creates a new version on every change.

TypeScript

```python
const agent = new bedrock.Agent(this, 'Agent', {
  foundationModel: bedrock.BedrockFoundationModel.ANTHROPIC_CLAUDE_V2_1,
  instruction: 'You are a helpful and friendly agent that answers questions about literature.',
  knowledgeBases: [kb],
  aliasName: 'latest',
});
```

Python

```python
agent = bedrock.Agent(
    self,
    "Agent",
    foundation_model=bedrock.BedrockFoundationModel.ANTHROPIC_CLAUDE_V2_1,
    instruction="You are a helpful and friendly agent that answers questions about insurance claims.",
    knowledge_bases= [kb],
    alias_name='latest'
)
```

#### Specific version

Using the `addAlias` method you can create aliases with a specific agent version.

TypeScript

```python
agent.addAlias({
  aliasName: 'prod',
  agentVersion: '12',
});
```

Python

```python
agent.add_alias(
    alias_name='prod',
    agent_version='12'
)
```

Alternatively, you can use the `AgentAlias` resource if you want to create an Alias for an existing Agent.

TypeScript

```python
const alias = new bedrock.AgentAlias(this, 'ProdAlias', {
  agentId:  'ABCDE12345',
  aliasName: 'prod',
  agentVersion: '12',
});
```

Python

```python
alias = bedrock.AgentAlias(self, 'ProdAlias',
    agent_id='ABCDE12345',
    alias_name='prod',
    agent_version='12'
)
```
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_bedrock as _aws_cdk_aws_bedrock_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_kms as _aws_cdk_aws_kms_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import constructs as _constructs_77d1e7e8
from ..amazonaurora import (
    AmazonAuroraDefaultVectorStore as _AmazonAuroraDefaultVectorStore_ec1da9eb,
    AmazonAuroraVectorStore as _AmazonAuroraVectorStore_bde12a1e,
)
from ..opensearch_vectorindex import VectorIndex as _VectorIndex_e5d266e9
from ..opensearchserverless import VectorCollection as _VectorCollection_91bfdaa9
from ..pinecone import PineconeVectorStore as _PineconeVectorStore_c017c196


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.AddAgentAliasProps",
    jsii_struct_bases=[],
    name_mapping={
        "alias_name": "aliasName",
        "agent_version": "agentVersion",
        "description": "description",
    },
)
class AddAgentAliasProps:
    def __init__(
        self,
        *,
        alias_name: builtins.str,
        agent_version: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties to add an Alias to an Agent.

        :param alias_name: (experimental) The name for the agent alias.
        :param agent_version: (experimental) The version of the agent to associate with the agent alias. Default: - Creates a new version of the agent.
        :param description: (experimental) Description for the agent alias.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b44b9cf8594977e12593faffc73197189c6b8c803579e66de51dc986e13c8d2a)
            check_type(argname="argument alias_name", value=alias_name, expected_type=type_hints["alias_name"])
            check_type(argname="argument agent_version", value=agent_version, expected_type=type_hints["agent_version"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "alias_name": alias_name,
        }
        if agent_version is not None:
            self._values["agent_version"] = agent_version
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def alias_name(self) -> builtins.str:
        '''(experimental) The name for the agent alias.

        :stability: experimental
        '''
        result = self._values.get("alias_name")
        assert result is not None, "Required property 'alias_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def agent_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The version of the agent to associate with the agent alias.

        :default: - Creates a new version of the agent.

        :stability: experimental
        '''
        result = self._values.get("agent_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Description for the agent alias.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddAgentAliasProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Agent(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.Agent",
):
    '''(experimental) Deploy a Bedrock Agent.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        foundation_model: "BedrockFoundationModel",
        instruction: builtins.str,
        action_groups: typing.Optional[typing.Sequence["AgentActionGroup"]] = None,
        alias_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        enable_user_input: typing.Optional[builtins.bool] = None,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        existing_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
        idle_session_ttl: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        knowledge_bases: typing.Optional[typing.Sequence["KnowledgeBase"]] = None,
        name: typing.Optional[builtins.str] = None,
        prompt_override_configuration: typing.Optional[typing.Union["PromptOverrideConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        should_prepare_agent: typing.Optional[builtins.bool] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param foundation_model: (experimental) The Bedrock text foundation model for the agent to use.
        :param instruction: (experimental) A narrative instruction to provide the agent as context.
        :param action_groups: (experimental) AgentActionGroup to make available to the agent. Default: - No AgentActionGroup is used.
        :param alias_name: (experimental) Name of the alias for the agent. Default: - No alias is created.
        :param description: (experimental) A description of the agent. Default: - No description is provided.
        :param enable_user_input: (experimental) Select whether the agent can prompt additional information from the user when it does not have enough information to respond to an utterance. Default: - False
        :param encryption_key: (experimental) KMS encryption key to use for the agent. Default: - An AWS managed key is used.
        :param existing_role: (experimental) The existing IAM Role for the agent with a trust policy that allows the Bedrock service to assume the role.
        :param idle_session_ttl: (experimental) How long sessions should be kept open for the agent. Default: - 1 hour
        :param knowledge_bases: (experimental) Knowledge Bases to make available to the agent. Default: - No knowledge base is used.
        :param name: (experimental) The name of the agent. Default: - A name is automatically generated.
        :param prompt_override_configuration: (experimental) Overrides for the agent. Default: - No overrides are provided.
        :param should_prepare_agent: (experimental) Whether to prepare the agent for use. Default: - false
        :param tags: (experimental) OPTIONAL: Tag (KEY-VALUE) bedrock agent resource. Default: - false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__627af24bb5e1ca4b3ebb82ecbd7a3f01cb1f5177248afdccbc1d0ffab70726de)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AgentProps(
            foundation_model=foundation_model,
            instruction=instruction,
            action_groups=action_groups,
            alias_name=alias_name,
            description=description,
            enable_user_input=enable_user_input,
            encryption_key=encryption_key,
            existing_role=existing_role,
            idle_session_ttl=idle_session_ttl,
            knowledge_bases=knowledge_bases,
            name=name,
            prompt_override_configuration=prompt_override_configuration,
            should_prepare_agent=should_prepare_agent,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addActionGroup")
    def add_action_group(self, action_group: "AgentActionGroup") -> None:
        '''(experimental) Add action group to the agent.

        :param action_group: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__417f1714f331f713e989d70b6417dbb800ceedf7de8245c42ba72cde605b3504)
            check_type(argname="argument action_group", value=action_group, expected_type=type_hints["action_group"])
        return typing.cast(None, jsii.invoke(self, "addActionGroup", [action_group]))

    @jsii.member(jsii_name="addActionGroups")
    def add_action_groups(
        self,
        action_groups: typing.Sequence["AgentActionGroup"],
    ) -> None:
        '''(experimental) Add action groups to the agent.

        :param action_groups: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd86fd4e92aa0f8ee4a2b95a5ad405d539c55043eec94bf739fcc7fc1455d7a4)
            check_type(argname="argument action_groups", value=action_groups, expected_type=type_hints["action_groups"])
        return typing.cast(None, jsii.invoke(self, "addActionGroups", [action_groups]))

    @jsii.member(jsii_name="addAlias")
    def add_alias(
        self,
        *,
        alias_name: builtins.str,
        agent_version: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> "AgentAlias":
        '''(experimental) Add an alias to the agent.

        :param alias_name: (experimental) The name for the agent alias.
        :param agent_version: (experimental) The version of the agent to associate with the agent alias. Default: - Creates a new version of the agent.
        :param description: (experimental) Description for the agent alias.

        :stability: experimental
        '''
        props = AddAgentAliasProps(
            alias_name=alias_name, agent_version=agent_version, description=description
        )

        return typing.cast("AgentAlias", jsii.invoke(self, "addAlias", [props]))

    @jsii.member(jsii_name="addKnowledgeBase")
    def add_knowledge_base(self, knowledge_base: "KnowledgeBase") -> None:
        '''(experimental) Add knowledge base to the agent.

        :param knowledge_base: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0ea7a1a86c29879ce5949318dae4e0d40df1772332d09e26ac0eebfde38479d)
            check_type(argname="argument knowledge_base", value=knowledge_base, expected_type=type_hints["knowledge_base"])
        return typing.cast(None, jsii.invoke(self, "addKnowledgeBase", [knowledge_base]))

    @jsii.member(jsii_name="addKnowledgeBases")
    def add_knowledge_bases(
        self,
        knowledge_bases: typing.Sequence["KnowledgeBase"],
    ) -> None:
        '''(experimental) Add knowledge bases to the agent.

        :param knowledge_bases: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca2617bd17ab91665385e57477c5d00b6dfffcd0be05ebe697f1f2d4ff1abc87)
            check_type(argname="argument knowledge_bases", value=knowledge_bases, expected_type=type_hints["knowledge_bases"])
        return typing.cast(None, jsii.invoke(self, "addKnowledgeBases", [knowledge_bases]))

    @builtins.property
    @jsii.member(jsii_name="agentArn")
    def agent_arn(self) -> builtins.str:
        '''(experimental) The ARN of the agent.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "agentArn"))

    @builtins.property
    @jsii.member(jsii_name="agentId")
    def agent_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the agent.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "agentId"))

    @builtins.property
    @jsii.member(jsii_name="agentInstance")
    def agent_instance(self) -> _aws_cdk_aws_bedrock_ceddda9d.CfnAgent:
        '''(experimental) Instance of Agent.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_bedrock_ceddda9d.CfnAgent, jsii.get(self, "agentInstance"))

    @builtins.property
    @jsii.member(jsii_name="agentversion")
    def agentversion(self) -> builtins.str:
        '''(experimental) The version for the agent.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "agentversion"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) The name of the agent.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> _aws_cdk_aws_iam_ceddda9d.Role:
        '''(experimental) The IAM role for the agent.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Role, jsii.get(self, "role"))

    @builtins.property
    @jsii.member(jsii_name="aliasArn")
    def alias_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ARN of the agent alias.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aliasArn"))

    @builtins.property
    @jsii.member(jsii_name="aliasId")
    def alias_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) The unique identifier of the agent alias.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aliasId"))

    @builtins.property
    @jsii.member(jsii_name="aliasName")
    def alias_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name for the agent alias.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aliasName"))

    @builtins.property
    @jsii.member(jsii_name="actionGroups")
    def action_groups(
        self,
    ) -> typing.List[_aws_cdk_aws_bedrock_ceddda9d.CfnAgent.AgentActionGroupProperty]:
        '''(experimental) A list of action groups associated with the agent.

        :stability: experimental
        :private: true
        '''
        return typing.cast(typing.List[_aws_cdk_aws_bedrock_ceddda9d.CfnAgent.AgentActionGroupProperty], jsii.get(self, "actionGroups"))

    @action_groups.setter
    def action_groups(
        self,
        value: typing.List[_aws_cdk_aws_bedrock_ceddda9d.CfnAgent.AgentActionGroupProperty],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__362bb8b9135358d9388689544abcd0d0c9e8e45ae46a6dc95b075f20007b92ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actionGroups", value)

    @builtins.property
    @jsii.member(jsii_name="knowledgeBases")
    def knowledge_bases(
        self,
    ) -> typing.List[_aws_cdk_aws_bedrock_ceddda9d.CfnAgent.AgentKnowledgeBaseProperty]:
        '''(experimental) A list of KnowledgeBases associated with the agent.

        :default: - No knowledge base is used.

        :stability: experimental
        '''
        return typing.cast(typing.List[_aws_cdk_aws_bedrock_ceddda9d.CfnAgent.AgentKnowledgeBaseProperty], jsii.get(self, "knowledgeBases"))

    @knowledge_bases.setter
    def knowledge_bases(
        self,
        value: typing.List[_aws_cdk_aws_bedrock_ceddda9d.CfnAgent.AgentKnowledgeBaseProperty],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b8a2ba31fca57d8bfcd42f9f0c012e95f4a9a95f52fe008b4777fe99b12b466)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "knowledgeBases", value)


class AgentActionGroup(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.AgentActionGroup",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        action_group_name: builtins.str,
        action_group_executor: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IFunction] = None,
        action_group_state: typing.Optional[builtins.str] = None,
        api_schema: typing.Optional["ApiSchema"] = None,
        description: typing.Optional[builtins.str] = None,
        parent_action_group_signature: typing.Optional[builtins.str] = None,
        skip_resource_in_use_check_on_delete: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param action_group_name: (experimental) The name of the action group. Default: - a name is generated by CloudFormation.
        :param action_group_executor: (experimental) The Lambda function containing the business logic that is carried out upon invoking the action.
        :param action_group_state: (experimental) Specifies whether the action group is available for the agent to invoke or not when sending an InvokeAgent request.
        :param api_schema: (experimental) Contains details about the S3 object containing the OpenAPI schema for the action group. For more information, see `Action group OpenAPI schemas <https://docs.aws.amazon.com/bedrock/latest/userguide/agents-api-schema.html>`_.
        :param description: (experimental) A description of the action group.
        :param parent_action_group_signature: (experimental) If you specify this value as AMAZON.UserInput, the agent will prompt additional information from the user when it doesn't have enough information to respond to an utterance. Leave this field blank if you don't want the agent to prompt additional information.
        :param skip_resource_in_use_check_on_delete: (experimental) Specifies whether the agent should skip the resource in use check on delete.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b3c9934294b04067f270151310db783e3b9ecde240109d0eed3c691351ae119)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AgentActionGroupProps(
            action_group_name=action_group_name,
            action_group_executor=action_group_executor,
            action_group_state=action_group_state,
            api_schema=api_schema,
            description=description,
            parent_action_group_signature=parent_action_group_signature,
            skip_resource_in_use_check_on_delete=skip_resource_in_use_check_on_delete,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="actionGroupName")
    def action_group_name(self) -> builtins.str:
        '''(experimental) The unique identifier of the action group.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "actionGroupName"))

    @builtins.property
    @jsii.member(jsii_name="actionGroupProperty")
    def action_group_property(
        self,
    ) -> _aws_cdk_aws_bedrock_ceddda9d.CfnAgent.AgentActionGroupProperty:
        '''(experimental) The action group.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_bedrock_ceddda9d.CfnAgent.AgentActionGroupProperty, jsii.get(self, "actionGroupProperty"))

    @builtins.property
    @jsii.member(jsii_name="actionGroupExecutor")
    def action_group_executor(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IFunction]:
        '''(experimental) The Lambda function containing the business logic that is carried out upon invoking the action.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IFunction], jsii.get(self, "actionGroupExecutor"))

    @builtins.property
    @jsii.member(jsii_name="actionGroupState")
    def action_group_state(self) -> typing.Optional[builtins.str]:
        '''(experimental) The action group state.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionGroupState"))

    @builtins.property
    @jsii.member(jsii_name="apiSchema")
    def api_schema(self) -> typing.Optional["ApiSchemaConfig"]:
        '''(experimental) The API schema.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["ApiSchemaConfig"], jsii.get(self, "apiSchema"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="parentActionGroupSignature")
    def parent_action_group_signature(self) -> typing.Optional[builtins.str]:
        '''(experimental) The parent action group signature.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentActionGroupSignature"))

    @builtins.property
    @jsii.member(jsii_name="skipResourceInUseCheckOnDelete")
    def skip_resource_in_use_check_on_delete(self) -> typing.Optional[builtins.bool]:
        '''(experimental) The skip resource in use check on delete.

        :default: - false

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "skipResourceInUseCheckOnDelete"))


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.AgentActionGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "action_group_name": "actionGroupName",
        "action_group_executor": "actionGroupExecutor",
        "action_group_state": "actionGroupState",
        "api_schema": "apiSchema",
        "description": "description",
        "parent_action_group_signature": "parentActionGroupSignature",
        "skip_resource_in_use_check_on_delete": "skipResourceInUseCheckOnDelete",
    },
)
class AgentActionGroupProps:
    def __init__(
        self,
        *,
        action_group_name: builtins.str,
        action_group_executor: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IFunction] = None,
        action_group_state: typing.Optional[builtins.str] = None,
        api_schema: typing.Optional["ApiSchema"] = None,
        description: typing.Optional[builtins.str] = None,
        parent_action_group_signature: typing.Optional[builtins.str] = None,
        skip_resource_in_use_check_on_delete: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param action_group_name: (experimental) The name of the action group. Default: - a name is generated by CloudFormation.
        :param action_group_executor: (experimental) The Lambda function containing the business logic that is carried out upon invoking the action.
        :param action_group_state: (experimental) Specifies whether the action group is available for the agent to invoke or not when sending an InvokeAgent request.
        :param api_schema: (experimental) Contains details about the S3 object containing the OpenAPI schema for the action group. For more information, see `Action group OpenAPI schemas <https://docs.aws.amazon.com/bedrock/latest/userguide/agents-api-schema.html>`_.
        :param description: (experimental) A description of the action group.
        :param parent_action_group_signature: (experimental) If you specify this value as AMAZON.UserInput, the agent will prompt additional information from the user when it doesn't have enough information to respond to an utterance. Leave this field blank if you don't want the agent to prompt additional information.
        :param skip_resource_in_use_check_on_delete: (experimental) Specifies whether the agent should skip the resource in use check on delete.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e47b674f810daa9a7bde371ad21ea6944cc41d81e91b4c04fca71b8f52c01288)
            check_type(argname="argument action_group_name", value=action_group_name, expected_type=type_hints["action_group_name"])
            check_type(argname="argument action_group_executor", value=action_group_executor, expected_type=type_hints["action_group_executor"])
            check_type(argname="argument action_group_state", value=action_group_state, expected_type=type_hints["action_group_state"])
            check_type(argname="argument api_schema", value=api_schema, expected_type=type_hints["api_schema"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument parent_action_group_signature", value=parent_action_group_signature, expected_type=type_hints["parent_action_group_signature"])
            check_type(argname="argument skip_resource_in_use_check_on_delete", value=skip_resource_in_use_check_on_delete, expected_type=type_hints["skip_resource_in_use_check_on_delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action_group_name": action_group_name,
        }
        if action_group_executor is not None:
            self._values["action_group_executor"] = action_group_executor
        if action_group_state is not None:
            self._values["action_group_state"] = action_group_state
        if api_schema is not None:
            self._values["api_schema"] = api_schema
        if description is not None:
            self._values["description"] = description
        if parent_action_group_signature is not None:
            self._values["parent_action_group_signature"] = parent_action_group_signature
        if skip_resource_in_use_check_on_delete is not None:
            self._values["skip_resource_in_use_check_on_delete"] = skip_resource_in_use_check_on_delete

    @builtins.property
    def action_group_name(self) -> builtins.str:
        '''(experimental) The name of the action group.

        :default: - a name is generated by CloudFormation.

        :stability: experimental
        '''
        result = self._values.get("action_group_name")
        assert result is not None, "Required property 'action_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def action_group_executor(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IFunction]:
        '''(experimental) The Lambda function containing the business logic that is carried out upon invoking the action.

        :stability: experimental
        '''
        result = self._values.get("action_group_executor")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IFunction], result)

    @builtins.property
    def action_group_state(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies whether the action group is available for the agent to invoke or not when sending an InvokeAgent request.

        :stability: experimental
        '''
        result = self._values.get("action_group_state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def api_schema(self) -> typing.Optional["ApiSchema"]:
        '''(experimental) Contains details about the S3 object containing the OpenAPI schema for the action group.

        For more information, see
        `Action group OpenAPI schemas <https://docs.aws.amazon.com/bedrock/latest/userguide/agents-api-schema.html>`_.

        :stability: experimental
        '''
        result = self._values.get("api_schema")
        return typing.cast(typing.Optional["ApiSchema"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of the action group.

        :stability: experimental
        :note: This object is a Union. Only one member of this object can be specified or returned.
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parent_action_group_signature(self) -> typing.Optional[builtins.str]:
        '''(experimental) If you specify this value as AMAZON.UserInput, the agent will prompt additional information from the user when it doesn't have enough information to respond to an utterance. Leave this field blank if you don't want the agent to prompt additional information.

        :stability: experimental
        '''
        result = self._values.get("parent_action_group_signature")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def skip_resource_in_use_check_on_delete(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether the agent should skip the resource in use check on delete.

        :stability: experimental
        '''
        result = self._values.get("skip_resource_in_use_check_on_delete")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AgentActionGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AgentAlias(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.AgentAlias",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        agent_id: builtins.str,
        agent_version: typing.Optional[builtins.str] = None,
        alias_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        resource_updates: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param agent_id: (experimental) The unique identifier of the agent.
        :param agent_version: (experimental) The version of the agent to associate with the agent alias. Default: - Creates a new version of the agent.
        :param alias_name: (experimental) The name for the agent alias. Default: - 'latest'
        :param description: (experimental) Description for the agent alias.
        :param resource_updates: (experimental) The list of resource update timestamps to let CloudFormation determine when to update the alias.
        :param tags: (experimental) OPTIONAL: Tag (KEY-VALUE) bedrock agent resource. Default: - false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d5252a70a25f0e579966376a7e29bb2527a503dda1a1fed24527d3559affff2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AgentAliasProps(
            agent_id=agent_id,
            agent_version=agent_version,
            alias_name=alias_name,
            description=description,
            resource_updates=resource_updates,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="aliasArn")
    def alias_arn(self) -> builtins.str:
        '''(experimental) The ARN of the agent alias.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "aliasArn"))

    @builtins.property
    @jsii.member(jsii_name="aliasId")
    def alias_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the agent alias.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "aliasId"))

    @builtins.property
    @jsii.member(jsii_name="aliasName")
    def alias_name(self) -> builtins.str:
        '''(experimental) The name for the agent alias.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "aliasName"))


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.AgentAliasProps",
    jsii_struct_bases=[],
    name_mapping={
        "agent_id": "agentId",
        "agent_version": "agentVersion",
        "alias_name": "aliasName",
        "description": "description",
        "resource_updates": "resourceUpdates",
        "tags": "tags",
    },
)
class AgentAliasProps:
    def __init__(
        self,
        *,
        agent_id: builtins.str,
        agent_version: typing.Optional[builtins.str] = None,
        alias_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        resource_updates: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param agent_id: (experimental) The unique identifier of the agent.
        :param agent_version: (experimental) The version of the agent to associate with the agent alias. Default: - Creates a new version of the agent.
        :param alias_name: (experimental) The name for the agent alias. Default: - 'latest'
        :param description: (experimental) Description for the agent alias.
        :param resource_updates: (experimental) The list of resource update timestamps to let CloudFormation determine when to update the alias.
        :param tags: (experimental) OPTIONAL: Tag (KEY-VALUE) bedrock agent resource. Default: - false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cae66eefc5f4c5599e0686171b63cba4b3c09493c31167b8afaa8bff00da6cc)
            check_type(argname="argument agent_id", value=agent_id, expected_type=type_hints["agent_id"])
            check_type(argname="argument agent_version", value=agent_version, expected_type=type_hints["agent_version"])
            check_type(argname="argument alias_name", value=alias_name, expected_type=type_hints["alias_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument resource_updates", value=resource_updates, expected_type=type_hints["resource_updates"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "agent_id": agent_id,
        }
        if agent_version is not None:
            self._values["agent_version"] = agent_version
        if alias_name is not None:
            self._values["alias_name"] = alias_name
        if description is not None:
            self._values["description"] = description
        if resource_updates is not None:
            self._values["resource_updates"] = resource_updates
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def agent_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the agent.

        :stability: experimental
        '''
        result = self._values.get("agent_id")
        assert result is not None, "Required property 'agent_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def agent_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The version of the agent to associate with the agent alias.

        :default: - Creates a new version of the agent.

        :stability: experimental
        '''
        result = self._values.get("agent_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alias_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name for the agent alias.

        :default: - 'latest'

        :stability: experimental
        '''
        result = self._values.get("alias_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Description for the agent alias.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_updates(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The list of resource update timestamps to let CloudFormation determine when to update the alias.

        :stability: experimental
        '''
        result = self._values.get("resource_updates")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) OPTIONAL: Tag (KEY-VALUE) bedrock agent resource.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AgentAliasProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.AgentProps",
    jsii_struct_bases=[],
    name_mapping={
        "foundation_model": "foundationModel",
        "instruction": "instruction",
        "action_groups": "actionGroups",
        "alias_name": "aliasName",
        "description": "description",
        "enable_user_input": "enableUserInput",
        "encryption_key": "encryptionKey",
        "existing_role": "existingRole",
        "idle_session_ttl": "idleSessionTTL",
        "knowledge_bases": "knowledgeBases",
        "name": "name",
        "prompt_override_configuration": "promptOverrideConfiguration",
        "should_prepare_agent": "shouldPrepareAgent",
        "tags": "tags",
    },
)
class AgentProps:
    def __init__(
        self,
        *,
        foundation_model: "BedrockFoundationModel",
        instruction: builtins.str,
        action_groups: typing.Optional[typing.Sequence[AgentActionGroup]] = None,
        alias_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        enable_user_input: typing.Optional[builtins.bool] = None,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        existing_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
        idle_session_ttl: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        knowledge_bases: typing.Optional[typing.Sequence["KnowledgeBase"]] = None,
        name: typing.Optional[builtins.str] = None,
        prompt_override_configuration: typing.Optional[typing.Union["PromptOverrideConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        should_prepare_agent: typing.Optional[builtins.bool] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''(experimental) Properties for a Bedrock Agent.

        :param foundation_model: (experimental) The Bedrock text foundation model for the agent to use.
        :param instruction: (experimental) A narrative instruction to provide the agent as context.
        :param action_groups: (experimental) AgentActionGroup to make available to the agent. Default: - No AgentActionGroup is used.
        :param alias_name: (experimental) Name of the alias for the agent. Default: - No alias is created.
        :param description: (experimental) A description of the agent. Default: - No description is provided.
        :param enable_user_input: (experimental) Select whether the agent can prompt additional information from the user when it does not have enough information to respond to an utterance. Default: - False
        :param encryption_key: (experimental) KMS encryption key to use for the agent. Default: - An AWS managed key is used.
        :param existing_role: (experimental) The existing IAM Role for the agent with a trust policy that allows the Bedrock service to assume the role.
        :param idle_session_ttl: (experimental) How long sessions should be kept open for the agent. Default: - 1 hour
        :param knowledge_bases: (experimental) Knowledge Bases to make available to the agent. Default: - No knowledge base is used.
        :param name: (experimental) The name of the agent. Default: - A name is automatically generated.
        :param prompt_override_configuration: (experimental) Overrides for the agent. Default: - No overrides are provided.
        :param should_prepare_agent: (experimental) Whether to prepare the agent for use. Default: - false
        :param tags: (experimental) OPTIONAL: Tag (KEY-VALUE) bedrock agent resource. Default: - false

        :stability: experimental
        '''
        if isinstance(prompt_override_configuration, dict):
            prompt_override_configuration = PromptOverrideConfiguration(**prompt_override_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c5254c1c0482eaa66699188ff0467d936350a386bbe823d4ef46c9ba982f91c)
            check_type(argname="argument foundation_model", value=foundation_model, expected_type=type_hints["foundation_model"])
            check_type(argname="argument instruction", value=instruction, expected_type=type_hints["instruction"])
            check_type(argname="argument action_groups", value=action_groups, expected_type=type_hints["action_groups"])
            check_type(argname="argument alias_name", value=alias_name, expected_type=type_hints["alias_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enable_user_input", value=enable_user_input, expected_type=type_hints["enable_user_input"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument existing_role", value=existing_role, expected_type=type_hints["existing_role"])
            check_type(argname="argument idle_session_ttl", value=idle_session_ttl, expected_type=type_hints["idle_session_ttl"])
            check_type(argname="argument knowledge_bases", value=knowledge_bases, expected_type=type_hints["knowledge_bases"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument prompt_override_configuration", value=prompt_override_configuration, expected_type=type_hints["prompt_override_configuration"])
            check_type(argname="argument should_prepare_agent", value=should_prepare_agent, expected_type=type_hints["should_prepare_agent"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "foundation_model": foundation_model,
            "instruction": instruction,
        }
        if action_groups is not None:
            self._values["action_groups"] = action_groups
        if alias_name is not None:
            self._values["alias_name"] = alias_name
        if description is not None:
            self._values["description"] = description
        if enable_user_input is not None:
            self._values["enable_user_input"] = enable_user_input
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if existing_role is not None:
            self._values["existing_role"] = existing_role
        if idle_session_ttl is not None:
            self._values["idle_session_ttl"] = idle_session_ttl
        if knowledge_bases is not None:
            self._values["knowledge_bases"] = knowledge_bases
        if name is not None:
            self._values["name"] = name
        if prompt_override_configuration is not None:
            self._values["prompt_override_configuration"] = prompt_override_configuration
        if should_prepare_agent is not None:
            self._values["should_prepare_agent"] = should_prepare_agent
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def foundation_model(self) -> "BedrockFoundationModel":
        '''(experimental) The Bedrock text foundation model for the agent to use.

        :stability: experimental
        '''
        result = self._values.get("foundation_model")
        assert result is not None, "Required property 'foundation_model' is missing"
        return typing.cast("BedrockFoundationModel", result)

    @builtins.property
    def instruction(self) -> builtins.str:
        '''(experimental) A narrative instruction to provide the agent as context.

        :stability: experimental
        '''
        result = self._values.get("instruction")
        assert result is not None, "Required property 'instruction' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def action_groups(self) -> typing.Optional[typing.List[AgentActionGroup]]:
        '''(experimental) AgentActionGroup to make available to the agent.

        :default: - No AgentActionGroup  is used.

        :stability: experimental
        '''
        result = self._values.get("action_groups")
        return typing.cast(typing.Optional[typing.List[AgentActionGroup]], result)

    @builtins.property
    def alias_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the alias for the agent.

        :default: - No alias is created.

        :stability: experimental
        '''
        result = self._values.get("alias_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of the agent.

        :default: - No description is provided.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_user_input(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Select whether the agent can prompt additional information from the user when it does not have enough information to respond to an utterance.

        :default: - False

        :stability: experimental
        '''
        result = self._values.get("enable_user_input")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) KMS encryption key to use for the agent.

        :default: - An AWS managed key is used.

        :stability: experimental
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def existing_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role]:
        '''(experimental) The existing IAM Role for the agent with a trust policy that allows the Bedrock service to assume the role.

        :stability: experimental
        '''
        result = self._values.get("existing_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role], result)

    @builtins.property
    def idle_session_ttl(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) How long sessions should be kept open for the agent.

        :default: - 1 hour

        :stability: experimental
        '''
        result = self._values.get("idle_session_ttl")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def knowledge_bases(self) -> typing.Optional[typing.List["KnowledgeBase"]]:
        '''(experimental) Knowledge Bases to make available to the agent.

        :default: - No knowledge base is used.

        :stability: experimental
        '''
        result = self._values.get("knowledge_bases")
        return typing.cast(typing.Optional[typing.List["KnowledgeBase"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the agent.

        :default: - A name is automatically generated.

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prompt_override_configuration(
        self,
    ) -> typing.Optional["PromptOverrideConfiguration"]:
        '''(experimental) Overrides for the agent.

        :default: - No overrides are provided.

        :stability: experimental
        '''
        result = self._values.get("prompt_override_configuration")
        return typing.cast(typing.Optional["PromptOverrideConfiguration"], result)

    @builtins.property
    def should_prepare_agent(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to prepare the agent for use.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("should_prepare_agent")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) OPTIONAL: Tag (KEY-VALUE) bedrock agent resource.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AgentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiSchema(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ApiSchema",
):
    '''(experimental) Bedrock Agents Action Group API Schema definition.

    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromAsset")
    @builtins.classmethod
    def from_asset(cls, path: builtins.str) -> "InlineApiSchema":
        '''(experimental) Loads the API Schema from a local disk path.

        :param path: Path to the Open API schema file in yaml or JSON.

        :return: ``InlineApiSchema`` with the contents of ``path``

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9707019db7cf1339382bbfdc3c35863966765af6485a09c40c302a504ad6876d)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast("InlineApiSchema", jsii.sinvoke(cls, "fromAsset", [path]))

    @jsii.member(jsii_name="fromBucket")
    @builtins.classmethod
    def from_bucket(
        cls,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        key: builtins.str,
    ) -> "S3ApiSchema":
        '''(experimental) API Schema as an S3 object.

        :param bucket: The S3 bucket.
        :param key: The object key.

        :return: ``S3ApiSchema`` with the S3 bucket and key.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3690bdbded4fc41debce4f674af4ba9794363c793e9f2f52ac27a4069270b3a3)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        return typing.cast("S3ApiSchema", jsii.sinvoke(cls, "fromBucket", [bucket, key]))

    @jsii.member(jsii_name="fromInline")
    @builtins.classmethod
    def from_inline(cls, schema: builtins.str) -> "InlineApiSchema":
        '''(experimental) Inline code for API Schema.

        :param schema: The actual Open API schema.

        :return: ``InlineApiSchema`` with inline schema

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c2792cc1fa0f16747e3820d17877eef4b648c9b158bc65527d5d5c852652166)
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
        return typing.cast("InlineApiSchema", jsii.sinvoke(cls, "fromInline", [schema]))

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(self, scope: _constructs_77d1e7e8.Construct) -> "ApiSchemaConfig":
        '''(experimental) Called when the action group is initialized to allow this object to bind to the stack, add resources and have fun.

        :param scope: The binding scope. Don't be smart about trying to down-cast or assume it's initialized. You may just use it as a construct scope.

        :stability: experimental
        '''
        ...


class _ApiSchemaProxy(ApiSchema):
    @jsii.member(jsii_name="bind")
    def bind(self, scope: _constructs_77d1e7e8.Construct) -> "ApiSchemaConfig":
        '''(experimental) Called when the action group is initialized to allow this object to bind to the stack, add resources and have fun.

        :param scope: The binding scope. Don't be smart about trying to down-cast or assume it's initialized. You may just use it as a construct scope.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f63a27d3f3e9a3d4c529eccceaa09a947c740c16c6fc454bb2b8aaf2030cee7a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast("ApiSchemaConfig", jsii.invoke(self, "bind", [scope]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, ApiSchema).__jsii_proxy_class__ = lambda : _ApiSchemaProxy


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ApiSchemaConfig",
    jsii_struct_bases=[],
    name_mapping={"payload": "payload", "s3": "s3"},
)
class ApiSchemaConfig:
    def __init__(
        self,
        *,
        payload: typing.Optional[builtins.str] = None,
        s3: typing.Optional[typing.Union["S3Identifier", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Result of binding ``ApiSchema`` into an ``ActionGroup``.

        :param payload: (experimental) The JSON or YAML-formatted payload defining the OpenAPI schema for the action group. (mutually exclusive with ``s3``)
        :param s3: (experimental) Contains details about the S3 object containing the OpenAPI schema for the action group. (mutually exclusive with ``payload``)

        :stability: experimental
        '''
        if isinstance(s3, dict):
            s3 = S3Identifier(**s3)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a607944f95610e7de935c34b4ac51de5be66c1a19adb648c5e285f3ef483bbe7)
            check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
            check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if payload is not None:
            self._values["payload"] = payload
        if s3 is not None:
            self._values["s3"] = s3

    @builtins.property
    def payload(self) -> typing.Optional[builtins.str]:
        '''(experimental) The JSON or YAML-formatted payload defining the OpenAPI schema for the action group.

        (mutually exclusive with ``s3``)

        :stability: experimental
        '''
        result = self._values.get("payload")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3(self) -> typing.Optional["S3Identifier"]:
        '''(experimental) Contains details about the S3 object containing the OpenAPI schema for the action group.

        (mutually exclusive with ``payload``)

        :stability: experimental
        '''
        result = self._values.get("s3")
        return typing.cast(typing.Optional["S3Identifier"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiSchemaConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BedrockFoundationModel(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.BedrockFoundationModel",
):
    '''(experimental) Bedrock models.

    If you need to use a model name that doesn't exist as a static member, you
    can instantiate a ``BedrockFoundationModel`` object, e.g: ``new BedrockFoundationModel('my-model')``.

    :stability: experimental
    '''

    def __init__(
        self,
        value: builtins.str,
        *,
        supports_agents: typing.Optional[builtins.bool] = None,
        supports_knowledge_base: typing.Optional[builtins.bool] = None,
        vector_dimensions: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param value: -
        :param supports_agents: (experimental) Bedrock Agents can use this model. Default: - false
        :param supports_knowledge_base: (experimental) Bedrock Knowledge Base can use this model. Default: - false
        :param vector_dimensions: (experimental) Embedding models have different vector dimensions. Only applicable for embedding models.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64a81fd58f8932cf2d8dbd47ee14e3d74d82d0d0245523bd77f54c7a3ebe2a31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        props = BedrockFoundationModelProps(
            supports_agents=supports_agents,
            supports_knowledge_base=supports_knowledge_base,
            vector_dimensions=vector_dimensions,
        )

        jsii.create(self.__class__, self, [value, props])

    @jsii.member(jsii_name="asArn")
    def as_arn(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.str:
        '''
        :param construct: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0736a1f1795a1917c49125732e66d2d15e2a25a6b98ac778b58a6ed32dc0df7b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.str, jsii.invoke(self, "asArn", [construct]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AMAZON_TITAN_PREMIER_V1_0")
    def AMAZON_TITAN_PREMIER_V1_0(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "AMAZON_TITAN_PREMIER_V1_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AMAZON_TITAN_TEXT_EXPRESS_V1")
    def AMAZON_TITAN_TEXT_EXPRESS_V1(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "AMAZON_TITAN_TEXT_EXPRESS_V1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANTHROPIC_CLAUDE_HAIKU_V1_0")
    def ANTHROPIC_CLAUDE_HAIKU_V1_0(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "ANTHROPIC_CLAUDE_HAIKU_V1_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANTHROPIC_CLAUDE_INSTANT_V1_2")
    def ANTHROPIC_CLAUDE_INSTANT_V1_2(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "ANTHROPIC_CLAUDE_INSTANT_V1_2"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANTHROPIC_CLAUDE_SONNET_V1_0")
    def ANTHROPIC_CLAUDE_SONNET_V1_0(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "ANTHROPIC_CLAUDE_SONNET_V1_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANTHROPIC_CLAUDE_V2")
    def ANTHROPIC_CLAUDE_V2(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "ANTHROPIC_CLAUDE_V2"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANTHROPIC_CLAUDE_V2_1")
    def ANTHROPIC_CLAUDE_V2_1(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "ANTHROPIC_CLAUDE_V2_1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="COHERE_EMBED_ENGLISH_V3")
    def COHERE_EMBED_ENGLISH_V3(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "COHERE_EMBED_ENGLISH_V3"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="COHERE_EMBED_MULTILINGUAL_V3")
    def COHERE_EMBED_MULTILINGUAL_V3(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "COHERE_EMBED_MULTILINGUAL_V3"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="TITAN_EMBED_TEXT_V1")
    def TITAN_EMBED_TEXT_V1(cls) -> "BedrockFoundationModel":
        '''
        :stability: experimental
        '''
        return typing.cast("BedrockFoundationModel", jsii.sget(cls, "TITAN_EMBED_TEXT_V1"))

    @builtins.property
    @jsii.member(jsii_name="modelId")
    def model_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "modelId"))

    @builtins.property
    @jsii.member(jsii_name="supportsAgents")
    def supports_agents(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "supportsAgents"))

    @builtins.property
    @jsii.member(jsii_name="supportsKnowledgeBase")
    def supports_knowledge_base(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "supportsKnowledgeBase"))

    @builtins.property
    @jsii.member(jsii_name="vectorDimensions")
    def vector_dimensions(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "vectorDimensions"))


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.BedrockFoundationModelProps",
    jsii_struct_bases=[],
    name_mapping={
        "supports_agents": "supportsAgents",
        "supports_knowledge_base": "supportsKnowledgeBase",
        "vector_dimensions": "vectorDimensions",
    },
)
class BedrockFoundationModelProps:
    def __init__(
        self,
        *,
        supports_agents: typing.Optional[builtins.bool] = None,
        supports_knowledge_base: typing.Optional[builtins.bool] = None,
        vector_dimensions: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param supports_agents: (experimental) Bedrock Agents can use this model. Default: - false
        :param supports_knowledge_base: (experimental) Bedrock Knowledge Base can use this model. Default: - false
        :param vector_dimensions: (experimental) Embedding models have different vector dimensions. Only applicable for embedding models.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e1a21a71ca2d85f4b0cb18a5ce955b8c59bb0c4403b3d6f750c90739061d548)
            check_type(argname="argument supports_agents", value=supports_agents, expected_type=type_hints["supports_agents"])
            check_type(argname="argument supports_knowledge_base", value=supports_knowledge_base, expected_type=type_hints["supports_knowledge_base"])
            check_type(argname="argument vector_dimensions", value=vector_dimensions, expected_type=type_hints["vector_dimensions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if supports_agents is not None:
            self._values["supports_agents"] = supports_agents
        if supports_knowledge_base is not None:
            self._values["supports_knowledge_base"] = supports_knowledge_base
        if vector_dimensions is not None:
            self._values["vector_dimensions"] = vector_dimensions

    @builtins.property
    def supports_agents(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Bedrock Agents can use this model.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("supports_agents")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def supports_knowledge_base(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Bedrock Knowledge Base can use this model.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("supports_knowledge_base")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def vector_dimensions(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Embedding models have different vector dimensions.

        Only applicable for embedding models.

        :stability: experimental
        '''
        result = self._values.get("vector_dimensions")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockFoundationModelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ChunkingStrategy")
class ChunkingStrategy(enum.Enum):
    '''(experimental) Knowledge base can split your source data into chunks.

    A chunk refers to an
    excerpt from a data source that is returned when the knowledge base that it
    belongs to is queried. You have the following options for chunking your
    data. If you opt for NONE, then you may want to pre-process your files by
    splitting them up such that each file corresponds to a chunk.

    :stability: experimental
    '''

    FIXED_SIZE = "FIXED_SIZE"
    '''(experimental) Amazon Bedrock splits your source data into chunks of the approximate size that you set in the ``fixedSizeChunkingConfiguration``.

    :stability: experimental
    '''
    DEFAULT = "DEFAULT"
    '''(experimental) ``FIXED_SIZE`` with the default chunk size of 300 tokens and 20% overlap.

    :stability: experimental
    '''
    NONE = "NONE"
    '''(experimental) Amazon Bedrock treats each file as one chunk.

    If you choose this option,
    you may want to pre-process your documents by splitting them into separate
    files.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.InferenceConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "maximum_length": "maximumLength",
        "stop_sequences": "stopSequences",
        "temperature": "temperature",
        "top_k": "topK",
        "top_p": "topP",
    },
)
class InferenceConfiguration:
    def __init__(
        self,
        *,
        maximum_length: jsii.Number,
        stop_sequences: typing.Sequence[builtins.str],
        temperature: jsii.Number,
        top_k: jsii.Number,
        top_p: jsii.Number,
    ) -> None:
        '''(experimental) LLM inference configuration.

        :param maximum_length: (experimental) The maximum number of tokens to generate in the response. Integer
        :param stop_sequences: (experimental) A list of stop sequences. A stop sequence is a sequence of characters that causes the model to stop generating the response.
        :param temperature: (experimental) The likelihood of the model selecting higher-probability options while generating a response. A lower value makes the model more likely to choose higher-probability options, while a higher value makes the model more likely to choose lower-probability options. Floating point
        :param top_k: (experimental) While generating a response, the model determines the probability of the following token at each point of generation. The value that you set for topK is the number of most-likely candidates from which the model chooses the next token in the sequence. For example, if you set topK to 50, the model selects the next token from among the top 50 most likely choices. Integer
        :param top_p: (experimental) While generating a response, the model determines the probability of the following token at each point of generation. The value that you set for Top P determines the number of most-likely candidates from which the model chooses the next token in the sequence. For example, if you set topP to 80, the model only selects the next token from the top 80% of the probability distribution of next tokens. Floating point

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__befd502c2937a36c672491bd2695d4ec887944e821efe023f2dc44cff4137750)
            check_type(argname="argument maximum_length", value=maximum_length, expected_type=type_hints["maximum_length"])
            check_type(argname="argument stop_sequences", value=stop_sequences, expected_type=type_hints["stop_sequences"])
            check_type(argname="argument temperature", value=temperature, expected_type=type_hints["temperature"])
            check_type(argname="argument top_k", value=top_k, expected_type=type_hints["top_k"])
            check_type(argname="argument top_p", value=top_p, expected_type=type_hints["top_p"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "maximum_length": maximum_length,
            "stop_sequences": stop_sequences,
            "temperature": temperature,
            "top_k": top_k,
            "top_p": top_p,
        }

    @builtins.property
    def maximum_length(self) -> jsii.Number:
        '''(experimental) The maximum number of tokens to generate in the response.

        Integer

        :stability: experimental
        :max: 4096
        :min: 0
        '''
        result = self._values.get("maximum_length")
        assert result is not None, "Required property 'maximum_length' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def stop_sequences(self) -> typing.List[builtins.str]:
        '''(experimental) A list of stop sequences.

        A stop sequence is a sequence of characters that
        causes the model to stop generating the response.

        :stability: experimental
        :length: 0-4
        '''
        result = self._values.get("stop_sequences")
        assert result is not None, "Required property 'stop_sequences' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def temperature(self) -> jsii.Number:
        '''(experimental) The likelihood of the model selecting higher-probability options while generating a response.

        A lower value makes the model more likely to choose
        higher-probability options, while a higher value makes the model more
        likely to choose lower-probability options.

        Floating point

        :stability: experimental
        :max: 1
        :min: 0
        '''
        result = self._values.get("temperature")
        assert result is not None, "Required property 'temperature' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def top_k(self) -> jsii.Number:
        '''(experimental) While generating a response, the model determines the probability of the following token at each point of generation.

        The value that you set for
        topK is the number of most-likely candidates from which the model chooses
        the next token in the sequence. For example, if you set topK to 50, the
        model selects the next token from among the top 50 most likely choices.

        Integer

        :stability: experimental
        :max: 500
        :min: 0
        '''
        result = self._values.get("top_k")
        assert result is not None, "Required property 'top_k' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def top_p(self) -> jsii.Number:
        '''(experimental) While generating a response, the model determines the probability of the following token at each point of generation.

        The value that you set for
        Top P determines the number of most-likely candidates from which the model
        chooses the next token in the sequence. For example, if you set topP to
        80, the model only selects the next token from the top 80% of the
        probability distribution of next tokens.

        Floating point

        :stability: experimental
        :max: 1
        :min: 0
        '''
        result = self._values.get("top_p")
        assert result is not None, "Required property 'top_p' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InferenceConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class InlineApiSchema(
    ApiSchema,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.InlineApiSchema",
):
    '''(experimental) API Schema from a string value.

    :stability: experimental
    '''

    def __init__(self, schema: builtins.str) -> None:
        '''
        :param schema: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abeb00812cdcb551f5f688ee295d8f225db974111b8872709130c22fef51592f)
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
        jsii.create(self.__class__, self, [schema])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: _constructs_77d1e7e8.Construct) -> ApiSchemaConfig:
        '''(experimental) Called when the action group is initialized to allow this object to bind to the stack, add resources and have fun.

        :param _scope: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__429693913d097a23421c6ed72f2363c20d20bbc2d34b374921e37cf4ac8d4157)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(ApiSchemaConfig, jsii.invoke(self, "bind", [_scope]))


class KnowledgeBase(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.KnowledgeBase",
):
    '''(experimental) Deploys a Bedrock Knowledge Base and configures a backend by OpenSearch Serverless, Pinecone, Redis Enterprise Cloud or Amazon Aurora PostgreSQL.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        embeddings_model: BedrockFoundationModel,
        description: typing.Optional[builtins.str] = None,
        existing_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
        index_name: typing.Optional[builtins.str] = None,
        instruction: typing.Optional[builtins.str] = None,
        knowledge_base_state: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        vector_field: typing.Optional[builtins.str] = None,
        vector_index: typing.Optional[_VectorIndex_e5d266e9] = None,
        vector_store: typing.Optional[typing.Union[_AmazonAuroraDefaultVectorStore_ec1da9eb, _AmazonAuroraVectorStore_bde12a1e, _VectorCollection_91bfdaa9, _PineconeVectorStore_c017c196]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param embeddings_model: (experimental) The embeddings model for the knowledge base.
        :param description: (experimental) The description of the knowledge base. Default: - No description provided.
        :param existing_role: (experimental) Existing IAM role with a policy statement granting permission to invoke the specific embeddings model. Any entity (e.g., an AWS service or application) that assumes this role will be able to invoke or use the specified embeddings model within the Bedrock service.
        :param index_name: (experimental) The name of the vector index. If vectorStore is not of type ``VectorCollection``, do not include this property as it will throw error. Default: - 'bedrock-knowledge-base-default-index'
        :param instruction: (experimental) A narrative description of the knowledge base. A Bedrock Agent can use this instruction to determine if it should query this Knowledge Base. Default: - No description provided.
        :param knowledge_base_state: (experimental) Specifies whether to use the knowledge base or not when sending an InvokeAgent request.
        :param name: (experimental) The name of the knowledge base.
        :param tags: (experimental) OPTIONAL: Tag (KEY-VALUE) bedrock agent resource. Default: - false
        :param vector_field: (experimental) The name of the field in the vector index. If vectorStore is not of type ``VectorCollection``, do not include this property as it will throw error. Default: - 'bedrock-knowledge-base-default-vector'
        :param vector_index: (experimental) The vector index for the OpenSearch Serverless backed knowledge base. If vectorStore is not of type ``VectorCollection``, do not include this property as it will throw error. Default: - A new vector index is created on the Vector Collection if vector store is of ``VectorCollection`` type.
        :param vector_store: (experimental) The vector store for the knowledge base. Must be either of type ``VectorCollection``, ``RedisEnterpriseVectorStore``, ``PineconeVectorStore``, ``AmazonAuroraVectorStore`` or ``AmazonAuroraDefaultVectorStore``. Default: - A new OpenSearch Serverless vector collection is created.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a416de40b883dde9bcfa680e69b09d8d8005e4e5d67e2254f09ebebb1b516bb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = KnowledgeBaseProps(
            embeddings_model=embeddings_model,
            description=description,
            existing_role=existing_role,
            index_name=index_name,
            instruction=instruction,
            knowledge_base_state=knowledge_base_state,
            name=name,
            tags=tags,
            vector_field=vector_field,
            vector_index=vector_index,
            vector_store=vector_store,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="associateToAgent")
    def associate_to_agent(self, agent: Agent) -> None:
        '''(experimental) Associate knowledge base with an agent.

        :param agent: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ca7cf4ff7c6392dfc7cae12d95e046e86c711e76659c1c94e920f30da3a066c)
            check_type(argname="argument agent", value=agent, expected_type=type_hints["agent"])
        return typing.cast(None, jsii.invoke(self, "associateToAgent", [agent]))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        '''(experimental) The description knowledge base.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="knowledgeBaseArn")
    def knowledge_base_arn(self) -> builtins.str:
        '''(experimental) The ARN of the knowledge base.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "knowledgeBaseArn"))

    @builtins.property
    @jsii.member(jsii_name="knowledgeBaseId")
    def knowledge_base_id(self) -> builtins.str:
        '''(experimental) The ID of the knowledge base.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "knowledgeBaseId"))

    @builtins.property
    @jsii.member(jsii_name="knowledgeBaseInstance")
    def knowledge_base_instance(self) -> _aws_cdk_aws_bedrock_ceddda9d.CfnKnowledgeBase:
        '''(experimental) Instance of knowledge base.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_bedrock_ceddda9d.CfnKnowledgeBase, jsii.get(self, "knowledgeBaseInstance"))

    @builtins.property
    @jsii.member(jsii_name="knowledgeBaseState")
    def knowledge_base_state(self) -> builtins.str:
        '''(experimental) Specifies whether to use the knowledge base or not when sending an InvokeAgent request.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "knowledgeBaseState"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) The name of the knowledge base.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> _aws_cdk_aws_iam_ceddda9d.Role:
        '''(experimental) The role the Knowledge Base uses to access the vector store and data source.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Role, jsii.get(self, "role"))

    @builtins.property
    @jsii.member(jsii_name="vectorStore")
    def vector_store(
        self,
    ) -> typing.Union[_AmazonAuroraDefaultVectorStore_ec1da9eb, _AmazonAuroraVectorStore_bde12a1e, _VectorCollection_91bfdaa9, _PineconeVectorStore_c017c196]:
        '''(experimental) The vector store for the knowledge base.

        :stability: experimental
        '''
        return typing.cast(typing.Union[_AmazonAuroraDefaultVectorStore_ec1da9eb, _AmazonAuroraVectorStore_bde12a1e, _VectorCollection_91bfdaa9, _PineconeVectorStore_c017c196], jsii.get(self, "vectorStore"))

    @builtins.property
    @jsii.member(jsii_name="instruction")
    def instruction(self) -> typing.Optional[builtins.str]:
        '''(experimental) A narrative instruction of the knowledge base.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instruction"))


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.KnowledgeBaseProps",
    jsii_struct_bases=[],
    name_mapping={
        "embeddings_model": "embeddingsModel",
        "description": "description",
        "existing_role": "existingRole",
        "index_name": "indexName",
        "instruction": "instruction",
        "knowledge_base_state": "knowledgeBaseState",
        "name": "name",
        "tags": "tags",
        "vector_field": "vectorField",
        "vector_index": "vectorIndex",
        "vector_store": "vectorStore",
    },
)
class KnowledgeBaseProps:
    def __init__(
        self,
        *,
        embeddings_model: BedrockFoundationModel,
        description: typing.Optional[builtins.str] = None,
        existing_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
        index_name: typing.Optional[builtins.str] = None,
        instruction: typing.Optional[builtins.str] = None,
        knowledge_base_state: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        vector_field: typing.Optional[builtins.str] = None,
        vector_index: typing.Optional[_VectorIndex_e5d266e9] = None,
        vector_store: typing.Optional[typing.Union[_AmazonAuroraDefaultVectorStore_ec1da9eb, _AmazonAuroraVectorStore_bde12a1e, _VectorCollection_91bfdaa9, _PineconeVectorStore_c017c196]] = None,
    ) -> None:
        '''(experimental) Properties for a knowledge base.

        :param embeddings_model: (experimental) The embeddings model for the knowledge base.
        :param description: (experimental) The description of the knowledge base. Default: - No description provided.
        :param existing_role: (experimental) Existing IAM role with a policy statement granting permission to invoke the specific embeddings model. Any entity (e.g., an AWS service or application) that assumes this role will be able to invoke or use the specified embeddings model within the Bedrock service.
        :param index_name: (experimental) The name of the vector index. If vectorStore is not of type ``VectorCollection``, do not include this property as it will throw error. Default: - 'bedrock-knowledge-base-default-index'
        :param instruction: (experimental) A narrative description of the knowledge base. A Bedrock Agent can use this instruction to determine if it should query this Knowledge Base. Default: - No description provided.
        :param knowledge_base_state: (experimental) Specifies whether to use the knowledge base or not when sending an InvokeAgent request.
        :param name: (experimental) The name of the knowledge base.
        :param tags: (experimental) OPTIONAL: Tag (KEY-VALUE) bedrock agent resource. Default: - false
        :param vector_field: (experimental) The name of the field in the vector index. If vectorStore is not of type ``VectorCollection``, do not include this property as it will throw error. Default: - 'bedrock-knowledge-base-default-vector'
        :param vector_index: (experimental) The vector index for the OpenSearch Serverless backed knowledge base. If vectorStore is not of type ``VectorCollection``, do not include this property as it will throw error. Default: - A new vector index is created on the Vector Collection if vector store is of ``VectorCollection`` type.
        :param vector_store: (experimental) The vector store for the knowledge base. Must be either of type ``VectorCollection``, ``RedisEnterpriseVectorStore``, ``PineconeVectorStore``, ``AmazonAuroraVectorStore`` or ``AmazonAuroraDefaultVectorStore``. Default: - A new OpenSearch Serverless vector collection is created.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d77925ffb8d3d9f229cccdf4b13498db4e9b0c20ca077db0cbe11892e0b36d5f)
            check_type(argname="argument embeddings_model", value=embeddings_model, expected_type=type_hints["embeddings_model"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument existing_role", value=existing_role, expected_type=type_hints["existing_role"])
            check_type(argname="argument index_name", value=index_name, expected_type=type_hints["index_name"])
            check_type(argname="argument instruction", value=instruction, expected_type=type_hints["instruction"])
            check_type(argname="argument knowledge_base_state", value=knowledge_base_state, expected_type=type_hints["knowledge_base_state"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vector_field", value=vector_field, expected_type=type_hints["vector_field"])
            check_type(argname="argument vector_index", value=vector_index, expected_type=type_hints["vector_index"])
            check_type(argname="argument vector_store", value=vector_store, expected_type=type_hints["vector_store"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "embeddings_model": embeddings_model,
        }
        if description is not None:
            self._values["description"] = description
        if existing_role is not None:
            self._values["existing_role"] = existing_role
        if index_name is not None:
            self._values["index_name"] = index_name
        if instruction is not None:
            self._values["instruction"] = instruction
        if knowledge_base_state is not None:
            self._values["knowledge_base_state"] = knowledge_base_state
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags
        if vector_field is not None:
            self._values["vector_field"] = vector_field
        if vector_index is not None:
            self._values["vector_index"] = vector_index
        if vector_store is not None:
            self._values["vector_store"] = vector_store

    @builtins.property
    def embeddings_model(self) -> BedrockFoundationModel:
        '''(experimental) The embeddings model for the knowledge base.

        :stability: experimental
        '''
        result = self._values.get("embeddings_model")
        assert result is not None, "Required property 'embeddings_model' is missing"
        return typing.cast(BedrockFoundationModel, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the knowledge base.

        :default: - No description provided.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def existing_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role]:
        '''(experimental) Existing IAM role with a policy statement granting permission to invoke the specific embeddings model.

        Any entity (e.g., an AWS service or application) that assumes
        this role will be able to invoke or use the
        specified embeddings model within the Bedrock service.

        :stability: experimental
        '''
        result = self._values.get("existing_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role], result)

    @builtins.property
    def index_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the vector index.

        If vectorStore is not of type ``VectorCollection``,
        do not include this property as it will throw error.

        :default: - 'bedrock-knowledge-base-default-index'

        :stability: experimental
        '''
        result = self._values.get("index_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instruction(self) -> typing.Optional[builtins.str]:
        '''(experimental) A narrative description of the knowledge base.

        A Bedrock Agent can use this instruction to determine if it should
        query this Knowledge Base.

        :default: - No description provided.

        :stability: experimental
        '''
        result = self._values.get("instruction")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def knowledge_base_state(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies whether to use the knowledge base or not when sending an InvokeAgent request.

        :stability: experimental
        '''
        result = self._values.get("knowledge_base_state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the knowledge base.

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) OPTIONAL: Tag (KEY-VALUE) bedrock agent resource.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def vector_field(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the field in the vector index.

        If vectorStore is not of type ``VectorCollection``,
        do not include this property as it will throw error.

        :default: - 'bedrock-knowledge-base-default-vector'

        :stability: experimental
        '''
        result = self._values.get("vector_field")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vector_index(self) -> typing.Optional[_VectorIndex_e5d266e9]:
        '''(experimental) The vector index for the OpenSearch Serverless backed knowledge base.

        If vectorStore is not of type ``VectorCollection``, do not include
        this property as it will throw error.

        :default:

        - A new vector index is created on the Vector Collection
        if vector store is of ``VectorCollection`` type.

        :stability: experimental
        '''
        result = self._values.get("vector_index")
        return typing.cast(typing.Optional[_VectorIndex_e5d266e9], result)

    @builtins.property
    def vector_store(
        self,
    ) -> typing.Optional[typing.Union[_AmazonAuroraDefaultVectorStore_ec1da9eb, _AmazonAuroraVectorStore_bde12a1e, _VectorCollection_91bfdaa9, _PineconeVectorStore_c017c196]]:
        '''(experimental) The vector store for the knowledge base.

        Must be either of
        type ``VectorCollection``, ``RedisEnterpriseVectorStore``,
        ``PineconeVectorStore``, ``AmazonAuroraVectorStore`` or
        ``AmazonAuroraDefaultVectorStore``.

        :default: - A new OpenSearch Serverless vector collection is created.

        :stability: experimental
        '''
        result = self._values.get("vector_store")
        return typing.cast(typing.Optional[typing.Union[_AmazonAuroraDefaultVectorStore_ec1da9eb, _AmazonAuroraVectorStore_bde12a1e, _VectorCollection_91bfdaa9, _PineconeVectorStore_c017c196]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KnowledgeBaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.ParserMode")
class ParserMode(enum.Enum):
    '''(experimental) Specifies whether to override the default parser Lambda function when parsing the raw foundation model output in the part of the agent sequence defined by the promptType.

    If you set the field as OVERRIDEN, the
    overrideLambda field in the PromptOverrideConfiguration must be specified
    with the ARN of a Lambda function.

    :stability: experimental
    '''

    DEFAULT = "DEFAULT"
    '''
    :stability: experimental
    '''
    OVERRIDDEN = "OVERRIDDEN"
    '''
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.PromptConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "base_prompt_template": "basePromptTemplate",
        "inference_configuration": "inferenceConfiguration",
        "prompt_creation_mode": "promptCreationMode",
        "prompt_state": "promptState",
        "prompt_type": "promptType",
        "parser_mode": "parserMode",
    },
)
class PromptConfiguration:
    def __init__(
        self,
        *,
        base_prompt_template: builtins.str,
        inference_configuration: typing.Union[InferenceConfiguration, typing.Dict[builtins.str, typing.Any]],
        prompt_creation_mode: "PromptCreationMode",
        prompt_state: "PromptState",
        prompt_type: "PromptType",
        parser_mode: typing.Optional[ParserMode] = None,
    ) -> None:
        '''(experimental) Contains configurations to override a prompt template in one part of an agent sequence.

        :param base_prompt_template: (experimental) Defines the prompt template with which to replace the default prompt template.
        :param inference_configuration: (experimental) Contains inference parameters to use when the agent invokes a foundation model in the part of the agent sequence defined by the promptType.
        :param prompt_creation_mode: (experimental) Specifies whether to override the default prompt template for this promptType. Set this value to OVERRIDDEN to use the prompt that you provide in the basePromptTemplate. If you leave it as DEFAULT, the agent uses a default prompt template.
        :param prompt_state: (experimental) Specifies whether to allow the agent to carry out the step specified in the promptType. If you set this value to DISABLED, the agent skips that step. The default state for each promptType is as follows:: PRE_PROCESSING – ENABLED ORCHESTRATION – ENABLED KNOWLEDGE_BASE_RESPONSE_GENERATION – ENABLED POST_PROCESSING – DISABLED
        :param prompt_type: (experimental) The step in the agent sequence that this prompt configuration applies to.
        :param parser_mode: (experimental) Specifies whether to override the default parser Lambda function when parsing the raw foundation model output in the part of the agent sequence defined by the promptType. If you set the field as OVERRIDEN, the overrideLambda field in the PromptOverrideConfiguration must be specified with the ARN of a Lambda function.

        :stability: experimental
        '''
        if isinstance(inference_configuration, dict):
            inference_configuration = InferenceConfiguration(**inference_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9e333bbbacb815921d7a258c01d4d87250548623e984fd2e844c23791ddeeed)
            check_type(argname="argument base_prompt_template", value=base_prompt_template, expected_type=type_hints["base_prompt_template"])
            check_type(argname="argument inference_configuration", value=inference_configuration, expected_type=type_hints["inference_configuration"])
            check_type(argname="argument prompt_creation_mode", value=prompt_creation_mode, expected_type=type_hints["prompt_creation_mode"])
            check_type(argname="argument prompt_state", value=prompt_state, expected_type=type_hints["prompt_state"])
            check_type(argname="argument prompt_type", value=prompt_type, expected_type=type_hints["prompt_type"])
            check_type(argname="argument parser_mode", value=parser_mode, expected_type=type_hints["parser_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "base_prompt_template": base_prompt_template,
            "inference_configuration": inference_configuration,
            "prompt_creation_mode": prompt_creation_mode,
            "prompt_state": prompt_state,
            "prompt_type": prompt_type,
        }
        if parser_mode is not None:
            self._values["parser_mode"] = parser_mode

    @builtins.property
    def base_prompt_template(self) -> builtins.str:
        '''(experimental) Defines the prompt template with which to replace the default prompt template.

        :stability: experimental
        :length: 0-100000
        '''
        result = self._values.get("base_prompt_template")
        assert result is not None, "Required property 'base_prompt_template' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def inference_configuration(self) -> InferenceConfiguration:
        '''(experimental) Contains inference parameters to use when the agent invokes a foundation model in the part of the agent sequence defined by the promptType.

        :stability: experimental
        '''
        result = self._values.get("inference_configuration")
        assert result is not None, "Required property 'inference_configuration' is missing"
        return typing.cast(InferenceConfiguration, result)

    @builtins.property
    def prompt_creation_mode(self) -> "PromptCreationMode":
        '''(experimental) Specifies whether to override the default prompt template for this promptType.

        Set this value to OVERRIDDEN to use the prompt that you
        provide in the basePromptTemplate. If you leave it as DEFAULT, the agent
        uses a default prompt template.

        :stability: experimental
        '''
        result = self._values.get("prompt_creation_mode")
        assert result is not None, "Required property 'prompt_creation_mode' is missing"
        return typing.cast("PromptCreationMode", result)

    @builtins.property
    def prompt_state(self) -> "PromptState":
        '''(experimental) Specifies whether to allow the agent to carry out the step specified in the promptType.

        If you set this value to DISABLED, the agent skips that
        step. The default state for each promptType is as follows::

           PRE_PROCESSING – ENABLED
           ORCHESTRATION – ENABLED
           KNOWLEDGE_BASE_RESPONSE_GENERATION – ENABLED
           POST_PROCESSING – DISABLED

        :stability: experimental
        '''
        result = self._values.get("prompt_state")
        assert result is not None, "Required property 'prompt_state' is missing"
        return typing.cast("PromptState", result)

    @builtins.property
    def prompt_type(self) -> "PromptType":
        '''(experimental) The step in the agent sequence that this prompt configuration applies to.

        :stability: experimental
        '''
        result = self._values.get("prompt_type")
        assert result is not None, "Required property 'prompt_type' is missing"
        return typing.cast("PromptType", result)

    @builtins.property
    def parser_mode(self) -> typing.Optional[ParserMode]:
        '''(experimental) Specifies whether to override the default parser Lambda function when parsing the raw foundation model output in the part of the agent sequence defined by the promptType.

        If you set the field as OVERRIDEN, the
        overrideLambda field in the PromptOverrideConfiguration must be specified
        with the ARN of a Lambda function.

        :stability: experimental
        '''
        result = self._values.get("parser_mode")
        return typing.cast(typing.Optional[ParserMode], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PromptConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.PromptCreationMode"
)
class PromptCreationMode(enum.Enum):
    '''(experimental) Specifies whether to override the default prompt template for this promptType.

    Set this value to OVERRIDDEN to use the prompt that you
    provide in the basePromptTemplate. If you leave it as DEFAULT, the agent
    uses a default prompt template.

    :stability: experimental
    '''

    DEFAULT = "DEFAULT"
    '''
    :stability: experimental
    '''
    OVERRIDDEN = "OVERRIDDEN"
    '''
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.PromptOverrideConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "prompt_configurations": "promptConfigurations",
        "override_lambda": "overrideLambda",
    },
)
class PromptOverrideConfiguration:
    def __init__(
        self,
        *,
        prompt_configurations: typing.Sequence[typing.Union[PromptConfiguration, typing.Dict[builtins.str, typing.Any]]],
        override_lambda: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Contains configurations to override prompts in different parts of an agent sequence.

        :param prompt_configurations: (experimental) Contains configurations to override a prompt template in one part of an agent sequence.
        :param override_lambda: (experimental) The ARN of the Lambda function to use when parsing the raw foundation model output in parts of the agent sequence. If you specify this field, at least one of the promptConfigurations must contain a parserMode value that is set to OVERRIDDEN.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87069825e4e1447731b12e085f8869b15f2bd52ca2b57df2d0342674371c9580)
            check_type(argname="argument prompt_configurations", value=prompt_configurations, expected_type=type_hints["prompt_configurations"])
            check_type(argname="argument override_lambda", value=override_lambda, expected_type=type_hints["override_lambda"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "prompt_configurations": prompt_configurations,
        }
        if override_lambda is not None:
            self._values["override_lambda"] = override_lambda

    @builtins.property
    def prompt_configurations(self) -> typing.List[PromptConfiguration]:
        '''(experimental) Contains configurations to override a prompt template in one part of an agent sequence.

        :stability: experimental
        '''
        result = self._values.get("prompt_configurations")
        assert result is not None, "Required property 'prompt_configurations' is missing"
        return typing.cast(typing.List[PromptConfiguration], result)

    @builtins.property
    def override_lambda(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ARN of the Lambda function to use when parsing the raw foundation model output in parts of the agent sequence.

        If you specify this field,
        at least one of the promptConfigurations must contain a parserMode value
        that is set to OVERRIDDEN.

        :stability: experimental
        '''
        result = self._values.get("override_lambda")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PromptOverrideConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.PromptState")
class PromptState(enum.Enum):
    '''(experimental) Specifies whether to allow the agent to carry out the step specified in the promptType.

    If you set this value to DISABLED, the agent skips that step.
    The default state for each promptType is as follows::

       PRE_PROCESSING – ENABLED
       ORCHESTRATION – ENABLED
       KNOWLEDGE_BASE_RESPONSE_GENERATION – ENABLED
       POST_PROCESSING – DISABLED

    :stability: experimental
    '''

    ENABLED = "ENABLED"
    '''
    :stability: experimental
    '''
    DISABLED = "DISABLED"
    '''
    :stability: experimental
    '''


@jsii.enum(jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.PromptType")
class PromptType(enum.Enum):
    '''(experimental) The step in the agent sequence that this prompt configuration applies to.

    :stability: experimental
    '''

    PRE_PROCESSING = "PRE_PROCESSING"
    '''
    :stability: experimental
    '''
    ORCHESTRATION = "ORCHESTRATION"
    '''
    :stability: experimental
    '''
    POST_PROCESSING = "POST_PROCESSING"
    '''
    :stability: experimental
    '''
    KNOWLEDGE_BASE_RESPONSE_GENERATION = "KNOWLEDGE_BASE_RESPONSE_GENERATION"
    '''
    :stability: experimental
    '''


class S3ApiSchema(
    ApiSchema,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.S3ApiSchema",
):
    '''(experimental) API Schema in an S3 object.

    :stability: experimental
    '''

    def __init__(
        self,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        key: builtins.str,
    ) -> None:
        '''
        :param bucket: -
        :param key: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04c4db74d64f90be972766dae3c6ab8b2ee388726bb4dec1fa1458939ab93a5f)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        jsii.create(self.__class__, self, [bucket, key])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: _constructs_77d1e7e8.Construct) -> ApiSchemaConfig:
        '''(experimental) Called when the action group is initialized to allow this object to bind to the stack, add resources and have fun.

        :param _scope: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdd50c8c86df0f0a2a5a95b774555d2e2c1d079404953f77717653ea8e3f768a)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(ApiSchemaConfig, jsii.invoke(self, "bind", [_scope]))


class S3DataSource(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.S3DataSource",
):
    '''(experimental) Sets up a data source to be added to a knowledge base.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        data_source_name: builtins.str,
        knowledge_base: KnowledgeBase,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        inclusion_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        max_tokens: typing.Optional[jsii.Number] = None,
        overlap_percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param bucket: (experimental) The bucket that contains the data source.
        :param data_source_name: (experimental) The name of the data source.
        :param knowledge_base: (experimental) The knowledge base that this data source belongs to.
        :param chunking_strategy: (experimental) The chunking strategy to use. Default: ChunkingStrategy.DEFAULT
        :param inclusion_prefixes: (experimental) The prefixes of the objects in the bucket that should be included in the data source. Default: - All objects in the bucket.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: Amazon Bedrock encrypts your data with a key that AWS owns and manages
        :param max_tokens: (experimental) The maximum number of tokens to use in a chunk. Default: 300
        :param overlap_percentage: (experimental) The percentage of overlap to use in a chunk. Default: 20

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48fbbb836e75c99d63b1aecb8d429a451f727eaf6d350fa9c8a3e73f4932c719)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = S3DataSourceProps(
            bucket=bucket,
            data_source_name=data_source_name,
            knowledge_base=knowledge_base,
            chunking_strategy=chunking_strategy,
            inclusion_prefixes=inclusion_prefixes,
            kms_key=kms_key,
            max_tokens=max_tokens,
            overlap_percentage=overlap_percentage,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="dataSource")
    def data_source(self) -> _aws_cdk_aws_bedrock_ceddda9d.CfnDataSource:
        '''(experimental) The Data Source cfn resource.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_bedrock_ceddda9d.CfnDataSource, jsii.get(self, "dataSource"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceId")
    def data_source_id(self) -> builtins.str:
        '''(experimental) The unique identifier of the data source.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "dataSourceId"))


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.S3DataSourceProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "data_source_name": "dataSourceName",
        "knowledge_base": "knowledgeBase",
        "chunking_strategy": "chunkingStrategy",
        "inclusion_prefixes": "inclusionPrefixes",
        "kms_key": "kmsKey",
        "max_tokens": "maxTokens",
        "overlap_percentage": "overlapPercentage",
    },
)
class S3DataSourceProps:
    def __init__(
        self,
        *,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        data_source_name: builtins.str,
        knowledge_base: KnowledgeBase,
        chunking_strategy: typing.Optional[ChunkingStrategy] = None,
        inclusion_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        max_tokens: typing.Optional[jsii.Number] = None,
        overlap_percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Properties for an S3 Data Source.

        :param bucket: (experimental) The bucket that contains the data source.
        :param data_source_name: (experimental) The name of the data source.
        :param knowledge_base: (experimental) The knowledge base that this data source belongs to.
        :param chunking_strategy: (experimental) The chunking strategy to use. Default: ChunkingStrategy.DEFAULT
        :param inclusion_prefixes: (experimental) The prefixes of the objects in the bucket that should be included in the data source. Default: - All objects in the bucket.
        :param kms_key: (experimental) The KMS key to use to encrypt the data source. Default: Amazon Bedrock encrypts your data with a key that AWS owns and manages
        :param max_tokens: (experimental) The maximum number of tokens to use in a chunk. Default: 300
        :param overlap_percentage: (experimental) The percentage of overlap to use in a chunk. Default: 20

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__061fd79f5c6cc3fdad0a0fcccc8c2a083f5deeb769270d6795cc47edeeaecc0b)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument data_source_name", value=data_source_name, expected_type=type_hints["data_source_name"])
            check_type(argname="argument knowledge_base", value=knowledge_base, expected_type=type_hints["knowledge_base"])
            check_type(argname="argument chunking_strategy", value=chunking_strategy, expected_type=type_hints["chunking_strategy"])
            check_type(argname="argument inclusion_prefixes", value=inclusion_prefixes, expected_type=type_hints["inclusion_prefixes"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument max_tokens", value=max_tokens, expected_type=type_hints["max_tokens"])
            check_type(argname="argument overlap_percentage", value=overlap_percentage, expected_type=type_hints["overlap_percentage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
            "data_source_name": data_source_name,
            "knowledge_base": knowledge_base,
        }
        if chunking_strategy is not None:
            self._values["chunking_strategy"] = chunking_strategy
        if inclusion_prefixes is not None:
            self._values["inclusion_prefixes"] = inclusion_prefixes
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if max_tokens is not None:
            self._values["max_tokens"] = max_tokens
        if overlap_percentage is not None:
            self._values["overlap_percentage"] = overlap_percentage

    @builtins.property
    def bucket(self) -> _aws_cdk_aws_s3_ceddda9d.IBucket:
        '''(experimental) The bucket that contains the data source.

        :stability: experimental
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucket, result)

    @builtins.property
    def data_source_name(self) -> builtins.str:
        '''(experimental) The name of the data source.

        :stability: experimental
        '''
        result = self._values.get("data_source_name")
        assert result is not None, "Required property 'data_source_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def knowledge_base(self) -> KnowledgeBase:
        '''(experimental) The knowledge base that this data source belongs to.

        :stability: experimental
        '''
        result = self._values.get("knowledge_base")
        assert result is not None, "Required property 'knowledge_base' is missing"
        return typing.cast(KnowledgeBase, result)

    @builtins.property
    def chunking_strategy(self) -> typing.Optional[ChunkingStrategy]:
        '''(experimental) The chunking strategy to use.

        :default: ChunkingStrategy.DEFAULT

        :stability: experimental
        '''
        result = self._values.get("chunking_strategy")
        return typing.cast(typing.Optional[ChunkingStrategy], result)

    @builtins.property
    def inclusion_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The prefixes of the objects in the bucket that should be included in the data source.

        :default: - All objects in the bucket.

        :stability: experimental
        '''
        result = self._values.get("inclusion_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key to use to encrypt the data source.

        :default: Amazon Bedrock encrypts your data with a key that AWS owns and manages

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def max_tokens(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum number of tokens to use in a chunk.

        :default: 300

        :stability: experimental
        '''
        result = self._values.get("max_tokens")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def overlap_percentage(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The percentage of overlap to use in a chunk.

        :default: 20

        :stability: experimental
        '''
        result = self._values.get("overlap_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3DataSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.bedrock.S3Identifier",
    jsii_struct_bases=[],
    name_mapping={"s3_bucket_name": "s3BucketName", "s3_object_key": "s3ObjectKey"},
)
class S3Identifier:
    def __init__(
        self,
        *,
        s3_bucket_name: builtins.str,
        s3_object_key: builtins.str,
    ) -> None:
        '''(experimental) Result of the bind when ``S3ApiSchema`` is used.

        :param s3_bucket_name: (experimental) The name of the S3 bucket.
        :param s3_object_key: (experimental) The S3 object key containing the resource.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8dfefeb74c7ac32b2ae5113a03ce2743b27b34cfa67e342053f0fb90d0050f0)
            check_type(argname="argument s3_bucket_name", value=s3_bucket_name, expected_type=type_hints["s3_bucket_name"])
            check_type(argname="argument s3_object_key", value=s3_object_key, expected_type=type_hints["s3_object_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "s3_bucket_name": s3_bucket_name,
            "s3_object_key": s3_object_key,
        }

    @builtins.property
    def s3_bucket_name(self) -> builtins.str:
        '''(experimental) The name of the S3 bucket.

        :stability: experimental
        '''
        result = self._values.get("s3_bucket_name")
        assert result is not None, "Required property 's3_bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_object_key(self) -> builtins.str:
        '''(experimental) The S3 object key containing the resource.

        :stability: experimental
        '''
        result = self._values.get("s3_object_key")
        assert result is not None, "Required property 's3_object_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3Identifier(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AddAgentAliasProps",
    "Agent",
    "AgentActionGroup",
    "AgentActionGroupProps",
    "AgentAlias",
    "AgentAliasProps",
    "AgentProps",
    "ApiSchema",
    "ApiSchemaConfig",
    "BedrockFoundationModel",
    "BedrockFoundationModelProps",
    "ChunkingStrategy",
    "InferenceConfiguration",
    "InlineApiSchema",
    "KnowledgeBase",
    "KnowledgeBaseProps",
    "ParserMode",
    "PromptConfiguration",
    "PromptCreationMode",
    "PromptOverrideConfiguration",
    "PromptState",
    "PromptType",
    "S3ApiSchema",
    "S3DataSource",
    "S3DataSourceProps",
    "S3Identifier",
]

publication.publish()

def _typecheckingstub__b44b9cf8594977e12593faffc73197189c6b8c803579e66de51dc986e13c8d2a(
    *,
    alias_name: builtins.str,
    agent_version: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__627af24bb5e1ca4b3ebb82ecbd7a3f01cb1f5177248afdccbc1d0ffab70726de(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    foundation_model: BedrockFoundationModel,
    instruction: builtins.str,
    action_groups: typing.Optional[typing.Sequence[AgentActionGroup]] = None,
    alias_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    enable_user_input: typing.Optional[builtins.bool] = None,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    existing_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
    idle_session_ttl: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    knowledge_bases: typing.Optional[typing.Sequence[KnowledgeBase]] = None,
    name: typing.Optional[builtins.str] = None,
    prompt_override_configuration: typing.Optional[typing.Union[PromptOverrideConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    should_prepare_agent: typing.Optional[builtins.bool] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__417f1714f331f713e989d70b6417dbb800ceedf7de8245c42ba72cde605b3504(
    action_group: AgentActionGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd86fd4e92aa0f8ee4a2b95a5ad405d539c55043eec94bf739fcc7fc1455d7a4(
    action_groups: typing.Sequence[AgentActionGroup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0ea7a1a86c29879ce5949318dae4e0d40df1772332d09e26ac0eebfde38479d(
    knowledge_base: KnowledgeBase,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca2617bd17ab91665385e57477c5d00b6dfffcd0be05ebe697f1f2d4ff1abc87(
    knowledge_bases: typing.Sequence[KnowledgeBase],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__362bb8b9135358d9388689544abcd0d0c9e8e45ae46a6dc95b075f20007b92ec(
    value: typing.List[_aws_cdk_aws_bedrock_ceddda9d.CfnAgent.AgentActionGroupProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b8a2ba31fca57d8bfcd42f9f0c012e95f4a9a95f52fe008b4777fe99b12b466(
    value: typing.List[_aws_cdk_aws_bedrock_ceddda9d.CfnAgent.AgentKnowledgeBaseProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b3c9934294b04067f270151310db783e3b9ecde240109d0eed3c691351ae119(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    action_group_name: builtins.str,
    action_group_executor: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IFunction] = None,
    action_group_state: typing.Optional[builtins.str] = None,
    api_schema: typing.Optional[ApiSchema] = None,
    description: typing.Optional[builtins.str] = None,
    parent_action_group_signature: typing.Optional[builtins.str] = None,
    skip_resource_in_use_check_on_delete: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e47b674f810daa9a7bde371ad21ea6944cc41d81e91b4c04fca71b8f52c01288(
    *,
    action_group_name: builtins.str,
    action_group_executor: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IFunction] = None,
    action_group_state: typing.Optional[builtins.str] = None,
    api_schema: typing.Optional[ApiSchema] = None,
    description: typing.Optional[builtins.str] = None,
    parent_action_group_signature: typing.Optional[builtins.str] = None,
    skip_resource_in_use_check_on_delete: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d5252a70a25f0e579966376a7e29bb2527a503dda1a1fed24527d3559affff2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    agent_id: builtins.str,
    agent_version: typing.Optional[builtins.str] = None,
    alias_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    resource_updates: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cae66eefc5f4c5599e0686171b63cba4b3c09493c31167b8afaa8bff00da6cc(
    *,
    agent_id: builtins.str,
    agent_version: typing.Optional[builtins.str] = None,
    alias_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    resource_updates: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c5254c1c0482eaa66699188ff0467d936350a386bbe823d4ef46c9ba982f91c(
    *,
    foundation_model: BedrockFoundationModel,
    instruction: builtins.str,
    action_groups: typing.Optional[typing.Sequence[AgentActionGroup]] = None,
    alias_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    enable_user_input: typing.Optional[builtins.bool] = None,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    existing_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
    idle_session_ttl: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    knowledge_bases: typing.Optional[typing.Sequence[KnowledgeBase]] = None,
    name: typing.Optional[builtins.str] = None,
    prompt_override_configuration: typing.Optional[typing.Union[PromptOverrideConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    should_prepare_agent: typing.Optional[builtins.bool] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9707019db7cf1339382bbfdc3c35863966765af6485a09c40c302a504ad6876d(
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3690bdbded4fc41debce4f674af4ba9794363c793e9f2f52ac27a4069270b3a3(
    bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c2792cc1fa0f16747e3820d17877eef4b648c9b158bc65527d5d5c852652166(
    schema: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f63a27d3f3e9a3d4c529eccceaa09a947c740c16c6fc454bb2b8aaf2030cee7a(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a607944f95610e7de935c34b4ac51de5be66c1a19adb648c5e285f3ef483bbe7(
    *,
    payload: typing.Optional[builtins.str] = None,
    s3: typing.Optional[typing.Union[S3Identifier, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64a81fd58f8932cf2d8dbd47ee14e3d74d82d0d0245523bd77f54c7a3ebe2a31(
    value: builtins.str,
    *,
    supports_agents: typing.Optional[builtins.bool] = None,
    supports_knowledge_base: typing.Optional[builtins.bool] = None,
    vector_dimensions: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0736a1f1795a1917c49125732e66d2d15e2a25a6b98ac778b58a6ed32dc0df7b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e1a21a71ca2d85f4b0cb18a5ce955b8c59bb0c4403b3d6f750c90739061d548(
    *,
    supports_agents: typing.Optional[builtins.bool] = None,
    supports_knowledge_base: typing.Optional[builtins.bool] = None,
    vector_dimensions: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__befd502c2937a36c672491bd2695d4ec887944e821efe023f2dc44cff4137750(
    *,
    maximum_length: jsii.Number,
    stop_sequences: typing.Sequence[builtins.str],
    temperature: jsii.Number,
    top_k: jsii.Number,
    top_p: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abeb00812cdcb551f5f688ee295d8f225db974111b8872709130c22fef51592f(
    schema: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__429693913d097a23421c6ed72f2363c20d20bbc2d34b374921e37cf4ac8d4157(
    _scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a416de40b883dde9bcfa680e69b09d8d8005e4e5d67e2254f09ebebb1b516bb(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    embeddings_model: BedrockFoundationModel,
    description: typing.Optional[builtins.str] = None,
    existing_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
    index_name: typing.Optional[builtins.str] = None,
    instruction: typing.Optional[builtins.str] = None,
    knowledge_base_state: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    vector_field: typing.Optional[builtins.str] = None,
    vector_index: typing.Optional[_VectorIndex_e5d266e9] = None,
    vector_store: typing.Optional[typing.Union[_AmazonAuroraDefaultVectorStore_ec1da9eb, _AmazonAuroraVectorStore_bde12a1e, _VectorCollection_91bfdaa9, _PineconeVectorStore_c017c196]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ca7cf4ff7c6392dfc7cae12d95e046e86c711e76659c1c94e920f30da3a066c(
    agent: Agent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d77925ffb8d3d9f229cccdf4b13498db4e9b0c20ca077db0cbe11892e0b36d5f(
    *,
    embeddings_model: BedrockFoundationModel,
    description: typing.Optional[builtins.str] = None,
    existing_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role] = None,
    index_name: typing.Optional[builtins.str] = None,
    instruction: typing.Optional[builtins.str] = None,
    knowledge_base_state: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    vector_field: typing.Optional[builtins.str] = None,
    vector_index: typing.Optional[_VectorIndex_e5d266e9] = None,
    vector_store: typing.Optional[typing.Union[_AmazonAuroraDefaultVectorStore_ec1da9eb, _AmazonAuroraVectorStore_bde12a1e, _VectorCollection_91bfdaa9, _PineconeVectorStore_c017c196]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9e333bbbacb815921d7a258c01d4d87250548623e984fd2e844c23791ddeeed(
    *,
    base_prompt_template: builtins.str,
    inference_configuration: typing.Union[InferenceConfiguration, typing.Dict[builtins.str, typing.Any]],
    prompt_creation_mode: PromptCreationMode,
    prompt_state: PromptState,
    prompt_type: PromptType,
    parser_mode: typing.Optional[ParserMode] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87069825e4e1447731b12e085f8869b15f2bd52ca2b57df2d0342674371c9580(
    *,
    prompt_configurations: typing.Sequence[typing.Union[PromptConfiguration, typing.Dict[builtins.str, typing.Any]]],
    override_lambda: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04c4db74d64f90be972766dae3c6ab8b2ee388726bb4dec1fa1458939ab93a5f(
    bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdd50c8c86df0f0a2a5a95b774555d2e2c1d079404953f77717653ea8e3f768a(
    _scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48fbbb836e75c99d63b1aecb8d429a451f727eaf6d350fa9c8a3e73f4932c719(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    data_source_name: builtins.str,
    knowledge_base: KnowledgeBase,
    chunking_strategy: typing.Optional[ChunkingStrategy] = None,
    inclusion_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    max_tokens: typing.Optional[jsii.Number] = None,
    overlap_percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__061fd79f5c6cc3fdad0a0fcccc8c2a083f5deeb769270d6795cc47edeeaecc0b(
    *,
    bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    data_source_name: builtins.str,
    knowledge_base: KnowledgeBase,
    chunking_strategy: typing.Optional[ChunkingStrategy] = None,
    inclusion_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    max_tokens: typing.Optional[jsii.Number] = None,
    overlap_percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8dfefeb74c7ac32b2ae5113a03ce2743b27b34cfa67e342053f0fb90d0050f0(
    *,
    s3_bucket_name: builtins.str,
    s3_object_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
