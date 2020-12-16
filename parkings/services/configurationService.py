from ..daos import ConfigurationDao

class ConfigurationService:
    
    def get(self, filters):
       return ConfigurationDao().get(filters)