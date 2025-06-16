# SurveillanceRoom — Kodi Matrix/Nexus/Omega Fork

[![Kodi Version](https://img.shields.io/badge/Kodi-19%20|%2020%20|%2021-blue.svg)](https://kodi.tv/)
[![Python](https://img.shields.io/badge/Python-3.x-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-GPL--2.0-red.svg)](LICENSE)

> **A powerful Kodi add-on for IP camera surveillance with motion detection and multi-camera support**

Originally developed by **Maikito26**, this community-maintained fork brings compatibility with modern Kodi versions (Matrix, Nexus, Omega), enhanced MJPEG stream handling, and robust support for multiple camera feeds with intelligent on-screen previews.

---

## 🎯 What It Does

**Smart Motion Detection**: When motion or sound is detected, a small preview slides onto your screen without interrupting your current media. One click opens the full camera feed with controls.

**Seamless Integration**: Your movie, show, or music automatically pauses for camera viewing and resumes exactly where you left off when you close the camera feed.

**Multi-Camera Support**: Monitor up to **4 cameras simultaneously** with individual configuration and control options.

---

## ✨ Key Features

- 🎯 **Modern Kodi Support**: Compatible with **Kodi 19 (Matrix)**, **20 (Nexus)**, and **21 (Omega)**
- 📹 **Multi-Camera Setup**: Connect up to 4 IP cameras or Foscam-compatible devices
- 🔐 **Flexible Authentication**: Supports Foscam credentials and manual URL overrides for RTSP streams (port 554)
- 🎮 **Interactive Controls**: On-screen pan/tilt/zoom controls for compatible cameras
- 👁️ **Smart Previews**: Motion/sound-triggered overlays or manual activation via `RunPlugin()`
- ⏯️ **Auto-Resume**: Seamlessly returns to your media after camera viewing
- ⚙️ **Configurable Logic**: Customize when previews are shown or disabled
- 🏠 **PTZ Home Position**: Auto-position Foscam cameras at Kodi startup
- 🔧 **Enhanced MJPEG**: Improved stream parsing, frame extraction, and camera compatibility

---

## 🚀 Quick Start

1. **Install** the add-on in Kodi
2. **Configure** camera settings in Add-on Settings
3. **Enable** your configured cameras
4. **Access** via **Programs** → **SurveillanceRoom** or **Video Add-ons**
5. **Enjoy** automatic motion detection or manual camera viewing

---

## 🎮 External Control (RunPlugin)

Integrate with home automation, remote controls, or scripts:

### Camera Preview Commands
```bash
# Show preview overlay for camera 1
XBMC.RunPlugin(plugin://plugin.video.surveillanceroom?action=show_preview&camera_number=1)

# View all cameras in grid layout
XBMC.RunPlugin(plugin://plugin.video.surveillanceroom?action=all_cameras)

# Single camera with PTZ controls
XBMC.RunPlugin(plugin://plugin.video.surveillanceroom?action=single_camera&camera_number=1)

# Single camera, controls disabled
XBMC.RunPlugin(plugin://plugin.video.surveillanceroom?action=single_camera_no_controls&camera_number=1)
```

### Remote Control Integration
```xml
<!-- Example: Blue button shows camera 1 preview -->
<blue>XBMC.RunPlugin(plugin://plugin.video.surveillanceroom?action=show_preview&camera_number=1)</blue>
```

---

## 🖥️ Tested Environment

### Current Development
- **OS**: Debian 12
- **Kodi**: v21 (Omega)
- **Python**: 3.x

### Legacy Compatibility  
- **OS**: Windows 10
- **Kodi**: v15.2+
- **Cameras**: Foscam F19831w & F19804p (firmware v2.11.1.118), D-Link DCS-932L

**Cross-Platform**: Tested and maintained for Linux, Windows, and other Kodi-supported platforms.

---

## 🤝 Credits & Acknowledgments

### Core Contributors
- **Original Developer**: [Maikito26](https://github.com/maikito26) — Created the foundational SurveillanceRoom plugin
- **Matrix Porting**: **kodinerds.net** community (pünktchen, fritsch, and contributors)
- **Community Discussion**: [kodinerds.net Matrix thread](https://www.kodinerds.net/thread/72131-plugin-video-surveillanceroom-f%C3%BCr-kodi-19-matrix/)
- **This Fork**: Enhanced MJPEG handling, multi-version Kodi support, and ongoing maintenance

### Inspiration & Groundwork
- [script.foscam](https://github.com/LS80/script.foscam) — Foscam camera integration patterns
- [XbmcSecuritycam](https://github.com/RyanMelenaNoesis/XbmcSecuritycam) — Security camera concepts
- [script.securitycams](https://github.com/Shigoru/script.securitycams) — Multi-camera architecture ideas

---

## 📜 License

This project maintains the same license as the original SurveillanceRoom plugin. See [LICENSE](LICENSE) for details.

---

## 🔗 Related Projects

- **Upstream Repository**: [maikito26/plugin.video.surveillanceroom](https://github.com/maikito26/plugin.video.surveillanceroom)
- **Community Discussion**: [kodinerds.net thread](https://www.kodinerds.net/thread/72131-plugin-video-surveillanceroom-f%C3%BCr-kodi-19-matrix/)

---

*Made with ❤️ by the Kodi community*
