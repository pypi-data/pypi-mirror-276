from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN

CDN = CommonCDN(
    name="limelight",
    asn_patterns=["limelight"],
    cname_suffixes=[
        CNAMEPattern(suffix=".llnwd.net"),
        CNAMEPattern(suffix=".lldns.net"),
        CNAMEPattern(suffix=".llnwi.net"),
    ],
    cidr=BGPViewCIDR(query_term_list=["limelight"]),
)
