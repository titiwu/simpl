simpl - A Simple Music Player
===============

The goal of this project is to create a simple to use (mp3) music player for children.
On the hardware side a Raspberry Pi will be used, but any other should work as well (GPIO Pins assumed). The design is inspired by ["Hoerbert"](https://de.hoerbert.com/), however it will have more features (but need more power). 

## Software requirements

### Raspian packages (OS requirements)

- Music playback: [mpd](https://www.musicpd.org/) (`mpd`)
- Speech synthesis: [Google Android TTS engine (svox-pico-tts)](https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)) (`libttspico-utils`)
- Speech-playback: [aplay](https://www.alsa-project.org/main/index.php/Main_Page) (`alsa-utils`)

TODO: Add configuration

### Python packages

- Raspberry Pi GPIO Access: [RPi.GPIO](https://sourceforge.net/projects/raspberry-gpio-python/)
- MPD-Control: [python-mpd2](https://github.com/Mic92/python-mpd2) 

## Configuratiom

### MPD

Dmix allows mixing of speech synthesis messages and music.

The software mixer allows volume control via MPD interface.

```
audio_output {
        type            "alsa"
        name            "dmixer"
#        options         "dev=dmixer"
#        device          "plug:dmix"
#        format          "44100:16:2"
#        options         "dev=dmixer"
#        device          "dev=dmixer"
        mixer_type      "software"
#        mixer_device    "default"    # optional
#        mixer_control    "PCM"        # optional
}
```