import logging
from azure.data.tables import TableSasPermissions
from .Azurestoragebaseclasse import AzureStorageConnector
from datetime import datetime, timezone, timedelta
from azure.data.tables import TableServiceClient, generate_table_sas, TableSasPermissions
from azure.core.credentials import AzureNamedKeyCredential


class AzureDataTablesClient(AzureStorageConnector):
    """
    Cette classe permet d'interagir avec Azure Data Tables en utilisant l'héritage de AzureStorageConnector.

    :param str table_name: Le nom de la table dans Azure Data Tables.
    :param str connection_string: La chaîne de connexion à utiliser pour se connecter au service. 
                                  Par défaut, None.
    :param str account_name: Le nom du compte de stockage Azure. Par défaut, None.
    :param str account_key: La clé du compte de stockage Azure. Par défaut, None.

    :ivar str table_name: Le nom de la table dans Azure Data Tables.
    :ivar str connection_string: La chaîne de connexion à utiliser pour se connecter au service.
    :ivar str account_name: Le nom du compte de stockage Azure.
    :ivar str account_key: La clé du compte de stockage Azure.
    """

    def __init__(self, table_name, connection_string=None, account_name=None, account_key=None):
        """
        Initialise une instance de la classe AzureDataTablesClient.

        :param str table_name: Le nom de la table dans Azure Data Tables.
        :param str connection_string: La chaîne de connexion à utiliser pour se connecter au service. 
                                      Par défaut, None.
        :param str account_name: Le nom du compte de stockage Azure. Par défaut, None.
        :param str account_key: La clé du compte de stockage Azure. Par défaut, None.
        """
        super().__init__(connection_string, account_name, account_key)
        self.table_name = table_name
        self.table_service_client = None

    def connect_table_service(self, table_name, table_permissions=TableSasPermissions(read=True), table_expiry=None):
        """
        Établit une connexion avec le service de table Azure.

        :param str table_name: Le nom de la table.
        :param TableSasPermissions table_permissions: Les permissions pour le SAS de la table. Par défaut, TableSasPermissions(read=True).
        :param datetime table_expiry: La date d'expiration du SAS de la table. Par défaut, None.

        :raises ValueError: Si aucune chaîne de connexion ni nom de compte et clé ne sont fournis.

        :return: None
        """
        try:
            if self.connection_string:
                self.table_service_client = TableServiceClient.from_connection_string(self.connection_string)
                self.logger.info("Connected to Azure Table Service using connection string")
            elif self.account_name and self.account_key:
                sas_key = self.generate_table_sas_key(table_name, permissions=table_permissions, expiry=table_expiry)
                self.table_service_client = TableServiceClient(sas_key)
                self.logger.info("Connected to Azure Table Service using SAS token")
            else:
                raise ValueError("Either connection string or both account name and account key must be provided")
        except Exception as e:
            self.logger.error(f"Error connecting to Azure Table Service: {e}")

    def generate_table_sas_key(self, credentials : AzureNamedKeyCredential  , table_name="test", permissions=TableSasPermissions(read=True), expiry=None):
        """
        Génère un jeton SAS pour le stockage de table Azure.

        :param str table_name: Le nom de la table.
        :param TableSasPermissions permissions: Les permissions pour le SAS de la table. Par défaut, TableSasPermissions(read=True).
        :param datetime expiry: La date d'expiration du SAS de la table. Par défaut, None.

        :return: Le jeton SAS généré.
        :rtype: str
        """
        expiry = expiry or datetime.now(timezone.utc) + timedelta(hours=1)  
        sas_token = generate_table_sas(
            credentials,
            table_name=table_name,
     
            permission=permissions,
            expiry=expiry
        )
        return sas_token



    def insert_batch_entities(self, entities, PartitionKey, RowKey, columnstoinsert, batch_size=1,
                              table_permissions=TableSasPermissions(read=True), table_expiry=None):
        """
        Insère des entités dans une table Azure Data Table en lots.

        :param entities: La liste des entités à insérer dans la table.
        :type entities: list
        :param PartitionKey: La clé de partition pour les entités.
        :type PartitionKey: str
        :param RowKey: La clé de ligne pour les entités.
        :type RowKey: str
        :param columnstoinsert: La liste des colonnes à insérer dans la table.
        :type columnstoinsert: list
        :param batch_size: La taille de chaque lot pour l'insertion par lots. Par défaut, 1.
        :type batch_size: int
        :param table_permissions: Les permissions pour le SAS de la table. Par défaut, TableSasPermissions(read=True).
        :type table_permissions: azure.data.tables.TableSasPermissions
        :param table_expiry: La date d'expiration du SAS de la table. Par défaut, None.
        :type table_expiry: datetime

        :raises ValueError: Si une erreur se produit lors de l'insertion des données.

        :return: None
        """
        try:
   
            logging.info(f'Preparing data to insert into {self.table_name} table')
            table_client = self.table_service_client.get_table_client(self.table_name)
            entities_to_insert = []
            for row in entities:
                entity = {'PartitionKey': PartitionKey, 'RowKey': row[RowKey]}
                for col in columnstoinsert:
                    entity[col] = row[col]
                entities_to_insert.append(("upsert", entity))
                if len(entities_to_insert) == batch_size:
                     logging.info(f'batch to insert : {entities_to_insert}')
                     table_client.submit_transaction(entities_to_insert)
                     entities_to_insert = []
            if len(entities_to_insert) > 0:
                logging.info(f'batch to insert : {entities_to_insert}')
                table_client.submit_transaction(entities_to_insert)
            logging.info(f'All lines are successfully inserted into {self.table_name} table.')
        except ValueError as e:
             logging.error(f'An error was occured while trying to insert data into {self.table_name} table : {e}')

    def query_entities(self, filter_condition, batch_size=1,
                       table_permissions=TableSasPermissions(read=True), table_expiry=None):
        """
        Exécute une requête pour récupérer des entités d'une table Azure Data Table.

        :param str filter_condition: La condition de filtrage à appliquer à la requête.
        :param int batch_size: Le nombre de résultats par page. Par défaut, 1.
        :param table_permissions: Les permissions pour le SAS de la table. Par défaut, TableSasPermissions(read=True).
        :type table_permissions: azure.data.tables.TableSasPermissions
        :param table_expiry: La date d'expiration du SAS de la table. Par défaut, None.
        :type table_expiry: datetime

        :return: Une liste d'entités récupérées de la table.
        :rtype: list
        """
        try:

            table_client = self.table_service_client.get_table_client(self.table_name)
            entities = []
            logging.info(f'Executing query : {filter_condition}')
            for entity_page in table_client.query_entities(query_filter=filter_condition, results_per_page=batch_size).by_page():
                entities.extend(list(entity_page))
                break
            logging.info(f'Query Results : {entities}')
            return entities
        except ValueError as e:
            logging.error(f'An error occured while trying to query data from {self.table_name} table : {e}')
  