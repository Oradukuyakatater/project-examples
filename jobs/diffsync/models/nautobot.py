# """Nautobot Models for Cisco ACI integration with SSoT app."""

# import ipaddress

# from nautobot.dcim.models import Device as OrmVirtualMachine
# from nautobot.dcim.models import Interface as OrmVMInterface
# from nautobot.ipam.models import (
#     IPAddress as OrmIPAddress,
#     IPAddressToInterface as OrmIPAddressToInterface,
#     Prefix as OrmPrefix,
# )
# from nautobot.extras.models import Status

# from .base import (
#     IPAddress,
# )

# class NautobotIPAddress(IPAddress):
#     """Nautobot implementation of the IPAddress Model."""

#     @classmethod
#     def create(cls, diffsync, ids, attrs):
#         """
#             Create IPAddress object in Nautobot.

#             It will create the parent prefix from the provided host and netmask_length if it doesn't already exists
#             It will set the virtual machine's primary_ip4 if attr 'is_primary' is present and set to True
#             It will create an interface to IP association if the object:
#             - has both virtual_machine and interface attributes provided
#             - both objects exists in nautobot database
#         """

#         _virtual_machine = attrs["virtual_machine"]
#         _vm_interface = attrs["vm_interface"]

#         nb_interface = None
#         if attrs["virtual_machine"] and attrs["interface"]:
#             try:
#                 nb_interface = OrmVMInterface.objects.get(name=_vm_interface, device__name=_virtual_machine)
#             except OrmVMInterface.DoesNotExist:
#                 diffsync.job.logger.warning(f"{_virtual_machine} missing interface {_vm_interface} to assign {ids['address']}")

#         nb_status = Status.objects.get(name=attrs["status"]),
#         network_object = ipaddress.IPv4Network(f"{attrs['address']}/{attrs['mask_length']}", strict=False)
#         nb_prefix, created = OrmPrefix.objects.get_or_create(
#             prefix=network_object.with_prefixlen,
#             defaults={
#                 "prefix": network_object.with_prefixlen,
#                 "namespace__name": "Global",
#                 "status__name": nb_status
#             }
#         )
#         if created:
#             diffsync.job.logger.info(f"Prefix {network_object.with_prefixlen} created")

#         nb_ipaddress = OrmIPAddress.objects.create(
#             address=ids["address"],
#             status=nb_status,
#         )
#         if nb_interface:
#             mapping = OrmIPAddressToInterface.objects.create(ip_address=nb_ipaddress, interface=nb_interface)
#             mapping.validated_save()
#             diffsync.job.logger.info(f"IP {nb_ipaddress.address} assigned to interfacez {_vm_interface} on virtual machine {_virtual_machine}")
#         nb_ipaddress.validated_save()

#         if attrs["virtual_machine"] and attrs["is_primary"]:
#             device = OrmVirtualMachine.objects.get(
#                 name=_virtual_machine,
#             )
#             device.primary_ip4 = OrmIPAddress.objects.get(address=ids["address"])
#             device.save()

#         return super().create(ids=ids, diffsync=diffsync, attrs=attrs)
