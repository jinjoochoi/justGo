class Path(object):
  source_id = 0
  source_name = ""
  destination_id = 0
  destination_name = ""

  def __init__(self, source_id, source_name, destination_id, destination_name):
     self.source_id = source_id
     self.source_name = source_name
     self.destination_id = destination_id
     self.destination_name = destination_name
