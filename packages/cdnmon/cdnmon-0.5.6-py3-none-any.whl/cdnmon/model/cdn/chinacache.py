from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="chinacache",
    asn_patterns=["chinacache"],
    cname_suffixes=[
        CNAMEPattern(suffix=".ccgslb.com"),
    ],
    cidr=BGPViewCIDR(["chinacache"]),
)
