"""

  ____       _ ____  _ _         _____           _ _    _ _
 / ___|  ___(_) __ )(_) |_ ___  |_   _|__   ___ | | | _(_) |_
 \___ \ / __| |  _ \| | __/ _ \   | |/ _ \ / _ \| | |/ / | __|
  ___) | (__| | |_) | | ||  __/   | | (_) | (_) | |   <| | |_
 |____/ \___|_|____/|_|\__\___|   |_|\___/ \___/|_|_|\_\_|\__|

WorkbenchRequestBuilder- make requests to the Workbench API and process results.

"""

__author__ = 'SciBite'
__version__ = '0.6.2'
__copyright__ = '(c) 2024, SciBite Ltd'
__license__ = 'Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License'

import configparser
import requests
import os
import time


class WorkbenchRequestBuilder:
    """
    Class for creating Workbench Requests
    """

    def __init__(self):
        self.session = requests.Session()
        self.url = ''
        self.file_input = None
        self.headers = {}
        self.verify_request = False
        self.dataset_name = ''
        self.dataset_id = ''
        self.dataset_description = ''
        self.file_ext = ''
        self.user_info = {}
        self.termite_config = ''

    def set_oauth2(self, client_id, username, password, verification=True):
        """
        Pass username and password for the Workbench token api
        It then uses these credentials to generate an access token and adds
        this to the request header.
        We will also gather the user's info to pass to subsequent API calls
        :client_id: client_id to access the token api
        :username: scibite search username
        :password: scibite search password for username above
        """
        token_address = self.url + "/auth/realms/Scibite/protocol/openid-connect/token"

        req = requests.post(token_address, data={"grant_type": "password", "client_id": client_id, "username": username,
                                                 "password": password},
                            headers={"Content-Type": "application/x-www-form-urlencoded"})
        access_token = req.json()["access_token"]
        user_info_url = "{}/api/users/me/internal".format(self.url.rstrip("/"))
        self.headers = {"Authorization": "Bearer " + access_token}

        user_info_request = requests.get(user_info_url, headers=self.headers)
        user_info_json = user_info_request.json()
        user_info_json["memberOf"][0]["group"]["userGroup"] = 'true'
        self.user_info = user_info_json
        self.verify_request = verification

    def set_url(self, url):
        """
        Set the URL of the Workbench instance
        :url: the URL of the Workbench instance to be hit
        """
        self.url = url.rstrip('/')

    def set_file_input(self, input_file_path):
        """
        For annotating file content, send file path string and process file as a binary

        :param input_file_path: file path to the file to be sent to TERMite
        """
        file_obj = open(input_file_path, 'rb')
        file_name = os.path.basename(input_file_path)
        split_tup = os.path.splitext(input_file_path)
        self.file_ext = split_tup[1]
        self.file_input = {"file": (file_name, file_obj)}

    def set_dataset_name(self, name):
        """
        Set the name of the dataset you will create on your instance
        @param name: name of dataset to create
        """
        self.dataset_name = name

    def set_dataset_desc(self, desc):
        """
        Set the desc of the dataset you will create on your instance
        @param desc: description of dataset to create
        """
        self.dataset_description = desc

    def set_dataset_id(self, dataset_id):
        """
        Set the id of the dataset you would like to edit/use.
        @param dataset_id: id of the dataset you would like to edit/use
        """
        self.dataset_description = dataset_id

    def create_dataset(self):
        """
        Given a dataset name, description and owner, this method will attempt
        to create a dataset with those given details.
        """
        endpoint = "{}/api/datasets".format(self.url.rstrip("/"))
        payload = {
            "title": self.dataset_name,
            "description": self.dataset_description,
            "owner": self.user_info
        }
        req = requests.post(endpoint, json=payload, headers=self.headers)
        if req.ok:
            self.dataset_id = req.json()['id']

    def upload_file_to_dataset(self, dataset_id='', first_row_is_header=True):
        """
        Upload file provided to class to dataset - do not pass a dataset_id if you previously created a dataset using
        this class
        @param dataset_id: id of dataset to upload file to - do no pass anything if previously set
        @param first_row_is_header: True if first row in file is header row (default), otherwise False
        @return:
        """
        if dataset_id != "":
            self.dataset_id = dataset_id
        endpoint_options = {
            '.xls': "{}/api/datasets/{}/uploadExcel?firstRowIsAttributes={}".format(self.url.rstrip("/"),
                                                                                    self.dataset_id,
                                                                                    first_row_is_header),
            '.xlsx': "{}/api/datasets/{}/uploadExcel?firstRowIsAttributes={}".format(self.url.rstrip("/"),
                                                                                     self.dataset_id,
                                                                                     first_row_is_header),
            '.csv': "{}/api/datasets/{}/uploadCsv?firstRowIsAttributes={}".format(self.url.rstrip("/"),
                                                                                  self.dataset_id,
                                                                                  first_row_is_header),
            '.tsv': "{}/api/datasets/{}/uploadTsv?firstRowIsAttributes={}".format(self.url.rstrip("/"),
                                                                                  self.dataset_id,
                                                                                  first_row_is_header)
        }
        endpoint = endpoint_options[self.file_ext]
        req = requests.post(endpoint, headers=self.headers, files=self.file_input)
        job_id = req.json()["jobId"]
        while not check_job_status(self.url, self.headers, job_id):
            time.sleep(5)

    def auto_annotate_dataset(self, dataset_id=''):
        """
        Annotate a dataset in Workbench automatically.
        Please call set_termite_config first if you want to customize the VOCabs used and/or the attributes to annotate.
        If you do not set a termite config, the system will annotate each column in the dataset with every VOCab.
        @param dataset_id: id of dataset to annotate - do not pass anything if previously set

        """
        if dataset_id != "":
            self.dataset_id = dataset_id
        annotate_dataset_endpoint = "{}/api/datasets/{}/autoAnnotateWithTermite?exact=false&replace=false".format(
            self.url.rstrip("/"),
            self.dataset_id)
        if self.termite_config == '':
            req = requests.post(annotate_dataset_endpoint, headers=self.headers)
        else:
            req = requests.post(annotate_dataset_endpoint, headers=self.headers, json=self.termite_config)

        job_id = req.json()["jobId"]

        while not check_job_status(self.url, self.headers, job_id):
            time.sleep(5)
        return True

    def set_termite_config(self, dataset_id='', vocabs=None, passed_attrs=None):
        """
        Use this method to set the termite config for the dataset you want to annotate. Please note the following:
        - The vocabs and passed_attrs objects must match in length.
        - You do not need to set a TERMite Config to WB - if you do not, the system will annotate with all VOCabs.
        - If you specify an attribute/column, but pass an empty list of VOCabs,
                    the system will annotate that attribute with all VOCabs.
        Here is an example run of this method: wb.set_termite_config('500',[[5],[6]], [2000,2001])
            - The system will annotate dataset 500's, 2000 and 2001 attributes/columns with vocabs 5 and 6 respectively.

        @param dataset_id: id of dataset to annotate - do not pass anything if previously set
        @param vocabs: a list of list<int> representing the VOCabs that you want to annotate each attribute/column
        @param passed_attrs: list<int> of attributes/columns you would like to set a TERMite config for.
        """
        if vocabs is None or passed_attrs is None:
            return 0
        elif len(passed_attrs) != len(vocabs):
            return 0
        termite_configs = []
        if dataset_id != "":
            self.dataset_id = dataset_id
        get_attributes_endpoint = "{}/api/datasets/{}/attributes".format(self.url, self.dataset_id)
        attr_resp = requests.get(get_attributes_endpoint, headers=self.headers)
        all_attributes = attr_resp.json()
        attributes = [attr for attr in all_attributes if attr['id'] in passed_attrs]
        for idx, attribute in enumerate(attributes):
            termite_config = {'termiteConfig': attribute['termiteConfig']}
            termite_config['termiteConfig']['vocabIds'] = vocabs[idx]
            termite_config['attributeIds'] = [attribute['id']]
            termite_configs.append(termite_config)
        self.termite_config = termite_configs

    def export_dataset(self, dataset_id='', form='EXCEL', table_format='GROUPED_ANNOTATIONS', exact='false', filt='',
                       filter_attributes=None, filter_vocab='', filter_primary_id='', filter_annotation_type='',
                       exclude_attributes=None):
        """
        Use this method to export a dataset from WB. We will default to export with all annotations to excel as grouped.
        @param dataset_id: id of dataset to export - do not pass anything if previously set
        @param form: the file extension of the export - can be 'EXCEL', 'TSV', or 'CSV'
        @param table_format: format of resulting export - can be 'GROUPED_ANNOTATIONS' or 'FLATTENED_ANNOTATIONS'
        @param exact:
        @param filt: string filter to filter what rows are provided in the export
        @param filter_attributes: provide a list<int> of attributes/columns to include in the export
        @param filter_vocab: export only annotations made by this VOCab
        @param filter_primary_id: export only annotations that include this primary id
        @param filter_annotation_type: export rows according to annotation type
                                       - can be 'MANUEL_VERFIED', 'INFERRED_FROM_RULE', or 'AUTOMATED'.
                                       defaults to include all annotations.
        @param exclude_attributes: provide a list<int> of attributes/columns to NOT include in the export
        @return:
        """
        if exclude_attributes is None:
            exclude_attributes = []
        if filter_attributes is None:
            filter_attributes = []
        if dataset_id != "":
            self.dataset_id = dataset_id

        export_dataset_endpoint = "{}/api/datasets/{}/export".format(self.url, self.dataset_id)
        params = {
            'format': form,
            'tableFormat': table_format,
            'exact': exact,
            'filter': filt,
            'filter_attributes': filter_attributes,
            'filter_vocab': filter_vocab,
            'filter_primary_id': filter_primary_id,
            'filter_annotation_type': filter_annotation_type,
            'exclude_attributes': exclude_attributes,
        }

        job_request = requests.post(export_dataset_endpoint, params=params, headers=self.headers)
        json_job_req = job_request.json()
        job_id = json_job_req['jobId']
        while not check_job_status(self.url, self.headers, job_id):
            time.sleep(5)
        download_link = '{}/api/datasets/{}/download/{}'.format(self.url, self.dataset_id, job_id)
        export = requests.get(download_link, headers=self.headers)
        return export.content


def check_job_status(url, headers, job_id):
    """
    Check the status of a job on a workbench server
    @param url: the url of the workbench instance to check
    @param headers: the authentication header to send to authenticate with the instance
    @param job_id: the job_id to check
    @return: True if job is complete, False otherwise
    """
    job_status_endpoint = "{}/api/jobs/{}".format(url.rstrip("/"), job_id)
    req = requests.get(job_status_endpoint, headers=headers)
    json_req = req.json()
    status = json_req['jobStatus']

    if status == 'COMPLETE':
        return True
    else:
        return False


def upload_and_annotate_directory(input_directory_path, wb_url, username, password, client_id, annotate=False,
                                  vocabs=None, attrs=None):
    """
    Given an input directory, this method will create WB datasets for each applicable file
    (file ext of csv,tsv, xlsx or xls) in the directory and upload the files to WB. It will also annotate each file if
    annotate is set to true according to the vocabs and attrs passed.
    @param input_directory_path: directory of files to upload to WB
    @param wb_url: url of WB instance to use.
    @param username: username of user to authenticate with
    @param password: password of user to authenticate with
    @param client_id: client_id of instance to authenticate with
    @param annotate: boolean - True to annotate each file in directory, false to do nothing. Defaults to false
    @param vocabs: a list of list<int> representing the VOCabs that you want to annotate each attribute/column
    @param attrs: list<int> of attributes/columns you would like to set a TERMite config for.
    @return:
    """
    wb = WorkbenchRequestBuilder()
    wb.set_url(wb_url)
    wb.set_oauth2(client_id, username, password)
    datasets = []
    for path, _, filenames in os.walk(input_directory_path):
        for filename in filenames:
            file_path = os.path.join(path, filename)
            if filename.endswith(".csv") or filename.endswith(".xlsx") \
                    or filename.endswith(".tsv") or filename.endswith(".xls"):
                wb.set_dataset_name(os.path.splitext(filename)[0])
                wb.set_dataset_desc(os.path.splitext(filename)[0])
                wb.create_dataset()
                wb.set_file_input(file_path)
                wb.upload_file_to_dataset()
                if annotate:
                    wb.set_termite_config('', vocabs, attrs)
                    wb.auto_annotate_dataset()
                datasets.append(wb.dataset_id)
    return datasets


def export_datasets(export_directory_path, wb_url, username, password, client_id, datasets, form='EXCEL',
                    table_format='GROUPED_ANNOTATIONS', exact='false', filt='',
                    filter_attributes=None, filter_vocab='', filter_primary_id='', filter_annotation_type='',
                    exclude_attributes=None):
    """
    Given a list of WB datasets, this method with export all of them to a given directory.
    @param export_directory_path: path of where the exports should be saved
    @param wb_url: url of WB instance to use.
    @param username: username of user to authenticate with
    @param password: password of user to authenticate with
    @param client_id: client_id of instance to authenticate with
    @param datasets: list<int> of datasets to export.
    @param form: the file extension of the export - can be 'EXCEL', 'TSV', or 'CSV'
    @param table_format: format of resulting export - can be 'GROUPED_ANNOTATIONS' or 'FLATTENED_ANNOTATIONS'
    @param exact:
    @param filt: string filter to filter what rows are provided in the export
    @param filter_attributes: provide a list<int> of attributes/columns to include in the export
    @param filter_vocab: export only annotations made by this VOCab
    @param filter_primary_id: export only annotations that include this primary id
    @param filter_annotation_type: export rows according to annotation type
                                       - can be 'MANUEL_VERFIED', 'INFERRED_FROM_RULE', or 'AUTOMATED'.
                                       defaults to include all annotations.
    @param exclude_attributes: provide a list<int> of attributes/columns to NOT include in the export
    @return:
    """
    wb = WorkbenchRequestBuilder()
    wb.set_url(wb_url)
    wb.set_oauth2(client_id, username, password)
    file_exts = {
        'EXCEL': '.xlsx',
        'CSV': '.csv',
        'TSV': '.tsv'
    }
    file_ext = file_exts[form]
    for dataset in datasets:
        dataset_info_link = '{}/api/datasets/{}'.format(wb.url, dataset)
        file_export = wb.export_dataset(dataset, form, table_format, exact, filt, filter_attributes, filter_vocab,
                                        filter_primary_id, filter_annotation_type, exclude_attributes)
        dataset_info = requests.get(dataset_info_link, headers=wb.headers)
        dataset_name = dataset_info.json()['title']
        filename = dataset_name + file_ext
        with open(os.path.join(export_directory_path, filename), 'wb') as file:
            file.write(file_export)
            file.close()


def get_attributes(columns_to_clean, wb_url, headers, dataset_id):
    """
    Given a list<string> of column names, this method will return a list<int> of attributes (what are called columns
    in Workbench) for a given dataset.
    If the returned list does not have the same length as the inputted list, we will not return it
     and will print an error.
    @param columns_to_clean: list<string> of columns to identify by attribute number
    @param wb_url: url of workbench to connect to
    @param headers: the wb object headers attribute
    @param dataset_id: id of dataset to use.
    @return: list<int> of attribute ids that correspond with column names
    """
    attribute_endpoint = '{}/api/datasets/{}/attributes'.format(wb_url.rstrip('/'), dataset_id)
    resp = requests.get(attribute_endpoint, headers=headers)
    all_attrs = resp.json()
    attrs_ids = []
    for attr in all_attrs:
        if attr['name'] in columns_to_clean:
            attrs_ids.append(attr['id'])
    if len(columns_to_clean) != len(attrs_ids):
        print('ERROR: One of the columns inputted was not found.')
        exit(2)
    return attrs_ids


def get_vocabs(vocabs, wb_url, headers):
    """
    Given a list<string> of vocab names, this method will return a list<int> of vocabs by their number ID in Workbench.
    If the returned list does not have the same length as the inputted list, we will not return it
    and will print an error.
    @param vocabs: list<string> of vocabs to identify by vocab number
    @param wb_url: url of workbench to connect to
    @param headers: the wb object headers attribute
    @return: list<int> of vocab ids that correspond with vocab names
    """
    vocab_endpoint = '{}/api/vocabs/active'.format(wb_url.rstrip('/'))
    resp = requests.get(vocab_endpoint, headers=headers)
    all_vocabs = resp.json()
    vocab_ids = []
    for vocab in all_vocabs:
        if vocab['termiteId'] in vocabs:
            vocab_ids.append(vocab['id'])

    if len(vocabs) != len(vocab_ids):
        print('ERROR: One of the vocab names inputted was not found.')
        exit(2)
    return vocab_ids

