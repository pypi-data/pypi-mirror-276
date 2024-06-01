from cdnmon.model.cdn import BGPViewCIDR
from cdnmon.model.cdn import CNAMEPattern
from cdnmon.model.cdn import CommonCDN
from cdnmon.model.cdn import DomainOwnershipVerficationStatus
from cdnmon.model.cdn import DomainOwnershipVerification
from cdnmon.model.cdn import HTTPOwnershipVerification
from cdnmon.model.cdn import OwnershipVerification

CDN = CommonCDN(
    name="tencent",
    asn_patterns=["tencent"],
    cname_suffixes=[
        CNAMEPattern(suffix=".dsa.dnsv1.com", pattern=r"${domain}.dsa.dnsv1.com"),
        CNAMEPattern(suffix=".dsa.dnsv1.com.cn", pattern=r"${domain}.dsa.dnsv1.com.cn", is_root=True),
        CNAMEPattern(suffix=".cdn.dnsv1.com", pattern=r"${domain}.cdn.dnsv1.com"),
        CNAMEPattern(suffix=".cdn.dnsv1.com.cn", pattern=r"${domain}.cdn.dnsv1.com.cn", is_root=True),
        CNAMEPattern(suffix=".eo.dnse0.com", pattern=r"${domain}.eo.dnse0.com"),
        CNAMEPattern(suffix=".eo.dnse1.com", pattern=r"${domain}.eo.dnse1.com"),
        CNAMEPattern(suffix=".eo.dnse2.com", pattern=r"${domain}.eo.dnse2.com"),
        CNAMEPattern(suffix=".eo.dnse3.com", pattern=r"${domain}.eo.dnse3.com"),
        CNAMEPattern(suffix=".eo.dnse4.com", pattern=r"${domain}.eo.dnse4.com"),
        CNAMEPattern(suffix=".eo.dnse5.com", pattern=r"${domain}.eo.dnse5.com"),
        CNAMEPattern(suffix=".cdn.qcloudcdn.cn", pattern=r"${domain}.cdn.qcloudcdn.cn"),
        CNAMEPattern(suffix=".txlivecdn.com", pattern=r"${domain}.txlivecdn.com"),
        CNAMEPattern(suffix=".ovscdns.com", pattern=r"${domain}.ovscdns.com"),
        CNAMEPattern(suffix=".slt-dk.sched.tdnsv8.com", pattern=r"${random}.slt-dk.sched.tdnsv8.com", is_leaf=True),
    ],
    cidr=BGPViewCIDR(query_term_list=["tencent"]),
    frontend_ownership_verification=OwnershipVerification(
        txt=DomainOwnershipVerification(
            status=DomainOwnershipVerficationStatus.REQUIRED,
            prefix="_cdnauth",
            pattern=r"[0-9]{14}[0-9a-f]{32}",
        ),
    ),
    backend_ownership_verification=OwnershipVerification(
        txt=DomainOwnershipVerification(status=DomainOwnershipVerficationStatus.NOT_REQUIRED),
        http=HTTPOwnershipVerification(status=DomainOwnershipVerficationStatus.NOT_REQUIRED),
    ),
)
