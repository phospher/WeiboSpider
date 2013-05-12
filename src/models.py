class DictEntity(dict):
	def __getattr__(self, attr):
		return self[attr]

	def __setattr__(self, attr, value):
		self[attr] = value
		
class WeiboModel(DictEntity):
	pass

class UserModel(DictEntity):
    pass