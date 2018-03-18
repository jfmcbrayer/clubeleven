from json import JSONEncoder

class ClubElevenActivityPubEncoder(JSONEncoder):
    def default(self, ob):
        try:
            ap_dict = ob.to_activitypub()
        except AttributeError:
            pass
        else:
            return ap_dict
        return JSONEncoder.default(self, ob)
