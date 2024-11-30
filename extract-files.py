#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/xiaomi/msm8953-common',
    'hardware/qcom-caf/msm8996',
    'vendor/qcom/opensource/dataservices',
]


def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None


lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'com.qualcomm.qti.dpm.api@1.0',
        'vendor.qti.ims.callinfo@1.0',
        'vendor.qti.ims.rcsconfig@1.0',
        'vendor.qti.imsrtpservice@2.0',
        'vendor.qti.imsrtpservice@2.1',
    ): lib_fixup_vendor_suffix,
    ('libwpa_client', 'libwifi-hal-ctrl'): lib_fixup_remove,
}

blob_fixups: blob_fixups_user_type = {
    ('system_ext/etc/init/dpmd.rc', 'system_ext/etc/permissions/com.qti.dpmframework.xml', 'system_ext/etc/permissions/dpmapi.xml', 'system_ext/etc/permissions/qcrilhook.xml', 'system_ext/etc/permissions/telephonyservice.xml'): blob_fixup()
        .regex_replace('/product/', '/system_ext/'),
    ('system_ext/lib/libdpmframework.so', 'system_ext/lib64/libdpmframework.so'): blob_fixup()
        .add_needed('libcutils_shim.so'),
    ('system_ext/lib64/lib-imscamera.so', 'system_ext/lib64/lib-imsvideocodec.so'): blob_fixup()
        .add_needed('libgui_shim.so'),
    'vendor/bin/pm-service': blob_fixup()
        .add_needed('libutils-v33.so'),
    ('vendor/etc/data/dsi_config.xml', 'vendor/etc/data/netmgr_config.xml'): blob_fixup()
        .fix_xml(),
    ('vendor/lib64/mediadrm/libwvdrmengine.so', 'vendor/lib64/libwvhidl.so'): blob_fixup()
        .add_needed('libcrypto_shim.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'msm8953-common',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
