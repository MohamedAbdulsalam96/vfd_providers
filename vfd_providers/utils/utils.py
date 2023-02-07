import click
import frappe
from frappe import _
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


@frappe.whitelist()
def generate_tra_vfd(docname, sinv_doc=None):
    if not sinv_doc:
        sinv_doc = frappe.get_doc("Sales Invoice", docname)
    if sinv_doc.is_not_vfd_invoice or sinv_doc.vfd_status == "Sent":
        return
    comp_vfd_provider = frappe.get_cached_doc(
        "Company VFD Provider", filters={"name": sinv_doc.company}
    )
    if not comp_vfd_provider:
        return
    vfd_provider = frappe.get_cached_doc(
        "VFD Provider", filters={"name": comp_vfd_provider.vfd_provider}
    )
    if not vfd_provider:
        return
    vfd_provider_settings = frappe.get_cached_doc(
        "VFD Provider Settings", filters={"name": vfd_provider.vfd_provider_settings}
    )
    if not vfd_provider_settings:
        return
    if vfd_provider_settings.vfd_provider == "VFDPlus":
        from vfd_providers.vfd_providers.doctype.vfdplus_settings.vfdplus_settings import (
            post_fiscal_receipt,
        )

        post_fiscal_receipt(sinv_doc)


def autogenerate_vfd(doc, method):
    if doc.is_not_vfd_invoice or doc.vfd_status == "Sent":
        return
    if doc.is_auto_generate_vfd and doc.docstatus == 1:
        generate_tra_vfd(docname=doc.name, sinv_doc=doc)
