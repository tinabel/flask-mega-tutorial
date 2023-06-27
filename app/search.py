from flask import current_app


def add_to_index(index, model):
  # This function adds a model to the index.
  #
  # Parameters:
  #   index (str): The index.
  #   model (Model): The model.
  #
  # Returns:
  #   None
  if not current_app.opensearch:
    return
  payload = {}
  for field in model.__searchable__:
    payload[field] = getattr(model, field)
  current_app.opensearch.index(index=index, id=model.id, body=payload)


def remove_from_index(index, model):
  # This function removes a model from the index.
  #
  # Parameters:
  #   index (str): The index.
  #   model (Model): The model.
  #
  # Returns:
  #   None
  if not current_app.opensearch:
      return
  current_app.opensearch.delete(index=index, id=model.id)


def query_index(index, query, page, per_page):
  # This function queries the index.
  #
  # Parameters:
  #   index (str): The index.
  #   query (str): The query.
  #   page (int): The page number.
  #   per_page (int): The number of items per page.
  #
  # Returns:
  #   tuple: The ids of the items found and the total number of items.

  if not current_app.opensearch:
    return [], 0

  search = current_app.opensearch.search(
    index=index,
    body={'query': {'multi_match': {'query': query, 'fields': ['*']}},
      'from': (page - 1) * per_page, 'size': per_page})
  ids = [int(hit['_id']) for hit in search['hits']['hits']]
  return ids, search['hits']['total']['value']