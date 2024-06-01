from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="azion",
    asn_patterns=["azion"],
    cname_suffixes=[
        CNAMEPattern(suffix=".map.azionedge.net"),
        CNAMEPattern(suffix=".azioncdn.net"),
        CNAMEPattern(suffix=".azioncdn.com"),
        CNAMEPattern(suffix=".azion.net"),
    ],
    cidr=BGPViewCIDR(["azion"]),
)
