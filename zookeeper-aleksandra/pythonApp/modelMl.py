
class ModelMl:
  def __init__(self, id, model_name, guid, path, accuracy, auc):
    self.id = id
    self.modelName = model_name
    self.guid = guid
    self.modelPath = path
    self.accuracy = accuracy
    self.auc = auc