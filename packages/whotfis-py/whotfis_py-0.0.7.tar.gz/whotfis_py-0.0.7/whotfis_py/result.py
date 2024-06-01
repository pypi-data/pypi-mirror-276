class whois_result(object):
    def __init__(self):
        pass

    def dict(self):
        return self.__dict__


class radb_result(whois_result):

    def router(self):
        return self.route.split("/")[0] if self.route is not None else None

    def mask(self):
        return self.route.split("/")[1] if self.route is not None else None

    def dict(self):
        parent_dict = super().dict()
        parent_dict["router"] = self.router()
        parent_dict["mask"] = self.mask()
        return parent_dict

    def __init__(self,
                 route=None,
                 origin=None,
                 descr=None,
                 notify=None,
                 mnt_by=None,
                 changed=None,
                 source=None,
                 last_modified=None,
                 rpki_ov_states=None):
        super().__init__()
        self.route = route

        self.origin = origin
        self.descr = descr
        self.notify = notify
        self.mnt_by = mnt_by
        self.changed = changed
        self.source = source
        self.last_modified = last_modified
        self.rpki_ov_states = rpki_ov_states


class ripe_result(whois_result):
    def __init__(self,
                 inetnum=None,
                 netname=None,
                 descr=None,
                 remarks=None,
                 country=None,
                 admin_c=None,
                 tech_c=None,
                 status=None,
                 mnt_by=None,
                 created=None,
                 last_modified=None,
                 source=None):
        super().__init__()
        self.inetnum = inetnum
        self.netname = netname
        self.descr = descr
        self.remarks = remarks
        self.country = country
        self.admin_c = admin_c
        self.tech_c = tech_c
        self.status = status
        self.mnt_by = mnt_by
        self.created = created
        self.last_modified = last_modified
        self.source = source


class lacninc_result(whois_result):
    def __init__(self,
                 ASNumber=None,
                 ASName=None,
                 ASHandle=None,
                 RegDate=None,
                 Updated=None,
                 Comment=None,
                 Ref=None,
                 OrgName=None,
                 OrgId=None,
                 Address=None,
                 City=None,
                 StateProv=None,
                 PostalCode=None,
                 Country=None,
                 OrgNOCHandle=None,
                 OrgNOCName=None,
                 OrgNOCPhone=None,
                 OrgNOCEmail=None,
                 OrgNOCRef=None,
                 OrgAbuseHandle=None,
                 OrgAbuseName=None,
                 OrgAbusePhone=None,
                 OrgAbuseEmail=None,
                 OrgAbuseRef=None,
                 OrgTechHandle=None,
                 OrgTechName=None,
                 OrgTechPhone=None,
                 OrgTechEmail=None,
                 OrgTechRef=None,
                 ):
        super().__init__()
        self.ASNumber = ASNumber
        self.ASName = ASName
        self.ASHandle = ASHandle
        self.RegDate = RegDate
        self.Updated = Updated
        self.Comment = Comment
        self.Ref = Ref
        self.OrgName = OrgName
        self.OrgId = OrgId
        self.Address = Address
        self.City = City
        self.StateProv = StateProv
        self.PostalCode = PostalCode
        self.Country = Country
        self.OrgNOCHandle = OrgNOCHandle
        self.OrgNOCName = OrgNOCName
        self.OrgNOCPhone = OrgNOCPhone
        self.OrgNOCEmail = OrgNOCEmail
        self.OrgNOCRef = OrgNOCRef
        self.OrgAbuseHandle = OrgAbuseHandle
        self.OrgAbuseName = OrgAbuseName
        self.OrgAbusePhone = OrgAbusePhone
        self.OrgAbuseEmail = OrgAbuseEmail
        self.OrgAbuseRef = OrgAbuseRef
        self.OrgTechHandle = OrgTechHandle
        self.OrgTechName = OrgTechName
        self.OrgTechPhone = OrgTechPhone
        self.OrgTechEmail = OrgTechEmail
        self.OrgTechRef = OrgTechRef


class custom_result(whois_result):
    def __init__(self, data=None):
        super().__init__()
        if not isinstance(data, dict):
            data = {}

        keys = data.keys()
        for key in keys:
            setattr(self, key, data[key])
