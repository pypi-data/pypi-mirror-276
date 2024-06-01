from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="edgio",
    asn_patterns=["edgio"],
    cname_suffixes=[CNAMEPattern(suffix=".edgio.net")],
    cidr=BGPViewCIDR(["edgio"]),
)
