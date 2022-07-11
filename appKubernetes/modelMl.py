
class ModelMl:
  def __init__(self, id, model_name, guid, path, accuracy, auc):
    self.id = id
    self.model_name = model_name
    self.guid = guid
    self.path = path
    self.accuracy = accuracy
    self.auc = auc