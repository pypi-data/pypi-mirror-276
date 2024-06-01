from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="baishan",
    asn_patterns=["baishan"],
    cname_suffixes=[
        CNAMEPattern(suffix=".baishan-cloud.com"),
        CNAMEPattern(suffix=".baishancloud.com"),
        CNAMEPattern(suffix=".baishangeek.cn"),
        CNAMEPattern(suffix=".baishangeek.com"),
        CNAMEPattern(suffix=".bsclink.cn"),
        CNAMEPattern(suffix=".bsclink.com"),
        CNAMEPattern(suffix=".bscstorage.com"),
        CNAMEPattern(suffix=".bsgslb.cn", pattern=r"${domain}.bsgslb.cn"),
        CNAMEPattern(suffix=".bsgslb.com"),
        CNAMEPattern(suffix=".qianxun.com"),
        CNAMEPattern(suffix=".qingcdn.com"),
        CNAMEPattern(suffix=".trpcdn.com"),
        CNAMEPattern(suffix=".trpcdn.net", pattern=r"${domain}.bsgslb.cn"),
    ],
    cidr=BGPViewCIDR(["baishan"]),
)
