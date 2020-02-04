def generate_certificate_name(certificate):
    return 'Certificate-{}-{}'.format(
            certificate.get_fullname(),
            certificate.certificate_type
        )
