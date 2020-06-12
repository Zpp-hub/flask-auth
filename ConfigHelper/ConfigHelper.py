import os, sys

try:
    # Python 2 only:
    import ConfigParser as Cp
except ImportError:
    # Python 2 and 3 (after ``pip install configparser``)
    import configparser as Cp


class ConfigHelper(object):
    def __init__(self, config_path="/home/zpp/PycharmProjects/flask-demo/config/config.cfg"):
        self.config = Cp.ConfigParser()
        self.config.optionxform = str
        if os.path.exists(config_path):
            self.config.read(config_path)
        else:
            self.config.read(os.path.join(os.path.split(os.path.realpath(__file__))[0], config_path))

    def ConfigSectionMap(self, section):
        tp_dict = {}
        options = self.config.options(section)
        for option in options:
            try:
                tp_dict[option] = self.config.get(section, option)
                if tp_dict[option] == -1:
                    print(("skip: %s" % option))
            except:
                print(("exception on %s!" % option))
                tp_dict[option] = None
        return tp_dict

    def ConfigSectionMapCompatiable(self, section, key):
        tp_env_key = section + "_" + key
        tp_value = os.environ.get(tp_env_key)
        if tp_value:
            return tp_value
        tp_dict = {}
        options = self.config.options(section)
        for option in options:
            try:
                tp_dict[option] = self.config.get(section, option)
                if tp_dict[option] == -1:
                    print(("skip: %s" % option))
            except:
                print(("exception on %s!" % option))
                tp_dict[option] = None
        return tp_dict[key]

# print ConfigSectionMap("ServerConfig")["DssServerUrl"];
