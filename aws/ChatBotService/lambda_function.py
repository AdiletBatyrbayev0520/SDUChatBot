import json
import boto3
import os
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Tuple
import logging
from boto3.dynamodb.types import Decimal
import uuid


KNOWLEDGE_BASE_ID = os.environ['KNOWLEDGE_BASE_ID']
MODEL_ID = os.environ.get('MODEL_ID')
PROMPT_ID = os.environ['PROMPT_ID']
PROMPT_VERSION = os.environ['PROMPT_VERSION']
CONDENSE_PROMPT_ID = os.environ['CONDENSE_PROMPT_ID']
CONDENSE_PROMPT_VERSION = os.environ['CONDENSE_PROMPT_VERSION']
TOPIC_PROMPT_ID = os.environ['TOPIC_PROMPT_ID']
TOPIC_PROMPT_VERSION = os.environ['TOPIC_PROMPT_VERSION']
REGION_NAME = os.environ['REGION_NAME']
RERANKER_MODEL_ID = os.environ['RERANKER_MODEL_ID']

bedrock_runtime = boto3.client('bedrock-runtime', region_name=REGION_NAME)
bedrock_agent_runtime = boto3.client('bedrock-agent-runtime')
bedrock_agent = boto3.client(service_name="bedrock-agent")
dynamodb = boto3.resource('dynamodb')
chat_history_table = os.environ['CHAT_HISTORY_TABLE']
chat_table = dynamodb.Table(chat_history_table)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.info(boto3.__version__)

logger.info(f"KNOWLEDGE_BASE_ID: {KNOWLEDGE_BASE_ID}\nMODEL_ID: {MODEL_ID}\nREGION_NAME: {REGION_NAME}\nRERANKER_MODEL_ID:{RERANKER_MODEL_ID}")
class ConversationalRetirevalChain:
    def __init__(self, chat_history=None, question="", main_prompt="", condense_prompt="", topic_prompt="", current_time=""):
        self.topic = "New Chat"
        self.chat_history = chat_history or []
        self.question = question
        self.condensed_question = question
        self.input_tokens = 0
        self.output_tokens = 0
        self.total_tokens = 0
        self.cacheReadInputTokens = 0
        self.cacheWriteInputTokens = 0
        self.cacheHitCount = 0
        self.costUsd = 0.0
        self.contextualized_chat_history = []
        self.chat_history_for_converse = []
        self.unfilled_condense_prompt = condense_prompt
        self.unfilled_main_prompt = main_prompt
        self.unfilled_topic_prompt = topic_prompt
        self.current_time = current_time
        if chat_history:
            self.format_chat_history_for_converse()
            self.contextualize_chat_history()
            self.condense_question()
            
    def _get_anthropic_claude_token_cost(self, input_tokens: int, output_tokens: int, cacheWriteInputTokens: int, cacheReadInputTokens: int) -> float:
        """Get the cost of tokens for the Claude model."""
        return (input_tokens / 1000) * 0.003 + (output_tokens / 1000) * 0.015 + (cacheWriteInputTokens / 1000) * 0.00375 + (cacheReadInputTokens / 1000) * 0.0003

    def update_usage_metadata(self, input_tokens, output_tokens, cacheReadInputTokens, cacheWriteInputTokens, total_tokens=0):
        self.output_tokens += output_tokens
        self.cacheReadInputTokens += cacheReadInputTokens
        self.cacheWriteInputTokens += cacheWriteInputTokens
        if total_tokens == 0:
            self.total_tokens += (input_tokens + output_tokens)
        else:
            self.total_tokens += total_tokens
            input_tokens = total_tokens-output_tokens
        self.input_tokens += input_tokens
        if cacheReadInputTokens != 0:
            self.cacheHitCount += 1
        self.costUsd += self._get_anthropic_claude_token_cost(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cacheReadInputTokens=cacheReadInputTokens,
            cacheWriteInputTokens=cacheWriteInputTokens
        )
    
    def get_usage_metadata(self):
        usage_metadata_dict = {
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "total_tokens": self.total_tokens,
            "cacheReadInputTokens": self.cacheReadInputTokens,
            "cacheWriteInputTokens": self.cacheWriteInputTokens,
            "cacheHitCount": self.cacheHitCount,
            "costUsd": self.costUsd
        }
        return usage_metadata_dict

    def model_invoke(self, prompt):
        try:
            native_request = {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 4096,
                    "temperature": 0.0,
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text", 
                                    "text": prompt,
                                    "cache_control": {
                                        "type": "ephemeral"
                                    }
                                }             
                            ],
                        }
                    ],
                }
            request = json.dumps(native_request)
            response = bedrock_runtime.invoke_model(modelId=MODEL_ID, body=request)
            logger.info(f"Response from model invoke: {response}")
            model_response_body = json.loads(response["body"].read())
            logger.info(f"Model response body: {model_response_body}")
            usage_metadata = model_response_body["usage"]
            cacheWriteInputTokens = usage_metadata["cache_creation_input_tokens"]
            cacheReadInputTokens = usage_metadata["cache_read_input_tokens"]
            input_tokens = usage_metadata["input_tokens"]
            output_tokens = usage_metadata["output_tokens"]
            self.update_usage_metadata(input_tokens, output_tokens, cacheReadInputTokens, cacheWriteInputTokens)
            response_text = model_response_body["content"][0]["text"]
            logger.info(f"Model invoked successfully: {response_text}, \n\n1.Input_tokens: {input_tokens}\n2.Output_tokens: {output_tokens}\n3.CacheReadInputTokens: {cacheReadInputTokens}\n4.CacheWriteInputTokens: {cacheWriteInputTokens}")
            return response_text
        except Exception as e:
            logger.error(f"Error in model_invoke: {e}")
            raise 

    def model_converse(self, prompt):
        try:
            messages = self.get_chat_history_for_converse()
            messages.append(self.get_user_message_formatted(self.condensed_question))

            response = bedrock_runtime.converse(
                modelId=MODEL_ID, 
                messages=messages, 
                system=[
                    {
                        'text': prompt
                    },
                    {
                        'cachePoint': {
                            'type': 'default'
                        }
                    }
                ],
                inferenceConfig={
                    'maxTokens': 4096,
                    'temperature': 0.0
                }
            )
            logger.info(f"Response from model invoke: {response}")
            usage_metadata = response["usage"]
            cacheWriteInputTokens = usage_metadata["cacheWriteInputTokens"]
            cacheReadInputTokens = usage_metadata["cacheReadInputTokens"]
            input_tokens = usage_metadata["inputTokens"]
            output_tokens = usage_metadata["outputTokens"]
            total_tokens = usage_metadata["totalTokens"]
            self.update_usage_metadata(input_tokens, output_tokens, cacheReadInputTokens, cacheWriteInputTokens, total_tokens)
            response_text = response['output']['message']['content'][0]['text']
            logger.info(f"Model Converse invoked successfully: {response_text}, \n\n1.Input_tokens: {input_tokens}\n2.Output_tokens: {output_tokens}\n3.CacheReadInputTokens: {cacheReadInputTokens}\n4.CacheWriteInputTokens: {cacheWriteInputTokens}")
            return response_text
        except Exception as e:
            logger.error(f"Error in model_converse: {e}")
            raise
    
    def get_user_message_formatted_cache(self, question: str) -> Dict:
        return {
            "role": "user",
            "content": [
                {
                    "text": question,
                },
                {
                    'cachePoint': {
                        'type': 'default'
                    }
                }
            ],
        }

    def get_user_message_formatted(self, question: str) -> Dict:
        userMessage = {
            "role": "user",
            "content": [
                {
                    "text": question,
                }
            ]
        }
        return userMessage

    def get_assistant_message_formatted(self, answer: str) -> Dict:
        return {
            "role": "assistant",
            "content": [
                {
                    "text": answer,
                }
            ],
        }

    def format_chat_history_for_converse(self):
        if not self.chat_history:            
            logger.info("format_chat_history_for_converse: No chat history to format.")
            return []

        for idx, item in enumerate(self.chat_history):
            is_last_two = idx >= len(self.chat_history) - 2
            if is_last_two:
                user_message = self.get_user_message_formatted_cache(item['question'])
            else:
                user_message = self.get_user_message_formatted(question=item['question'])
            self.chat_history_for_converse.append(user_message)
            assistant_message = self.get_assistant_message_formatted(item['answer'])
            self.chat_history_for_converse.append(assistant_message)

        logger.info(f"Formatted {len(self.chat_history_for_converse)} messages from {len(self.chat_history[-2:])} conversations")

    def get_chat_history_for_converse(self) -> List[Dict]:
        return self.chat_history_for_converse

    def contextualize_chat_history(self):
        required_keys = ['question', 'answer']  
        for item in self.chat_history:
            contextualized_chat_item = {key: item[key] for key in required_keys if key in item}
            self.contextualized_chat_history.append(contextualized_chat_item)
        logger.info(f"Contextualized chat history ({len(self.contextualized_chat_history)} conversations): {self.contextualized_chat_history}")

    def get_contextualized_chat_history(self) -> List[Dict]:
        return self.contextualized_chat_history

    def generate_topic(self):
        if self.chat_history or self.question:
            filled_topic_prompt = self.unfilled_topic_prompt.format(
                chat_history=self.chat_history,
                question=self.question,
                current_time=self.current_time
            )
            logger.info(f"Topic Prompt formatted successfully: {filled_topic_prompt}")
            self.topic = self.model_invoke(filled_topic_prompt)
            logger.info(f"Topic: {self.topic}")

    def get_topic(self):
        return self.topic
        
    def condense_question(self):
        if self.chat_history:
            filled_condense_prompt = self.unfilled_condense_prompt.format(
                chat_history=self.get_contextualized_chat_history(),
                question=self.question,
                current_time=self.current_time
            )
            logger.info(f"Condense Prompt formatted successfully: {filled_condense_prompt}")
            self.condensed_question = self.model_invoke(filled_condense_prompt)
    
    def get_condensed_question(self):
        return self.condensed_question

def load_prompt(promptIdentifier, promptVersion) -> str:
    try:
        response = bedrock_agent.get_prompt(
            promptIdentifier=promptIdentifier,
            promptVersion=promptVersion
        )
        logger.info(f"Not Filtered Prompt: {response}")
        
        system_instructions = response['variants'][0]['templateConfiguration']['chat']['system'][0]['text']
        logger.info(f"System Instructions: {system_instructions}")
        
        user_message = response['variants'][0]['templateConfiguration']['chat']['messages'][0]['content'][0]['text']
        logger.info(f"User Message: {user_message}")
        
        prompt_text = system_instructions + '\n' + user_message
        prompt_text = prompt_text.replace('{{', '{').replace('}}', '}')
        logger.info(f"Final Prompt: {prompt_text}")
        return prompt_text
    except Exception as e:
        logger.error(f"Failed to load prompt: {e}")
        return "Default prompt fallback"

unfilled_main_prompt = load_prompt(PROMPT_ID, PROMPT_VERSION)
unfilled_condense_prompt = load_prompt(CONDENSE_PROMPT_ID, CONDENSE_PROMPT_VERSION)
unfilled_topic_prompt = load_prompt(TOPIC_PROMPT_ID, TOPIC_PROMPT_VERSION)

def get_chat_history(chat_id: str, limit: int = 7) -> List[Dict]:
    try:
        response = chat_table.query(  
            IndexName='user-id-timestamp-index',
            KeyConditionExpression=boto3.dynamodb.conditions.Key('user_id').eq(chat_id),
            ScanIndexForward=False,  # Sort by timestamp descending
            Limit=limit
        )
        
        items = response.get('Items', [])
        items.reverse()
        logger.info(f"Retrieved {len(items)} chat history items for user {chat_id}")
        return items
        
    except Exception as e:
        logger.error(f"Error querying chat history for user {chat_id}: {str(e)}")  # Fixed: was 'questioning'
        return []

def save_chat_message(chat_id: str, question: str, answer: str,
                     sources: list, conversation_id: str = None):
    try:
        timestamp = datetime.now().isoformat()
        if not conversation_id:
            conversation_id = f"{chat_id}-{str(uuid.uuid4())[:8]}"
        ttl = int((datetime.now() + timedelta(days=30)).timestamp())
        item = {
            'conversation_id': conversation_id,
            'user_id': chat_id,
            'timestamp': timestamp,
            'question': question,
            'answer': answer,
            'sources': sources,
            'ttl': ttl
        }
        chat_table.put_item(Item=item)
        return conversation_id
        
    except Exception as e:
        logger.error(f"Error saving chat message: {str(e)}")
        return None

def get_filter():
    filter_ret= {
        "andAll": [
            {
                "equals": {
                    "key": "genres",
                    "value": "Strategy"
                }
            },
            {
                "greaterThanOrEquals": {
                    "key": "year",
                    "value": 2023
                }
            }
        ]
    }   

    return filter_ret

def rerank(query, docs, limit=5):
    try:
        sources = []
        for i, doc in enumerate(docs):
            sources.append({
                "type": "INLINE",
                "inlineDocumentSource": {
                    "type": "TEXT",
                    "textDocument": {
                        "text": doc['content']
                    }
                }
            })

        rerank_request = {
            "rerankingConfiguration": {
                "type": "BEDROCK_RERANKING_MODEL",
                "bedrockRerankingConfiguration": {
                    "modelConfiguration": {
                        "modelArn": f"arn:aws:bedrock:{REGION_NAME}::foundation-model/{RERANKER_MODEL_ID}"
                    }
                }
            },
            "queries": [
                {
                    "type": "TEXT",
                    "textQuery": {
                        "text": query
                    }
                }
            ],
            "sources": sources
        }
        
        rerank_response = bedrock_agent_runtime.rerank(**rerank_request)
        reranked_results = []

        if 'results' in rerank_response and len(rerank_response['results']) > 0:
            query_results = rerank_response['results'][0]  
            if 'results' in query_results:
                for result in query_results['results']:
                    source_index = result['index']
                    score = result['relevanceScore']
                    original_doc = docs[source_index]
                    original_doc_with_score = original_doc.copy()
                    original_doc_with_score['rerank_score'] = score
                    reranked_results.append((score, original_doc_with_score))
                
                reranked_results.sort(key=lambda x: x[0], reverse=True)
                reranked_docs = [doc for _, doc in reranked_results]
                
                logger.info(f"Reranked {len(reranked_docs)} documents successfully")
                return reranked_docs[:limit]
        
        logger.warning(f"Reranking returned no results, returning original documents with limit: {limit}")
        return docs[:limit]
        
    except Exception as e:
        logger.error(f"Error in reranking: {e}")
        return docs[:limit]


def retrieve_docs_from_kb(question: str) -> Tuple[List[str], List[Dict[str, Any]]]:
    
    if not question or not question.strip():
        logger.error("Empty or invalid question provided")
        raise ValueError("Question cannot be empty")
    
    logger.info(f"Starting knowledge base retrieval for question: '{question[:100]}{'...' if len(question) > 100 else ''}'")
    
    try:
        logger.debug(f"Calling bedrock_agent_runtime.retrieve with knowledgeBaseId: {KNOWLEDGE_BASE_ID}")
        kb_response = bedrock_agent_runtime.retrieve(
            knowledgeBaseId=KNOWLEDGE_BASE_ID,
            retrievalQuery={
                'text': question
            },
            retrievalConfiguration={
                'vectorSearchConfiguration': {
                    'numberOfResults': 10,
                    'overrideSearchType': 'HYBRID',
                }
            }
        )
        logger.debug("Successfully retrieved response from knowledge base")
        logger.info(f"Knowledge base response: {kb_response}")
    except Exception as e:
        logger.error(f"Failed to retrieve from knowledge base: {str(e)}", exc_info=True)
        return [], []
        # raise Exception(f"Knowledge base retrieval failed: {str(e)}") from e
    
    sources = []
    try:
        retrieval_results = kb_response.get('retrievalResults', [])
        if not retrieval_results:
            logger.warning("No retrieval results found in knowledge base response")
            return [], []
        
        logger.info(f"Retrieved {len(retrieval_results)} raw results from knowledge base")
        
        try:
            sorted_kb_response = sorted(
                retrieval_results, 
                key=lambda x: x.get('score', 0), 
                reverse=True
            )
            logger.debug("Successfully sorted results by score")
        except Exception as e:
            logger.warning(f"Failed to sort results by score, using original order: {str(e)}")
            sorted_kb_response = retrieval_results
        
        for i, result in enumerate(sorted_kb_response):
            try:
                content = ''
                if isinstance(result.get('content'), dict):
                    content = result.get('content', {}).get('text', '')
                else:
                    logger.warning(f"Unexpected content structure in result {i}")
                    continue
                
                if not content or not content.strip():
                    logger.debug(f"Skipping result {i} - no content found")
                    continue
                
                score = result.get('score', 0)
                
                try:
                    score_decimal = Decimal(str(score))
                except (ValueError, TypeError) as e:
                    logger.warning(f"Failed to convert score to Decimal for result {i}: {str(e)}")
                    score_decimal = Decimal('0')
                
                source_data = {
                    'content': content,
                    'score': score_decimal,
                    'location': result.get('location', {}),
                    'metadata': result.get('metadata', {})
                }
                sources.append(source_data)
                logger.debug(f"Processed result {i} with score {score}")
                
            except Exception as e:
                logger.warning(f"Failed to process result {i}: {str(e)}", exc_info=True)
                continue
        
        logger.info(f"Successfully processed {len(sources)} sources from {len(retrieval_results)} raw results")
        
    except Exception as e:
        logger.error(f"Failed to process knowledge base results: {str(e)}", exc_info=True)
        return [], []
    
    if RERANKER_MODEL_ID and sources:
        try:
            logger.info(f"Applying reranking with model {RERANKER_MODEL_ID}")
            reranked_sources = rerank(question, sources)
            if reranked_sources is not None:
                sources = reranked_sources
                logger.info(f"Successfully applied reranking to {len(sources)} sources")
            else:
                logger.warning("Reranking returned None, using original sources")
        except Exception as e:
            logger.error(f"Reranking failed, using original sources: {str(e)}", exc_info=True)
    elif not RERANKER_MODEL_ID:
        logger.debug("No reranker model configured, skipping reranking")
    elif not sources:
        logger.warning("No sources available for reranking")
    
    context_chunks = []
    try:
        for i, source in enumerate(sources):
            try:
                content = source.get('content', '')
                if content and content.strip():
                    context_chunks.append(content)
                else:
                    logger.debug(f"Skipping empty content for source {i}")
            except Exception as e:
                logger.warning(f"Failed to extract content from source {i}: {str(e)}")
                continue
        
        logger.info(f"Extracted {len(context_chunks)} context chunks from {len(sources)} sources")
        
    except Exception as e:
        logger.error(f"Failed to extract context chunks: {str(e)}", exc_info=True)
        return [], sources
    
    if context_chunks:
        logger.info(f"Successfully retrieved {len(context_chunks)} context chunks")
        logger.debug(f"Context chunk lengths: {[len(chunk) for chunk in context_chunks[:5]]}")
        
        if sources:
            scores = [float(source.get('score', 0)) for source in sources[:5]]
            logger.debug(f"Top 5 source scores: {scores}")
    else:
        logger.warning("No context chunks retrieved - this may indicate a problem with the knowledge base or query")
    
    return context_chunks, sources
    
    
def create_response(status_code, body, headers=None):
    if headers is None:
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        }
    
    return {
        'statusCode': status_code,
        # 'headers': headers,
        'body': json.dumps(body, ensure_ascii=False) if isinstance(body, dict) else body
    }

def lambda_handler(event, context):
    logger.info(f"Received event: {json.dumps(event, default=str)}")
    http_method = event.get('requestContext', {}).get('http', {}).get('method') or event.get('httpMethod')
    raw_path = event.get('requestContext', {}).get('http', {}).get('path') or event.get('path', '/')
    origin = '*'
    logger.info(f"HTTP Method: {http_method}, Path: {raw_path}, Origin: {origin}")
    
    if http_method == 'OPTIONS':
        return create_response(200, {'message': 'CORS preflight successful'})

    if http_method == 'GET':
        try:
            with open('api_docs.json', 'r') as json_file:
                api_docs = json.load(json_file)
                return create_response(200, {'body': api_docs})
        except FileNotFoundError:
            return create_response(404, {'error': 'API docs not found'})


    if http_method == 'POST':
        try:
            raw_body = event.get('body', '')
            utc_plus5 = timezone(timedelta(hours=5))
            current_time = datetime.now(utc_plus5)
            formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
            if not raw_body:
                raise ValueError("Request body is empty")
            body = json.loads(raw_body) if isinstance(raw_body, str) else raw_body
            
            question = body.get('question', '')
            chat_id = body.get('chat_id', '')
            is_need_topic = body.get('is_need_topic', False)
            if not question:
                return create_response(400, {'error': 'Missing required parameter: question'})
            if not chat_id:
                return create_response(400, {'error': 'Missing required parameter: chat_id'})

            logger.info(f"Question: {question}, User ID: {chat_id}, need topic: {is_need_topic}")
            
            chat_history = get_chat_history(chat_id=chat_id)
            chain = ConversationalRetirevalChain(
                chat_history=chat_history, 
                question=question, 
                condense_prompt = unfilled_condense_prompt,
                topic_prompt = unfilled_topic_prompt,
                current_time = formatted_time
            )
            if is_need_topic:
                chain.generate_topic()
                logger.info(f"Topic generated successfully: {chain.get_topic()}")
            condensed_question = chain.get_condensed_question()
            logger.info(f"Condense Model invoked successfully: {condensed_question}")

            context_chunks, sources = retrieve_docs_from_kb(condensed_question)
            context = "\n\n".join(context_chunks)

            filled_prompt = unfilled_main_prompt.format(
                context=context,
                current_time=current_time
            )
            logger.info(f"Prompt formatted successfully: {filled_prompt}")

            # answer = model_invoke(filled_prompt)
            answer = chain.model_converse(prompt=filled_prompt)            

            source_uris = []
            for source in sources:
                    source_uri = source.get('location', {}).get('s3Location', {}).get('uri', '')
                    if source_uri:
                        source_uris.append(source_uri)
            
            logger.info(f"Response received from model: {answer}")
            if answer:
                save_chat_message(chat_id=chat_id, question=question, answer=answer, 
                                    sources=source_uris)
                locations = []
                for source in sources:
                    location = str(source.get('location', {}).get('s3Location', {}).get('uri', '')).split('/')[-1]
                    if location:
                        locations.append(location)

                logger.info(f"Sources: {locations}")
                usage_metadata = chain.get_usage_metadata()
                result = {
                    'question': question,
                    'answer': answer,
                    'sources': locations,
                    'usage_metadata': usage_metadata,
                }
                if is_need_topic:
                    result['topic'] = chain.get_topic()
                    
                body_content = json.dumps(result, ensure_ascii=False)
                
                logger.info(f"Returning response with status: {result.get('statusCode', 200)}")
                logger.info(f"Response body preview: {body_content[:200]}...")

                return create_response(200, result)
            else:
                result = {'error': 'No response from model'}
                return create_response(500, {'error': 'No response from model'})
        except ValueError as ve:
            return create_response(400, {'error': 'Invalid request', 'message': str(ve)})
        except Exception as e:
            logger.error(f"POST processing error: {e}", exc_info=True)
            return create_response(500, {'error': 'Internal server error', 'message': str(e)})

    return create_response(404, {'error': 'Not Found', 'message': f'Path {raw_path} not found'})