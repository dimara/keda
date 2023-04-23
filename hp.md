## HP Proliant server

* Model: HP ML310eGen8v2 E3-1220v3 NHP EU Svr/GO

* Enable Network boot
  - https://serverfault.com/questions/416954/network-boot-from-a-non-default-nic-on-a-hp-proliant-g7-server

* Use undionly.kpxe to chainload pxelinux.0.3.86
  - https://github.com/puppetlabs/Razor/wiki/Alternate-PXE-boot-Options
  - http://ipxe.org/howto/chainloading

* Disable Smart Array B120i and use HPSA. No firmware required. Had to set
  "Enable SATA AHCI" under "System Options" in BIOS to get it booting from hard
  drive.
  - https://wiki.debian.org/HP/ProLiant


## VMware

This controller is not officially supported by VMware as it's not on the HCL.
But most importantly, like it's brother the B140i, it's a fake-RAID controller and not a real hardware RAID controller (see https://communities.vmware.com/thread/526436)


### RAID

Advisory: HP ProLiant Gen8 Servers - The HP Dynamic Smart Array B120i and B320i
Controller Driver for Linux and VMware (hpvsa) Must Be Downloaded from HP.COM
in Order to Use RAID Functionality

HP strongly recommends RAID protection of data and/or boot volumes when using
RAID capable controllers, such as HP Dynamic Smart Array Controllers. However,
the HP Dynamic Smart Array Controller driver for Linux and VMware (hpvsa) is
not included in the operating system distribution media, as some customers may
expect.

Links:

* https://askubuntu.com/questions/660860/how-to-use-hps-raid-driver-for-smart-array-b120i-e-g-proliant-microserver-g8
* https://support.hpe.com/hpsc/doc/public/display?docId=emr_na-c03742583
* https://support.hpe.com/hpsc/swd/public/detail?swItemId=MTX_9200a10168684afbbb4efce88a
* https://support.hpe.com/hpsc/doc/public/display?docId=emr_na-c03871499
* https://supportex.net/blog/2010/11/determine-raid-controller-type-model/
