%global tarball xf86-input-fpit
%global moduledir %(pkg-config xorg-server --variable=moduledir )
%global driverdir %{moduledir}/input

Summary:   Xorg X11 fpit input driver
Name:      xorg-x11-drv-fpit
Version:   1.4.0
Release:   5%{?dist}
URL:       http://www.x.org
License:   MIT
Group:     User Interface/X Hardware Support
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:   ftp://ftp.x.org/pub/individual/driver/%{tarball}-%{version}.tar.bz2
Source1:   10-fpit.fdi
Patch01:   0001-Don-t-free-anything-on-PreInit-failure-let-UnInit-ta.patch
Patch02:   0002-Test-opening-the-device-in-PreInit-fail-if-necessary.patch
Patch03:   0003-Use-xf86SetStrOption-to-print-Option-Device-to-the-l.patch
Patch04:   0004-Don-t-call-DEVICE_OFF-in-UnInit-the-server-does-it-f.patch
Patch05:   0005-Check-for-priv-before-dereferencing-it.patch
Patch06:   0006-Don-t-assign-a-static-name-strdup-it.patch
Patch07:   0007-Don-t-force-pInfo-flags-to-0-40870.patch

ExcludeArch: s390 s390x

BuildRequires: xorg-x11-server-sdk >= 1.10.0-1

Requires:  Xorg %(xserver-sdk-abi-requires ansic)
Requires:  Xorg %(xserver-sdk-abi-requires xinput)

%description 
X.Org X11 fpit input driver.

%prep
%setup -q -n %{tarball}-%{version}
%patch01 -p1
%patch02 -p1
%patch03 -p1
%patch04 -p1
%patch05 -p1
%patch06 -p1
%patch07 -p1

%build
%configure --disable-static
make

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# FIXME: Remove all libtool archives (*.la) from modules directory.  This
# should be fixed in upstream Makefile.am or whatever.
find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --

mkdir -p $RPM_BUILD_ROOT%{_datadir}/hal/fdi/policy/20thirdparty
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/hal/fdi/policy/20thirdparty

# We don't ship .conf files for this driver
rm $RPM_BUILD_ROOT%{_datadir}/X11/xorg.conf.d/50-fpit.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{driverdir}/fpit_drv.so
%{_mandir}/man4/fpit.4*
%{_datadir}/hal/fdi/policy/20thirdparty/10-fpit.fdi

%changelog
* Wed Aug 22 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1.4.0-5
- Rebuild for server 1.13

* Mon Aug 20 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.4.0-4
- Don't overwrite pInfo->flags to avoid the device come up floating (#835229)

* Wed Aug 01 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1.4.0-3
- Rebuild for server 1.13 (#835229)

* Tue Jul 19 2011 Peter Hutterer <peter.hutterer@redhat.com> 1.4.0-2
- Fix crashers if PreInit fails

* Mon Jun 27 2011 Peter Hutterer <peter.hutterer@redhat.com> 1.4.0-1
- fpit 1.4.0 (#713788)
- Drop fpit-1.3.0-abi.patch, merged

* Wed Jan 06 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.3.0-5
- Use global instead of define as per Packaging Guidelines
- Fix indentation of Version and Release.

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 1.3.0-4.1
- Rebuilt for RHEL 6

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 17 2009 Peter Hutterer <peter.hutterer@redhat.com> - 1.3.0-3
- fpit-1.3.0-abi.patch: Cope with XINPUT ABI 7.

* Wed Jul 15 2009 Adam Jackson <ajax@redhat.com> - 1.3.0-2.1
- ABI bump

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.3.0-1
- fpit 1.3.0

* Mon Feb 16 2009 Matthew Garrett <mjg@redhat.com> 1.2.0-2
- Add an fdi file for autoconfig
- Fix build on newer XInput

* Thu Mar 20 2008 Adam Jackson <ajax@redhat.com> 1.2.0-1
- fpit 1.2.0

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1.0-5
- Autorebuild for GCC 4.3

* Wed Aug 22 2007 Adam Jackson <ajax@redhat.com> - 1.1.0-4
- Rebuild for PPC toolchain bug

* Mon Jun 18 2007 Adam Jackson <ajax@redhat.com> 1.1.0-3
- Update Requires and BuildRequires.  Disown the module directories.

* Fri Feb 16 2007 Adam Jackson <ajax@redhat.com> 1.1.0-2
- ExclusiveArch -> ExcludeArch

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - sh: line 0: fg: no job control
- rebuild

* Sun Apr  9 2006 Adam Jackson <ajackson@redhat.com> 1.1.0-1
- Updatte to 1.1.0 from 7.1RC1.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.0.0.5-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.0.0.5-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 1.0.0.5-1
- Updated xorg-x11-drv-fpit to version 1.0.0.5 from X11R7.0

* Tue Dec 20 2005 Mike A. Harris <mharris@redhat.com> 1.0.0.4-1
- Updated xorg-x11-drv-fpit to version 1.0.0.4 from X11R7 RC4
- Removed 'x' suffix from manpage dirs to match RC4 upstream.

* Wed Nov 16 2005 Mike A. Harris <mharris@redhat.com> 1.0.0.2-1
- Updated xorg-x11-drv-fpit to version 1.0.0.2 from X11R7 RC2

* Fri Nov 4 2005 Mike A. Harris <mharris@redhat.com> 1.0.0.1-1
- Updated xorg-x11-drv-fpit to version 1.0.0.1 from X11R7 RC1
- Fix *.la file removal.

* Fri Sep 2 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-0
- Initial spec file for fpit input driver generated automatically
  by my xorg-driverspecgen script.
