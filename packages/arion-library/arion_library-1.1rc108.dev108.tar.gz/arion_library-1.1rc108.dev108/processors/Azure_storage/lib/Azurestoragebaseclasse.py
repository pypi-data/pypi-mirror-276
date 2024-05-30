import logging
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from azure.data.tables import TableServiceClient, generate_table_sas, TableSasPermissions
from datetime import datetime, timezone, timedelta
from azure.core.credentials import AzureNamedKeyCredential


class AzureStorageConnector:
    """
    Cette classe permet d'établir une connexion avec les services de stockage Azure Blob et Azure Table.

    :param str connection_string: La chaîne de connexion à utiliser pour se connecter au service. 
                                  Par défaut, None.
    :param str account_name: Le nom du compte de stockage Azure. Par défaut, None.
    :param str account_key: La clé du compte de stockage Azure. Par défaut, None.

    :ivar str connection_string: La chaîne de connexion à utiliser pour se connecter au service.
    :ivar str account_name: Le nom du compte de stockage Azure.
    :ivar str account_key: La clé du compte de stockage Azure.
    :ivar logging.Logger logger: Le logger pour enregistrer les messages.
    """

    def __init__(self, connection_string=None, account_name=None, account_key=None):
        """
        Initialise une instance de la classe AzureStorageConnector.

        :param str connection_string: La chaîne de connexion à utiliser pour se connecter au service. 
                                      Par défaut, None.
        :param str account_name: Le nom du compte de stockage Azure. Par défaut, None.
        :param str account_key: La clé du compte de stockage Azure. Par défaut, None.
        """
        self.connection_string = connection_string
        self.account_name = account_name
        self.account_key = account_key
        self.logger = logging.getLogger('AzureStorageConnector')

 