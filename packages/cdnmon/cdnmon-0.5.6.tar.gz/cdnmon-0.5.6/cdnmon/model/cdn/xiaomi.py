from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="xiaomi",
    asn_patterns=["xiaomi"],
    cname_suffixes=[
        CNAMEPattern(suffix=".mgslb.com", pattern=r"${domain}.mgslb.com"),
    ],
    cidr=BGPViewCIDR(["xiaomi"]),
)
