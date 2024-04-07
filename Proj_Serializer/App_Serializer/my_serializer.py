import pytz


class DjangoSerializer:
    """
    Convert Django Instance and QuerySet into Python-Json Readable Format
    Parameters:
        request: HTTP request,
        is_nested: default False, set to True for Nested Serializer

    Features:
    1) Date: Default: 17 December, 1994
    1) Time: Default: 12:30:00 (24 Hour)
    2) DateTime: Default: 17 December, 1994 12:30 PM
    3) None: Default: ''
    4) Contact Number With Country Code: +91 9712397123
    5) Decrypt Data: Fernet
    6) Add Path to Media Files
    7) Custom Functions:
    8) Django ORM Optimization

    Returns:
        Dictionary for single instance and List of Dictionary for QuerySet

    Notes:
        For Django ORM Optimization Follow These Rules:
        1) For One level FK and M2M, care already taken by serializer

        2) For deep level, set select_related and prefetch_related explicitly
            Example: selected_related(company_branch_id__company_id), prefetch_related(team_members__designation_id)

        For Custom Function Follow These Rules:
        1) For Model Fields pass (obj, value) as arguments
            where obj is model instance and value is resolved value
            Example: lambda obj, value: obj.name + value

        2) For FK and M2M pass (obj) as arguments
            where obj is django instance of related model
            Example: lambda obj: obj.get_full_name()

        3) For Annotate keys pass (obj) as arguments
            where obj is django instance of main model
            Example: lambda obj: 'Hi ' + obj.name
    """

    def __init__(self, request, is_nested=False):
        self.request, self.is_nested = request, is_nested
        self.path, self.a = None, None
        self.fields, self.fk, self.m2m, self.ann = [], [], [], []
        self.null, self.datetime, self.contact, self.filter, self.func, self.decrypt, self.media = \
            dict(), dict(), dict(), dict(), dict(), [], []
        self.select, self.prefetch = [], []
        self.first = True

    def set_null(self, **kwargs):
        self.null.update(kwargs)

    def set_datetime_format(self, **kwargs):
        self.datetime.update(kwargs)

    def set_contact_detail(self, **kwargs):
        self.contact.update(kwargs)

    def set_media(self, *args):
        self.media.extend(args)
        self.null.update({arg: '' for arg in args})
        self.path = f"{self.request.scheme}://{self.request.get_host()}/media/"

    def set_decrypt(self, *args):
        self.decrypt.extend(args)
        self.a = EncryptData()

    def set_filter(self, **kwargs):
        self.filter.update(kwargs)

    def set_select_related(self, *args):
        self.select.extend(args)

    def set_prefetch_related(self, *args):
        self.prefetch.extend(args)

    def set_func(self, **kwargs):
        self.func.update(kwargs)

    def get_data(self, inst, fields=(), fk=(), m2m=(), ann=(), is_form=False):
        self.fields.extend(fields)
        self.fk.extend(fk)
        self.m2m.extend(m2m)
        self.ann.extend(ann)
        return self.__get_data(inst, is_form)

    def __get_data(self, inst, is_form):
        if type(inst).__name__ == 'QuerySet':
            if not inst.exists():
                return []

            if self.first and not self.is_nested:
                self.first = False
                self.select.extend(self.fk)
                self.prefetch.extend(self.m2m)
                if self.select and self.prefetch:
                    inst = inst.select_related(*self.select).prefetch_related(*self.prefetch)
                elif self.select:
                    inst = inst.select_related(*self.select)
                elif self.prefetch:
                    inst = inst.prefetch_related(*self.prefetch)

            return [self.__get_data(i, is_form) for i in inst]

        else:
            data = dict()
            if not inst:
                return data

            for k in self.fields:
                v = getattr(inst, k)
                if not v:
                    data[k] = self.null.get(k, v if v is not None else '')
                else:
                    if k in self.decrypt:
                        v = self.a.decrypt(v)

                    if type(v).__name__ == 'date':
                        data[k] = v.strftime(self.datetime.get(k, '%Y-%m-%d' if is_form else '%d %B, %Y'))

                    elif type(v).__name__ == 'datetime':
                        data[k] = v.astimezone(pytz.timezone(get_user_timezone(self.request))).strftime(
                            self.datetime.get(k, '%Y-%m-%dT%H:%M' if is_form else '%d %B, %Y %I:%M %p'))

                    elif type(v).__name__ == 'time':
                        data[k] = v.strftime(self.datetime.get(k, '%H:%M:%S'))

                    elif k in self.media:
                        data[k] = f"{self.path}{v}"

                    elif k in self.contact:
                        code = getattr(inst, self.contact[k], None)
                        data[k] = f'+{code} {v}' if code else v

                    else:
                        data[k] = v

                    if k in self.func:
                        data[k] = self.func[k](inst=inst, value=data[k])

            for i in self.fk:
                obj = getattr(inst, i)
                if not obj:
                    data[i] = self.null.get(i, '')
                else:
                    func = self.func.get(i, None)
                    if func:
                        data[i] = func(obj)
                    elif is_form:
                        data[i] = obj.pk
                    else:
                        data[i] = str(obj)

            for i in self.m2m:
                obj = getattr(inst, i)
                dic = self.filter.get(i, None)
                objs = obj.filter(**dic) if dic else obj.all()
                if not objs.exists():
                    data[i] = self.null.get(i, [])
                else:
                    func = self.func.get(i, None)
                    if func:
                        data[i] = [func(j) for j in objs]
                    elif is_form:
                        data[i] = [j.pk for j in objs]
                    else:
                        data[i] = [str(j) for j in objs]

            for i in self.ann:
                data[i] = self.func.get(i)(inst)

            return data


class EncryptData:
    """ This is Simpleset Possible Decryption Logic """

    @staticmethod
    def decrypt(enc_data):
        if enc_data and isinstance(enc_data, str) and enc_data.endswith('@encrypted'):
            return enc_data.split('@encrypted')[0]
        else:
            return enc_data


def get_user_timezone(request):
    """ This is Simpleset Possible Timezone """
    try:
        return request.user.timezone
    except:
        return 'Asia/Kolkata'












