<h2 align="center">
  <a href="https://www.devialet.com"><img src="https://github.com/fwestenberg/homeassistant-devialet/blob/main/logo%402x.png" alt="Devialet logotype" width="400"></a>
  <br>
  <i>Home Assistant Devialet custom integration</i>
  <br>
</h2>

<p align="center">
  <a href="https://github.com/custom-components/hacs"><img src="https://img.shields.io/badge/HACS-Custom-orange.svg"></a>
  <img src="https://img.shields.io/github/v/release/fwestenberg/homeassistant-devialet" alt="Current version">
</p>

The `devialet` integration allows you to integrate your [Devialet](https://www.devialet.com) devices in Home Assistant.

> **Warning**
Make sure your Devialet firmware version >= 2.16.1. Otherwise expect functions not to work.

## Installation instructions

### HACS
Add this repository `https://github.com/fwestenberg/homeassistant-devialet` to your HACS custom repositories (Go to HACS->Integrations->Press `...` top right and choose Custom repositories)

### Manual
- Add the `devialet` folder to your `config/custom_components/` folder
- Restart HA

## Configuration
The Devialet device(s) will automatically be discovered and can be viewed in the integrations overview, by using this My button:

[![integrations](https://my.home-assistant.io/badges/integrations.svg)](https://my.home-assistant.io/redirect/integrations/)

If discovery did not complete within 1-2 minutes, adding Devialet to your Home Assistant instance can be done via the user interface, by using this My button:

[![devialet](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=devialet)


> **Note**
For a stereo setup, only one of the speakers need to be configured
  
## Known issues:
- When using Airplay, no media art is available


## Screenshots:

### Discovery
 
<img width="300" alt="image" src="https://user-images.githubusercontent.com/47930023/208066307-24cc39eb-6f21-47a5-9674-5e3f0996e4b0.png">
 
<img width="300" alt="image" src="https://user-images.githubusercontent.com/47930023/208066552-fcd21bf9-a8ad-400a-8a60-04250e6c296e.png">
 

### Manual configuration

<img width="300" alt="image" src="https://user-images.githubusercontent.com/47930023/208067522-3b416cda-a4aa-4d8a-b3a5-fea23b0a81d9.png">
 
 
### Device overview

<img width="300" alt="image" src="https://user-images.githubusercontent.com/47930023/208066755-b5c072bd-1a27-4947-be64-90d6a4e87c7d.png">
 

<img width="300" alt="image" src="https://user-images.githubusercontent.com/47930023/208066926-ee08cb60-29f1-4b33-950f-edc6ab5366c9.png">
 
<img width="300" alt="image" src="https://user-images.githubusercontent.com/47930023/208067167-a7ea516b-38f5-4cc8-84a0-6dffc8ed0639.png">
 
