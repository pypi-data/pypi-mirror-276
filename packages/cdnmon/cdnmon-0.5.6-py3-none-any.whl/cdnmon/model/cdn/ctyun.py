from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN
from cdnmon.model.cdn import DomainOwnershipVerficationStatus
from cdnmon.model.cdn import DomainOwnershipVerification
from cdnmon.model.cdn import HTTPOwnershipVerification
from cdnmon.model.cdn import OwnershipVerification

CDN = CommonCDN(
    name="ctyun",
    asn_patterns=["ctyun", "chinanet"],
    cname_suffixes=[
        CNAMEPattern(suffix=".ctadns.cn", pattern=r"${domain}.ctadns.cn"),
        CNAMEPattern(suffix=".ctacdn.cn", pattern=r"${domain}.ctacdn.cn"),
        CNAMEPattern(suffix=".ctlcdn.cn", pattern=r"${domain}.ctlcdn.cn"),
    ],
    cidr=BGPViewCIDR(["ctyun", "chinanet"]),
    frontend_ownership_verification=OwnershipVerification(
        txt=DomainOwnershipVerification(
            status=DomainOwnershipVerficationStatus.REQUIRED,
            prefix="dnsverify",
            pattern=r"[0-9]{14}[0-9a-f]{50}",
        ),
    ),
    backend_ownership_verification=OwnershipVerification(
        txt=DomainOwnershipVerification(status=DomainOwnershipVerficationStatus.NOT_REQUIRED),
        http=HTTPOwnershipVerification(status=DomainOwnershipVerficationStatus.NOT_REQUIRED),
    ),
)
