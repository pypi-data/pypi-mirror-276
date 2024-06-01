from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="cdn77",
    asn_patterns=["cdn77"],
    cname_suffixes=[
        CNAMEPattern(suffix=".cdn77.org"),
        CNAMEPattern(suffix=".cdn77.net"),
    ],
    cidr=BGPViewCIDR(["cdn77"]),
)
