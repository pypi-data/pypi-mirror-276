class DBMANAGER(object):
    """
    A base class for interacting with MongoDB using CRUD operations.
    """
    sample_document = {
        "PATIENT_ID": "X40135202726",
        "Name": "Johnny B. Goode",
        "Age": 45,
        "Sex": "m",
        "Neurological-data-list": [
            {
                "Stroke on-set (mins)": 40,
                "NIHSS": 6,
                "mRS": 2,
                "Scan paths": {"NCCT": None, "CTA": None, "DW-MR": None, "TOF-MRI": None},
                "Video path": None,
                "Date": None,
            }
        ],
    }

    def __init__(self, uri=None, database_name=None, collection_name=None):
        """
        Initializes the connection to MongoDB.

        Args:
          client_uri (str): The connection URI for your MongoDB instance.
          database_name (str): The name of the database to use.
          collection_name (str): The name of the collection to interact with.
        """
        super(DBMANAGER, self).__init__()

        import sys
        import pymongo

        try:
            self.client = pymongo.MongoClient(uri)
        except pymongo.errors.ConfigurationError:
            print(
                "An Invalid URI host error was received. Is your Atlas host name correct in your connection string?"
            )
            sys.exit(1)

        # Set self.db as "cerebrum_scanner" database
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]
        
        if not self.sample_document in list(self.collection.find()):
            self.create(document=self.sample_document)


    def create(self, document):
        """
        Inserts a new document into the collection.

        Args:
          document (dict): The document data to insert.

        Returns:
          The inserted document's ID (ObjectId) on success, None otherwise.
        """
        result = self.collection.insert_one(document)
        return result.inserted_id if result.inserted_id else None

    def read(self, filter=None):
        """
        Retrieves documents from the collection based on a filter (optional).

        Args:
          filter (dict, optional): A dictionary representing the filter criteria. Defaults to None (retrieve all documents).

        Returns:
          A list of dictionaries representing the retrieved documents.
        """
        documents = self.collection.find(filter)
        return [doc for doc in documents]  # Convert Cursor object to list

    def update(self, filter, update_data):
        """
        Updates documents in the collection matching the filter.

        Args:
          filter (dict): A dictionary representing the filter criteria for documents to update.
          update_data (dict): A dictionary containing the update operations (e.g., $set, $inc).

        Returns:
          The number of documents updated.
        """
        result = self.collection.update_many(filter, update_data)
        return result.modified_count

    def delete(self, filter):
        """
        Deletes documents from the collection matching the filter.

        Args:
          filter (dict): A dictionary representing the filter criteria for documents to delete.

        Returns:
          The number of documents deleted.
        """
        result = self.collection.delete_many(filter)
        return result.deleted_count




    def create_collection(self, collection_name=None):
        # Try to create a 'students' collection within the selected database
        try:
            # Creating a collection named with "collection_name" within the selected database
            collection = self.db[collection_name]

            # Printing a message indicating a successful collection creation
            print(f"Collection {collection_name} created successfully")

        except Exception as e:
            # Handling exceptions and printing an error message if collection creation fails
            print(f"Error: {e}")

    def insert_document(self, collection_name=None, document=None):
        # e.g., self.db["patient_list"].insert_one(document)
        self.db[collection_name].insert_one(document)

    # Method to fetch all students' data from the 'students' collection
    def fetch_documents(self, collection_name=None):
        # Querying the 'students' collection to find all data
        data = self.db[collection_name].find()
        return data

    # Method to update a specific document's data based on a document's property
    def update(self, collection_name=None, document_id=None):
        data = self.fetch_documents(collection_name=collection_name)
        self.db[collection_name].update_one({"_id": document_id}, {"$set": data})

        # Updating the student data in the 'students' collection
        self.collection.update_one({"_id": document_id}, {"$set": data})

    def delete_document(self, document=None):
        self.collection_patient_list.insert_one(document)


# class MongoDbManager:




# # Example usage
# client_uri = "mongodb://localhost:27017/"  # Replace with your connection URI
# database_name = "my_database"
# collection_name = "my_collection"

# mongo_manager = MongoDbManager(client_uri, database_name, collection_name)

# # Create a document
# new_document = {"name": "Alice", "age": 30}
# document_id = mongo_manager.create(new_document)

# # Read all documents
# documents = mongo_manager.read()

# # Update a document by name
# filter = {"name": "Alice"}
# update_data = {"$set": {"age": 31}}
# mongo_manager.update(filter, update_data)

# # Delete documents older than 25
# filter = {"age": {"$gt": 25}}  # greater than 25
# mongo_manager.delete(filter)
