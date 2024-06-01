from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="douyin",
    asn_patterns=["bytedance", "douyin"],
    cname_suffixes=[
        CNAMEPattern(suffix=".cdnbuild.com", pattern=r"${domain}.cdnbuild.com"),
        CNAMEPattern(suffix=".zjgslb.com", pattern=r"${domain}.zjgslb.com"),
        CNAMEPattern(suffix=".bytegslb.com", pattern=r"${name}.bytegslb.com"),
    ],
    cidr=BGPViewCIDR(["bytedance", "douyin"]),
)
