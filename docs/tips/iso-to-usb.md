Installing an ISO image to a USB drive
======================================

TurnKey ISOs are built as a "hybrid" image, which means that the structure of
the ISO can be written directly to a USB and it should "just work" - either to
boot in "live" mode or to install to bare metal if you wish.

Note that if you copy the ISO file to an existing filesystem on a USB, it can
be shared with others and used for a VM. However to be able to boot directly
from the USB, the ISO filesystem must be written directly to the USB -
overwriting all existing content.

Many third party tools that support "burning" an ISO to a USB although
unfortunately not all of them will work. As a general rule 
any tool that supports writing a Debian ISO to a USB should work fine with
TurnKey.

Linux and Mac
-------------

On Linux and Mac, no third party tools are required as the 'dd' CLI tool can
be used. Be careful that you are writing to the right device as the contents of
it will be lost.

The following instructions are for Linux, but will likely also work on Mac. The
first step is to confirm the identify the device path (e.g., /dev/sdc) of your
USB drive. There are a number of ways to do that, but 'lsblk' works well. E.g.
an "8GB" USB ('lsblk' reports size in GiB):

```
# lsblk
sde                                     8:64   1   7.4G  0 disk  
└─sde1                                  8:65   1   7.4G  0 part  /media/usbdrive
```

USBs may automount on some systems so be sure that it's unmounted:

```
umount /media/usbdrive
```

Use dd to write the ISO image to the disk path. As noted above, be sure that
you are writing to the correct device and also note that you write to the whole
device. I.e. in this example, I'm using '/dev/sde' - NOT '/dev/sde1':

```
dd if=build/product.iso of=/dev/sde
```

Things to keep in mind:

- **Root access is required**: You will need to perform the above commands as
  root. Use 'sudo' if you are a normal user.

- **dd will completely overwrite your USB drive**:. Any data on it will be lost
  so use a dedicated USB device.

- **dd needs to write to the disk path, not the partition path**: in the above
  example /dev/sde is the disk path device, /dev/sde1 is the partition path
  (the first partition on sde). The ISO contains a full filesystem and needs to
  overwrite any existing USB filesystem.
