%if 0%{?fedora} >= 27
%global debug_package %{nil}
%endif

%ifarch s390x
%define with_hardware 0
%define base_drivers swrast
%else
%define with_hardware 1
%define with_vdpau 1
%define with_vaapi 1
%define with_nine 1
%define with_omx 1
%define with_opencl 1
%define base_drivers swrast,nouveau,radeon,r200
%endif

%ifarch %{ix86} x86_64
%define platform_drivers ,i915,i965
%define with_vmware 1
%define with_xa     1
%define vulkan_drivers --with-vulkan-drivers=intel,radeon
%else
%define vulkan_drivers --with-vulkan-drivers=radeon
%endif

%ifarch %{arm} aarch64
%define with_etnaviv   1
%define with_freedreno 1
%define with_tegra     1
%define with_vc4       1
%define with_xa        1
%endif

%ifnarch %{arm} s390x
%define with_radeonsi 1
%endif

## this repo provides wayland 1.15 for f27 and we stopped building for earlier versions
%define with_wayland_egl 0


%define dri_drivers --with-dri-drivers=%{?base_drivers}%{?platform_drivers}

%global sanitize 1

Name:           mesa
Summary:        Mesa graphics libraries
%global ver 18.2.0-rc4
Version:        %{lua:ver = string.gsub(rpm.expand("%{ver}"), "-", "~"); print(ver)}
Release: 1.stable%{?dist}

License:        MIT
URL:            http://www.mesa3d.org
Source0:        %{name}-%{ver}.tar.xz
Source1:        vl_decoder.c
Source2:        vl_mpeg12_decoder.c
Source3:        Makefile
# src/gallium/auxiliary/postprocess/pp_mlaa* have an ... interestingly worded license.
# Source4 contains email correspondence clarifying the license terms.
# Fedora opts to ignore the optional part of clause 2 and treat that code as 2 clause BSD.
Source4:        Mesa-MLAA-License-Clarification-Email.txt

Patch1:         0001-llvm-SONAME-without-version.patch
Patch3:         0003-evergreen-big-endian.patch
Patch4:         0004-bigendian-assert.patch

# glvnd support patches
# non-upstreamed ones
#Patch10:        glvnd-fix-gl-dot-pc.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool

%if %{with_hardware}
BuildRequires:  kernel-headers
%endif
BuildRequires:  libdrm-devel >= 2.4.77
BuildRequires:  libXxf86vm-devel
BuildRequires:  expat-devel
BuildRequires:  xorg-x11-proto-devel
BuildRequires:  makedepend
BuildRequires:  libselinux-devel
BuildRequires:  libXext-devel
BuildRequires:  libXfixes-devel
BuildRequires:  libXdamage-devel
BuildRequires:  libXi-devel
BuildRequires:  libXmu-devel
BuildRequires:  libxshmfence-devel
BuildRequires:  elfutils
BuildRequires:  python3
BuildRequires:  python2
BuildRequires:  gettext
BuildRequires: llvm-devel >= 3.4-7
%if 0%{?with_opencl}
BuildRequires: clang-devel >= 3.0
%endif
BuildRequires: elfutils-libelf-devel
BuildRequires: python3-libxml2
BuildRequires: python2-libxml2
BuildRequires: libudev-devel
BuildRequires: bison flex
BuildRequires: pkgconfig(wayland-client)
BuildRequires: pkgconfig(wayland-server)
BuildRequires: pkgconfig(wayland-protocols)
%if 0%{?with_vdpau}
BuildRequires: libvdpau-devel
%endif
%if 0%{?with_vaapi}
BuildRequires: libva-devel >= 0.39.0
%endif
BuildRequires: pkgconfig(zlib)
%if 0%{?with_omx}
BuildRequires: libomxil-bellagio-devel
%endif
%if 0%{?with_opencl}
BuildRequires: libclc-devel opencl-filesystem
%endif
%if 0%{?with_hardware}
BuildRequires: vulkan-devel
BuildRequires: libXrandr-devel
%endif
BuildRequires: python3-mako
%if 0%{?fedora} < 28
BuildRequires: python-mako
%else
BuildRequires: python2-mako
%endif
%ifarch %{valgrind_arches}
BuildRequires: pkgconfig(valgrind)
%endif
BuildRequires: pkgconfig(libglvnd) >= 0.2.0

%description
%{summary}.

%package filesystem
Summary:        Mesa driver filesystem
Provides:       mesa-dri-filesystem = %{?epoch:%{epoch}}%{version}-%{release}
Obsoletes:      mesa-dri-filesystem < %{?epoch:%{epoch}}%{version}-%{release}

%description filesystem
%{summary}.

%package libGL
Summary:        Mesa libGL runtime libraries
Requires:       %{name}-libglapi%{?_isa} = %{?epoch:%{epoch}}%{version}-%{release}
Requires:       libglvnd-glx%{?_isa} >= 1:1.0.1-0.6.99

%description libGL
%{summary}.

%package libGL-devel
Summary:        Mesa libGL development package
Requires:       %{name}-libGL%{?_isa} = %{?epoch:%{epoch}}%{version}-%{release}
Requires:       libglvnd-devel%{?_isa}
Provides:       libGL-devel
Provides:       libGL-devel%{?_isa}

%description libGL-devel
%{summary}.

%package libEGL
Summary:        Mesa libEGL runtime libraries
Requires:       libglvnd-egl%{?_isa}

%description libEGL
%{summary}.

%package libEGL-devel
Summary:        Mesa libEGL development package
Requires:       %{name}-libEGL%{?_isa} = %{?epoch:%{epoch}}%{version}-%{release}
Requires:       libglvnd-devel%{?_isa}
Provides:       libEGL-devel
Provides:       libEGL-devel%{?_isa}

%description libEGL-devel
%{summary}.

%package libGLES
Summary:        Mesa libGLES runtime libraries
Requires:       %{name}-libglapi%{?_isa} = %{?epoch:%{epoch}}%{version}-%{release}
Requires:       libglvnd-gles%{?_isa}

%description libGLES
%{summary}.

%package libGLES-devel
Summary:        Mesa libGLES development package
Requires:       %{name}-libGLES%{?_isa} = %{?epoch:%{epoch}}%{version}-%{release}
Requires:       libglvnd-devel%{?_isa}
Provides:       libGLES-devel
Provides:       libGLES-devel%{?_isa}

%description libGLES-devel
%{summary}.

%package dri-drivers
Summary:        Mesa-based DRI drivers
Requires:       %{name}-filesystem%{?_isa} = %{?epoch:%{epoch}}%{version}-%{release}

%description dri-drivers
%{summary}.

%if 0%{?with_omx}
%package omx-drivers
Summary:        Mesa-based OMX drivers
Requires:       %{name}-filesystem%{?_isa} = %{?epoch:%{epoch}}%{version}-%{release}

%description omx-drivers
%{summary}.
%endif

%if 0%{?with_vdpau}
%package        vdpau-drivers
Summary:        Mesa-based VDPAU drivers
Requires:       %{name}-filesystem%{?_isa} = %{?epoch:%{epoch}}%{version}-%{release}

%description vdpau-drivers
%{summary}.
%endif

%package libOSMesa
Summary:        Mesa offscreen rendering libraries
Requires:       %{name}-libglapi%{?_isa} = %{?epoch:%{epoch}}%{version}-%{release}
Provides:       libOSMesa
Provides:       libOSMesa%{?_isa}

%description libOSMesa
%{summary}.

%package libOSMesa-devel
Summary:        Mesa offscreen rendering development package
Requires:       %{name}-libOSMesa%{?_isa} = %{?epoch:%{epoch}}%{version}-%{release}

%description libOSMesa-devel
%{summary}.

%package libgbm
Summary:        Mesa gbm runtime library
Provides:       libgbm
Provides:       libgbm%{?_isa}

%description libgbm
%{summary}.

%package libgbm-devel
Summary:        Mesa libgbm development package
Requires:       %{name}-libgbm%{?_isa} = %{?epoch:%{epoch}}%{version}-%{release}
Provides:       libgbm-devel
Provides:       libgbm-devel%{?_isa}

%description libgbm-devel
%{summary}.

%if %{?with_wayland_egl}
%package libwayland-egl
Summary:        Mesa libwayland-egl runtime library
Provides:       libwayland-egl
Provides:       libwayland-egl%{?_isa}

%description libwayland-egl
%{summary}.

%package libwayland-egl-devel
Summary:        Mesa libwayland-egl development package
Requires:       %{name}-libwayland-egl%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       libwayland-egl-devel
Provides:       libwayland-egl-devel%{?_isa}

%description libwayland-egl-devel
%{summary}.
%endif

%if 0%{?with_xa}
%package libxatracker
Summary:        Mesa XA state tracker
Provides:       libxatracker
Provides:       libxatracker%{?_isa}

%description libxatracker
%{summary}.

%package libxatracker-devel
Summary:        Mesa XA state tracker development package
Requires:       %{name}-libxatracker%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       libxatracker-devel
Provides:       libxatracker-devel%{?_isa}

%description libxatracker-devel
%{summary}.
%endif

%package libglapi
Summary:        Mesa shared glapi
Provides:       libglapi
Provides:       libglapi%{?_isa}

%description libglapi
%{summary}.

%if 0%{?with_opencl}
%package libOpenCL
Summary:        Mesa OpenCL runtime library
Requires:       ocl-icd%{?_isa}
Requires:       libclc%{?_isa}
Requires:       %{name}-libgbm%{?_isa} = %{?epoch:%{epoch}}%{version}-%{release}
Requires:       opencl-filesystem

%description libOpenCL
%{summary}.

%package libOpenCL-devel
Summary:        Mesa OpenCL development package
Requires:       %{name}-libOpenCL%{?_isa} = %{?epoch:%{epoch}}%{version}-%{release}

%description libOpenCL-devel
%{summary}.
%endif

%if 0%{?with_nine}
%package libd3d
Summary:        Mesa Direct3D9 state tracker

%description libd3d
%{summary}.

%package libd3d-devel
Summary:        Mesa Direct3D9 state tracker development package
Requires:       %{name}-libd3d%{?_isa} = %{?epoch:%{epoch}}%{version}-%{release}

%description libd3d-devel
%{summary}.
%endif

%package vulkan-drivers
Summary:        Mesa Vulkan drivers
Requires:       vulkan%{_isa}

%description vulkan-drivers
The drivers with support for the Vulkan API.

%package vulkan-devel
Summary:        Mesa Vulkan development files
Requires:       %{name}-vulkan-drivers%{?_isa} = %{?epoch:%{epoch}}%{version}-%{release}
Requires:       vulkan-devel

%description vulkan-devel
Headers for development with the Vulkan API.

%prep
%autosetup -n %{name}-%{ver} -p1
%if 0%{sanitize}
  cp -f %{SOURCE1} src/gallium/auxiliary/vl/vl_decoder.c
  cp -f %{SOURCE2} src/gallium/auxiliary/vl/vl_mpeg12_decoder.c
%else
  cmp %{SOURCE1} src/gallium/auxiliary/vl/vl_decoder.c
  cmp %{SOURCE2} src/gallium/auxiliary/vl/vl_mpeg12_decoder.c
%endif

cp %{SOURCE4} docs/

%build
autoreconf -vfi

export CFLAGS="%{optflags}"
# C++ note: we never say "catch" in the source.  we do say "typeid" once,
# in an assert, which is patched out above.  LLVM doesn't use RTTI or throw.
#
# We do say 'catch' in the clover and d3d1x state trackers, but we're not
# building those yet.
#%if 0%{?fedora} < 28
#export CXXFLAGS="%{optflags} %{?with_opencl:-frtti -fexceptions} %{!?with_opencl:-fno-rtti -fno-exceptions}"
#export LDFLAGS="%{__global_ldflags} -static-libstdc++"
#%endif
%ifarch %{ix86}
# i do not have words for how much the assembly dispatch code infuriates me
%global asm_flags --disable-asm
%endif

## enable LTO
LTO_FLAGS="-g0 -flto=8 -ffat-lto-objects -flto-odr-type-merging"
export CFLAGS="$CFLAGS -falign-functions=32 -fno-semantic-interposition $LTO_FLAGS "
export FCFLAGS="$CFLAGS -falign-functions=32 -fno-semantic-interposition $LTO_FLAGS "
export FFLAGS="$CFLAGS -falign-functions=32 -fno-semantic-interposition $LTO_FLAGS "
export CXXFLAGS="$CXXFLAGS -falign-functions=32 -fno-semantic-interposition $LTO_FLAGS "
export LDFLAGS="$LDFLAGS -flto=8 "

%configure \
    %{?asm_flags} \
    --enable-libglvnd \
    --enable-selinux \
    --enable-gallium-osmesa \
    --with-dri-driverdir=%{_libdir}/dri \
    --enable-egl \
    --disable-gles1 \
    --enable-gles2 \
    --disable-xvmc \
    %{?with_vdpau:--enable-vdpau} \
    %{?with_vaapi:--enable-va} \
    --with-platforms=x11,drm,surfaceless,wayland \
    --enable-shared-glapi \
    --enable-gbm \
    %{?with_omx:--enable-omx-bellagio} \
    %{?with_opencl:--enable-opencl --enable-opencl-icd} %{!?with_opencl:--disable-opencl} \
    --enable-glx-tls \
    --enable-texture-float=yes \
%if 0%{?with_hardware}
    %{?vulkan_drivers} \
%endif
    --enable-llvm \
    --enable-llvm-shared-libs \
    --enable-dri \
%if %{with_hardware}
    %{?with_xa:--enable-xa} \
    %{?with_nine:--enable-nine} \
    --with-gallium-drivers=%{?with_vmware:svga,}%{?with_radeonsi:radeonsi,r600,}swrast,%{?with_freedreno:freedreno,}%{?with_etnaviv:etnaviv,imx,}%{?with_tegra:tegra,}%{?with_vc4:vc4,}virgl,r300,nouveau \
%else
    --with-gallium-drivers=swrast,virgl \
%endif
    %{?dri_drivers}

%make_build MKDEP=/bin/true V=1

%install
%make_install

%if !%{with_hardware}
rm -f %{buildroot}%{_sysconfdir}/drirc
%endif

# libvdpau opens the versioned name, don't bother including the unversioned
rm -f %{buildroot}%{_libdir}/vdpau/*.so
# likewise glvnd
rm -f %{buildroot}%{_libdir}/libGLX_mesa.so
rm -f %{buildroot}%{_libdir}/libEGL_mesa.so
# XXX can we just not build this
rm -f %{buildroot}%{_libdir}/libGLES*

# remove libwayland-egl on F28+ where it's built as part of wayland source package
%if !%{?with_wayland_egl}
rm -f %{buildroot}%{_libdir}/libwayland-egl.so*
rm -f %{buildroot}%{_libdir}/pkgconfig/wayland-egl.pc
%endif

# glvnd needs a default provider for indirect rendering where it cannot
# determine the vendor
ln -s %{_libdir}/libGLX_mesa.so.0 %{buildroot}%{_libdir}/libGLX_system.so.0

# strip out useless headers
rm -f %{buildroot}%{_includedir}/GL/w*.h

# these are shipped already in vulkan-devel
mkdir -p %{buildroot}/%{_includedir}/vulkan/
rm -f %{buildroot}/%{_includedir}/vulkan/vk_platform.h
rm -f %{buildroot}/%{_includedir}/vulkan/vulkan.h

# remove .la files
find %{buildroot} -name '*.la' -delete

# this keeps breaking, check it early.  note that the exit from eu-ftr is odd.
pushd %{buildroot}%{_libdir}
for i in libOSMesa*.so libGL.so ; do
    eu-findtextrel $i && exit 1
done
popd

%files filesystem
%doc docs/Mesa-MLAA-License-Clarification-Email.txt
%dir %{_libdir}/dri
%if %{with_hardware}
%if 0%{?with_vdpau}
%dir %{_libdir}/vdpau
%endif
%endif

%files libGL
%{_libdir}/libGLX_mesa.so.0*
%{_libdir}/libGLX_system.so.0*
%files libGL-devel
%{_includedir}/GL/gl.h
%{_includedir}/GL/gl_mangle.h
%{_includedir}/GL/glext.h
%{_includedir}/GL/glx.h
%{_includedir}/GL/glx_mangle.h
%{_includedir}/GL/glxext.h
%{_includedir}/GL/glcorearb.h
%dir %{_includedir}/GL/internal
%{_includedir}/GL/internal/dri_interface.h
%{_libdir}/pkgconfig/dri.pc
%{_libdir}/libglapi.so
%{_libdir}/pkgconfig/gl.pc

%files libEGL
%{_datadir}/glvnd/egl_vendor.d/50_mesa.json
%{_libdir}/libEGL_mesa.so.0*
%files libEGL-devel
%dir %{_includedir}/EGL
%{_includedir}/EGL/eglext.h
%{_includedir}/EGL/egl.h
%{_includedir}/EGL/eglmesaext.h
%{_includedir}/EGL/eglplatform.h
%{_includedir}/EGL/eglextchromium.h
%dir %{_includedir}/KHR
%{_includedir}/KHR/khrplatform.h
%{_libdir}/pkgconfig/egl.pc

%files libGLES
# No files, all provided by libglvnd
%files libGLES-devel
%dir %{_includedir}/GLES2
%{_includedir}/GLES2/gl2platform.h
%{_includedir}/GLES2/gl2.h
%{_includedir}/GLES2/gl2ext.h
%dir %{_includedir}/GLES3
%{_includedir}/GLES3/gl3platform.h
%{_includedir}/GLES3/gl3.h
%{_includedir}/GLES3/gl3ext.h
%{_includedir}/GLES3/gl31.h
%{_includedir}/GLES3/gl32.h
%{_libdir}/pkgconfig/glesv2.pc

%ldconfig_scriptlets libglapi
%files libglapi
%{_libdir}/libglapi.so.0
%{_libdir}/libglapi.so.0.*

%ldconfig_scriptlets libOSMesa
%files libOSMesa
%{_libdir}/libOSMesa.so.8*
%files libOSMesa-devel
%dir %{_includedir}/GL
%{_includedir}/GL/osmesa.h
%{_libdir}/libOSMesa.so
%{_libdir}/pkgconfig/osmesa.pc

%ldconfig_scriptlets libgbm
%files libgbm
%{_libdir}/libgbm.so.1
%{_libdir}/libgbm.so.1.*
%files libgbm-devel
%{_libdir}/libgbm.so
%{_includedir}/gbm.h
%{_libdir}/pkgconfig/gbm.pc

%if %{?with_wayland_egl}
%ldconfig_scriptlets libwayland-egl
%files libwayland-egl
%{_libdir}/libwayland-egl.so.1
%{_libdir}/libwayland-egl.so.1.*
%files libwayland-egl-devel
%{_libdir}/libwayland-egl.so
%{_libdir}/pkgconfig/wayland-egl.pc
%endif

%if 0%{?with_xa}
%ldconfig_scriptlets libxatracker
%files libxatracker
%if %{with_hardware}
%{_libdir}/libxatracker.so.2
%{_libdir}/libxatracker.so.2.*
%endif

%files libxatracker-devel
%if %{with_hardware}
%{_libdir}/libxatracker.so
%{_includedir}/xa_tracker.h
%{_includedir}/xa_composite.h
%{_includedir}/xa_context.h
%{_libdir}/pkgconfig/xatracker.pc
%endif
%endif

%if 0%{?with_opencl}
%ldconfig_scriptlets libOpenCL
%files libOpenCL
%{_libdir}/libMesaOpenCL.so.*
%{_sysconfdir}/OpenCL/vendors/mesa.icd
%files libOpenCL-devel
%{_libdir}/libMesaOpenCL.so
%endif

%if 0%{?with_nine}
%files libd3d
%dir %{_libdir}/d3d/
%{_libdir}/d3d/*.so.*

%files libd3d-devel
%{_libdir}/pkgconfig/d3d.pc
%{_includedir}/d3dadapter/
%{_libdir}/d3d/*.so
%endif

%files dri-drivers
%if %{with_hardware}
%config(noreplace) %{_sysconfdir}/drirc
%{_libdir}/dri/radeon_dri.so
%{_libdir}/dri/r200_dri.so
%{_libdir}/dri/nouveau_vieux_dri.so
%{_libdir}/dri/r300_dri.so
%if 0%{?with_radeonsi}
%{_libdir}/dri/r600_dri.so
%{_libdir}/dri/radeonsi_dri.so
%endif
%ifarch %{ix86} x86_64
%{_libdir}/dri/i915_dri.so
%{_libdir}/dri/i965_dri.so
%endif
%if 0%{?with_vc4}
%{_libdir}/dri/vc4_dri.so
%endif
%if 0%{?with_freedreno}
%{_libdir}/dri/kgsl_dri.so
%{_libdir}/dri/msm_dri.so
%endif
%if 0%{?with_etnaviv}
%{_libdir}/dri/etnaviv_dri.so
%{_libdir}/dri/imx-drm_dri.so
%endif
%if 0%{?with_tegra}
%{_libdir}/dri/tegra_dri.so
%endif
%{_libdir}/dri/nouveau_dri.so
%if 0%{?with_vmware}
%{_libdir}/dri/vmwgfx_dri.so
%endif
%{_libdir}/dri/nouveau_drv_video.so
%if 0%{?with_radeonsi}
%{_libdir}/dri/r600_drv_video.so
%{_libdir}/dri/radeonsi_drv_video.so
%endif
%endif
%if 0%{?with_hardware}
%dir %{_libdir}/gallium-pipe
%{_libdir}/gallium-pipe/*.so
%endif
%{_libdir}/dri/kms_swrast_dri.so
%{_libdir}/dri/swrast_dri.so
%{_libdir}/dri/virtio_gpu_dri.so

%if %{with_hardware}
%if 0%{?with_omx}
%files omx-drivers
%{_libdir}/bellagio/libomx_mesa.so
%endif
%if 0%{?with_vdpau}
%files vdpau-drivers
%{_libdir}/vdpau/libvdpau_nouveau.so.1*
%{_libdir}/vdpau/libvdpau_r300.so.1*
%if 0%{?with_radeonsi}
%{_libdir}/vdpau/libvdpau_r600.so.1*
%{_libdir}/vdpau/libvdpau_radeonsi.so.1*
%endif
%if 0%{?with_tegra}
%{_libdir}/vdpau/libvdpau_tegra.so.1*
%endif
%endif
%endif

%files vulkan-drivers
%if 0%{?with_hardware}
%ifarch %{ix86} x86_64
%{_libdir}/libvulkan_intel.so
%{_datadir}/vulkan/icd.d/intel_icd.*.json
%endif
%{_libdir}/libvulkan_radeon.so
%{_datadir}/vulkan/icd.d/radeon_icd.*.json
%endif

%files vulkan-devel
%{_includedir}/vulkan/

%changelog
* Mon Oct 10 2016 Rudolf Kastl <rudolf@redhat.com>
- Synced with Leighs spec.
