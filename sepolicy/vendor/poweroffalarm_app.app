# Allow poweroffalarm_app access to files labeled as mnt_vendor_file as fallback
# This is needed when /persist/alarm directory incorrectly inherits mnt_vendor_file label
allow poweroffalarm_app mnt_vendor_file:dir rw_dir_perms;
allow poweroffalarm_app mnt_vendor_file:file create_file_perms;
