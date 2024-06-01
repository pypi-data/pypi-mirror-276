"""

  ____       _ ____  _ _         _____           _ _    _ _
 / ___|  ___(_) __ )(_) |_ ___  |_   _|__   ___ | | | _(_) |_
 \___ \ / __| |  _ \| | __/ _ \   | |/ _ \ / _ \| | |/ / | __|
  ___) | (__| | |_) | | ||  __/   | | (_) | (_) | |   <| | |_
 |____/ \___|_|____/|_|\__\___|   |_|\___/ \___/|_|_|\_\_|\__|

TERMiteRequestBuilder- make requests to the TERMite API and process results.

"""

__author__ = 'SciBite'
__version__ = '0.6.2'
__copyright__ = '(c) 2024, SciBite Ltd'
__license__ = 'Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License'


import requests
import os
import pandas as pd
import json
import base64
from bs4 import BeautifulSoup
import itertools


class TermiteRequestBuilder():
    """
    Class for creating TERMite requests
    """

    def __init__(self):
        self.login_url = None
        self.session = requests.Session()
        self.url = 'http://localhost:9090/termite'
        self.input_file_path = ''
        self.payload = {"output": "json"}
        self.options = {}
        self.binary_content = None
        self.basic_auth = ()
        self.headers = {}
        self.verify_request = True

    def set_basic_auth(self, username='', password='', verification=True):
        """
        Pass basic authentication credentials
        **ONLY change verification if you are calling a known source**

        :param username: username to be used for basic authentication
        :param password: password to be used for basic authentication
        :param verification: if set to False requests will ignore verifying the SSL certificate, can also pass the path
        to a certificate file
        """
        self.basic_auth = (username, password)
        self.verify_request = verification

    def set_oauth2(self, token_user, token_pw, verification=True,
                   token_address="https://api.healthcare.elsevier.com:443/token"):
        """Pass username and password for the Elsevier token api
        It then uses these credentials to generate an access token and adds 
        this to the request header.
        :token_user:    username to access Elsevier token api. Specific to the hosting website
        :token_pw:      password to access Elsevier token api. Specific to the hosting website
        :token_address: address of the token api
        """
        auth64 = base64.b64encode(bytearray(token_user + ":" + token_pw, 'utf8'))  # base64 encoded Username+password
        auth64 = auth64.decode('utf8')
        token_address = token_address or "https://api.healthcare.elsevier.com:443/token"
        req = self.session.post(token_address, data={"grant_type": "client_credentials"},
                                headers={"Authorization": "Basic " + auth64,
                                         "Content-Type": "application/x-www-form-urlencoded"})
        access_token = req.json()['access_token']
        self.headers = {"Authorization": "Bearer " + access_token}
        self.verify_request = verification

    def set_auth_saas(self, username, password, verification=True):
        """Pass API username and password to authenticate on SaaS
        We take that username and password and pass through the authentication steps as save
        this information to the session requests variable for use in the
        :token_user:    username to access Elsevier token api. Specific to the hosting website
        :token_pw:      password to access Elsevier token api. Specific to the hosting website
        :token_address: address of the token api
        """
        # first login via username and password
        if self.login_url is None or self.login_url == "":
            raise Exception("Please set your provided login_url. If you do not know this URL, please reach out your "
                            "SciBite contacts.")
        login_resp = self.session.post(self.login_url,
                                       data={"grant_type": "password", "credentialId": "", "username": username,
                                             "password": password},
                                       headers={"Content-Type": "application/x-www-form-urlencoded"})
        # parse login response to find correct URL and then login again
        soup = BeautifulSoup(login_resp.text, "html.parser")
        form_data = soup.find('form')
        action_url = form_data['action']
        form_resp = self.session.post(action_url,
                                      data={"credentialId": "", "username": username, "password": password},
                                      headers={"Content-Type": "application/x-www-form-urlencoded"},
                                      allow_redirects=False
                                      )
        # get final authentication
        url3 = form_resp.headers.get("Location")
        resp = self.session.get(url3,
                                data={"credentialId": "", "username": username, "password": password},
                                headers={"Content-Type": "application/x-www-form-urlencoded"},
                                allow_redirects=False
                                )
        self.verify_request = verification

    def set_saas_login_url(self, login_url):
        """
                Set the SaaS login URL of the TERMite instance

                :param login_url: the URL of the TERMite instance to be hit
        """
        self.login_url = login_url.rstrip("/")

    def set_url(self, url):
        """
        Set the URL of the TERMite instance e.g. for local instance http://localhost:9090/termite

        :param url: the URL of the TERMite instance to be hit
        """
        self.url = url.rstrip('/')

    def set_username(self, username):
        """
        Set the username for the user making the current termite request

        :param username: string variable to specify the username of the user making the current termite request
        """
        self.payload["username"] = username

    def set_usertoken(self, usertoken):
        """
        Set the usertoken for the user making the current termite request

        :param usertoken: string variable to specify the usertoken of the user making the current termite request
        """
        self.payload["usertoken"] = usertoken

    def set_bgjob(self, bgjob):
        """
        Set if a termite job should be handled ass a background process

        :param bgjob: boolean variable to specify if the termite should should be done in the background
        """
        self.payload["bgjob"] = bgjob

    def set_bginfo(self, bginfo):
        """
        Set any information associated with the background task

        :param bginfo: string variable to specify any information about the background task
        """
        self.payload["bginfo"] = bginfo

    def set_binary_content(self, input_file_path):
        """
        For annotating file content, send file path string and process file as a binary
        multiple files of the same type can be scanned at once if placed in a zip archive

        :param input_file_path: file path to the file to be sent to TERMite
        """
        file_obj = open(input_file_path, 'rb')
        file_name = os.path.basename(input_file_path)
        self.binary_content = {"binary": (file_name, file_obj)}

    def set_text(self, string):
        """
        Use this for tagging raw text e.g. if looping through some file content

        :param string: text to be sent to TERMite
        """
        self.payload["text"] = string

    def set_bundle(self, string):
        """
        Use this for specifying a TERMite bundle to use

        :param string: string variable to specify a bundle name
        """
        self.payload["bundle"] = string

    def set_df(self, dataframe):
        """Use this for tagging pandas dataframes"""

        dataframe = dataframe.T
        df_dict = dataframe.to_dict()
        termite_input = []
        for row in df_dict:
            dic = {"sections": [], "uid": "Row_" + str(row)}
            for column in df_dict[row]:
                mini_dic = {"body": df_dict[row][column], "header": "", "partName": column}
                dic["sections"] += [mini_dic]
            termite_input += [dic]
        self.payload["text"] = json.dumps(termite_input)
        self.payload["format"] = "jsonc"

    def set_options(self, options_dict):
        """
        For bulk setting multiple TERMite API options in a single call, send a dictionary object here

        :param options_dict: a dictionary of options to be passed to TERMite
        """

        if 'output' in options_dict:
            self.payload['output'] = options_dict['output']

        options = []
        for k, v in options_dict.items():
            options.append(k + "=" + str(v))
        option_string = '&'.join(options)
        if "opts" in self.payload:
            self.payload["opts"] = option_string + "&" + self.payload["opts"]
        else:
            self.payload["opts"] = option_string

    #######
    # individual options for applying the major TERMite settings
    #######

    def set_fuzzy(self, bool):
        """
        Use fuzzy matching?

        :param bool: set to True if fuzzy matching is to be enabled
        """
        input = bool_to_string(bool)
        if "opts" in self.payload:
            self.payload["opts"] = "fzy.promote=" + input + "&" + self.payload["opts"]
        else:
            self.payload["opts"] = "fzy.promote=" + input

        self.payload["fuzzy"] = input

    def set_subsume(self, bool):
        """
        Take longest hit where an entity is a hit against more than one dictionary

        :param bool: set subsume if True
        """
        input = bool_to_string(bool)
        self.payload["subsume"] = input

    def set_entities(self, string):
        """
        Limit the entities to be annotated

        :param string: a comma separated string of entity types, e.g. 'DRUG,GENE'
        """
        self.payload["entities"] = string

    def set_input_format(self, string):
        """
        Set input format e.g. txt, medline.xml, node.xml, pdf, xlsx

        :param string: string input format
        """
        self.payload["format"] = string

    def set_output_format(self, string):
        """
        Set output format e.g. tsv, json, doc.json

        :param string: provide the output format to be used
        """
        self.payload["output"] = string

    def set_reject_minor_hits(self, bool):
        """
        Reject highly suspicious hits (normally true)

        :param bool: set True to reject highly suspicious hits
        """
        input = bool_to_string(bool)
        if "opts" in self.payload:
            self.payload["opts"] = self.payload["opts"] + "&rejectMinorHits=" + input
        else:
            self.payload["opts"] = "rejectMinorHits=" + input

    def set_reject_ambiguous(self, bool):
        """
        Automatically reject any hits flagged as ambiguous

        :param bool: set True to reject any ambiguous hits
        """
        input = bool_to_string(bool)
        if "opts" in self.payload:
            self.payload["opts"] = self.payload["opts"] + "&rejectAmbig=" + input
        else:
            self.payload["opts"] = "rejectAmbig=" + input

    def set_max_docs(self, integer):
        """
        When tagging a zip file of multiple documents, limit how many to scan
        also applies where there are multiple document records in a single xml e.g. from a medline XML export

        :param integer: number of documents to limit annotation too
        """
        self.payload["maxDocs"] = integer

    def set_no_empty(self, bool):
        """
        Reject all documents where there were no hits

        :param bool: if True do not return any docs with no hits
        """
        input = bool_to_string(bool)
        self.payload["noEmpty"] = input

    def execute(self, display_request=False, return_text=False):
        """
        Once all settings are done, POST the parameters to the TERMite RESTful API

        :param display_request: if True request will be printed out before being submitted
        :return: request response
        """
        if display_request:
            print("REQUEST: ", self.url, self.payload)
        try:
            if self.binary_content:
                response = self.session.post(self.url, data=self.payload, files=self.binary_content)
            else:
                response = self.session.post(self.url, data=self.payload,
                                             headers={'content-type': 'application/x-www-form'
                                                                      '-urlencoded; '
                                                                      'charset=UTF-8'})
            '''if self.binary_content and bool(self.basic_auth):
                # Basic authentication request for binary content
                response = session.post(self.url, data=self.payload, files=self.binary_content, auth=self.basic_auth,
                                        verify=self.verify_request)

            elif self.binary_content and bool(self.basic_auth) == False and bool(self.headers):
                # OAuth2 authentication request for binary content
                response = session.post(self.url, data=self.payload, files=self.binary_content,
                                        verify=self.verify_request, headers=self.headers)
            elif self.binary_content and bool(self.basic_auth) == False and bool(self.headers) == False:
                # No authentication request for binary content
                response = session.post(self.url, data=self.payload, files=self.binary_content)
            elif not self.binary_content and bool(self.basic_auth):
                # Basic authentication for text content
                response = session.post(self.url, data=self.payload, verify=self.verify_request, auth=self.basic_auth)
            elif not self.binary_content and bool(self.headers):
                # OAuth2 authentication request for text content
                response = session.post(self.url, data=self.payload, verify=self.verify_request, headers=self.headers)
            else:
                response = session.post(self.url, data=self.payload)'''
        except Exception as e:
            return print(
                "Failed with the following error {}\n\nPlease check that TERMite can be accessed via the following URL {}\nAnd that the necessary credentials have been provided (done so using the set_basic_auth() function)".format(
                    e, self.url))

        if self.payload["output"] in ["json", "doc.json", "doc.jsonx"] and not return_text:
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(response.json()['RESP_META']['ERR_TRACE'])
        else:
            return response.text


def bool_to_string(bool):
    """
    Convert a boolean to a string

    :param bool: provide boolean to be converted
    :return: string
    """
    string = str(bool)
    string = string.lower()

    return string


def annotate_files(url, input_file_path, options_dict):
    """
    Wrapper function to execute a TERMite request for annotating individual files or a zip archive

    :param url: url of TERMite instance
    :param input_file_path: path to file to be annotated
    :param options_dict: dictionary of options to be used during annotation
    :return: result of request
    """
    t = TermiteRequestBuilder()
    t.set_url(url)
    t.set_binary_content(input_file_path)
    t.set_options(options_dict)
    result = t.execute()

    return result


def annotate_text(url, text, options_dict):
    """
    Wrapper function to execute a TERMite request for annotating strings of text

    :param url: url of TERMite instance
    :param text: text to be annotated
    :param options_dict: dictionary of options to be used during annotation
    :return: result of request
    """
    t = TermiteRequestBuilder()
    t.set_url(url)
    t.set_text(text)
    t.set_options(options_dict)
    result = t.execute()

    return result


def process_payload(filtered_hits, response_payload, filter_entity_types, doc_id='', reject_ambig=True, score_cutoff=0,
                    remove_subsumed=True):
    """
    Parses the termite json output to filter out only entity types of interest and their major metadata
    includes rules for rejecting ambiguous or low-relevance hits

    :param filtered_hits: input
    :param response_payload: json response
    :param filter_entity_types: entity types to filter
    :param doc_id: doc id to filter
    :param reject_ambig: boolean reject ambiguous hits
    :param score_cutoff: int score cit-off
    :param remove_subsumed: boolean remove subsumed
    :return: dictionary of filtered hits
    """
    for entity_type, entity_hits in response_payload.items():
        if entity_type in filter_entity_types:
            for entity_hit in entity_hits:
                nonambigsyns = entity_hit["nonambigsyns"]
                entity_score = entity_hit["score"]
                if reject_ambig == True:
                    if nonambigsyns == 0:
                        continue
                if "subsume" in entity_hit and remove_subsumed == True:
                    if True in entity_hit["subsume"]:
                        continue
                if entity_hit["score"] >= score_cutoff:
                    hit_id = entity_hit["hitID"]
                    entity_id = entity_type + '$' + hit_id
                    entity_name = entity_hit["name"]
                    hit_count = entity_hit["hitCount"]
                    if entity_id in filtered_hits:
                        filtered_hits[entity_id]["hit_count"] += hit_count
                        filtered_hits[entity_id]["doc_count"] += 1
                        filtered_hits[entity_id]["doc_id"].append(doc_id)
                        if entity_score > filtered_hits[entity_id]["max_relevance_score"]:
                            filtered_hits[entity_id]["max_relevance_score"] = entity_score
                    else:
                        filtered_hits[entity_id] = {"id": hit_id, "type": entity_type, "name": entity_name,
                                                    "hit_count": hit_count, "max_relevance_score": entity_score,
                                                    "doc_id": [doc_id], "doc_count": 1}

    return filtered_hits


def get_entity_hits_from_json(termite_json_response, filter_entity_types, reject_ambig=True, score_cutoff=0):
    """
    Extract entity hits from TERMite JSON

    :param termite_json_response: JSON returned from TERMite
    :param filter_entity_types: comma separated list
    :param reject_ambig: boolean
    :param score_cutoff: a numeric value between 1-5
    :return: dictionary of filtered hits
    """
    filtered_hits = {}
    if "RESP_MULTIDOC_PAYLOAD" in termite_json_response:
        doc_results = termite_json_response["RESP_MULTIDOC_PAYLOAD"]
        for doc_id, response_payload in doc_results.items():
            filtered_hits = process_payload(filtered_hits, response_payload, filter_entity_types,
                                            reject_ambig=reject_ambig, score_cutoff=score_cutoff, doc_id=doc_id)

    elif "RESP_PAYLOAD" in termite_json_response:
        response_payload = termite_json_response["RESP_PAYLOAD"]
        filtered_hits = process_payload(filtered_hits, response_payload, filter_entity_types, reject_ambig=reject_ambig,
                                        score_cutoff=score_cutoff)

    return filtered_hits


def docjsonx_payload_records(docjsonx_response_payload, reject_ambig=True, score_cutoff=0, remove_subsumed=True):
    """
    Parses TERMite doc.JSONx payload into records, includes rules to filter out ambiguous and low-relevance hits

    :param docjsonx_response_payload: doc.JSONx TERMite response.
    :param reject_ambig: boolean
    :param score_cutoff: a numerical value between 1-5
    :param remove_subsumed: boolean
    :return: TERMite response in records format
    """
    payload = []
    for doc in docjsonx_response_payload:
        if 'termiteTags' in doc.keys():
            for entity_hit in doc['termiteTags']:
                # update document record with entity hit record
                entity_hit.update(doc)
                del entity_hit['termiteTags']

                # filtering
                if reject_ambig is True and entity_hit['nonambigsyns'] == 0:
                    continue
                if "subsume" in entity_hit and remove_subsumed is True:
                    if True in entity_hit['subsume']:
                        continue
                if entity_hit['score'] >= score_cutoff:
                    payload.append(entity_hit)

    return (payload)


def json_payload_records(response_payload, reject_ambig=True, score_cutoff=0, remove_subsumed=True):
    """
    Parses TERMite json payload into records, includes rules to filter out ambiguous and low-relevance hits

    :param response_payload: REP_PAYLOAD of JSON TERMite response
    :param reject_ambig: boolean
    :param score_cutoff: a numerical value between 1-5
    :param remove_subsumed: boolean
    :return: TERMite response in records format
    """
    payload = []
    for entity_type, entity_hits in response_payload.items():
        for entity_hit in entity_hits:
            if reject_ambig is True and entity_hit['nonambigsyns'] == 0:
                continue
            if "subsume" in entity_hit and remove_subsumed is True:
                if True in entity_hit['subsume']:
                    continue
            if entity_hit['score'] >= score_cutoff:
                payload.append(entity_hit)

    return (payload)


def payload_records(termiteResponse, reject_ambig=True, score_cutoff=0, remove_subsumed=True):
    """
    Parses TERMite JSON or doc.JSONx output into records format

    :param termiteResponse: JSON or doc.JSONx TERMite response
    :param reject_ambig: boolean
    :param score_cutoff: a numerical value between 1-5
    :param remove_subsumed: boolean
    :return: TERMite response in records format
    """
    payload = []

    if "RESP_MULTIDOC_PAYLOAD" in termiteResponse:
        for docID, termite_hits in termiteResponse['RESP_MULTIDOC_PAYLOAD'].items():
            payload = payload + json_payload_records(termite_hits, reject_ambig=reject_ambig,
                                                     score_cutoff=score_cutoff, remove_subsumed=remove_subsumed)
    elif "RESP_PAYLOAD" in termiteResponse:
        payload = payload + json_payload_records(termiteResponse['RESP_PAYLOAD'], reject_ambig=reject_ambig,
                                                 score_cutoff=score_cutoff, remove_subsumed=remove_subsumed)

    else:
        payload = docjsonx_payload_records(termiteResponse, reject_ambig=reject_ambig,
                                           score_cutoff=score_cutoff, remove_subsumed=remove_subsumed)

    return (payload)


def get_termite_dataframe(termiteResponse, cols_to_add="", reject_ambig=True, score_cutoff=0,
                          remove_subsumed=True):
    """
    Parses TERMite JSON or doc.JSONx into a dataframe of hits, filtering out ambiguous and low-relevance hits
    By default returns docID, entityType, hitID, name, score, realSynList, totnosyns, nonambigsyns, frag_vector_array
    and hitCount
    Additional hit information not included in the default output can be included by use of a comma separated list

    :param termiteResponse: JSON or doc.JSONx response from TERMite
    :param cols_to_add: comma separated list of additional fields to include
    :param reject_ambig: boolean
    :param score_cutoff: a numerical value between 1-5
    :param remove_subsumed: boolean
    :return: dataframe of TERMite hits
    """

    payload = payload_records(termiteResponse, reject_ambig=reject_ambig,
                              score_cutoff=score_cutoff, remove_subsumed=remove_subsumed)

    df = pd.DataFrame(payload)

    cols = ["docID", "entityType", "hitID", "name", "score", "realSynList", "totnosyns", "nonambigsyns",
            "frag_vector_array", "hitCount"]

    if cols_to_add:
        cols_to_add = cols_to_add.replace(" ", "").split(",")
        try:
            cols = cols + cols_to_add
            if df.empty:
                return pd.DataFrame(columns=cols)
            return (df[cols])
        except KeyError as e:
            print("Invalid column selection.", e)
    else:
        if df.empty:
            return pd.DataFrame(columns=cols)
        return (df[cols])


def get_entity_hits_from_docjsonx(termite_response, filter_entity_types):
    """
    Parses doc.JSONx TERMite response and returns a summary of the hits

    :param termite_response: doc.JSONx TERMite response
    :param filter_entity_types: comma separated list
    :return: dictionary of filtered hits
    """
    processed = docjsonx_payload_records(termite_response)

    filtered_hits = {}
    for entity_hit in processed:
        hit_id = entity_hit['hitID']
        entityType = entity_hit['entityType']
        entity_id = entityType + '$' + hit_id
        entity_name = entity_hit['name']
        hit_count = entity_hit['hitCount']
        entity_score = entity_hit['score']
        doc_id = entity_hit['docID']

        if entityType in filter_entity_types:
            if entity_id in filtered_hits:
                filtered_hits[entity_id]['hit_count'] += hit_count
                if entity_score > filtered_hits[entity_id]['max_relevance_score']:
                    filtered_hits[entity_id]['max_relevance_score'] = entity_score
                if doc_id not in filtered_hits[entity_id]['doc_id']:
                    filtered_hits[entity_id]['doc_id'].append(doc_id)
                    filtered_hits[entity_id]['doc_count'] += 1
            else:
                filtered_hits[entity_id] = {"id": hit_id, "type": entityType, "name": entity_name,
                                            "hit_count": hit_count,
                                            "max_relevance_score": entity_score, "doc_id": [doc_id], "doc_count": 1}

    return (filtered_hits)


def termite_entity_hits_df(termite_response, filter_entity_types):
    """
    Parses TERmite json or docjson(x) response and returns a summary of the hits where each column 
    corresponds to an entity or its ID.
    :param termite_response: doc.JSONx TERMite response
    :param filter_entity_types: comma separated list of entities to be annotated
    :return: pandas dataframe
    """
    payload = payload_records(termite_response)

    # Magic formula that adds vocab ID header right after each vocab
    entitieswid = ['docID',
                   *sum(zip(filter_entity_types, [entity_type + '_ID' for entity_type in filter_entity_types]), ())]
    # Initiate empty list that will be populated with one dictionary/row
    df_list = []

    # Loop through hits
    for hit in payload:
        # Populate dictionary with relevant entity hits
        dic = {header: '' for header in entitieswid}
        if hit['entityType'] in filter_entity_types:
            dic['docID'] = hit['docID']
            dic[hit['entityType']] = hit['name']
            dic[hit['entityType'] + '_ID'] = hit['hitID']
            df_list += [dic]

    df = pd.DataFrame(df_list, columns=entitieswid)
    return df


def all_entities(termite_response):
    """
    Parses TERMite response and returns a list of VOCab modules with hits

    :param termite_response: JSON or doc.JSONx TERMite response
    :return: list
    """
    payload = payload_records(termite_response)

    entities_used = []
    for entity_hit in payload:
        if entity_hit['entityType'] not in entities_used:
            entities_used.append(entity_hit['entityType'])

    return (entities_used)


def all_entities_df(termite_response):
    """
    Parses JSON or doc.JSONx TERMite response into summary of hits dataframe

    :param termite_response: JSON or doc.JSONx TERMite response
    :return: pandas dataframe
    """

    # identify all entitiy hit types in the text
    entities_used = all_entities(termite_response)
    entities_string = (',').join(entities_used)

    if "RESP_MULTIDOC_PAYLOAD" in termite_response or "RESP_PAYLOAD" in termite_response:
        filtered_hits = get_entity_hits_from_json(termite_response, entities_string)
    else:
        filtered_hits = get_entity_hits_from_docjsonx(termite_response, entities_string)

    df = pd.DataFrame(filtered_hits).T

    return (df)


def entity_freq(termite_response):
    """
    Parses TERMite JSON or doc.JSONx response and returns dataframe of entity type frequencies

    :param termite_response: JSON or doc.JSONx TERMite response
    :return: pandas dataframe
    """

    df = get_termite_dataframe(termite_response)

    values = pd.value_counts(df['entityType'])
    values = pd.DataFrame(values)
    return (values)


def top_hits_df(termite_response, selection=10, entity_subset=None, include_docs=False):
    """
    Parses JSON or doc.JSONx TERMite response and returns a pandas dataframe of the most frequent hits. By default the
    top 10 most frequent hits are returned. The entity types to include can be set by a comma separated list
    For multidoc results the documents in which hits occur can be included

    :param termite_response: JSON or doc.JSONx TERMite response
    :param selection: number of most frequent hits to return
    :param entity_subset: comma separated list
    :param include_docs: boolean
    :return: pandas dataframe
    """

    # get entity hits and sort by hit_count
    df = get_termite_dataframe(termite_response)
    df.sort_values(by=['hitCount'], ascending=False, inplace=True)
    df2 = df.copy()

    # select relevant columns and filtering
    if include_docs is True:
        columns = [3, 5, 6, 2, 1]
    else:
        columns = [3, 5, 6, 2]
    if entity_subset is not None:
        entity_subset = entity_subset.replace(" ", "").split(",")
        criteria = df2['entityType'].isin(entity_subset)
        return (df2[criteria].iloc[0:selection, columns])
    else:
        return (df2.iloc[0:selection, columns])


def markup(
        docjsonx,
        normalisation='id',
        substitute=True,
        wrap=False,
        wrapChars=('{!', '!}'),
        vocabs=None,
        labels=None,
        replacementDict=None
):
    '''
    Receives TERMite docjsonx output. Processes the original text, normalising identified hits.

    :param str docjsonx: JSON string generated by TERMite. Must be docjsonx.
    :param str normalisation: Type of normalisation to substitute/add (must be 'id', 'type', 'name', 'typeplusname' or 'typeplusid')
    :param bool substitute: Whether to replace the found term (or add normalisation alongside)
    :param bool wrap: Whether to wrap found hits with 'bookends'
    :param tuple(str) wrapChars: Tuple of length 2, containing strings to insert at start/end of found hits
    :param array(str) vocabs: List of vocabs to be substituted, ordered by priority. These vocabs MUST be in the TERMite results. If left
    empty, all vocabs found will be used with random priority where overlaps are found.
    :param dict replacementDict: Dictionary with <VOCAB>:<string_to_replace_hits_in_vocab>. '~ID~' will be replaced with the entity id,
    and '~TYPE~' will be replaced with the vocab name. Example: {'GENE':'ENTITY_~TYPE~_~ID~'} would result in BRCA1 -> ENTITY_GENE_BRCA1.
    replacementDict supercedes normalisation. ~NAME~ can also be used to get the preferred name.
    :return dict:
    '''

    results = {}

    validTypes = ['id', 'type', 'name', 'typeplusname', 'typeplusid']
    if normalisation not in validTypes:
        raise ValueError(
            'Invalid normalisation requested. Valid options are \'id\', \'name\', \'type\', \'typeplusname\' and \'tyeplusid\'.'
        )

    if len(wrapChars) != 2 or not all(isinstance(wrapping, str) for wrapping in wrapChars):
        raise ValueError('wrapChars must be a tuple of length 2, containing strings.')

    if labels:
        if labels not in ['word', 'char']:
            raise ValueError('labels, if specified, must be either \'word\' or \'char\'')

    hierarchy = {}
    if vocabs:
        for idx, vocab in enumerate(vocabs):
            hierarchy[vocab] = idx

    if isinstance(docjsonx, str):
        json_docs = json.loads(docjsonx)
    else:
        json_docs = docjsonx

    for doc_idx, doc in enumerate(json_docs):
        text = doc['body']

        try:
            substitutions = get_hits(doc['termiteTags'], hierarchy=hierarchy, vocabs=vocabs)
        except KeyError:
            results[doc_idx] = {'termited_text': text}
            continue

        if len(substitutions) > 0:
            substitutions.sort(key=lambda x: x['startLoc'])
            substitutions = reversed(substitutions)

        if wrap:
            prefix = wrapChars[0]
            postfix = wrapChars[1]
        else:
            prefix, postfix = '', ''

        for sub in substitutions:
            subtext = ''
            if replacementDict:
                subtext = replacementDict[sub['entityType']].replace(
                    '~TYPE~', sub['entityType']
                ).replace(
                    '~ID~', sub['entityID']
                ).replace(
                    '~NAME~', sub['entityName']
                )
            elif normalisation == 'id':
                subtext = '_'.join([sub['entityType'], sub['entityID']])
                if not substitute:
                    subtext += ' %s' % text[sub['startLoc']:sub['endLoc']]
            elif normalisation == 'type':
                subtext = sub['entityType']
                if not substitute:
                    subtext += ' %s' % text[sub['startLoc']:sub['endLoc']]
            elif normalisation == 'name':
                subtext = sub['entityName']
                if not substitute:
                    subtext += ' %s' % text[sub['startLoc']:sub['endLoc']]
            elif normalisation == 'typeplusname':
                subtext = '%s %s' % (sub['entityType'], sub['entityName'])
                if not substitute:
                    subtext += ' %s' % text[sub['startLoc']:sub['endLoc']]
            elif normalisation == 'typeplusid':
                subtext = '%s %s' % (
                    sub['entityType'],
                    '_'.join([sub['entityType'], sub['entityID']])
                )

                if not substitute:
                    subtext += ' %s' % text[sub['startLoc']:sub['endLoc']]

            text = text[:sub['startLoc']] + prefix + subtext + postfix + text[sub['endLoc']:]

        results[doc_idx] = {'termited_text': text}

    return results


def pairwise_markup(
        docjsonx,
        pairwise_types_a,
        pairwise_types_b,
        normalisation='id',
        wrap=False,
        wrapChars=('{!', '!}'),
        substitute=True,
        replacementDict=None
):
    '''
    Receives TERMite docjsonx, returns a dictionary with pairwise TERMited substitutions.

    :param docjsonx: JSON string generated by TERMite. Must be docjsonx.
    :param array(str) pairwise_types_a: list of VOCABs to be found on one side of the pairwise relationships
    :param array(str) pairwise_types_b: list of VOCABS to be found on the other side of the pairwise relationships
    :param str normalisation: Type of normalisation to substitute/add (must be 'id', 'type', 'name', 'typeplusname' or 'typeplusid')
    :param bool substitute: Whether to replace the found term (or add normalisation alongside)
    :param bool wrap: Whether to wrap found hits with 'bookends'
    :param tuple(str) wrapChars: Tuple of length 2, containing strings to insert at start/end of found hits
    :param dict replacementDict: Dictionary with <VOCAB>:<string_to_replace_hits_in_vocab>. '~ID~' will be replaced with the entity id,
    and '~TYPE~' will be replaced with the vocab name. Example: {'GENE':'ENTITY_~TYPE~_~ID~'} would result in BRCA1 -> ENTITY_GENE_BRCA1
    replacementDict supercedes normalisation. ~NAME~ can also be used to get the preferred name.
    :return dict: a dictionary containing entity combinations to their respective masked sentences
    '''

    output = {}
    ent_id_to_hit_json = {}
    pairwise_ids_a = []
    pairwise_ids_b = []
    try:
        for hit in docjsonx[0]['termiteTags']:
            if hit['entityType'] in pairwise_types_a:
                pairwise_ids_a.append(hit['hitID'])
            elif hit['entityType'] in pairwise_types_b:
                pairwise_ids_b.append(hit['hitID'])
            else:
                continue

            ent_id_to_hit_json[hit['hitID']] = hit

    except TypeError:
        raise('Error retrieving results from TERMite')

    except KeyError:
        pass

    combos = itertools.product(pairwise_ids_a, pairwise_ids_b)

    for combo in combos:
        termiteTags = [ent_id_to_hit_json[combo[0]], ent_id_to_hit_json[combo[1]]]
        docjsonx[0]['termiteTags'] = termiteTags
        output[combo] = markup(
            docjsonx,
            vocabs=pairwise_types_a+pairwise_types_b,
            normalisation=normalisation,
            wrap=wrap,
            wrapChars=wrapChars,
            substitute=substitute,
            replacementDict=replacementDict
        )[0]['termited_text']
    return output


def text_markup(
        text,
        termiteAddr='http://localhost:9090/termite',
        vocabs=['GENE', 'INDICATION', 'DRUG'],
        normalisation='id',
        wrap=False,
        wrapChars=('{!', '!}'),
        substitute=True,
        replacementDict=None,
        termite_http_user=None,
        termite_http_pass=None,
        include_json=False
):
    '''
    Receives plain text, returns text with TERMited substitutions.

    :param str text: Text in which to markup entities
    :param str normalisation: Type of normalisation to substitute/add (must be 'id', 'type', 'name', 'typeplusname' or 'typeplusid')
    :param bool substitute: Whether to replace the found term (or add normalisation alongside)
    :param bool wrap: Whether to wrap found hits with 'bookends'
    :param tuple(str) wrapChars: Tuple of length 2, containing strings to insert at start/end of found hits
    :param array(str) vocabs: List of vocabs to be substituted, ordered by priority. These vocabs MUST be in the TERMite results. If left
    empty, all vocabs found will be used with random priority where overlaps are found.
    :param dict replacementDict: Dictionary with <VOCAB>:<string_to_replace_hits_in_vocab>. '~ID~' will be replaced with the entity id,
    and '~TYPE~' will be replaced with the vocab name. Example: {'GENE':'ENTITY_~TYPE~_~ID~'} would result in BRCA1 -> ENTITY_GENE_BRCA1
    replacementDict supercedes normalisation. ~NAME~ can also be used to get the preferred name.
    :return str:
    '''

    termite_handle = TermiteRequestBuilder()
    termite_handle.set_url(termiteAddr)
    termite_handle.set_text(text)
    termite_handle.set_entities(','.join(vocabs))
    termite_handle.set_subsume(True)
    termite_handle.set_input_format("txt")
    termite_handle.set_output_format("doc.jsonx")

    if termite_http_pass:
        termite_handle.set_basic_auth(
            termite_http_user,
            termite_http_pass,
            verification=False
        )

    docjsonx = termite_handle.execute()
    # print(docjsonx)

    if include_json:
        return markup(
            docjsonx,
            vocabs=vocabs,
            normalisation=normalisation,
            wrap=wrap,
            wrapChars=wrapChars,
            substitute=substitute,
            replacementDict=replacementDict
        )[0]['termited_text'], docjsonx

    return markup(
        docjsonx,
        vocabs=vocabs,
        normalisation=normalisation,
        wrap=wrap,
        wrapChars=wrapChars,
        substitute=substitute,
        replacementDict=replacementDict
    )[0]['termited_text']


def pairwise_text_markup(
        text,
        pairwise_types_a,
        pairwise_types_b,
        termiteAddr='http://localhost:9090/termite',
        normalisation='id',
        wrap=False,
        wrapChars=('{!', '!}'),
        substitute=True,
        replacementDict=None,
        termite_http_user=None,
        termite_http_pass=None,
        include_json=False
):
    '''
    Receives plain text, returns a dictionary with pairwise TERMited substitutions.

    :param str text: Text in which to markup entities
    :param array(str) pairwise_types_a: list of VOCABs to be found on one side of the pairwise relationships
    :param array(str) pairwise_types_b: list of VOCABS to be found on the other side of the pairwise relationships
    :param str normalisation: Type of normalisation to substitute/add (must be 'id', 'type', 'name', 'typeplusname' or 'typeplusid')
    :param bool substitute: Whether to replace the found term (or add normalisation alongside)
    :param bool wrap: Whether to wrap found hits with 'bookends'
    :param tuple(str) wrapChars: Tuple of length 2, containing strings to insert at start/end of found hits
    :param dict replacementDict: Dictionary with <VOCAB>:<string_to_replace_hits_in_vocab>. '~ID~' will be replaced with the entity id,
    and '~TYPE~' will be replaced with the vocab name. Example: {'GENE':'ENTITY_~TYPE~_~ID~'} would result in BRCA1 -> ENTITY_GENE_BRCA1
    replacementDict supercedes normalisation. ~NAME~ can also be used to get the preferred name.
    :return dict: a dictionary containing entity combinations to their respective masked sentences
    '''
    t = TermiteRequestBuilder()
    t.set_url(termiteAddr)
    t.set_text(text)
    t.set_entities(','.join(pairwise_types_a+pairwise_types_b))
    t.set_subsume(True)
    t.set_input_format("txt")
    t.set_output_format("doc.jsonx")
    if termite_http_pass:
        t.set_basic_auth(termite_http_user, termite_http_pass, verification=False)
    docjsonx = t.execute()

    if include_json:
        return pairwise_markup(
            docjsonx,
            pairwise_types_a=pairwise_types_a,
            pairwise_types_b=pairwise_types_b,
            normalisation=normalisation,
            wrap=wrap,
            wrapChars=wrapChars,
            substitute=substitute,
            replacementDict=replacementDict
        ), docjsonx

    return pairwise_markup(
        docjsonx,
        pairwise_types_a=pairwise_types_a,
        pairwise_types_b=pairwise_types_b,
        normalisation=normalisation,
        wrap=wrap,
        wrapChars=wrapChars,
        substitute=substitute,
        replacementDict=replacementDict
    )

def get_hits(termiteTags, hierarchy=None, vocabs=None):
    '''
    Uses termiteTags and hierarchy to collect info on the highest priority hits.

    :param array termiteTags: Locations of TERMite hits found, extracted from the TERMite json
    :param dict hierarchy: Dictionary with a hierarchy of vocabs to prioritise in case of overlap
    :param array(str) vocabs: List of vocabs to be substituted, ordered by priority. These vocabs MUST be in the TERMite results. If left
    empty, all vocabs found will be used with random priority where overlaps are found.
    :return array(dict):
    '''
    hits = []
    for hit in termiteTags:
        if not vocabs:
            if hit['entityType'] not in hierarchy:
                hierarchy[hit['entityType']] = len(hierarchy)
        else:
            if hit['entityType'] not in vocabs:
                continue

        if 'fls' in hit['exact_array'][0]: #TERMite 6.3...
            hitLocs, subsumeStates = hit['exact_array'], hit['subsume']
        else: #TERMite 6.4...
            hitLocs = []
            subsumeStates = []
            for hit_array in hit['exact_array']:
                hitLocs.append({'fls': [hit_array['sentence'], hit_array['start'], hit_array['end']]})
                subsumeStates.append(hit_array['subsumed'])

        assert len(hitLocs) == len(subsumeStates)

        for idx, hitLoc in enumerate(hitLocs):
            if hitLoc['fls'][0] < 1:
                continue
            hitInfo = {}
            hitInfo['entityType'], hitInfo['entityID'], hitInfo['entityName'] = hit['entityType'], hit['hitID'], hit[
                'name']
            breakBool = False
            hitInfo['startLoc'], hitInfo['endLoc'] = hitLoc['fls'][1], hitLoc['fls'][2]
            if subsumeStates[idx] == False:  # If hit is not subsumed...
                for hitIdx, hit_ in enumerate(hits):
                    # Compare to already found hits to check there's no conflict
                    if ((hit_['endLoc'] >= hitInfo['startLoc'] and hit_['endLoc'] <= hitInfo['endLoc']) or
                            (hit_['startLoc'] >= hitInfo['startLoc'] and hit_['startLoc'] <= hitInfo['endLoc'])):
                        # If they overlap, check their position in the hierarchy
                        if hierarchy[hit_['entityType']] >= hierarchy[hitInfo['entityType']]:
                            del hits[hitIdx]
                            break
                        else:
                            breakBool = True
                            break
            if not breakBool:
                hits.append(hitInfo)
    return hits

