"""
  ____       _ ____  _ _         _____           _ _    _ _
 / ___|  ___(_) __ )(_) |_ ___  |_   _|__   ___ | | | _(_) |_
 \___ \ / __| |  _ \| | __/ _ \   | |/ _ \ / _ \| | |/ / | __|
  ___) | (__| | |_) | | ||  __/   | | (_) | (_) | |   <| | |_
 |____/ \___|_|____/|_|\__\___|   |_|\___/ \___/|_|_|\_\_|\__|

SearchRequestBuilder- make requests to the Scibite Search API and process results.

"""

__author__ = 'SciBite'
__version__ = '0.6.2'
__copyright__ = '(c) 2024, SciBite Ltd'
__license__ = 'Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License'

import json

import requests
import re
import os
import sys
import pprint
import pandas as pd


####################################################################################################################
# Request Builder object contains all functions that actually require a working connection to SciBite Search       #
####################################################################################################################

class SBSRequestBuilder:
    """
    Class for creating SciBite Search requests
    """

    def __init__(self):
        self.url = ""
        self.auth_url = ""
        self.token_url = ""
        self.payload = {"output": "json", "method": "texpress"}
        self.options = {}
        self.basic_auth = ()
        self.verify_request = True

    def set_oauth2_legacy(self, client_id, username, password, verification=True):
        """
        For SciBite Search version < 2.2

        Pass username and password for the Scibite Search token api
        It then uses these credentials to generate an access token and adds
        this to the request header.
        :client_id: client_id to access the token api
        :username: scibite search username
        :password: scibite search password for username above
        """
        if self.token_url != "":
            token_address = self.token_url + "/auth/realms/Scibite/protocol/openid-connect/token"
        # SaaS set up uses a different url for authentication
        elif self.auth_url != "":
            token_address = self.auth_url + "/auth/realms/Scibite/protocol/openid-connect/token"
        else:
            token_address = self.url + "/auth/realms/Scibite/protocol/openid-connect/token"

        req = requests.post(token_address, data={"grant_type": "password", "client_id": client_id, "username": username,
                                                 "password": password},
                            headers={"Content-Type": "application/x-www-form-urlencoded"})
        access_token = req.json()["access_token"]
        self.headers = {"Authorization": "Bearer " + access_token}
        self.verify_request = verification

    def set_oauth2(self, client_id, client_secret, verification=True):
        """
        For SciBite Search version >= 2.2

        Pass client id and client secret for the Scibite Search token api
        It then uses these credentials to generate an access token and adds
        this to the request header.
        :client_id: client_id to access the token api e.g. scibitesearch-app
        :client_secret: scibite search client_secret for API use
        """
        if self.token_url != "":
            token_address = self.token_url + "/auth/realms/Scibite/protocol/openid-connect/token"
        # SaaS set up uses a different url for authentication
        elif self.auth_url != "":
            token_address = self.auth_url + "/auth/realms/Scibite/protocol/openid-connect/token"
        else:
            token_address = self.url + "/auth/realms/Scibite/protocol/openid-connect/token"

        req = requests.post(token_address, data={"grant_type": "client_credentials", "client_id": client_id,
                                                 "client_secret": client_secret},
                            headers={"Content-Type": "application/x-www-form-urlencoded"})
        access_token = req.json()["access_token"]
        self.headers = {"Authorization": "Bearer " + access_token}
        self.verify_request = verification

    def set_token_url(self, token_url):
        """Set the URL for the token API
        :token_url: the URL for the token API
        """
        self.token_url = token_url.rstrip('/')

    def set_url(self, url):
        """
        Set the URL of the Scibite Search instance
        :url: the URL of the Scibite Search instance to be hit
        """
        self.url = url.rstrip('/')

    def set_auth_url(self, auth_url):
        """
        Set the URL of the Scibite Search instance
        :url: the URL of the Scibite Search instance to be hit
        for SaaS instances only, this is different to the search url
        """
        self.auth_url = auth_url.rstrip('/')

    def get_docs(self, query='', markup=True, limit=20, offset=0, additional_fields=[]):
        """This endpoint allows searching and retrieval of documents.
        :query: SSQL query
        :type query: string
        :markup: Whether annotated text should markup the entities
        :type markup: bool
        :limit: Limits the number of results
        :type limit: int
        :offset: The number of resources to skip before returning results. Used for implementing paging.
        :type offset: int
        :additional_fields: Additional document fields to output in the response
        :type additional_fields: list of strings. If ['*'] it will get all fields from that doc schema.
        """
        options = {"markup": markup, "limit": limit, "offset": offset}
        if query:
            options["queries"] = query
        if additional_fields:
            options["fields"] = additional_fields

        req = requests.get(self.url + "/api/search/v1/documents", params=options, headers=self.headers,
                           verify=self.verify_request)
        return req.json()

    def get_entities(self, synonym_name="", limit=20, additional_fields=[]):
        """Wrapper to call the entity endpoint. Currently only working with the synonymName option. """
        options = {"limit": limit}
        if synonym_name:
            options["synonymName"] = synonym_name
        if additional_fields:
            options["fields"] = additional_fields

        req = requests.get(self.url + "/api/search/v1/entities", params=options, headers=self.headers,
                           verify=self.verify_request)
        return req.json()

    def get_document(self, document_id, query='', markup=True):
        """This endpoint retrieves a customizable view of a document
        :document_id: required, the id of the document to be retrieved
        :type document_id: str
        :query: optional, SSQL query
        :type query: str
        :markup: optional, whether annotated text should markup the entities. Default is true
        :type markup: bool
        """
        options = {"markup": markup}
        if query:
            options["queries"] = query

        req = requests.get(self.url + "/api/search/v1/documents/" + document_id, params=options, headers=self.headers,
                           verify=self.verify_request)
        return req.json()

    def get_sentences(self, query='', markup=True, limit=20, offset=0):
        """This endpoint allows searching and retrieval of the sentences in the documents.
        :query: SSQL query
        :markup: Whether annotated text should markup the entities
        :limit: Limits the number of results
        :offset: The number of resources to skip before returning results. Used for implementing paging.
        """
        options = {"markup": markup, "limit": limit, "offset": offset}
        if query:
            options["queries"] = query

        req = requests.get(self.url + "/api/search/v1/sentences/", params=options, headers=self.headers,
                           verify=self.verify_request)
        return req.json()

    def get_searchlogs(self, limit=20, offset=0):
        """ Function to call the GET searchlogs endpoint for search usage API
        Args:
            limit (int, optional): _description_. Defaults to 20.
            offset (int, optional): _description_. Defaults to 0.
        """
        options = {"limit": limit, "offset": offset}
        req = requests.get(self.url + "/api/search-usage/v1/searchlogs", params=options, headers=self.headers,
                           verify=self.verify_request)
        return req.json()

    def get_aggregates(self, query='', vocabs=[], sentences=True, significant=False, limit=20, offset=0):
        """This function hits either the document aggregates or sentence aggregates API
        endpoints and returns aggregate counts for the provided query
        :query: SSQL query
        :vocabs: list of vocabularies to select the entity counts from
        :sentences: True for sentence aggregates, False for Document counts
        :significant: If true it sorts by significance score, if false it sorts by count
        :limit: Limits the number of results
        :offset: The number of resources to skip before returing results. Used for implementing paging.
        """
        options = {"limit": limit, "offset": offset, "includeVocabularies": vocabs}
        if query:
            options["queries"] = query
        if sentences:
            if significant:
                req = requests.get(self.url + "/api/search/v1/sentence-aggregates/significant-entity", params=options,
                                   headers=self.headers, verify=self.verify_request)
            else:
                req = requests.get(self.url + "/api/search/v1/sentence-aggregates/entity", params=options,
                                   headers=self.headers, verify=self.verify_request)
        else:
            if significant:
                req = requests.get(self.url + "/api/search/v1/document-aggregates/significant-entity", params=options,
                                   headers=self.headers, verify=self.verify_request)
            else:
                req = requests.get(self.url + "/api/search/v1/document-aggregates/entity", params=options,
                                   headers=self.headers, verify=self.verify_request)
        return req.json()

    def get_pipelines(self, datasetId='', limit=20, offset=0):
        """This endpoint calls the jobs API to get the description of a pipeline"""
        # options = {'datasetId':datasetId,'limit':limit,'offset':offset}
        # not sure why in this case limit and offset should be sent like that instead of options?
        # pending to implement datasetId
        req = requests.get(
            self.url + "/jobserver/jobs/v1/ingest-pipelines?limit=" + str(limit) + "&offset=" + str(offset),
            headers=self.headers, verify=self.verify_request)
        return req.json()

    def get_pipeline_by_id(self, id=''):
        """This endpoint calls the jobs API to get the description of a pipeline
        :id: the SciBite Search uuid for the pipeline you want to retrieve
        :type id: str
        """
        if id:
            options = {"id": id}
        else:
            raise ValueError('You need to provide a string id for the pipeline to be obtained')

        # You first need to get the identifier using another endpoint
        # This is a first naive implementation without considering paging
        pipelines = self.get_pipelines()
        pipelines = pipelines['data']
        for i, pipeline_object in enumerate(pipelines):
            if pipeline_object['name'] == id:
                uuid = pipeline_object['id']
                req = requests.get(self.url + "/jobserver/jobs/v1/ingest-pipelines/" + uuid, params=options,
                                   headers=self.headers, verify=self.verify_request)
                return req.json()
        print('No pipeline was found with such name')

    def document_schemas(self, json_body):
        """This endpoint posts a new document schema to a ScibiteSearch instance
        :json_body: a valid JSON containing the new document schema with the correct fields
        :type json_body: JSON string"""
        headers = self.headers
        headers['Content-type'] = 'application/json'
        requests.post(self.url + '/api/search/v1/document-schemas', json=json_body, headers=headers,
                      verify=self.verify_request)


class SBSChat:

    def __init__(self, instance_of_sbs):
        self.conversation_id = ""
        self.SBS_instance = instance_of_sbs
        self.conversation_obj_list = []

    def start_conversation(self, question, num_candidates=10, filter_query='', rewrite_question=True):
        """
        wrapper for post /conversations. Submit a question to start a new conversation for the logged-in user.
        The conversation objects will be saved to the class variable conversation_obj_list.
        @param question: <string> question to submit.
        @param num_candidates: <int> number of documents to return to answer the question. Restricted by token limit.
        @param filter_query: <string> SSQL query to filter documents returned to answer questions as needed.
                             For example, you can filter documents that were published after 2022
                             via "publish_date >= 2022-01-01"
        @param rewrite_question: <boolean> pass True if you want the system to rewrite the question. Pass False if you
                                 don't want it to rewrite.
        """
        json_input_body = {
            "question": question,
            "candidates": num_candidates,
            "filterQuery": filter_query,
            "rewriteQuestion": rewrite_question
        }
        headers = self.SBS_instance.headers
        verify = self.SBS_instance.verify_request
        req = requests.post(self.SBS_instance.url + '/api/answer/v1/conversations', json=json_input_body,
                            verify=verify, headers=headers)

        self.conversation_obj_list = translate_resp_into_list(req)
        self.conversation_id = self.conversation_obj_list[0]['conversationId']

    def continue_conversation(self, question, num_candidates=10, filter_query='', rewrite_question=True,
                              conversation_id='', ):
        """
        wrapper for /conversations/{conversationId}/questions. Given a conversation id (that was created by the
        logged-in user) this method will submit a new question for that conversation. The conversation objects will be
        saved to the class variable conversation_obj.list
        @param question: <string> question to submit.
        @param num_candidates: <int> number of documents to return to answer the question. Restricted by token limit.
        @param filter_query: <string> SSQL query to filter documents returned to answer questions as needed.
                             For example, you can filter documents that were published after 2022
                             via "publish_date >= 2022-01-01"
        @param rewrite_question: <boolean> pass True if you want the system to rewrite the question. Pass False if you
                                 don't want it to rewrite.
        @param conversation_id: <string> id of conversation you want to continue.
        """
        json_input_body = {
            "question": question,
            "candidates": num_candidates,
            "filterQuery": filter_query,
            "rewriteQuestion": rewrite_question
        }
        if conversation_id != '':
            self.conversation_id = conversation_id
        headers = self.SBS_instance.headers
        verify = self.SBS_instance.verify_request

        req = requests.post(
            '{}/api/answer/v1/conversations/{}/questions'.format(self.SBS_instance.url, self.conversation_id),
            json=json_input_body, verify=verify, headers=headers)

        self.conversation_obj_list = translate_resp_into_list(req)
        self.conversation_id = self.conversation_obj_list[0]['conversationId']


def retrieve_conversation(conversation_id, sbs_request_builder_class):
    url = sbs_request_builder_class.url
    headers = sbs_request_builder_class.headers
    verify = sbs_request_builder_class.verify_request
    req = requests.get('{}/api/answer/v1/conversations/{}'.format(url, conversation_id), headers=headers, verify=verify)
    try:
        if req.ok:
            return req.json()
        else:
            print('Error with input. ', req.text)
    except ValueError:
        print('No conversation found for logged in user with that conversation id. ', conversation_id)


def get_candidates(sbs_request_builder_class, question, strategy='SIMPLE', limit=20, markup=False, sort=[],fields=[]):
    """_summary_

    Args:
        sbs_request_builder_class (_type_): _description_
        question (_type_): _description_
        strategy (str, optional): _description_. Defaults to 'SIMPLE'. Can also be 'OPENAI'.
        limit (int, optional): _description_. Defaults to 20. Maximum value is 1000.
        markup (bool, optional): _description_. Defaults to False.
        sort (list,optional): Set of sortable fields from the documents to use for ordering the pulled documents. Defaults to
        field (list,optional): Set of fields of the document to return. 
    """
    # TODO: add all options from the endpoint in swagger
    # TODO: figure out sorting and strategy well
    options = {"textQuestion": question, "strategy": strategy, "limit": limit, "markup": markup}
    if fields!=[]:
        options["fields"]=fields
    if sort!=[]:
        options["sort"]=sort

    req = requests.get(sbs_request_builder_class.url + "/api/answer/v1/candidates", params=options,
                       headers=sbs_request_builder_class.headers, verify=sbs_request_builder_class.verify_request)


def get_conversations(sbs_request_builder_class):
    """
    Wrapper for get /conversations endpoint. Will return all conversations for the logged-in user of the SBS instance.
    If the logged-in user is a client (used in API calls), endpoint will return all conversations made by that client.
    Must pass an already authenticated SBS request builder class - no authentication is done in this method.
    @param sbs_request_builder_class: already authenticated instance of SBSRequestBuilder Class
    @return: list<dict> of conversations made by logged-in user
    """
    url = sbs_request_builder_class.url
    headers = sbs_request_builder_class.headers
    verify = sbs_request_builder_class.verify_request
    req = requests.get('{}/api/answer/v1/conversations'.format(url), headers=headers, verify=verify)

    conversations = req.json()['data']
    return conversations


def translate_resp_into_list(resp):
    resp_text = resp.text
    try:
        # Split the API response into individual JSON strings
        json_strings = resp_text.split('\n')

        # Remove empty strings
        json_strings = [s for s in json_strings if s.strip()]

        # Parse each JSON string into a Python dictionary
        list_convo_objs = [json.loads(s[len('data:'):]) for s in json_strings]

        return list_convo_objs
    except:
        print('Error in response from SBS Chat.', resp_text)



#############################################################################################
# These are helper functions that don't necessarily require/perform a SciBite Search call   #
#############################################################################################

def excel_to_json(input_excel_file, output_json_file):
    # Read the Excel file into a pandas DataFrame
    df = pd.read_excel(input_excel_file)
    # Convert DataFrame to JSON
    json_data = df.to_json(orient='records')
    # Write JSON data to a file
    with open(output_json_file, 'w') as json_file:
        json_file.write(json_data)


def remove_markup_sbs(string_marked_up):
    try:
        pattern_all_markup = re.compile('\[([^\]]+)\]\(([^\$]+)\$([^\)]+)\)')
        clean_string = re.sub(pattern_all_markup, lambda match: match.group(1), string_marked_up)
        return clean_string
    except:
        print('Error in the marked up string', string_marked_up)


def extract_bracketed_words(input_string):
    return re.findall(r'\[([^]]*)\]', input_string)


def findall_iter(sub, string):
    def next_index(length):
        index = 0 - length
        while True:
            index = string.find(sub, index + length)
            yield index

    return iter(next_index(len(sub)).__next__, -1)


# NOTE CM: need to make sure this can deal with multiple instances of the same string
def find_positions(main_string, words):
    unique_words = set(words)
    positions = []
    for word in unique_words:
        return_findall = findall_iter(word, main_string)
        for instance_found in return_findall:
            start_pos = instance_found
            end_pos = start_pos + len(word)
            positions.append([word, (start_pos, end_pos)])
    return positions


def get_hit_positions_markup_sbs(string_marked_up, string_clean):
    """_summary_

    Args:
            string_marked_up (_type_): _description_
            string_clean (_type_): _description_

    Returns:
            _type_: _description_
    """
    pattern_hit_markup = re.compile('\[([^\]]+)\]\(_hit_term=([^\$]+)\$([^\)]+)\)')
    list_hit_words = []
    for match in pattern_hit_markup.finditer(string_marked_up):
        # extract word
        word_hit = match.group(1)
        # extract VOCAB
        vocab_hit = match.group(2)
        # Extract whole IDs matching
        term_id = match.group(3)
        # span
        # range_position = match.span()
        list_hit_words.append((word_hit, vocab_hit, term_id))

    # Get the bracketed words and their positions
    all_bracketed_words = extract_bracketed_words(string_marked_up)

    bracketed_words = []
    entity_dict = {}
    for ele in list_hit_words:
        if ele[0] in all_bracketed_words:
            bracketed_words.append(ele)
            entity_dict[ele[0]] = ele
    flat_bracketed_words = [word[0] for word in bracketed_words]
    positions = []
    positions = find_positions(string_clean, flat_bracketed_words)
    # print("Bracketed Words:", bracketed_words)
    # print("Bracketed Words flat:", flat_bracketed_words)
    # print("Positions in String2:", positions)
    # print('Entity dict',entity_dict)

    response_positions = []
    for i, pos in enumerate(positions):
        new_range = [pos[1][0], pos[1][1]]
        newpos = {'term': entity_dict[pos[0]][0], 'type': entity_dict[pos[0]][1], 'id': entity_dict[pos[0]][2],
                  'start': new_range[0], 'end': new_range[1]}
        response_positions.append(newpos)
    return response_positions


def translate_get_docs_response(response_to_process):
    """This function takes a marked up json response from the get_docs endpoint from SciBite Search and generates, for
    every field that is annotated text, a marked up version, a clean version, and a dictionary with information about the
    hit positions

    Args:
        response_to_process (str): JSON string

    Returns:
        str: processed JSON string
    """
    # NOTE CLAUDIA: this is now hardcoding fields to skip because either are not text or are not annotated text
    # the best practice would be to be able to make a difference depending on doc schema and also get that live from
    # an up-do-date instance, taking only fields that are marked as annotated text
    fields_to_skip = ['schema_id', 'native_id', 'dataset_id', 'dataset', 'owner',
                      'source_uri', 'ingest_date', 'publish_date', 'job_execution_id',
                      'provenance', 'authors', 'entity_ids', 'vocabulary_codes',
                      'journal_volume', 'last_author', 'journal_issue', 'journal_issue_abbreviation',
                      'journal_iso_abbreviation', 'affiliations', 'issn', 'first_author',
                      'language', 'date_revised', 'journal_title', 'id', 'doi', '_links', '_score', '_snippets',
                      'org_duns', 'project_uri', 'org_state', 'core_project_number', 'org_zip_code',
                      'full_project_number',
                      'fiscal_year', 'support_year', 'secondary_outcomes', 'phase', 'primary_outcomes',
                      'number_of_arms',
                      'funding', 'location_countries', 'lead_sponsor', 'sponsors', 'enrollment',
                      'study_design', 'date_completed', 'org_study_id', 'study_type', 'study_first_submitted',
                      'eudract_id',
                      'program_officer_name', 'study_section', 'budget_end', 'study_section_name',
                      'total_cost', 'investigators', 'project_start', 'project_end', 'foa_number', 'budget_start',
                      'award_notice_date',
                      'is_fda_regulated_drug', 'corresponding_author', 'has_expanded_access', 'locations',
                      'other_outcomes', 'secondary_ids', 'references','mesh_headings','entity_frequency']
    # nested ones that we need to consider and are currently ignoring
    # all the outcomes ones
    list_nested = ['eligibility', 'arm_groups', 'interventions']
    list_nested_skip = ['minimum_age', 'type', 'study_pop', 'sampling_method', 'gender', 'healthy_volunteers',
                        'maximum_age', 'intervention_type', 'other_names', 'intervention_name']
    processed_response = []
    for i, doc in enumerate(response_to_process):
        new_doc_dict = {}
        fields_available = doc.keys()
        for j, field in enumerate(fields_available):
            if field not in fields_to_skip:
                if field in list_nested:
                    if field not in ['arm_groups', 'interventions']:
                        try:
                            keys_in_field = doc[field].keys()
                        except:
                            print('Error in field', field)
                        for sec_key in keys_in_field:
                            new_doc_dict[field] = {}
                            if sec_key not in list_nested_skip:
                                new_doc_dict[field][sec_key + '_marked_up'] = doc[field][sec_key]
                                try:
                                    clean_string = remove_markup_sbs(doc[field][sec_key])
                                except:
                                    print('Error in ', sec_key)
                                    print(doc[field][sec_key])
                                new_doc_dict[field][sec_key + '_clean'] = clean_string
                                response_positions = get_hit_positions_markup_sbs(doc[field][sec_key], clean_string)
                                new_doc_dict[field][sec_key + '_hits'] = response_positions
                        else:
                            new_doc_dict[field][sec_key] = doc[field][sec_key]
                    else:
                        # arm group case is a list
                        new_arm_list = []
                        for ind, ag in enumerate(doc[field]):
                            new_arm_dict = {}
                            for key_ag in ag.keys():
                                if key_ag not in list_nested_skip:
                                    try:
                                        clean_string = remove_markup_sbs(doc[field][ind][key_ag])
                                    except:
                                        print('Error in ', key_ag)
                                        print(doc[field][ind][key_ag])
                                    new_arm_dict[key_ag + '_marked_up'] = doc[field][ind][key_ag]
                                    new_arm_dict[key_ag + '_clean'] = clean_string
                                    # Now get the positions of those hits
                                    response_positions = get_hit_positions_markup_sbs(doc[field][ind][key_ag],
                                                                                      clean_string)
                                    new_arm_dict[key_ag + '_hits'] = response_positions
                                else:
                                    new_arm_dict[key_ag] = doc[field][ind][key_ag]
                            new_arm_list.append(new_arm_dict)
                        new_doc_dict[field] = new_arm_list
                else:
                    try:
                        clean_string = remove_markup_sbs(doc[field])
                        new_doc_dict[field + '_marked_up'] = doc[field]
                        new_doc_dict[field + '_clean'] = clean_string
                        # Now get the positions of those hits
                        response_positions = get_hit_positions_markup_sbs(doc[field], clean_string)
                        new_doc_dict[field + '_hits'] = response_positions
                    except:
                        print('\n Error in ' + field + ' field: ')
                        print(doc[field])
            else:
                new_doc_dict[field] = doc[field]
        processed_response.append(new_doc_dict)
    return processed_response


def translate_get_sentences_response(response):
    """This function takes a marked up json response from the get_sentences endpoint from SciBite Search and generates, for
    content field, a marked up version, a clean version, and a dictionary with information about the
    hit positions

    Args:
        response_to_process (str): JSON string

    Returns:
        str: processed JSON string
    """
    processed_response = []
    for i, sent in enumerate(response):
        new_sent_dict = {}
        fields_available = sent.keys()
        # The only marked up content in sentences is the content field
        clean_string = remove_markup_sbs(sent['content'])
        new_sent_dict['content_marked_up'] = sent['content']
        new_sent_dict['content_clean'] = clean_string
        # Now get the positions of those hits
        response_positions = get_hit_positions_markup_sbs(sent['content'], clean_string)
        new_sent_dict['content_hits'] = response_positions
        # now add the remaining fields
        for field in fields_available:
            if field != 'content':
                new_sent_dict[field] = sent[field]
        processed_response.append(new_sent_dict)
    return processed_response


def process_s3_pipeline_log(sbs_ingestion_log):
    """Function to process the SciBite Search log of an S3 ingestion pipeline

    Args:
            sbs_ingestion_log (str): the filepath to the log

    Returns:
            list: a list with the exception types and numbers
    """
    list_exceptions = []
    list_size_errors = []
    fichilog = open(sbs_ingestion_log, 'r')
    log_lines = fichilog.readlines()
    pattern_pipeline_exception = re.compile('PipelineException')
    pattern_encryption_dictionary = re.compile('PDF contains an encryption dictionary')
    pattern_invalid_entity = re.compile('Invalid Entity')  # typical with measure vocab
    pattern_end_of_file = re.compile('End-of-File')
    pattern_large_file = re.compile('File too large to process')
    for i, line in enumerate(log_lines):
        if pattern_pipeline_exception.search(line):
            # Check if encryption error
            if pattern_encryption_dictionary.search(line):
                type_error = 'encryption'
            # Check if entity invalid error
            elif pattern_invalid_entity.search(line):
                type_error = 'invalid_entity'
            elif pattern_end_of_file.search(line):
                type_error = 'end_of_file'
            elif pattern_large_file.search(line):
                type_error = 'file_too_large'
                size = line.split(' ')[-2]
                list_size_errors.append(size)
            # Now save into the list
            split_line = log_lines[i - 1].split(',')
            provenance_error = os.path.basename((split_line[-1].split('='))[-1].split('}')[0])
            list_exceptions.append((type_error, provenance_error))
    sorted_list_exceptions = sorted(list_exceptions)
    unique_list = set(sorted_list_exceptions)
    total = len(unique_list)
    # for instance_exception in unique_list:
    #       print(instance_exception[0]+','+instance_exception[1])
    # print('\nTotal number of unique exceptions is ',total)
    if len(list_size_errors) >= 1:
        largest_file = max(list_size_errors)
        # print('\nThe largest file of the set is '+largest_file+' MB long')
    return list_exceptions
