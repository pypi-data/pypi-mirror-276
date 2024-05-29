from copy import deepcopy


class NodeMeta(type):
    def __new__(cls, name, bases, attrs):
        """Build accessors for each attribute in ATTRS.

        ATTRS is a dict of attribute names to dicts of attribute options that help to validate access to the attribute.
        """
        if attrs.get("ATTRS"):
            attr_map = deepcopy(attrs["ATTRS"])
            for key in attr_map:
                kwargs = attr_map[key]
                datatype = kwargs.pop("type")
                result = cls.build_accessors(key, datatype, **kwargs)
                for entry in result:
                    attrs[entry["name"]] = entry["function"]

        return super().__new__(cls, name, bases, attrs)

    @classmethod
    def build_accessors(cls, name, datatype, **kwargs):
        datatype = datatype.split(":")
        is_list = False
        if len(datatype) > 1:
            datatype = datatype[1]
            is_list = True
        else:
            datatype = datatype[0]
        if datatype == "str":
            if is_list:
                return cls.build_list_string_accessors(name, **kwargs)
            return cls.build_string_accessors(name, **kwargs)
        elif datatype == "int":
            if is_list:
                return cls.build_list_int_accessors(name, **kwargs)
            return cls.build_int_accessors(name, **kwargs)
        elif datatype == "Cmd":
            if is_list:
                return cls.build_list_cmd_accessors(name, **kwargs)
            return cls.build_cmd_accessors(name, **kwargs)
        elif datatype == "dict":
            if is_list:
                return cls.build_list_dict_accessors(name, **kwargs)
            return cls.build_dict_accessors(name, **kwargs)
        # we got here because we don't know how to handle the datatype
        raise TypeError("Invalid type: %s" % datatype)

    @classmethod
    def build_string_accessors(cls, name, **kwargs):
        default = kwargs.get("default")
        prop = "_{}".format(name)
        
        accessor_name = name

        def accessor(self, *args):
            if len(args) > 1:
                raise TypeError("Accessor takes at most one argument")
            if len(args) == 1:
                self.validate_string(accessor_name, args[0], **kwargs)
                setattr(self, prop, args[0])
                return self
            if hasattr(self, prop):
                return getattr(self, prop)
            return default

        return [{"name": accessor_name, "function": accessor}]

    @classmethod
    def build_int_accessors(cls, name, **kwargs):
        default = kwargs.get("default")
        prop = "_{}".format(name)
        accessor_name = name

        def accessor(self, *args):
            if len(args) > 1:
                raise TypeError("Accessor takes at most one argument")
            if len(args) == 1:
                self.validate_int(accessor_name, args[0], **kwargs)
                setattr(self, prop, args[0])
                return self
            if hasattr(self, prop):
                return getattr(self, prop)
            return default

        return [{"name": accessor_name, "function": accessor}]

    @classmethod
    def build_list_string_accessors(cls, name, **kwargs):
        default = kwargs.get("default", [])
        prop = "_{}".format(name)
        accessor_name = name
        appender_name = "push_{}".format(name)

        def accessor(self, *args):
            if len(args) > 0:
                self.validate_string(accessor_name, *args, **kwargs)
                setattr(self, prop, list(args))
                return self
            if hasattr(self, prop):
                return getattr(self, prop)
            return default

        def appender(self, *args):
            self.validate_string(appender_name, *args, **kwargs)
            if hasattr(self, prop):
                value = getattr(self, prop)
            else:
                value = []
            value.extend(args)
            setattr(self, prop, list(value))
            return self

        return [
            {"name": accessor_name, "function": accessor},
            {"name": appender_name, "function": appender},
        ]

    @classmethod
    def build_list_int_accessors(cls, name, **kwargs):
        default = kwargs.get("default", [])
        prop = "_{}".format(name)
        accessor_name = name
        appender_name = "push_{}".format(name)

        def accessor(self, *args):
            if len(args) > 0:
                self.validate_int(accessor_name, *args, **kwargs)
                setattr(self, prop, list(args))
                return self
            if hasattr(self, prop):
                return getattr(self, prop)
            return default

        def appender(self, *args):
            self.validate_int(appender_name, *args, **kwargs)
            if hasattr(self, prop):
                value = getattr(self, prop)
            else:
                value = []
            value.extend(args)
            setattr(self, prop, list(value))
            return self

        return [
            {"name": accessor_name, "function": accessor},
            {"name": appender_name, "function": appender},
        ]

    @classmethod
    def build_cmd_accessors(cls, name, **kwargs):
        prop = "_{}".format(name)
        accessor_name = name

        def accessor(self, *args):
            if len(args) > 1:
                raise TypeError("Accessor takes at most one argument")
            if len(args) == 1:
                self.validate_cmd(accessor_name, args[0], **kwargs)
                setattr(self, prop, args[0])
                return self
            if hasattr(self, prop):
                return getattr(self, prop)
            return None

        return [{"name": accessor_name, "function": accessor}]

    @classmethod
    def build_list_cmd_accessors(cls, name, **kwargs):
        prop = "_{}".format(name)
        accessor_name = name
        appender_name = "push_{}".format(name)

        def accessor(self, *args):
            if len(args) > 0:
                self.validate_cmd(accessor_name, *args, **kwargs)
                setattr(self, prop, list(args))
                return self
            if hasattr(self, prop):
                return getattr(self, prop)
            return []

        def appender(self, *args):
            self.validate_cmd(appender_name, *args, **kwargs)
            if hasattr(self, prop):
                value = getattr(self, prop)
            else:
                value = []
            value.extend(args)
            setattr(self, prop, list(value))
            return self

        return [
            {"name": accessor_name, "function": accessor},
            {"name": appender_name, "function": appender},
        ]

    @classmethod
    def build_dict_accessors(cls, name, **kwargs):
        default = kwargs.get("default", {})
        prop = "_{}".format(name)
        accessor_name = name
        updater_name = "update_{}".format(name)

        def accessor(self, rhs=None):
            if rhs:
                rhs = deepcopy(rhs)
                self.validate_dict(accessor_name, rhs, **kwargs)
                setattr(self, prop, rhs)
                return self
            if hasattr(self, prop):
                return getattr(self, prop)
            return default

        def updater(self, rhs):
            rhs = deepcopy(rhs)
            self.validate_dict(updater_name, rhs, **kwargs)
            if hasattr(self, prop):
                value = getattr(self, prop)
            else:
                value = {}
            value = {**value, **rhs}
            setattr(self, prop, value)
            return self

        return [
            {"name": accessor_name, "function": accessor},
            {"name": updater_name, "function": updater},
        ]

    @classmethod
    def build_list_dict_accessors(cls, name, **kwargs):
        default = kwargs.get("default", [])
        prop = "_{}".format(name)
        accessor_name = name
        appender_name = "push_{}".format(name)

        def accessor(self, *args):
            if len(args) > 0:
                self.validate_dict(accessor_name, *args, **kwargs)
                setattr(self, prop, list(args))
                return self
            if hasattr(self, prop):
                return getattr(self, prop)
            return default

        def appender(self, *args):
            self.validate_dict(appender_name, *args, **kwargs)
            if hasattr(self, prop):
                value = getattr(self, prop)
            else:
                value = []
            value.extend(args)
            setattr(self, prop, list(value))
            return self

        return [
            {"name": accessor_name, "function": accessor},
            {"name": appender_name, "function": appender},
        ]
