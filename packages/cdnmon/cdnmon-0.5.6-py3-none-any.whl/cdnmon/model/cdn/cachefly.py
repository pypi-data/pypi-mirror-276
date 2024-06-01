from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="cachefly",
    asn_patterns=["cachefly"],
    cname_suffixes=[
        CNAMEPattern(
            suffix=".cachefly.net",
            source="https://help.cachefly.com/hc/en-us/articles/215068846-DNS-Configuration-for-CNAMEs-Hostname-Aliases",
        ),
    ],
    cidr=BGPViewCIDR(["cachefly"]),
)
