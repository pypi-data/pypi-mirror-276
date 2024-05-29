# -*- coding: utf-8 -*-
###############################################################################
# author       # TecDroiD
# date         # 2022-12-02
# ---------------------------------------------------------------------------
# description  # a Template for files or directories
#              #
#              #
##############################################################################
import json
import base64
import os
import logging


def pattern_replace(text, pattern, pre='{{', post='}}'):
    """ replace text with pattern if possible
    """
    haystack = text
    for key, value in pattern.items():
        logging.debug(f'replacing {key} with {value}')
        haystack = haystack.replace(pre + key + post, value)
    return haystack


class Template(object):
    """ this is a filesystem template for upm
    """

    @staticmethod
    def from_file(filename):
        """ read a json file and create a template from it
        """
        os.path.basename(filename)
        with open(filename) as fp:
            template = Template('')
            template.__values = json.load(fp)
            return template

    @staticmethod
    def __get_parameters(path, template):
        """ get the parameters of a template directory if neccessary
        """
        try:
            with open(os.path.join(path, ".upmparams")) as fp:
                logging.debug("reading parameter file")
                data = json.load(fp)
                logging.debug(data)
                template["params"] = data
        except:
            pass

    @staticmethod
    def scan(name, path, description='', _cpath='', _tmpl=None):
        """ scan a directory to create a template
        """
        logging.debug(f'scanning path {path}/{_cpath}')
        template = _tmpl if _tmpl is not None else Template(name, description)

        if _cpath == '':
            # we are in our first iteration, load parameter file
            logging.debug(
                "loading template"
                )
            Template.__get_parameters(path, template)

        for file in os.listdir(os.path.join(path, _cpath)):
            # get all files in directory
            relpath = os.path.join(_cpath, file)
            filepath = os.path.join(path, relpath)
            if os.path.isdir(filepath):
                # scan subdirs
                Template.scan(name, path, description, relpath, template)
            else:
                # read file and append data
                with open(filepath, 'rb') as fp:
                    content = fp.read()
                    logging.debug(
                        f"creating file {path}/{_cpath}/{file}"
                        )
                    template.add_item(_cpath, file, content)
        return template

    def __init__(self, name, description=''):
        """ initialize a template
        """
        self.__values = {
            'name': name,
            'description': description,
            'files': {}
            }

    def add_item(self, path, name, content=b''):
        """ create a directory path in files structure
        """
        files = self.files
        if path != '':
            directory = path.split('/')
            # create directory structure if neccessary
            for subdir in directory:
                if subdir not in files:
                    files[subdir] = {}
                files = files[subdir]
        # create the file
        files[name] = base64.b64encode(content).decode('utf8')

    @staticmethod
    def write_content(filename, content, pattern, replace=True):
        """ write file content
        """
        # entry is file
        with open(filename, 'wb') as fp:
            logging.debug(f'filecontent {content}')
            bcontent = base64.b64decode(content.encode('utf8')).decode()
            if replace is True:
                bcontent = pattern_replace(bcontent, pattern)
            # write file
            fp.write(bcontent.encode('utf8'))

    def apply_parameters(self, pattern={}):
        """ apply parameters that are neccessary
        -- may be scanned directly in future --
        this is done by simply looking if a parameter is already in the
        pattern. if not, ask for it
        parameters can be set in a .upmparams file which has entries in
        the form
            "parametername" : "_type_[:optional]"

        possible types are currently:
            "str" - for string
            "int" - for an integer
            "float" - for a float

        so possible values could be
        {
           "foo": "str",    -- this would be a required value
           "bar": "int:optional" -- this would be an optional integer
        }
        """
        for pname in self.parameters.keys():
            logging.debug(f"checking parameter {pname}")
            if pname not in pattern:
                ptype = self.parameters[pname].split(':', maxsplit=1)
                logging.debug(f"ptype : {ptype} ({len(ptype)})")
                if len(ptype) == 1 or ptype[1] != "optional":
                    # parameter is not given and its not optional
                    # ask for it
                    inval = input(f"Please set parameter {pname}:")
                    # convert type
                    match ptype[0]:
                        case "str":
                            value = inval
                        case "int":
                            value = int(value)
                        case "float":
                            value = float(value)
                        case _:
                            raise "unknown parameter type"
                    pattern[pname] = value

    def create(self, basepath, pattern={}, _cpath='', _files=None, _replace=True):
        """ create the template file structure using the patterns
        for pattern replacement
        """
        if pattern is None:
            pattern = {}

        files = _files if _files is not None else self.files

        logging.debug(f'---- iterating subpath {_cpath}')
        for name, entry in files.items():
            logging.debug(f'** {_cpath} : having {name}')
            # replace
            nname = pattern_replace(name, pattern, '', '')
            relpath = os.path.join(_cpath, nname)
            abspath = os.path.join(basepath, relpath)
            if isinstance(entry, dict):
                # entry is a directory, create subdir
                logging.debug(f'creating directory {abspath}')
                if not os.path.exists(abspath):
                    os.mkdir(abspath)
                logging.debug(f'---- iterating into directory {relpath}')
                self.create(basepath, pattern, relpath, entry, _replace)
            else:
                # entry is a file, create and write
                # create filename entry for internal replacement
                pattern['current_file'] = entry
                # and write file
                logging.debug(f'creating file  {abspath}')
                self.write_content(abspath, entry, pattern, _replace)
        # done - hopefully..

    def dump(self, filename):
        """ write yourself to a file
        """
        with open(filename, 'w') as fp:
            fp.write(self.json)

    def __repr__(self):
        desc = self.description
        if len(desc) == 0:
            desc = '<NO DESCRIPTION>'
        return f'Template {self.name}\n{desc}'

    @property
    def json(self):
        """ dump the template to json
        """
        return json.dumps(self.__values, indent=2)

    @property
    def files(self):
        """ get the files object of the template
        """
        return self.__values['files']

    @property
    def name(self):
        return self.__values.get('name')

    @property
    def description(self):
        return self.__values['description']

    @property
    def parameters(self):
        return self.__values.get("params", {})
